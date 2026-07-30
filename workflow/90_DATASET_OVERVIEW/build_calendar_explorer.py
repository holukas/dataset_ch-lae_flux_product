"""Build a self-contained interactive calendar explorer for the CH-LAE meteo products.

The per-variable dashboards in this folder answer "what does this variable do over twenty years".
This page answers the other question: "what happened in *that* month". It puts every month of every
year on one grid, marks each of them with the notable things that occurred in it, and lets a reader
open a month and walk it day by day.

Three levels, one page
----------------------
1. **The grid.** One tile per month, twenty-one years by twelve months, coloured by whichever
   metric is selected and carrying badges for what was remarkable about that month. Each tile can
   also show its own days as a micro-strip, so a heat wave is visible as a streak before anything
   is clicked.
2. **The month.** Its statistics against the calendar-month normal, its rank among the same month
   of every other year, its badges spelled out with the numbers behind them, the daily course of
   temperature against the climatological band, daily precipitation, and a day calendar.
3. **The day.** Every variable's statistics for that day, the flags it set, and - where the hourly
   arrays are included - the diurnal course of temperature, radiation and precipitation.

What it computes, and what it must not
--------------------------------------
It aggregates and it compares; it corrects nothing. A value on this page is the exported product,
read from the file named in the registry of `build_meteo_dashboard.py`, which is also where the
variable definitions, the integrity checks and the threshold-day definitions come from. Importing
them rather than restating them is deliberate: a "hot day" has to mean the same thing on the
calendar as it does on the temperature dashboard, and a second definition here would eventually
disagree with the first.

Two rules keep the badges honest.

- **A badge is a claim about a month, so a month that was not measured cannot make one.** Every
  badge names the variables it reads, and is skipped where the measured share of that variable
  falls below `MIN_BADGE_COVERAGE`. The month view says which badges were suppressed and why,
  rather than showing a tile that silently means "we do not know".
- **A normal is built from the months that can support one.** A calendar-month normal, and every
  anomaly, z-score and rank derived from it, uses only the years whose month is at least
  `NORMAL_MIN_COVERAGE` measured, and is withheld entirely below `MIN_NORMAL_YEARS` of them. A
  sparse month is ranked against nothing and can therefore never be "the driest on record".

Where this page belongs
-----------------------
It is currently built into `docs/_build/html/dashboards/` beside the per-variable dashboards, and
linked from `docs/Meteo_Data.md`, because the products it reads are the meteo products. That is a
temporary home. Nothing about the page is specific to meteorology - it is a calendar over whatever
the dataset carries, and the registries below are what decide which variables that is. **When the
flux products are available it should move out of the meteo section into a place of its own beside
them**, gain the flux variables in `CALENDAR`, and take its link with it. The three places that
would have to change are the `CALENDAR` registry here, the step in `deploy.ps1`, and the section in
`docs/Meteo_Data.md`.

Usage
-----
    uv run python workflow/90_DATASET_OVERVIEW/build_calendar_explorer.py --list
    uv run python workflow/90_DATASET_OVERVIEW/build_calendar_explorer.py --open
    uv run python workflow/90_DATASET_OVERVIEW/build_calendar_explorer.py --no-hourly
    uv run python workflow/90_DATASET_OVERVIEW/build_calendar_explorer.py --outdir docs/_build/html/dashboards

The hourly arrays are what make the day panel a chart rather than a table, and they are also most
of the file. `--no-hourly` drops them; the day panel then shows the day's statistics alone.

Author: Lukas Hoertnagl (holukas@ethz.ch)
"""

from __future__ import annotations

import argparse
import calendar
import json
import re
import sys
import webbrowser
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

# The variable registry, the loader with its integrity checks and the small formatting helpers are
# shared with the per-variable dashboards. Explicit path insertion so the import also works when the
# script is called from another working directory.
sys.path.insert(0, str(Path(__file__).parent))

from build_meteo_dashboard import (  # noqa: E402
    OUTDIR, PRODUCTS, SITE, SITE_LONG, VARIABLES, Variable,
    load_product, longest_spell, r, rlist,
)

ASSETS = Path(__file__).parent / "calendar_assets"

# The design tokens, base layout, cards, tables and tooltip are the dashboards' own stylesheet,
# inlined unchanged. The calendar's components are the only thing this page adds, so the two pages
# cannot drift apart visually and no colour is decided twice.
SHARED_CSS = Path(__file__).parent / "dashboard_assets" / "dashboard.css"

MIN_BADGE_COVERAGE = 80.0   # % of a month's half-hours measured, below which its badges are withheld
NORMAL_MIN_COVERAGE = 90.0  # % measured for a month to contribute to a normal, or to be ranked
MIN_NORMAL_YEARS = 8        # qualifying years below which a calendar-month normal is not computed
SPARSE_COVERAGE = 90.0      # % measured below which a month is marked as sparsely measured
CLIM_WINDOW = 7             # +/- days around a calendar date that go into its daily normal


# ----------------------------------------------------------------------------------------------
# Which products the calendar reads
#
# `ship` names the daily statistics that travel into the page; the rest are computed and dropped.
# `hourly` marks the variables whose diurnal course the day panel draws - each one is roughly half
# a megabyte of the finished file, so the set is deliberately short.
# ----------------------------------------------------------------------------------------------

CALENDAR = {
    "TA": dict(ship=("min", "mean", "max"), digits=1, hourly=True, scale=10,
               short="Air temperature"),
    "PREC": dict(ship=("sum", "max"), digits=1, hourly=True, scale=10,
                 short="Precipitation"),
    "SW_IN": dict(ship=("mean", "max"), digits=0, hourly=True, scale=1,
                  short="Shortwave in"),
    "VPD": dict(ship=("mean", "max"), digits=2, hourly=False, scale=100,
                short="Vapour pressure deficit"),
    "RH": dict(ship=("min", "mean"), digits=0, hourly=False, scale=1,
               short="Relative humidity"),
    "SWC_0.2": dict(ship=("mean",), digits=1, hourly=False, scale=10,
                    short="Soil water, 0.2 m"),
}

# Threshold days beyond the ones the dashboards already define. Everything else in `DAY_FLAGS` is
# lifted from the `index_groups` of the shared registry, so the calendar cannot disagree with the
# temperature dashboard about what a hot day is.
EXTRA_INDICES = {
    "PREC": [dict(key="verywet", label="very wet days (≥ 30 {units})", stat="sum",
                  op="ge", value=30.0)],
}


def day_flags(variables):
    """The per-day threshold tests, each with the bit it occupies in the day flag word."""
    flags = []
    for key, v in variables.items():
        items = [i for group in VARIABLES[key].get("index_groups", []) for i in group["items"]]
        items = items + EXTRA_INDICES.get(key, [])
        for item in items:
            flags.append(dict(bit=len(flags), var=key, key=item["key"], stat=item["stat"],
                              op=item["op"], value=item["value"], label=v.fmt(item["label"])))
    # The word is read in JavaScript, where a bitwise operation is defined on 32 bits.
    assert len(flags) <= 30, f"{len(flags)} day flags do not fit in one 30-bit word"
    return flags


# ----------------------------------------------------------------------------------------------
# Badges
#
# A badge is one notable thing about one month. `rule` receives the month's statistics and returns
# the sentence that states the evidence, or None where the badge does not apply - so the text a
# reader sees is generated from the same numbers that decided whether to show it at all, and cannot
# describe a month it was not computed on.
#
# `needs` names the variables the rule reads. A badge is only evaluated where all of them are
# present and sufficiently measured, and - unless `needs_normal` is False - where their calendar-
# month normal exists.
#
# `priority` orders the icons on a tile, which shows only the first few. Sparse coverage sorts
# first: it qualifies every other badge on the tile.
# ----------------------------------------------------------------------------------------------

BADGES = [
    dict(key="sparse", label="Sparsely measured", group="Data quality", icon="alert",
         tone="warn", priority=0, needs=(), needs_normal=False,
         about="Less than {sparse:.0f} % of the month's half-hours are measured for temperature or "
               "precipitation. Its statistics rest on gap-filled or missing records.",
         rule=lambda s: (
             "Only " + ", ".join(f"{s[k + '_meas']:.0f} % of {k}" for k in ("TA", "PREC")
                                 if s[k + "_meas"] is not None and s[k + "_meas"] < SPARSE_COVERAGE)
             + " is measured in this month; its statistics rest on filled or missing records.")
         if any(s[k + "_meas"] is not None and s[k + "_meas"] < SPARSE_COVERAGE
                for k in ("TA", "PREC")) else None),

    dict(key="record_warm", label="Warmest on record", group="Temperature", icon="award",
         tone="warm", priority=1, needs=("TA",),
         about="The warmest occurrence of this calendar month in the record.",
         rule=lambda s: (f"Warmest {s['month_name']} in the record: {s['TA']:.1f} {s['u_TA']} "
                         f"mean, {s['TA_anom']:+.1f} {s['u_TA']} against the normal of "
                         f"{s['TA_n']} years") if s["TA_rank"] == 1 else None),

    dict(key="record_cold", label="Coldest on record", group="Temperature", icon="award",
         tone="cold", priority=1, needs=("TA",),
         about="The coldest occurrence of this calendar month in the record.",
         rule=lambda s: (f"Coldest {s['month_name']} in the record: {s['TA']:.1f} {s['u_TA']} "
                         f"mean, {s['TA_anom']:+.1f} {s['u_TA']} against the normal of "
                         f"{s['TA_n']} years") if s["TA_rank"] == s["TA_n"] else None),

    dict(key="warm", label="Warmer than normal", group="Temperature", icon="arrow-up",
         tone="warm", priority=4, needs=("TA",),
         about="The monthly mean is at least one standard deviation above the calendar-month "
               "normal.",
         rule=lambda s: (f"{s['TA_anom']:+.1f} {s['u_TA']} against the {s['month_name']} normal "
                         f"of {s['TA_norm']:.1f} {s['u_TA']} ({s['TA_z']:+.1f} standard "
                         f"deviations), rank {s['TA_rank']} of {s['TA_n']}")
         if s["TA_z"] >= 1 else None),

    dict(key="cold", label="Colder than normal", group="Temperature", icon="arrow-down",
         tone="cold", priority=4, needs=("TA",),
         about="The monthly mean is at least one standard deviation below the calendar-month "
               "normal.",
         rule=lambda s: (f"{s['TA_anom']:+.1f} {s['u_TA']} against the {s['month_name']} normal "
                         f"of {s['TA_norm']:.1f} {s['u_TA']} ({s['TA_z']:+.1f} standard "
                         f"deviations), rank {s['TA_rank']} of {s['TA_n']}")
         if s["TA_z"] <= -1 else None),

    dict(key="heat", label="Hot days", group="Temperature", icon="flame", tone="warm",
         priority=3, needs=("TA",), needs_normal=False,
         about="At least one day reached the hot-day threshold.",
         rule=lambda s: (f"{s['n_hot']} hot day{'s' if s['n_hot'] > 1 else ''} "
                         f"(daily maximum ≥ 30 {s['u_TA']}), warmest "
                         f"{s['TA_daymax']:.1f} {s['u_TA']}") if s["n_hot"] >= 1 else None),

    dict(key="heat_spell", label="Heat spell", group="Temperature", icon="flames", tone="warm",
         priority=2, needs=("TA",), needs_normal=False,
         about="Three or more consecutive hot days.",
         rule=lambda s: (f"{s['spell_hot']} consecutive hot days, the longest run of this month")
         if s["spell_hot"] >= 3 else None),

    dict(key="tropical", label="Tropical nights", group="Temperature", icon="moon", tone="warm",
         priority=3, needs=("TA",), needs_normal=False,
         about="At least one night stayed above the tropical-night threshold.",
         rule=lambda s: (f"{s['n_tropical']} night{'s' if s['n_tropical'] > 1 else ''} with a "
                         f"daily minimum ≥ 20 {s['u_TA']}") if s["n_tropical"] >= 1 else None),

    dict(key="frost", label="Frost days", group="Temperature", icon="snowflake", tone="cold",
         priority=3, needs=("TA",), needs_normal=False,
         about="Five or more days with a daily minimum below freezing.",
         rule=lambda s: (f"{s['n_frost']} frost days (daily minimum < 0 {s['u_TA']}), coldest "
                         f"{s['TA_daymin']:.1f} {s['u_TA']}") if s["n_frost"] >= 5 else None),

    dict(key="ice", label="Ice days", group="Temperature", icon="icicles", tone="cold",
         priority=3, needs=("TA",), needs_normal=False,
         about="At least one day stayed below freezing all day.",
         rule=lambda s: (f"{s['n_ice']} ice day{'s' if s['n_ice'] > 1 else ''} (daily maximum "
                         f"< 0 {s['u_TA']})") if s["n_ice"] >= 1 else None),

    dict(key="record_wet", label="Wettest on record", group="Precipitation", icon="award",
         tone="wet", priority=1, needs=("PREC",),
         about="The wettest occurrence of this calendar month in the record.",
         rule=lambda s: (f"Wettest {s['month_name']} in the record: {s['PREC']:.0f} "
                         f"{s['u_PREC']}, {s['PREC_pctn']:.0f} % of the normal of "
                         f"{s['PREC_norm']:.0f} {s['u_PREC']}") if s["PREC_rank"] == 1 else None),

    dict(key="record_dry", label="Driest on record", group="Precipitation", icon="award",
         tone="dry", priority=1, needs=("PREC",),
         about="The driest occurrence of this calendar month in the record.",
         rule=lambda s: (f"Driest {s['month_name']} in the record: {s['PREC']:.0f} "
                         f"{s['u_PREC']}, {s['PREC_pctn']:.0f} % of the normal of "
                         f"{s['PREC_norm']:.0f} {s['u_PREC']}")
         if s["PREC_rank"] == s["PREC_n"] else None),

    dict(key="wet", label="Wet month", group="Precipitation", icon="droplets", tone="wet",
         priority=4, needs=("PREC",),
         about="The monthly total is at least 150 % of the calendar-month normal.",
         rule=lambda s: (f"{s['PREC']:.0f} {s['u_PREC']}, {s['PREC_pctn']:.0f} % of the "
                         f"{s['month_name']} normal, on {s['n_wet']} wet days")
         if s["PREC_pctn"] >= 150 else None),

    dict(key="dry", label="Dry month", group="Precipitation", icon="droplet-off", tone="dry",
         priority=4, needs=("PREC",),
         about="The monthly total is at most 50 % of the calendar-month normal.",
         rule=lambda s: (f"{s['PREC']:.0f} {s['u_PREC']}, {s['PREC_pctn']:.0f} % of the "
                         f"{s['month_name']} normal, on {s['n_wet']} wet days")
         if s["PREC_pctn"] <= 50 else None),

    dict(key="dry_spell", label="Dry spell", group="Precipitation", icon="calendar-dry",
         tone="dry", priority=2, needs=("PREC",), needs_normal=False,
         about="Fourteen or more consecutive days below 1 mm.",
         rule=lambda s: (f"{s['spell_dry']} consecutive days below 1 {s['u_PREC']}")
         if s["spell_dry"] >= 14 else None),

    # The threshold is a day of 30 mm rather than a count of 10 mm days: at this site three days
    # above 10 mm occur in nearly half of all months, and a badge that common marks nothing.
    dict(key="heavy_rain", label="Heavy rain day", group="Precipitation", icon="cloud-rain",
         tone="wet", priority=3, needs=("PREC",), needs_normal=False,
         about="At least one day reached 30 mm.",
         rule=lambda s: (f"{s['n_verywet']} day{'s' if s['n_verywet'] > 1 else ''} above 30 "
                         f"{s['u_PREC']}, the wettest {s['PREC_daysum']:.0f} {s['u_PREC']}; "
                         f"{s['n_heavy']} days above 10 {s['u_PREC']}")
         if s["n_verywet"] >= 1 else None),

    dict(key="sunny", label="Sunnier than normal", group="Radiation", icon="sun", tone="warm",
         priority=4, needs=("SW_IN",),
         about="Mean incoming shortwave radiation is at least one standard deviation above the "
               "calendar-month normal.",
         rule=lambda s: (f"{s['SW_IN']:.0f} {s['u_SW_IN']} mean, {s['SW_IN_anom']:+.0f} "
                         f"{s['u_SW_IN']} against the {s['month_name']} normal "
                         f"({s['SW_IN_z']:+.1f} standard deviations)")
         if s["SW_IN_z"] >= 1 else None),

    dict(key="dull", label="Duller than normal", group="Radiation", icon="cloud", tone="cold",
         priority=4, needs=("SW_IN",),
         about="Mean incoming shortwave radiation is at least one standard deviation below the "
               "calendar-month normal.",
         rule=lambda s: (f"{s['SW_IN']:.0f} {s['u_SW_IN']} mean, {s['SW_IN_anom']:+.0f} "
                         f"{s['u_SW_IN']} against the {s['month_name']} normal "
                         f"({s['SW_IN_z']:+.1f} standard deviations)")
         if s["SW_IN_z"] <= -1 else None),

    dict(key="vpd_high", label="High evaporative demand", group="Radiation", icon="gauge",
         tone="dry", priority=4, needs=("VPD",),
         about="Mean vapour pressure deficit is at least one standard deviation above the "
               "calendar-month normal.",
         rule=lambda s: (f"{s['VPD']:.2f} {s['u_VPD']} mean, {s['VPD_anom']:+.2f} "
                         f"{s['u_VPD']} against the {s['month_name']} normal "
                         f"({s['VPD_z']:+.1f} standard deviations)")
         if s["VPD_z"] >= 1 else None),

    dict(key="soil_dry", label="Dry soil", group="Soil", icon="soil", tone="dry", priority=3,
         needs=("SWC_0.2",),
         about="Mean soil water content at 0.2 m is at least one standard deviation below the "
               "calendar-month normal.",
         rule=lambda s: (f"{s['SWC_0.2']:.1f} {s['u_SWC_0.2']} at 0.2 m, "
                         f"{s['SWC_0.2_anom']:+.1f} {s['u_SWC_0.2']} against the "
                         f"{s['month_name']} normal ({s['SWC_0.2_z']:+.1f} standard deviations)")
         if s["SWC_0.2_z"] <= -1 else None),
]


# ----------------------------------------------------------------------------------------------
# Metrics
#
# What a tile can be coloured by. Each metric names the field it reads on the month, the ramp it is
# drawn with and the daily quantity the micro-strip inside the tile shows. Every colour is a token
# of the shared stylesheet, resolved in the browser, so the light and the dark set stay the only
# place a colour is decided.
#
#   scale 'div'  two poles either side of `center`, neutral at the centre
#   scale 'seq'  one ramp from the low end of the domain to the high end
#
#   day  'value'  the daily statistic itself      'anom'  its departure from the daily normal
#        'flag'   whether the day set a threshold  'meas'  the measured share of the day
# ----------------------------------------------------------------------------------------------

METRICS = [
    dict(key="TA_anom", var="TA", field="anom", scale="div", center=0.0,
         poles=("--pole-cold", "--pole-warm"), digits=1,
         label="Air temperature anomaly", short="TA anomaly",
         about="Monthly mean temperature minus the normal of that calendar month.",
         day=dict(kind="anom", stat="mean")),
    dict(key="TA", var="TA", field="value", scale="div", center=None,
         poles=("--pole-cold", "--pole-warm"), digits=1,
         label="Air temperature, monthly mean", short="TA",
         about="Monthly mean temperature. The colour diverges about the mean of the whole record, "
               "so the seasons separate rather than the years.",
         day=dict(kind="value", stat="mean")),
    dict(key="PREC_pctn", var="PREC", field="pctn", scale="div", center=100.0,
         poles=("--series-4", "--series-1"), digits=0, unit="%",
         label="Precipitation, % of normal", short="PREC % of normal",
         about="Monthly total as a percentage of the normal of that calendar month.",
         day=dict(kind="value", stat="sum")),
    dict(key="PREC", var="PREC", field="value", scale="seq",
         stops=("--seq-1", "--seq-2", "--seq-3", "--seq-4", "--seq-5", "--seq-6", "--seq-7"),
         digits=0, label="Precipitation, monthly total", short="PREC total",
         about="Monthly precipitation total. A month with gaps under-reports, so the measured "
               "share is worth reading beside it.",
         day=dict(kind="value", stat="sum")),
    dict(key="SW_IN", var="SW_IN", field="value", scale="seq",
         stops=("--neutral-mid", "--warm-1", "--warm-2", "--warm-3"), digits=0,
         label="Incoming shortwave, monthly mean", short="SW_IN",
         about="Monthly mean incoming shortwave radiation.",
         day=dict(kind="value", stat="mean")),
    dict(key="VPD", var="VPD", field="value", scale="seq",
         stops=("--neutral-mid", "--series-2"), digits=2,
         label="Vapour pressure deficit, monthly mean", short="VPD",
         about="Monthly mean vapour pressure deficit, the atmosphere's evaporative demand.",
         day=dict(kind="value", stat="mean")),
    dict(key="RH", var="RH", field="value", scale="seq",
         stops=("--neutral-mid", "--series-3"), digits=0,
         label="Relative humidity, monthly mean", short="RH",
         about="Monthly mean relative humidity.",
         day=dict(kind="value", stat="mean")),
    dict(key="SWC_0.2", var="SWC_0.2", field="value", scale="seq",
         stops=("--neutral-mid", "--series-1"), digits=1,
         label="Soil water content at 0.2 m", short="SWC 0.2 m",
         about="Monthly mean volumetric soil water content at 0.2 m, homogenised across the "
               "2020 sensor change.",
         day=dict(kind="value", stat="mean")),
    dict(key="n_hot", var="TA", field="count", count="hot", scale="seq",
         stops=("--neutral-mid", "--warm-1", "--warm-2", "--warm-3"), digits=0, unit="days",
         label="Hot days per month", short="Hot days",
         about="Days with a daily maximum at or above 30 °C.",
         day=dict(kind="flag", flag="hot")),
    dict(key="n_frost", var="TA", field="count", count="frost", scale="seq",
         stops=("--neutral-mid", "--cold-1", "--cold-2"), digits=0, unit="days",
         label="Frost days per month", short="Frost days",
         about="Days with a daily minimum below 0 °C.",
         day=dict(kind="flag", flag="frost")),
    dict(key="meas", var="TA", field="meas", scale="seq",
         stops=("--seq-7", "--seq-4", "--seq-1"), digits=0, unit="%",
         label="Measured share, air temperature", short="Coverage",
         about="Percentage of the month's half-hours that are measured rather than gap-filled or "
               "missing. Dark is complete.",
         day=dict(kind="meas")),
]


# ----------------------------------------------------------------------------------------------
# Small helpers
# ----------------------------------------------------------------------------------------------

def doy365(index):
    """Day of year with 29 February folded onto 1 March, so one array serves every year.

    A daily normal is a smooth function of the date, so sharing one slot between 29 February and
    1 March costs nothing measurable and buys an array that is indexed the same way in a leap year
    and in an ordinary one.
    """
    doy = np.asarray(index.dayofyear)
    leap = np.asarray(index.is_leap_year)
    return np.where(leap & (doy > 59), doy - 1, doy)


def resample_agg(series, freq, how):
    """Resample with a sum that keeps an all-missing period missing.

    `agg('sum')` reports 0 for a period with no records at all, which for precipitation is the
    difference between "it did not rain" and "the gauge was not read".
    """
    if how == "sum":
        return series.resample(freq).sum(min_count=1)
    return series.resample(freq).agg(how)


def rank_of(values, mask):
    """Rank of every qualifying value, 1 = highest, with the others left out of the ranking."""
    ranked = values.where(mask)
    return ranked.rank(ascending=False, method="min").astype("Int64")


def percentile_domain(values, lo=2, hi=98, symmetric=False):
    """A colour domain that a handful of extreme months cannot flatten.

    The tail of a precipitation distribution is long enough that a domain taken from the maximum
    leaves every ordinary month the same pale colour, which is the failure this avoids.
    """
    clean = np.asarray([v for v in values if v is not None and not pd.isna(v)], dtype=float)
    if clean.size == 0:
        return [0.0, 1.0]
    a, b = float(np.percentile(clean, lo)), float(np.percentile(clean, hi))
    if symmetric:
        m = max(abs(a), abs(b)) or 1.0
        return [-m, m]
    if a == b:
        b = a + 1.0
    return [a, b]


# ----------------------------------------------------------------------------------------------
# Load
# ----------------------------------------------------------------------------------------------

def load(keys):
    """Read every calendar variable, with the same integrity checks the dashboards run."""
    out = {}
    for key in keys:
        if key not in VARIABLES:
            raise SystemExit(f"unknown variable {key!r}; known keys: {', '.join(VARIABLES)}")
        v = Variable(key, VARIABLES[key])
        df, _ = load_product(v)
        series = df[v.value]
        measured = ((df[v.fill_flag].eq(v.measured_code) & series.notna()) if v.fill_flag
                    else series.notna())
        out[key] = dict(v=v, df=df, series=series, measured=measured)
        print(f"  {key:<9} {v.path.name:<44} {len(df):>9,} records  "
              f"{measured.mean() * 100:5.1f} % measured")
    return out


def span(loaded):
    """The whole-year span the calendar covers: the union of the variables' own periods."""
    first = min(d["v"].first_year for d in loaded.values())
    last = max(d["v"].last_year for d in loaded.values())
    return first, last


# ----------------------------------------------------------------------------------------------
# Daily and hourly layers
#
# Both are columnar: one flat array per quantity over the whole span, indexed by the number of days
# (or hours) since the start. A month therefore carries an offset and a length instead of its own
# copy of the data, and the page can slice any window without an index of timestamps.
# ----------------------------------------------------------------------------------------------

def daily_frame(loaded, dates):
    """Daily statistics, the measured share of each day and the day flag word."""
    day = {}
    meas = {}
    for key, d in loaded.items():
        v = d["v"]
        agg = d["series"].resample("D").agg(list(v.daily_stats))
        if v.agg == "sum":
            # The gap-preserving sum replaces the one agg() produced, which reports 0 for a day
            # with no records at all.
            agg["sum"] = resample_agg(d["series"], "D", "sum")
        day[key] = agg.reindex(dates)
        meas[key] = (d["measured"].astype(float).resample("D").mean() * 100).reindex(dates)
    return day, meas


def flag_words(flags, day, dates):
    """One integer per day holding every threshold that day set."""
    word = np.zeros(len(dates), dtype="int64")
    counts = {}
    for f in flags:
        stat = day[f["var"]][f["stat"]]
        hit = (stat.lt(f["value"]) if f["op"] == "lt" else stat.ge(f["value"])).fillna(False)
        counts[f["key"]] = hit
        word |= hit.to_numpy().astype("int64") << f["bit"]
    return pd.Series(word, index=dates), counts


def daily_normals(day, dates, keys):
    """The normal course of the year for every shipped daily statistic.

    Built from a centred window of `CLIM_WINDOW` days around each calendar date, pooled across all
    years, so a single cold 14 July does not become the normal for 14 July. The window is circular:
    the days around New Year use the end of the previous year.
    """
    doy = doy365(dates)
    normals = {}
    for key in keys:
        stats = {}
        for stat in ("mean", "sum", "min", "max"):
            if stat not in day[key].columns:
                continue
            values = day[key][stat].to_numpy(dtype=float)
            mean = np.full(366, np.nan)
            p10 = np.full(366, np.nan)
            p90 = np.full(366, np.nan)
            for target in range(1, 366):
                dist = np.abs(doy - target)
                sel = np.minimum(dist, 365 - dist) <= CLIM_WINDOW
                block = values[sel]
                block = block[~np.isnan(block)]
                if block.size < 20:
                    continue
                mean[target] = block.mean()
                p10[target] = np.percentile(block, 10)
                p90[target] = np.percentile(block, 90)
            stats[stat] = dict(mean=[r(x, 2) for x in mean],
                               p10=[r(x, 2) for x in p10], p90=[r(x, 2) for x in p90])
        normals[key] = stats
    return normals


def hourly_layer(loaded, first_year, last_year):
    """The diurnal detail, as one flat integer array per variable.

    Stored scaled to whole numbers because the precision the day panel draws at is a tenth of a
    degree, and a full float repr of two hundred thousand values is most of the finished page.
    """
    start = pd.Timestamp(f"{first_year}-01-01 00:00")
    stop = pd.Timestamp(f"{last_year}-12-31 23:00")
    index = pd.date_range(start, stop, freq="h")
    out = {}
    for key, d in loaded.items():
        cfg = CALENDAR[key]
        if not cfg["hourly"]:
            continue
        how = "sum" if d["v"].agg == "sum" else "mean"
        series = resample_agg(d["series"], "h", how).reindex(index)
        scaled = (series * cfg["scale"]).round()
        out[key] = dict(scale=cfg["scale"], units=d["v"].units, title=d["v"].title,
                        values=[None if pd.isna(x) else int(x) for x in scaled])
    assert not out or len(index) == (pd.Timestamp(f"{last_year}-12-31") -
                                     pd.Timestamp(f"{first_year}-01-01")).days * 24 + 24, \
        "the hourly index is not a whole number of days"
    return dict(start=f"{first_year}-01-01", n=len(index), vars=out)


# ----------------------------------------------------------------------------------------------
# Monthly layer, normals and badges
# ----------------------------------------------------------------------------------------------

def monthly_frames(loaded, months):
    """Monthly aggregate, measured share and available share, per variable."""
    out = {}
    for key, d in loaded.items():
        v = d["v"]
        value = resample_agg(d["series"], "MS", v.agg).reindex(months)
        meas = (d["measured"].astype(float).resample("MS").mean() * 100).reindex(months)
        avail = (d["series"].notna().astype(float).resample("MS").mean() * 100).reindex(months)
        out[key] = dict(value=value, meas=meas, avail=avail)
    return out


def normals(monthly, months):
    """Calendar-month normals from the months complete enough to support one.

    A normal built from whatever happens to be present would be pulled by exactly the months that
    are least trustworthy, and every anomaly and rank derived from it would inherit that. The
    qualifying rule is stated once here and used by everything downstream.
    """
    out = {}
    for key, frames in monthly.items():
        value, meas = frames["value"], frames["meas"]
        qualifies = meas >= NORMAL_MIN_COVERAGE
        by_month = {}
        for m in range(1, 13):
            sel = (months.month == m) & qualifies.to_numpy()
            block = value[sel].dropna()
            if len(block) < MIN_NORMAL_YEARS:
                by_month[m] = None
                continue
            by_month[m] = dict(mean=float(block.mean()), sd=float(block.std()), n=int(len(block)),
                               min=float(block.min()), max=float(block.max()),
                               min_year=int(block.idxmin().year), max_year=int(block.idxmax().year))
        # Ranks are computed within the qualifying months only, so a sparse month is not ranked.
        ranks = pd.Series(pd.NA, index=months, dtype="Int64")
        for m in range(1, 13):
            sel = months.month == m
            ranks[sel] = rank_of(value[sel], qualifies[sel])
        out[key] = dict(by_month=by_month, ranks=ranks, qualifies=qualifies)
    return out


def month_stats(y, m, keys, monthly, norm, counts_month, spells, day, dates, loaded):
    """Every number a badge rule may read, for one month, as one flat dictionary."""
    ts = pd.Timestamp(y, m, 1)
    s = dict(y=y, m=m, month_name=calendar.month_name[m],
             n_days=calendar.monthrange(y, m)[1])
    for key in keys:
        v = loaded[key]["v"]
        frames, n = monthly[key], norm[key]
        value = frames["value"].get(ts)
        value = None if pd.isna(value) else float(value)
        nm = n["by_month"][m]
        rank = n["ranks"].get(ts)
        s[key] = value
        s[f"u_{key}"] = v.units
        s[f"{key}_meas"] = None if pd.isna(frames["meas"].get(ts)) else float(frames["meas"][ts])
        s[f"{key}_avail"] = None if pd.isna(frames["avail"].get(ts)) else float(frames["avail"][ts])
        s[f"{key}_norm"] = nm["mean"] if nm else None
        s[f"{key}_sd"] = nm["sd"] if nm else None
        s[f"{key}_n"] = nm["n"] if nm else None
        s[f"{key}_rank"] = None if pd.isna(rank) else int(rank)
        if value is not None and nm:
            s[f"{key}_anom"] = value - nm["mean"]
            s[f"{key}_z"] = (value - nm["mean"]) / nm["sd"] if nm["sd"] else None
            s[f"{key}_pctn"] = 100 * value / nm["mean"] if nm["mean"] > 0 else None
        else:
            s[f"{key}_anom"] = s[f"{key}_z"] = s[f"{key}_pctn"] = None

        # The extreme day of the month, which is what a badge quotes as its evidence.
        block = day[key].loc[f"{y}-{m:02d}"]
        for stat in ("min", "max", "sum"):
            if stat in block.columns:
                col = block[stat].dropna()
                s[f"{key}_day{stat}"] = float(col.max()) if len(col) else None
        if "min" in block.columns:
            col = block["min"].dropna()
            s[f"{key}_daymin"] = float(col.min()) if len(col) else None

    for key, series in counts_month.items():
        s[f"n_{key}"] = int(series.get(ts, 0))
    for key, series in spells.items():
        s[f"spell_{key}"] = int(series.get(ts, 0))
    return s


def evaluate_badges(s, keys):
    """Which badges this month earns, and what each of them rests on.

    A rule that reads a key the statistics do not carry is a bug in the registry, not a month
    without a badge, so the KeyError is re-raised naming the badge rather than swallowed.
    """
    earned, suppressed = [], []
    for badge in BADGES:
        blocked = None
        for need in badge["needs"]:
            if need not in keys:
                blocked = f"{need} is not included in this build"
            elif s[need] is None:
                blocked = f"no {need} data in this month"
            elif s[f"{need}_meas"] is None or s[f"{need}_meas"] < MIN_BADGE_COVERAGE:
                blocked = (f"only {s[f'{need}_meas']:.0f} % of {need} is measured, below the "
                           f"{MIN_BADGE_COVERAGE:.0f} % a badge needs")
            elif badge.get("needs_normal", True) and s[f"{need}_norm"] is None:
                blocked = f"{need} has no normal for this calendar month"
            if blocked:
                break
        if blocked:
            suppressed.append(dict(key=badge["key"], why=blocked))
            continue
        try:
            why = badge["rule"](s)
        except KeyError as exc:
            raise KeyError(f"badge {badge['key']!r} reads {exc}, which the month statistics do "
                           f"not carry") from None
        if why:
            earned.append(dict(k=badge["key"], t=why))
    earned.sort(key=lambda b: next(x["priority"] for x in BADGES if x["key"] == b["k"]))
    return earned, suppressed


# ----------------------------------------------------------------------------------------------
# Payload
# ----------------------------------------------------------------------------------------------

def build_payload(loaded, with_hourly=True):
    keys = list(loaded)
    first_year, last_year = span(loaded)
    dates = pd.date_range(f"{first_year}-01-01", f"{last_year}-12-31", freq="D")
    months = pd.date_range(f"{first_year}-01-01", f"{last_year}-12-01", freq="MS")

    flags = day_flags({k: loaded[k]["v"] for k in keys})
    day, meas = daily_frame(loaded, dates)
    word, hits = flag_words(flags, day, dates)

    counts_month = {k: v.resample("MS").sum().reindex(months) for k, v in hits.items()}
    # Spells are the runs a count cannot show: a month can reach a high count without ever holding
    # the threshold for a week. The dry spell is the one run defined by the absence of a threshold.
    spell_defs = dict(hot=hits["hot"], frost=hits["frost"], wet=hits["wet"],
                      dry=~hits["wet"] & day["PREC"]["sum"].notna())
    spells = {}
    for name, mask in spell_defs.items():
        spells[name] = pd.Series({ts: longest_spell(mask.loc[f"{ts:%Y-%m}"])[0] for ts in months},
                                 dtype="int64")

    monthly = monthly_frames(loaded, months)
    norm = normals(monthly, months)

    # -- Months ------------------------------------------------------------------------------
    rows, all_stats = [], []
    for ts in months:
        y, m = int(ts.year), int(ts.month)
        s = month_stats(y, m, keys, monthly, norm, counts_month, spells, day, dates, loaded)
        earned, suppressed = evaluate_badges(s, keys)
        all_stats.append(s)
        row = dict(y=y, m=m, i0=int((ts - dates[0]).days), n=int(s["n_days"]),
                   b=earned, sup=suppressed,
                   c={k: int(s[f"n_{k}"]) for k in hits},
                   sp={k: int(s[f"spell_{k}"]) for k in spells})
        for key in keys:
            digits = CALENDAR[key]["digits"]
            row[key] = dict(v=r(s[key], digits), a=r(s[f"{key}_anom"], digits),
                            z=r(s[f"{key}_z"], 2), p=r(s[f"{key}_pctn"], 0),
                            r=s[f"{key}_rank"], n=s[f"{key}_n"],
                            meas=r(s[f"{key}_meas"], 0), avail=r(s[f"{key}_avail"], 0))
        rows.append(row)

    # -- Metric domains ----------------------------------------------------------------------
    # Computed here rather than in the browser so the scale bar, the tiles and the day strips all
    # read one domain, and so it does not move when a filter hides part of the grid.
    metrics = []
    for metric in METRICS:
        key, var, field = metric["key"], metric["var"], metric["field"]
        if var not in keys:
            continue
        if field == "count":
            values = [row["c"][metric["count"]] for row in rows]
            daily_values = [1.0]
        else:
            short = dict(value="v", anom="a", pctn="p", meas="meas")[field]
            values = [row[var][short] for row in rows]
            stat = metric["day"].get("stat")
            daily_values = ([] if metric["day"]["kind"] in ("flag", "meas")
                            else day[var][stat].dropna().tolist())
        if field == "meas":
            domain, day_domain = [0.0, 100.0], [0.0, 100.0]
        elif metric["scale"] == "div":
            # A diverging scale is symmetric about its centre, or the same departure reads as two
            # different colours depending on its sign. Where no centre is given the record's own
            # mean is it, which is what makes an absolute temperature tile separate the seasons.
            center = metric["center"]
            if center is None:
                center = float(np.nanmean([x for x in values if x is not None]))
            spread = percentile_domain([(x - center) if x is not None else None for x in values],
                                       symmetric=True)
            domain = [center + spread[0], center + spread[1]]
            if metric["day"]["kind"] == "value":
                spread = percentile_domain([x - center for x in daily_values], symmetric=True)
                day_domain = [center + spread[0], center + spread[1]]
            else:
                day_domain = percentile_domain(daily_values, symmetric=True) if daily_values \
                    else [-1.0, 1.0]
        else:
            # A quantity that accumulates is read against zero, so its ramp starts there; one that
            # does not would waste most of the ramp on values the record never reaches.
            center = None
            floor_at_zero = field == "count" or VARIABLES[var].get("agg") == "sum"
            domain = percentile_domain(values)
            day_domain = percentile_domain(daily_values) if daily_values else [0.0, 1.0]
            if floor_at_zero:
                domain = [0.0, domain[1]]
                day_domain = [0.0, day_domain[1]]
        entry = {k: metric[k] for k in ("key", "label", "short", "about", "scale", "digits", "day")}
        entry.update(var=var, field=field, count=metric.get("count"),
                     units=metric.get("unit", loaded[var]["v"].units),
                     poles=list(metric.get("poles", [])), stops=list(metric.get("stops", [])),
                     center=r(center, 3), domain=[r(domain[0], 3), r(domain[1], 3)],
                     day_domain=[r(day_domain[0], 3), r(day_domain[1], 3)])
        metrics.append(entry)

    # -- Badge registry, with the icons checked against the ones the page can draw ------------
    icons = set(re.findall(r"^\s{4}'([\w-]+)':", (ASSETS / "calendar.js").read_text(encoding="utf-8"),
                           flags=re.M))
    badge_meta = []
    for badge in BADGES:
        assert badge["icon"] in icons, (
            f"badge {badge['key']!r} asks for icon {badge['icon']!r}, which calendar.js does not "
            f"draw - it would render as an empty box")
        n = sum(1 for row in rows for b in row["b"] if b["k"] == badge["key"])
        badge_meta.append(dict(key=badge["key"], label=badge["label"], group=badge["group"],
                               icon=badge["icon"], tone=badge["tone"],
                               about=badge["about"].format(sparse=SPARSE_COVERAGE), n=n))

    # -- Variables and their day flags --------------------------------------------------------
    variables = []
    for key in keys:
        v = loaded[key]["v"]
        variables.append(dict(key=key, title=v.title, short=CALENDAR[key]["short"], units=v.units,
                              digits=CALENDAR[key]["digits"], agg=v.agg, product=v.path.name,
                              column=v.value, ship=list(CALENDAR[key]["ship"]),
                              first_year=int(v.first_year), last_year=int(v.last_year),
                              about=v.about))

    payload = dict(
        meta=dict(
            site=SITE, site_long=SITE_LONG,
            first_year=int(first_year), last_year=int(last_year),
            n_months=len(rows), n_days=len(dates),
            generated=datetime.now().strftime("%Y-%m-%d %H:%M"),
            min_badge_coverage=MIN_BADGE_COVERAGE, normal_min_coverage=NORMAL_MIN_COVERAGE,
            min_normal_years=MIN_NORMAL_YEARS, sparse_coverage=SPARSE_COVERAGE,
            clim_window=CLIM_WINDOW,
            products=str(PRODUCTS),
        ),
        variables=variables,
        metrics=metrics,
        badges=badge_meta,
        flags=[dict(key=f["key"], var=f["var"], bit=f["bit"], label=f["label"]) for f in flags],
        months=rows,
        days=dict(
            start=f"{dates[0]:%Y-%m-%d}", n=len(dates),
            flags=[int(x) for x in word.to_numpy()],
            series={f"{key}_{stat}": rlist(day[key][stat], CALENDAR[key]["digits"])
                    for key in keys for stat in CALENDAR[key]["ship"]},
            meas={key: [None if pd.isna(x) else int(round(x)) for x in meas[key].to_numpy()]
                  for key in keys},
        ),
        normals=daily_normals(day, dates, keys),
        climatology={key: {str(m): norm[key]["by_month"][m] for m in range(1, 13)} for key in keys},
        hourly=hourly_layer(loaded, first_year, last_year) if with_hourly else None,
    )

    # The grid is the page, so its shape is asserted rather than assumed: one tile per month of
    # every year, and every tile addressing a real window of the daily arrays.
    assert len(rows) == (last_year - first_year + 1) * 12, "the grid is not a whole number of years"
    assert all(row["i0"] + row["n"] <= len(dates) for row in rows), "a month runs past the days"
    return payload


# ----------------------------------------------------------------------------------------------
# Render
# ----------------------------------------------------------------------------------------------

def render(payload, out_path):
    """Inline the assets and the payload into one self-contained HTML file."""
    template = (ASSETS / "template.html").read_text(encoding="utf-8")
    css = SHARED_CSS.read_text(encoding="utf-8") + "\n" + (ASSETS / "calendar.css").read_text(
        encoding="utf-8")
    js = (ASSETS / "calendar.js").read_text(encoding="utf-8")

    # `</script>` inside the JSON would end the tag early, and `<!--` would open a comment.
    data = (json.dumps(payload, allow_nan=False, separators=(",", ":"))
            .replace("</", "<\\/").replace("<!--", "<\\!--"))
    m = payload["meta"]

    html = (template
            .replace("/*__CSS__*/", css)
            .replace("/*__DATA__*/", data)
            .replace("/*__JS__*/", js)
            .replace("__TITLE__", f"{m['site']} — meteo calendar "
                                  f"{m['first_year']}–{m['last_year']}"))

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    return out_path


def build(keys, out=None, outdir=None, with_hourly=True):
    print(f"reading {len(keys)} products from {PRODUCTS} ...")
    loaded = load(keys)
    first_year, last_year = span(loaded)
    print(f"building {(last_year - first_year + 1) * 12} months, "
          f"{first_year}–{last_year}{'' if with_hourly else ', without hourly detail'} ...")

    payload = build_payload(loaded, with_hourly=with_hourly)
    counted = sorted(((b["n"], b["label"]) for b in payload["badges"]), reverse=True)
    print("  badges awarded: " + ", ".join(f"{label} {n}" for n, label in counted if n))

    path = render(payload, out or Path(outdir or OUTDIR) / "METEO_CALENDAR_explorer.html")
    print(f"  written: {path}  ({path.stat().st_size / 1024 / 1024:.1f} MB)")
    return path


def main(argv=None):
    # Units carry superscripts and degree signs, which a console still on a legacy code page cannot
    # encode - and a build that has done its work must not fail on printing a unit.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):  # a redirected stream may not support it
        pass

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--vars", help="comma-separated variable keys; the default is "
                                       + ",".join(CALENDAR))
    parser.add_argument("--out", help="output HTML file")
    parser.add_argument("--outdir", help="output directory; the default is the external data folder")
    parser.add_argument("--no-hourly", action="store_true",
                        help="leave out the hourly arrays behind the day panel's diurnal charts")
    parser.add_argument("--list", action="store_true",
                        help="list the variables, metrics and badges this page is built from")
    parser.add_argument("--open", dest="open_browser", action="store_true",
                        help="open the finished page in the default browser")
    args = parser.parse_args(argv)

    if args.list:
        print(f"{'variable':<10} {'units':<14} {'hourly':<7} product")
        for key, cfg in CALENDAR.items():
            path = PRODUCTS / VARIABLES[key]["file"]
            print(f"{key:<10} {VARIABLES[key]['units']:<14} {'yes' if cfg['hourly'] else 'no':<7} "
                  f"{VARIABLES[key]['file']}{'' if path.exists() else '   MISSING'}")
        print(f"\n{len(METRICS)} metrics: " + ", ".join(m["key"] for m in METRICS))
        print(f"{len(BADGES)} badges:")
        for badge in BADGES:
            print(f"  {badge['key']:<12} {badge['group']:<14} {badge['label']}")
        return 0

    keys = [k.strip() for k in args.vars.split(",")] if args.vars else list(CALENDAR)
    unknown = [k for k in keys if k not in CALENDAR]
    if unknown:
        parser.error(f"unknown variable(s) {', '.join(unknown)}; known keys: {', '.join(CALENDAR)}")
    # Every badge that reads a variable not in the build is withheld rather than silently absent,
    # which the month view reports - so a partial build is allowed, but it says what it lost.
    path = build(keys, out=args.out, outdir=args.outdir, with_hourly=not args.no_hourly)
    if args.open_browser:
        webbrowser.open(path.resolve().as_uri())
    return 0


if __name__ == "__main__":
    sys.exit(main())
