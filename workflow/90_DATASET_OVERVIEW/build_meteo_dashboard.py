"""Build a self-contained interactive HTML dashboard for a CH-LAE meteo product.

The dashboard is the one-page form of the overview notebooks in this folder: the same products, the
same conventions, the same integrity checks, condensed into a single page a reader can scan without
running a notebook. It computes and corrects nothing - a value shown here is exactly what the
notebook in `10_METEO/30_PRODUCTS/` exported.

What it produces is **one HTML file with no external assets**: the data are embedded as JSON, the
charts are drawn by a small SVG renderer that ships inside the page, and the light and dark themes
are two selected sets of tokens rather than an automatic inversion. It therefore opens from disk,
travels by e-mail, and needs no server.

One engine, one entry per variable
----------------------------------
Everything variable-specific lives in the `VARIABLES` registry below; nothing above or below it
mentions a particular measurement. A registry entry names the file and its columns, and switches on
only the sections that variable actually supports - a product with no source flag draws no
instrument card, one with no reference station draws no comparison, one with no threshold days
draws no threshold section. Adding a variable is adding a dictionary.

**The corrected column is the product.** Where a product exports the series twice - as the
instrument reported it and homogenised across a hardware change - the registry points `value` at the
homogenised column and `uncorrected` at the other. The page shows the homogenised column throughout;
the uncorrected one is read only by the integrity checks, which measure what the correction does and
assert that it acts where it should. It is not a second product and is not offered as one.

Usage
-----
    uv run python workflow/90_DATASET_OVERVIEW/build_meteo_dashboard.py --list
    uv run python workflow/90_DATASET_OVERVIEW/build_meteo_dashboard.py --var TA --open
    uv run python workflow/90_DATASET_OVERVIEW/build_meteo_dashboard.py --var SW_IN
    uv run python workflow/90_DATASET_OVERVIEW/build_meteo_dashboard.py --all

`deploy.ps1` runs the last form with `--outdir docs/_build/html/dashboards`, **after** the Quarto
render: Quarto rewrites its output tree on every render, so a dashboard placed there beforehand
would be deleted. Building straight into the output tree also keeps five megabytes of generated
HTML out of the source tree, and keeps Quarto from seeing files it has no reason to touch.

Author: Lukas Hoertnagl (holukas@ethz.ch)
"""

from __future__ import annotations

import argparse
import calendar
import json
import math
import sys
import webbrowser
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import kendalltau, theilslopes

# ----------------------------------------------------------------------------------------------
# Where things live
# ----------------------------------------------------------------------------------------------

# Data files live in the external (untracked) data folder, mirroring the workflow tree of this repo.
DATA_ROOT = Path(r"F:\Sync\luhk_work\dev-data\datasets-data\dataset_ch-lae_flux_product-data")
PRODUCTS = DATA_ROOT / "workflow" / "10_METEO" / "30_PRODUCTS"
REFERENCES = DATA_ROOT / "workflow" / "10_METEO" / "10_REFERENCE"
OUTDIR = DATA_ROOT / "workflow" / "90_DATASET_OVERVIEW"

# Assets that make up the page. They sit beside this script and are inlined into the output.
ASSETS = Path(__file__).parent / "dashboard_assets"

SITE = "CH-LAE"
SITE_LONG = "L\u00e4geren, Switzerland \u2014 mixed forest"
SITE_LAT = 47.478333
SITE_LON = 8.364389
TIMEZONE_OFFSET_TO_UTC_HOURS = 1  # CET (winter time), the timezone the products are stored in

N_RECENT_YEARS = 10  # length of the recent period in the period means
N_EXTREMES = 10  # number of records listed in the extremes tables

# ----------------------------------------------------------------------------------------------
# Shared legends
#
# TA and RH come from one probe, so their source flags are the same flag, and VPD is computed from
# both and carries it unchanged. The legend is therefore written once.
# ----------------------------------------------------------------------------------------------

PROBE_SOURCE_LEGEND = {
    0: "Campbell CS215, SDI-12 (from 21 Jan 2016)",
    1: "Rotronic MP101A, analog (to 31 Dec 2015)",
    2: "acquisition changeover, era undetermined",
    3: "before the tower record begins",
}
PROBE_SOURCE_SHORT = {0: "CS215", 1: "MP101A", 2: "changeover", 3: "before record"}

MS_LAEGERN = dict(file="MeteoSwiss_LAE_30MIN_2004-2025.parquet",
                  station="MeteoSwiss L\u00e4geren", distance_km=2.5, elevation_m=845)


def ta_correction_checks(delta_pre, delta_post, units):
    """Assert the shape of the two corrections the TA homogenisation applies.

    Before the sensor change the difference between the two columns is a single positive constant,
    the zero-point error of the old analog chain. After it the difference is the radiation-shield
    term: never positive, exactly zero wherever there is no sun to drive it, and not a constant. If
    it were a constant it would be a second offset rather than a correction to the shape of the day,
    and every daily statistic on the page would mean something different.

    Passed to the registry as a hook rather than run unconditionally, because it describes this
    correction and not homogenisation in general.
    """
    assert delta_pre.nunique() == 1, \
        f"the pre-break offset is not a single constant: {sorted(delta_pre.unique())}"
    assert float(delta_pre.iloc[0]) > 0, "the pre-break correction does not raise the earlier era"
    assert (delta_post <= 0).all(), (
        f"the shield term warms the later era by up to {delta_post.max():+.4f} {units} somewhere - "
        f"it removes a warm bias and can only ever cool")
    assert (delta_post == 0).any(), \
        "the shield term is nowhere zero, so it is not acting only where there is radiation"
    assert delta_post.nunique() > 100, (
        f"the post-break correction takes only {delta_post.nunique()} distinct values - it is "
        f"behaving like a second constant rather than a term that follows the radiation")


# ----------------------------------------------------------------------------------------------
# The registry
#
# Keys used by an entry (everything but the first six is optional):
#
#   title, units, file, value          what the product is and where it is
#   first_year, last_year              whole years only; a partial first year is excluded
#   limits          (lo, hi)           wide physical bounds; they catch a broken unit, not a
#                                      remarkable day
#   about                              the opening paragraph of the page
#   uncorrected                        the same series as the instrument reported it. Present only
#                                      where the product exports both; read by the integrity checks
#   correction_checks                  hook asserting the shape of that correction
#   correction_note                    how the correction is described on the page
#   fill_flag, fill_legend,            provenance of each record. Without a fill flag, "measured"
#   fill_short, measured_code          means simply "not missing"
#   source_flag, source_legend,        which instrument produced each record
#   source_short
#   agg             'mean' | 'sum'     how the variable aggregates over time
#   daily_stats                        daily statistics to compute
#   ribbon          band, line         what the whole-record figure draws
#   index_groups                       threshold-day definitions, grouped and ramped
#   growing_season  base               only where a growing season means something
#   reference                          station file and column for the residual comparison
#   extremes        high, low          wording for the two ends of the scale
#   notes                              extra paragraphs under the tiles
# ----------------------------------------------------------------------------------------------

VARIABLES = {

    "TA": dict(
        title="Air temperature",
        units="\u00b0C",
        file="02_METEO_TA_GAPFILLED_2004-2025.parquet",
        value="TA_T1_47_1_HOMOGENIZED_gfXG",
        uncorrected="TA_T1_47_1_gfXG",
        correction_checks=ta_correction_checks,
        correction_note=(
            "The 47 m record spans two instruments: a Rotronic MP101A on an analog chain to "
            "31 Dec 2015 and a Campbell CS215 on SDI-12 from {break_ts}. The old chain carried a "
            "zero-point error and read about 1.3 {units} too cold, and the two sensors' radiation "
            "shields differ, which acts in daylight only. The homogenisation raises the earlier era "
            "by a constant {offset} and removes up to {shield_max} of radiation-shield excess from "
            "the later one. Both constants are re-measured from the file on every build."),
        first_year=2005, last_year=2025,
        limits=(-40.0, 45.0),
        about=(
            "Air temperature measured at 47 m on the tower, gap-filled and homogenised across the "
            "January 2016 sensor change. This is the column to use for anything that compares one "
            "year with another."),
        fill_flag="FLAG_TA_T1_47_1_ISFILLED",
        fill_legend={0: "measured", 1: "XGBoost model", 2: "timestamp-only fallback model",
                     4: "linear interpolation (short gap)", 5: "reconstructed from NABEL at 49 m"},
        fill_short={1: "XGBoost", 2: "timestamp-only", 4: "interpolated", 5: "NABEL 49 m"},
        source_flag="FLAG_TA_T1_47_1_SOURCE",
        source_legend=PROBE_SOURCE_LEGEND, source_short=PROBE_SOURCE_SHORT,
        index_groups=[
            dict(title="Cold indices", ramp="cold",
                 sub="Frost days have a daily minimum below 0 {units}; ice days a daily maximum "
                     "below it.",
                 items=[dict(key="frost", label="frost days (min < 0 {units})", stat="min",
                             op="lt", value=0.0),
                        dict(key="ice", label="ice days (max < 0 {units})", stat="max",
                             op="lt", value=0.0)]),
            dict(title="Warm indices", ramp="warm",
                 sub="Summer days reach 25 {units}, hot days 30 {units}, and a tropical night stays "
                     "above 20 {units}. Counts built on a daily maximum are the ones most exposed "
                     "to whatever daytime inhomogeneity the correction leaves behind.",
                 items=[dict(key="summer", label="summer days (max \u2265 25 {units})", stat="max",
                             op="ge", value=25.0),
                        dict(key="hot", label="hot days (max \u2265 30 {units})", stat="max",
                             op="ge", value=30.0),
                        dict(key="tropical", label="tropical nights (min \u2265 20 {units})",
                             stat="min", op="ge", value=20.0)]),
        ],
        growing_season=5.0,
        reference=dict(column="TA_LAE_MS", split="nightday", **MS_LAEGERN),
        reference_note=(
            "The split into night and day is the point. The constant was derived at night, where a "
            "radiation-shield error cannot contribute, and the shield term was derived against the "
            "aspirated NABEL sensor and acts only in sunlight, so the night residual tests the "
            "first and the day residual the second."),
        extremes=dict(high="warmest", low="coldest"),
    ),

    "SW_IN": dict(
        title="Incoming shortwave radiation",
        units="W m\u207b\u00b2",
        file="01_METEO_SW_IN_GAPFILLED_2004-2025.parquet",
        value="SW_IN_T1_47_1_gfXG",
        first_year=2006, last_year=2025,
        limits=(-20.0, 1400.0),
        about=(
            "Incoming shortwave radiation measured at 47 m on the tower, gap-filled. The tower "
            "record begins on 14 September 2005, so this page starts with the first complete year. "
            "The series was tested at both hardware changes \u2014 the 2016 logger replacement and "
            "the December 2021 CNR1 \u2192 CNR4 swap \u2014 and steps at neither, which is why "
            "there is only one column and no homogenised second one."),
        fill_flag="FLAG_SW_IN_T1_47_1_ISFILLED",
        fill_legend={0: "observed", 1: "daytime gap, XGBoost model",
                     2: "daytime gap, timestamp-only fallback model",
                     3: "nighttime gap, set to zero by physics"},
        fill_short={1: "XGBoost", 2: "timestamp-only", 3: "night zero"},
        agg="mean",
        daily_stats=("mean", "max"),
        ribbon=dict(band=("mean", "max"), band_label="daily mean to daily maximum", line=None),
        extremes=dict(high="brightest", low="dimmest", low_halfhour=False),
        notes=[
            "Two changes in this record are documented rather than corrected: the tower "
            "pyranometer rises about 3 % from 2013, and neither hardware change moves the series. "
            "Both develop over years rather than stepping at a date, so there is no boundary at "
            "which a correction could be applied.",
            "There is deliberately no comparison against the MeteoSwiss station on this page. "
            "Radiation errors are multiplicative, so radiation has to be compared in ratios under "
            "controls for season, illumination and how sunny the year was; and the station's own "
            "instrumentation was rebuilt on 6 October 2010, so a tower-minus-L\u00e4geren "
            "difference is not evidence about the tower across that date. The attribution is done "
            "properly in <code>10_METEO/30_PRODUCTS/RADIATION_SENSOR_CONTINUITY.ipynb</code>.",
        ],
    ),

    "PPFD_IN": dict(
        title="Incoming photosynthetic photon flux density",
        units="\u00b5mol m\u207b\u00b2 s\u207b\u00b9",
        file="03_METEO_PPFD_IN_GAPFILLED_2004-2025.parquet",
        value="PPFD_IN_T1_47_1_gfXG",
        first_year=2006, last_year=2025,
        limits=(-40.0, 2600.0),
        about=(
            "Incoming photosynthetic photon flux density at 47 m, gap-filled. Like incoming "
            "shortwave, it is exported as a single column: the series was tested at its hardware "
            "changes and does not step at them."),
        fill_flag="FLAG_PPFD_IN_T1_47_1_ISFILLED",
        fill_legend={0: "observed", 1: "XGBoost model", 2: "timestamp-only fallback model",
                     3: "nighttime gap, set to zero by physics",
                     4: "linear interpolation (short gap)"},
        fill_short={1: "XGBoost", 2: "timestamp-only", 3: "night zero", 4: "interpolated"},
        daily_stats=("mean", "max"),
        ribbon=dict(band=("mean", "max"), band_label="daily mean to daily maximum", line=None),
        extremes=dict(high="brightest", low="dimmest", low_halfhour=False),
        notes=[
            "This sensor has been falling about 7 % since 2021 and is still falling. The drift is "
            "documented rather than corrected: it develops over years rather than stepping at a "
            "date, and no fieldbook entry names a cause. Correcting an unattributed drift towards "
            "a reference replaces a measurement with a guess.",
        ],
    ),

    "RH": dict(
        title="Relative humidity",
        units="%",
        file="04_METEO_RH_CORRECTED_2004-2025.parquet",
        value="RH_T1_47_1",
        first_year=2005, last_year=2025,
        limits=(0.0, 100.5),
        about=(
            "Relative humidity at 47 m, corrected and with the damaged periods removed. Records "
            "that could not be measured are reconstructed from a co-located sensor rather than "
            "modelled; the provenance flag says which."),
        fill_flag="FLAG_RH_T1_47_1_MISSING",
        fill_legend={0: "measured at 47 m (corrected)", 1: "missing, never measured",
                     2: "missing, removed here as faulty", 3: "reconstructed from NABEL at 49 m",
                     4: "reconstructed from MeteoSwiss L\u00e4geren"},
        fill_short={1: "never measured", 2: "removed as faulty", 3: "NABEL 49 m",
                    4: "MeteoSwiss LAE"},
        source_flag="FLAG_RH_T1_47_1_SOURCE",
        source_legend=PROBE_SOURCE_LEGEND, source_short=PROBE_SOURCE_SHORT,
        reference=dict(column="RH_LAE_MS", split="nightday", **MS_LAEGERN),
        extremes=dict(high="most humid", low="driest"),
    ),

    "PA": dict(
        title="Air pressure",
        units="kPa",
        file="05_METEO_PA_2005-2025.parquet",
        value="PA_T1_47_1",
        first_year=2006, last_year=2025,
        limits=(80.0, 105.0),
        about=(
            "Air pressure at 47 m, exported as measured. There is no gap-filling and no correction, "
            "so the record carries its gaps; the coverage section says where they are."),
        reference=dict(column="PA_LAE_MS", split=None, **MS_LAEGERN),
        reference_note=(
            "The station sits about 160 m above the tower, so a constant offset is expected. What "
            "matters is whether that offset stays constant."),
        extremes=dict(high="highest", low="lowest"),
    ),

    "LW_IN": dict(
        title="Incoming longwave radiation",
        units="W m\u207b\u00b2",
        file="06_METEO_LW_IN_2005-2025.parquet",
        value="LW_IN_T1_47_1",
        first_year=2006, last_year=2025,
        limits=(100.0, 500.0),
        about=(
            "Incoming longwave radiation at 47 m, exported as measured with its gaps. The source "
            "flag names the pyrgeometer era, including the period in which the CNR1 was read with "
            "the pyranometer's calibration factor and therefore reads low."),
        source_flag="FLAG_LW_IN_T1_47_1_SOURCE",
        source_legend={0: "CNR4 on its own calibration factor",
                       1: "CNR1 at the pyrgeometer's own sensitivity",
                       2: "CNR1 at the pyranometer factor \u2014 reads low",
                       3: "changeover, era undetermined"},
        source_short={0: "CNR4", 1: "CNR1", 2: "CNR1 (low)", 3: "changeover"},
        extremes=dict(high="highest", low="lowest"),
        notes=[
            "No weather service near the site measures longwave, so this variable has no external "
            "reference and no comparison card. The source flag is what carries its provenance.",
        ],
    ),

    "VPD": dict(
        title="Vapour pressure deficit",
        units="kPa",
        file="07_METEO_VPD_2004-2025.parquet",
        # One value column, and deliberately no homogenised one. VPD is computed from two inputs
        # of which only TA can be put on one level across January 2016: the RH product carries no
        # homogenised column either, because its step depends on the humidity itself. A
        # VPD_..._HOMOGENIZED column would claim a continuity that only half its inputs have, so
        # notebook 07 does not export one and this dashboard must not ask for one.
        value="VPD_T1_47_1",
        first_year=2005, last_year=2025,
        limits=(0.0, 8.0),
        about=(
            "Vapour pressure deficit at 47 m, computed by formula from the air temperature and "
            "relative humidity products. Its flag says what each record was computed from rather "
            "than how it was filled: every VPD record follows from the formula."),
        fill_flag="FLAG_VPD_T1_47_1_ISFILLED",
        fill_legend={0: "computed from measured TA and RH",
                     5: "computed from measured RH and gap-filled TA",
                     6: "computed from RH reconstructed from NABEL at 49 m",
                     7: "computed from RH reconstructed from MeteoSwiss L\u00e4geren"},
        fill_short={5: "gap-filled TA", 6: "RH from NABEL", 7: "RH from MeteoSwiss"},
        source_flag="FLAG_VPD_T1_47_1_SOURCE",
        source_legend=PROBE_SOURCE_LEGEND, source_short=PROBE_SOURCE_SHORT,
        extremes=dict(high="driest", low="dampest"),
        notes=[
            "VPD inherits the January 2016 sensor change of both its inputs. It is computed from "
            "the homogenised air temperature, so that part is corrected, but relative humidity has "
            "no homogenised column and enters uncorrected. The step VPD is left with is about 17 % "
            "of its mean, and there is no single column that removes it.",
        ],
    ),

    "PREC": dict(
        title="Precipitation",
        units="mm",
        file="08_METEO_PREC_GAPFILLED_2004-2025.parquet",
        value="PREC_TOT_T1_47_1_HOMOGENIZED",
        uncorrected="PREC_TOT_T1_47_1",
        correction_note=(
            "The gauge was read by two acquisition systems either side of 2018, and the earlier one "
            "catches about 0.79 of what the reference does. The homogenised column rescales that "
            "earlier era onto the later one; the source flag names which chain produced each "
            "record, and the 71-day transition in 2018 has its own code rather than being assigned "
            "to one side."),
        first_year=2005, last_year=2025,
        limits=(0.0, 60.0),
        about=(
            "Precipitation at 47 m as 30-minute totals, homogenised across the 2018 acquisition "
            "change. This variable sums rather than averages: a yearly figure on this page is an "
            "annual total, and a record with no measurement contributes nothing to it rather than "
            "being treated as zero."),
        fill_flag="FLAG_PREC_TOT_T1_47_1_ISFILLED",
        fill_legend={0: "measured at the tower",
                     1: "filled from MeteoSwiss OED, scaled by the monthly factor",
                     2: "still missing, no sub-daily reference exists"},
        fill_short={1: "from OED", 2: "still missing"},
        source_flag="FLAG_PREC_TOT_T1_47_1_SOURCE",
        source_legend={0: "not measured at the tower",
                       1: "EMPA acquisition, to 28 May 2018 \u2014 catches ~0.79\u00d7",
                       2: "transition, acquisition unresolved (2018)",
                       3: "ETH logger, Aug\u2013Dec 2018",
                       4: "ETH logger, 2019 \u2013 1 Jan 2020 (MeteoScreeningTool)",
                       5: "ETH logger, 2020\u20132025 (diive)"},
        source_short={0: "not measured", 1: "EMPA", 2: "transition", 3: "ETH 2018",
                      4: "ETH 2019", 5: "ETH 2020+"},
        agg="sum",
        daily_stats=("sum",),
        ribbon=dict(band=None, line="sum", line_label="daily total"),
        index_groups=[
            dict(title="Wet-day counts", ramp="cold",
                 sub="Days reaching 1 {units} and 10 {units} of total precipitation.",
                 items=[dict(key="wet", label="wet days (\u2265 1 {units})", stat="sum",
                             op="ge", value=1.0),
                        dict(key="heavy", label="heavy days (\u2265 10 {units})", stat="sum",
                             op="ge", value=10.0)]),
        ],
        # Most half-hours and many whole days record no rain at all, so neither low end is a
        # statistic - it is a tie across twenty years broken by whichever record came first.
        extremes=dict(high="wettest", low="driest", low_halfhour=False, low_day=False),
    ),
}

# The five soil-moisture depths share one file and one shape, so their entries are generated rather
# than written out five times. Only 0.5 m has a single sensor era and therefore no homogenised
# column - a duplicate column there would invite someone to difference it, get zero and conclude the
# record is homogeneous.
SWC_SOURCE_LEGEND = {
    0: "no measurement (gap, or before this depth's record begins)",
    1: "EC-20 / M5 profile, MeteoScreeningTool screening (from 2004)",
    2: "TEROS 12 FF1 profile, installed 19 Mar 2020, diive screening",
    3: "TEROS 12 replacement probe, 40 cm downslope (0.3 m only, from 2025)",
}
SWC_SOURCE_SHORT = {0: "no measurement", 1: "EC-20", 2: "TEROS 12", 3: "TEROS replacement"}

for _depth in ("0.05", "0.1", "0.2", "0.3", "0.5"):
    _homogenized = _depth != "0.5"
    VARIABLES[f"SWC_{_depth}"] = dict(
        title=f"Soil water content at {_depth} m",
        units="%",
        file="09_METEO_SWC_FF1_2004-2025.parquet",
        value=f"SWC_FF1_{_depth}_1_HOMOGENIZED" if _homogenized else f"SWC_FF1_{_depth}_1",
        uncorrected=f"SWC_FF1_{_depth}_1" if _homogenized else None,
        correction_note=(
            "The record spans two sensor generations with no overlap between them, so the step at "
            "the changeover cannot be calibrated away against a common period. The homogenised "
            "column rescales the earlier generation on climatology, and the source flag names the "
            "sensor set behind every record - a depth is only interpretable next to the depths "
            "above and below it." if _homogenized else None),
        first_year=2005, last_year=2025,
        limits=(0.0, 70.0),
        about=(
            f"Volumetric soil water content at {_depth} m in the forest-floor profile, exported "
            "with its gaps. "
            + ("The record spans two sensor generations and is exported both as measured and "
               "rescaled onto one level; this page shows the rescaled column."
               if _homogenized
               else "This depth has a single sensor era, so it deliberately carries no homogenised "
                    "second column.")),
        source_flag=f"FLAG_SWC_FF1_{_depth}_1_SOURCE",
        source_legend=SWC_SOURCE_LEGEND, source_short=SWC_SOURCE_SHORT,
        extremes=dict(high="wettest", low="driest"),
    )


# ----------------------------------------------------------------------------------------------
# Small helpers
# ----------------------------------------------------------------------------------------------

def r(value, digits=2):
    """Round for JSON, mapping every flavour of missing onto `null`.

    Rounding here rather than in the browser is what keeps the embedded payload small: the daily
    series alone runs to several thousand records and full float repr triples its size.
    """
    if value is None:
        return None
    if isinstance(value, (np.floating, np.integer)):
        value = value.item()
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    if pd.isna(value):
        return None
    return round(float(value), digits)


def rlist(series, digits=2):
    """A pandas series as a rounded plain list."""
    return [r(v, digits) for v in series.to_numpy()]


def per_year(s, how="mean"):
    """Aggregate `s` to one value per year, indexed by the year number instead of by a timestamp."""
    out = s.resample("YE").agg(how)
    out.index = out.index.year
    out.index.name = "YEAR"
    return out


def trend(yearly):
    """Theil-Sen slope per decade of a yearly series, with its 95 % interval and Kendall's tau.

    Theil-Sen rather than least squares because a single extreme year does not move it, and
    Kendall's tau because it tests a monotonic trend without assuming normal residuals. Years
    without a value are dropped rather than interpolated.
    """
    yearly = yearly.dropna()
    years = yearly.index.to_numpy(dtype=float)
    values = yearly.to_numpy(dtype=float)
    slope, intercept, low, high = theilslopes(values, years, alpha=0.95)
    tau, pvalue = kendalltau(years, values)
    return dict(slope=slope * 10, low=low * 10, high=high * 10, tau=tau, pvalue=pvalue,
                fit=pd.Series(intercept + slope * years, index=yearly.index))


def window(tsmid):
    """The averaging window of a 30MIN record stored on TIMESTAMP_MIDDLE, as text."""
    start = tsmid - pd.Timedelta("15min")
    end = tsmid + pd.Timedelta("15min")
    return f"{start:%d %b %Y}, {start:%H:%M}\u2013{end:%H:%M}"


def longest_spell(mask):
    """Length in days and start date of the longest run of True in a daily boolean series."""
    mask = mask.fillna(False)
    blocks = mask.ne(mask.shift()).cumsum()
    runs = mask[mask].groupby(blocks[mask]).size()
    if runs.empty:
        return 0, pd.NaT
    return int(runs.max()), mask.index[blocks == runs.idxmax()][0]


def growing_season(daily_mean, base, span=6):
    """Start, end and length of the growing season of one year.

    Definition used here: the season starts on the first day of the first `span` consecutive days
    with a daily mean above `base`, and ends on the first day of the first such span below `base`
    after 1 July. Several conventions are in use, so the numbers only mean something together with
    this definition.
    """
    above = daily_mean > base
    runs = above.rolling(span).sum()
    starts = runs[runs == span]
    if starts.empty:
        return None
    start = starts.index[0] - pd.Timedelta(days=span - 1)
    second_half = (~above).loc[f"{daily_mean.index[0].year}-07-01":]
    runs_below = second_half.rolling(span).sum()
    ends = runs_below[runs_below == span]
    end = ends.index[0] - pd.Timedelta(days=span - 1) if not ends.empty else daily_mean.index[-1]
    return dict(start=start, end=end, length=(end - start).days)


def is_night(index):
    """Boolean mask marking records with the sun below the horizon.

    Potential radiation depends on nothing but the clock and the location, so this split introduces
    no further measurement. diive's own `potrad` is used when it is importable, so the split matches
    `10_METEO/30_PRODUCTS`; the fallback is the standard NOAA solar-position formula, which agrees
    with it to well under a half-hour and only decides which side of the horizon a record sits on.
    """
    try:
        import diive as dv
        pot = dv.variables.potrad(timestamp_index=index, lat=SITE_LAT, lon=SITE_LON,
                                  utc_offset=TIMEZONE_OFFSET_TO_UTC_HOURS)
        return pd.Series(np.asarray(pot) <= 0, index=index)
    except Exception:
        doy = index.dayofyear.to_numpy(dtype=float)
        hour = index.hour.to_numpy(dtype=float) + index.minute.to_numpy(dtype=float) / 60
        gamma = 2 * np.pi / 365 * (doy - 1 + (hour - 12) / 24)
        eqtime = 229.18 * (0.000075 + 0.001868 * np.cos(gamma) - 0.032077 * np.sin(gamma)
                           - 0.014615 * np.cos(2 * gamma) - 0.040849 * np.sin(2 * gamma))
        decl = (0.006918 - 0.399912 * np.cos(gamma) + 0.070257 * np.sin(gamma)
                - 0.006758 * np.cos(2 * gamma) + 0.000907 * np.sin(2 * gamma)
                - 0.002697 * np.cos(3 * gamma) + 0.00148 * np.sin(3 * gamma))
        offset = eqtime + 4 * SITE_LON - 60 * TIMEZONE_OFFSET_TO_UTC_HOURS
        tst = hour * 60 + offset
        hourangle = np.radians(tst / 4 - 180)
        lat = np.radians(SITE_LAT)
        cosz = np.sin(lat) * np.sin(decl) + np.cos(lat) * np.cos(decl) * np.cos(hourangle)
        return pd.Series(cosz <= 0, index=index)


class Variable:
    """A registry entry with its defaults filled in, so the rest of the file can read plain fields."""

    def __init__(self, key, cfg):
        self.key = key
        self.title = cfg["title"]
        self.units = cfg["units"]
        self.path = PRODUCTS / cfg["file"]
        self.value = cfg["value"]
        self.uncorrected = cfg.get("uncorrected")
        self.correction_checks = cfg.get("correction_checks")
        self.correction_note = cfg.get("correction_note")
        self.first_year = cfg["first_year"]
        self.last_year = cfg["last_year"]
        self.limits = cfg["limits"]
        self.about = cfg["about"]
        self.notes = cfg.get("notes", [])

        self.fill_flag = cfg.get("fill_flag")
        self.fill_legend = cfg.get("fill_legend", {})
        self.fill_short = cfg.get("fill_short", {})
        self.measured_code = cfg.get("measured_code", 0)
        self.source_flag = cfg.get("source_flag")
        self.source_legend = cfg.get("source_legend", {})
        self.source_short = cfg.get("source_short", {})

        self.agg = cfg.get("agg", "mean")
        self.daily_stats = tuple(cfg.get("daily_stats", ("min", "mean", "max")))
        self.ribbon = cfg.get("ribbon", dict(band=("min", "max"),
                                             band_label="daily minimum to maximum", line="mean"))
        self.index_groups = cfg.get("index_groups", [])
        self.growing_season = cfg.get("growing_season")
        self.reference = cfg.get("reference")
        self.reference_note = cfg.get("reference_note")
        # A variable whose scale has a hard floor has no informative low extreme: the dimmest
        # half-hour of a radiation record is any night, and the driest is any dry minute of twenty
        # years. Those ends are switched off rather than shown as a tie broken by whichever record
        # happened to come first.
        self.extremes = dict(high="highest", low="lowest", low_halfhour=True, low_day=True)
        self.extremes.update(cfg.get("extremes", {}))

        # `agg` is the statistic a year or a month is summarised by; `daily_agg` the one a day is.
        self.daily_agg = "sum" if self.agg == "sum" else "mean"
        for needed in (self.daily_agg, "min", "max"):
            if needed not in self.daily_stats:
                self.daily_stats = self.daily_stats + (needed,)

        # A threshold-day group is drawn with an ordinal ramp of one hue, and the ramps hold two
        # (cold) and three (warm) validated steps. Past that there is no further step to give an
        # index, and generating one would put two indistinguishable hues on the same axis - so the
        # registry is held to the ramp rather than the page quietly cycling.
        ramp_steps = dict(cold=2, warm=3)
        for group in self.index_groups:
            limit = ramp_steps[group["ramp"]]
            assert len(group["items"]) <= limit, (
                f"{key}: index group {group['title']!r} has {len(group['items'])} indices but the "
                f"{group['ramp']} ramp has {limit} steps - split the group or add a ramp")
        for item in (i for g in self.index_groups for i in g["items"]):
            assert item["stat"] in self.daily_stats, (
                f"{key}: index {item['key']!r} needs the daily {item['stat']}, which is not in "
                f"daily_stats {self.daily_stats}")

    def fmt(self, text):
        """Registry text carries `{units}` so a threshold never states the wrong one."""
        return None if text is None else text.format(units=self.units)


# ----------------------------------------------------------------------------------------------
# Load and check
# ----------------------------------------------------------------------------------------------

def load_product(v):
    """Read the product, cut it to whole years and check it is what everything else assumes.

    The checks are the ones the overview notebooks run, for the same reason: a silent violation here
    would be reported as a result. Two of them are deliberately conditional rather than universal -
    a product that is not gap-filled is allowed to carry gaps, and only a product that exports a
    correction has a correction to check.
    """
    if not v.path.exists():
        raise SystemExit(f"Product not found: {v.path}")
    df = pd.read_parquet(v.path)
    df = df[(df.index.year >= v.first_year) & (df.index.year <= v.last_year)].copy()
    if df.empty:
        raise SystemExit(f"{v.key}: no records in {v.first_year}-{v.last_year}")

    expected = pd.date_range(start=df.index[0], end=df.index[-1], freq="30min")
    assert df.index.equals(expected), f"{v.key}: index is not continuous at 30MIN"
    assert not df.index.duplicated().any(), f"{v.key}: duplicate timestamps"
    # Whole years only. A partial first year is excluded by `first_year`, not silently averaged in.
    assert (df.index[0].month, df.index[0].day) == (1, 1), (
        f"{v.key}: the period does not start on 1 January - raise first_year to the first complete "
        f"year (record starts {df.index[0]})")
    assert (df.index[-1].month, df.index[-1].day) == (12, 31), \
        f"{v.key}: the period does not end on 31 December (record ends {df.index[-1]})"

    columns = [c for c in (v.value, v.uncorrected) if c]
    for col in columns:
        assert col in df.columns, f"{v.key}: column {col} not in {v.path.name}"
        present = df[col].dropna()
        assert present.between(*v.limits).all(), (
            f"{v.key}: {col} outside {v.limits}: {present.min()} to {present.max()}")
    for flag, legend in ((v.fill_flag, v.fill_legend), (v.source_flag, v.source_legend)):
        if not flag:
            continue
        assert flag in df.columns, f"{v.key}: flag {flag} not in {v.path.name}"
        unknown = sorted(set(df[flag].dropna().unique()) - set(legend))
        assert not unknown, f"{v.key}: {flag} carries codes the legend does not describe: {unknown}"

    corrections = None
    if v.uncorrected:
        corrections = check_correction(v, df)
    return df, corrections


def check_correction(v, df):
    """Measure what the homogenisation does, and let the registry assert its shape.

    The two columns differ by the correction, so the correction can be read straight back out of the
    file rather than quoted from prose beside it. Where the difference splits at a hardware change,
    the source flag is what splits it; the reference era of a homogenisation is code 0 by convention
    in these products.
    """
    delta = (df[v.value] - df[v.uncorrected]).round(6).dropna()
    assert not delta.empty, f"{v.key}: the two columns never overlap, so the correction is unreadable"

    out = dict(n_changed=int((delta != 0).sum()), n=int(len(delta)),
               dmin=float(delta.min()), dmax=float(delta.max()), dmean=float(delta.mean()),
               distinct=int(delta.nunique()))
    if v.source_flag:
        era = df.loc[delta.index, v.source_flag]
        pre, post = delta[era != 0], delta[era == 0]
        if not pre.empty and not post.empty:
            out.update(offset=float(pre.iloc[0]) if pre.nunique() == 1 else None,
                       pre_mean=float(pre.mean()), post_mean=float(post.mean()),
                       post_min=float(post.min()), post_max=float(post.max()),
                       break_ts=df.index[df[v.source_flag] == 0][0])
            if v.correction_checks:
                v.correction_checks(pre, post, v.units)
    return out


# ----------------------------------------------------------------------------------------------
# Payload
# ----------------------------------------------------------------------------------------------

def build_payload(v, df, corrections, use_reference=True):
    """Everything the page draws, as one JSON-ready dictionary."""
    series = df[v.value]
    present = series.notna()

    # "Measured" means what the fill flag says where there is one, and simply "not missing" where
    # there is not. Everything downstream reads this mask rather than re-deciding.
    measured = (df[v.fill_flag].eq(v.measured_code) & present) if v.fill_flag else present
    measured_only = series.where(measured)
    not_measured = ~measured

    daily = series.resample("D").agg(list(v.daily_stats))
    daily["filled"] = not_measured.resample("D").mean() * 100
    daily_measured = measured_only.resample("D").agg(["min", "max"])
    day = daily[v.daily_agg]

    # A year or a month is summarised by `agg`; for a summed variable a period with gaps under-
    # reports, which is why the coverage section comes before the statistics on the page.
    ym = per_year(series, v.agg)
    fit = trend(ym)
    anomaly = ym - ym.mean()

    first_recent = ym.index.max() - N_RECENT_YEARS + 1
    assert first_recent > ym.index.min(), f"{v.key}: not enough years before the recent period"
    early = ym.loc[:first_recent - 1].mean()
    recent = ym.loc[first_recent:].mean()

    monthly = series.groupby([series.index.year, series.index.month]).agg(v.agg).unstack()
    monthly = monthly.reindex(columns=range(1, 13))
    monthly_anom = monthly - monthly.mean()
    filled_month = (not_measured.astype(float) * 100).groupby(
        [df.index.year, df.index.month]).mean().unstack().reindex(columns=range(1, 13))

    years = list(ym.index.astype(int))
    ranks = ym.rank(ascending=False).astype("Int64")
    year_min = per_year(measured_only, "min")
    year_max = per_year(measured_only, "max")

    # -- Threshold days, spells, growing season ---------------------------------------------
    indices, index_groups = {}, []
    for group in v.index_groups:
        items = []
        for item in group["items"]:
            stat = daily[item["stat"]]
            hit = stat.lt(item["value"]) if item["op"] == "lt" else stat.ge(item["value"])
            indices[item["key"]] = per_year(hit.astype(float), "sum")
            items.append(dict(key=item["key"], label=v.fmt(item["label"])))
        index_groups.append(dict(title=group["title"], sub=v.fmt(group["sub"]),
                                 ramp=group["ramp"], items=items))

    season_rows = {}
    if v.growing_season is not None:
        for year, daily_mean in day.groupby(daily.index.year):
            season = growing_season(daily_mean.dropna(), base=v.growing_season)
            if season is not None:
                season_rows[year] = dict(start=season["start"].dayofyear,
                                         end=season["end"].dayofyear, length=season["length"],
                                         start_label=f"{season['start']:%d %b}",
                                         end_label=f"{season['end']:%d %b}")
        gdd = per_year((day - v.growing_season).clip(lower=0), "sum")

    # The longest spell of each group's first index, which is the one worth a column beside a count:
    # a year can reach a high count without ever holding the threshold for a week.
    spells = {}
    for group in v.index_groups:
        item = group["items"][0]
        stat = daily[item["stat"]]
        hit = stat.lt(item["value"]) if item["op"] == "lt" else stat.ge(item["value"])
        per = {}
        for year, block in hit.groupby(daily.index.year):
            length, start = longest_spell(block)
            per[year] = dict(length=length, start="-" if pd.isna(start) else f"{start:%d %b}")
        spells[item["key"]] = per

    # -- New records, counted forwards ------------------------------------------------------
    # A record is a record against what came before it, not against the whole dataset. The first
    # year is left out: by construction almost every day of it sets one.
    new_high = daily_measured["max"] > daily_measured["max"].shift().cummax()
    new_low = daily_measured["min"] < daily_measured["min"].shift().cummin()
    records_high = per_year(new_high.astype(float), "sum")
    records_low = per_year(new_low.astype(float), "sum")

    # -- Coverage and provenance ------------------------------------------------------------
    methods = ([v.fill_short.get(c, f"code {c}") for c in sorted(v.fill_legend) if c != v.measured_code]
               if v.fill_flag else ["missing"])
    coverage_values = []
    for y in years:
        sel = df.index.year == y
        if v.fill_flag:
            row = [float((df.loc[sel, v.fill_flag] == c).sum())
                   for c in sorted(v.fill_legend) if c != v.measured_code]
        else:
            row = [float(not_measured[sel].sum())]
        coverage_values.append(row)

    blocks = not_measured.ne(not_measured.shift()).cumsum()[not_measured]
    lengths = not_measured[not_measured].groupby(blocks).size() * 0.5  # 30MIN records -> hours
    block_years = df.index[not_measured].to_series().groupby(blocks.to_numpy()).first().dt.year
    longest_gap = (pd.Series(lengths.to_numpy(), index=block_years.to_numpy())
                   .groupby(level=0).max().reindex(years).fillna(0))
    filled_pct = per_year(not_measured.astype(float), "mean") * 100

    source = None
    if v.source_flag:
        src = pd.crosstab(df.index.year, df[v.source_flag])
        codes = sorted(v.source_legend)
        src_pct = (src.div(src.sum(axis=1), axis=0) * 100).reindex(columns=codes, fill_value=0.0)
        source = dict(years=years,
                      labels=[v.source_short.get(c, f"code {c}") for c in codes],
                      full=[v.source_legend[c] for c in codes],
                      values=[[r(src_pct.loc[y, c], 1) for c in codes] for y in years])

    # For a summed variable most half-hours sit on the floor, so percentiles of the whole series are
    # a column of zeros that says nothing about the year. The distribution worth reporting is the
    # one of the records that are not on the floor - for precipitation, the intensity of the rain
    # when it rains.
    q_source = series[series > 0] if v.agg == "sum" else series
    q_basis = "half-hours above zero" if v.agg == "sum" else "half-hourly values"
    quantiles = q_source.groupby(q_source.index.year).quantile(
        [0.05, 0.25, 0.5, 0.75, 0.95]).unstack().reindex(ym.index)

    yearly = []
    for y in years:
        row = dict(
            year=y, mean=r(ym[y]), anomaly=r(anomaly[y]),
            rank=None if pd.isna(ranks[y]) else int(ranks[y]),
            min=r(year_min.get(y)), max=r(year_max.get(y)),
            filled=r(filled_pct.get(y), 1),
            longest_gap_h=r(longest_gap.get(y), 1),
            records=int((df.index.year == y).sum()),
            rec_high=int(records_high.get(y, 0)), rec_low=int(records_low.get(y, 0)),
            q05=r(quantiles.loc[y, 0.05]), q25=r(quantiles.loc[y, 0.25]),
            q50=r(quantiles.loc[y, 0.50]), q75=r(quantiles.loc[y, 0.75]),
            q95=r(quantiles.loc[y, 0.95]),
            fit=r(fit["fit"].get(y)),
        )
        for key, s in indices.items():
            row[key] = None if pd.isna(s.get(y)) else int(s[y])
        for key, per in spells.items():
            row[key + "_spell"] = per.get(y, {}).get("length")
            row[key + "_spell_start"] = per.get(y, {}).get("start")
        if v.growing_season is not None:
            row.update(gsl=season_rows.get(y, {}).get("length"),
                       gs_start_label=season_rows.get(y, {}).get("start_label"),
                       gs_end_label=season_rows.get(y, {}).get("end_label"),
                       gdd=r(gdd.get(y), 0))
        yearly.append(row)

    # -- Mean annual cycle ------------------------------------------------------------------
    doy = day.groupby(daily.index.dayofyear)
    last_year_daily = day.loc[str(v.last_year)]
    last_by_doy = pd.Series(last_year_daily.to_numpy(), index=last_year_daily.index.dayofyear)
    annual_cycle = dict(
        doy=[int(d) for d in doy.mean().index],
        mean=rlist(doy.mean(), 2), p10=rlist(doy.quantile(0.1), 2), p90=rlist(doy.quantile(0.9), 2),
        min=rlist(doy.min(), 2), max=rlist(doy.max(), 2),
        last=[r(last_by_doy.get(int(d)), 2) for d in doy.mean().index],
    )

    # -- Month by hour ----------------------------------------------------------------------
    by_mh = series.groupby([series.index.month, series.index.hour]).mean().unstack()
    last = series.loc[str(v.last_year)]
    by_mh_last = last.groupby([last.index.month, last.index.hour]).mean().unstack()
    month_hour = [[r(by_mh.loc[m, h]) for h in range(24)] for m in range(1, 13)]
    month_hour_anom = [[r(by_mh_last.loc[m, h] - by_mh.loc[m, h]) for h in range(24)]
                       for m in range(1, 13)]

    diurnal_x = sorted(set(series.index.hour + series.index.minute / 60))
    # Months become the columns, so the curve of one month is a column and the x axis is the index.
    diurnal = series.groupby([series.index.month,
                              series.index.hour + series.index.minute / 60]).mean().unstack(0)

    # -- Climatology per calendar month ------------------------------------------------------
    rec_low = measured_only.groupby(measured_only.index.month).min()
    rec_high = measured_only.groupby(measured_only.index.month).max()
    climatology = []
    for m in range(1, 13):
        col = monthly[m]
        climatology.append(dict(
            month=m, label=calendar.month_abbr[m], mean=r(col.mean()), sd=r(col.std()),
            min=r(col.min()), min_year=None if col.isna().all() else int(col.idxmin()),
            max=r(col.max()), max_year=None if col.isna().all() else int(col.idxmax()),
            rec_low=r(rec_low.get(m)), rec_high=r(rec_high.get(m)),
        ))

    monthly_trend = []
    for m in range(1, 13):
        f = trend(monthly[m])
        monthly_trend.append(dict(month=m, label=calendar.month_abbr[m], slope=r(f["slope"]),
                                  low=r(f["low"]), high=r(f["high"]), p=r(f["pvalue"], 4),
                                  significant=bool(f["pvalue"] < 0.05)))

    # -- Extremes ----------------------------------------------------------------------------
    # From the measured records only: a filled or reconstructed value is a model result and cannot
    # set a record.
    hh_high = measured_only.nlargest(N_EXTREMES)
    hh_low = measured_only.nsmallest(N_EXTREMES)
    day_high = day.nlargest(N_EXTREMES)
    day_low = day.nsmallest(N_EXTREMES)
    extremes = dict(
        high_label=v.extremes["high"], low_label=v.extremes["low"],
        show_low_halfhour=bool(v.extremes["low_halfhour"]),
        show_low_day=bool(v.extremes["low_day"]),
        high_halfhours=[dict(window=window(ts), value=r(x)) for ts, x in hh_high.items()],
        low_halfhours=[dict(window=window(ts), value=r(x)) for ts, x in hh_low.items()]
        if v.extremes["low_halfhour"] else None,
        high_days=[dict(date=f"{d:%d %b %Y}", value=r(x), filled=r(daily.loc[d, "filled"], 1))
                   for d, x in day_high.items()],
        low_days=[dict(date=f"{d:%d %b %Y}", value=r(x), filled=r(daily.loc[d, "filled"], 1))
                  for d, x in day_low.items()] if v.extremes["low_day"] else None,
        inside_measured=bool((series.max() <= measured_only.max())
                             and (series.min() >= measured_only.min())),
    )

    # -- The whole record, day by day ---------------------------------------------------------
    band = v.ribbon.get("band")
    line_stat = v.ribbon.get("line")
    ribbon = dict(
        dates=[f"{d:%Y-%m-%d}" for d in daily.index],
        band_label=v.ribbon.get("band_label"),
        line_label=v.ribbon.get("line_label", "daily " + str(line_stat)),
        lo=rlist(daily[band[0]], 1) if band else None,
        hi=rlist(daily[band[1]], 1) if band else None,
        line=rlist(daily[line_stat], 1) if line_stat else None,
        smooth=rlist(day.rolling(31, center=True, min_periods=10).mean(), 2),
    )

    payload = dict(
        meta=dict(
            site=SITE, site_long=SITE_LONG,
            key=v.key, title=v.title, units=v.units, varname=v.value,
            first_year=int(v.first_year), last_year=int(v.last_year),
            n_records=int(len(df)), n_measured=int(measured.sum()),
            resolution="30 min, TIMESTAMP_MIDDLE",
            product=v.path.name,
            generated=datetime.now().strftime("%Y-%m-%d %H:%M"),
            agg=v.agg,
            agg_label="total" if v.agg == "sum" else "mean",
            about=v.about, notes=[v.fmt(n) for n in v.notes],
            quantile_basis=q_basis,
            correction=correction_meta(v, corrections),
            has_fill_flag=bool(v.fill_flag),
            fill_legend={str(k): x for k, x in v.fill_legend.items()},
            growing_season_base=v.growing_season,
        ),
        hero=dict(
            mean=r(ym.mean()), sd=r(ym.std()),
            slope=r(fit["slope"]), slope_low=r(fit["low"]), slope_high=r(fit["high"]),
            tau=r(fit["tau"]), p=r(fit["pvalue"], 4),
            high_year=None if ym.isna().all() else int(ym.idxmax()), high_value=r(ym.max()),
            low_year=None if ym.isna().all() else int(ym.idxmin()), low_value=r(ym.min()),
            record_high=r(measured_only.max(), 1),
            record_high_when=window(measured_only.idxmax()),
            record_low=r(measured_only.min(), 1),
            record_low_when=window(measured_only.idxmin()),
            measured_pct=r(measured.mean() * 100, 1),
            early_period=[int(ym.index.min()), int(first_recent - 1)],
            recent_period=[int(first_recent), int(ym.index.max())],
            early_mean=r(early), recent_mean=r(recent), period_delta=r(recent - early),
            period_delta_pct=r(100 * (recent - early) / early, 1) if early else None,
            growing_season=r(pd.Series({y: s["length"] for y, s in season_rows.items()}).mean(), 0)
            if season_rows else None,
        ),
        years=years,
        yearly=yearly,
        index_groups=index_groups,
        monthly=dict(years=years, months=[calendar.month_abbr[m] for m in range(1, 13)],
                     values=[[r(monthly.loc[y, m]) for m in range(1, 13)] for y in years],
                     anomaly=[[r(monthly_anom.loc[y, m]) for m in range(1, 13)] for y in years],
                     filled=[[r(filled_month.loc[y, m], 1) for m in range(1, 13)] for y in years]),
        annual_cycle=annual_cycle,
        month_hour=dict(months=[calendar.month_abbr[m] for m in range(1, 13)],
                        hours=list(range(24)), values=month_hour, anomaly=month_hour_anom),
        diurnal=dict(x=[r(x, 2) for x in diurnal_x],
                     months=[calendar.month_abbr[m] for m in range(1, 13)],
                     values=[[r(diurnal.loc[t, m]) for t in diurnal_x] for m in range(1, 13)]),
        climatology=climatology,
        monthly_trend=monthly_trend,
        coverage=dict(years=years, methods=methods, values=coverage_values),
        source=source,
        extremes=extremes,
        ribbon=ribbon,
        reference=build_reference(v, df, measured, use_reference),
    )
    return payload


def correction_meta(v, corrections):
    """What the page says about the homogenisation, with its constants measured on this build."""
    if not v.uncorrected or corrections is None:
        return None
    offset = corrections.get("offset")
    note = v.correction_note or ""
    note = note.format(
        units=v.units,
        break_ts=f"{corrections['break_ts']:%d %b %Y}" if corrections.get("break_ts") else "",
        offset=f"{offset:+.4f} {v.units}" if offset is not None else "an era-wide offset",
        shield_max=f"{-corrections['post_min']:.3f} {v.units}"
        if corrections.get("post_min") is not None else "",
    )
    return dict(note=note,
                changed=corrections["n_changed"], n=corrections["n"],
                dmin=r(corrections["dmin"], 4), dmax=r(corrections["dmax"], 4),
                dmean=r(corrections["dmean"], 4), distinct=corrections["distinct"],
                offset=r(offset, 4) if offset is not None else None,
                break_ts=f"{corrections['break_ts']:%d %b %Y}" if corrections.get("break_ts") else None)


def build_reference(v, df, measured, use_reference=True):
    """The comparison against the reference station, or `None` where the variable has none.

    A nearby station operated by a different institution removes the weather and leaves the
    instruments, which is what makes a residual against it a check rather than a restatement. An
    elevation difference means a constant offset is expected; what matters is whether that offset
    stays constant.

    Only additive quantities are compared this way. Radiation is deliberately excluded in the
    registry: a radiation error is multiplicative, so it has to be compared in ratios under controls
    the page does not carry.
    """
    if not use_reference or not v.reference:
        return None
    path = REFERENCES / v.reference["file"]
    if not path.exists():
        print(f"  reference file missing, comparison skipped: {path.name}")
        return None
    ref = pd.read_parquet(path)[v.reference["column"]]
    # The reference products are stored on TIMESTAMP_END, so they are shifted onto the product's
    # TIMESTAMP_MIDDLE before anything is compared.
    ref.index = ref.index - pd.Timedelta("15min")

    both = pd.concat([df.loc[measured, v.value].rename("product"), ref.rename("reference")],
                     axis=1, sort=True).dropna()
    if len(both) < 10_000:
        print(f"  only {len(both):,} overlapping measured half-hours, comparison skipped")
        return None

    residual = both["product"] - both["reference"]
    split = v.reference.get("split") == "nightday"
    night = is_night(both.index) if split else None

    out = dict(
        station=v.reference["station"], distance_km=v.reference["distance_km"],
        elevation_m=v.reference["elevation_m"], note=v.reference_note,
        n=int(len(both)), start=f"{both.index[0]:%Y-%m-%d}", stop=f"{both.index[-1]:%Y-%m-%d}",
        correlation=r(both["product"].corr(both["reference"]), 4),
        residual_mean=r(residual.mean()), residual_sd=r(residual.std()),
        split=bool(split),
    )

    def roll(s):
        return s.rolling(12, center=True, min_periods=6).median()

    if split:
        monthly_night = residual[night.to_numpy()].resample("ME").mean()
        monthly_day = residual[(~night).to_numpy()].resample("ME").mean()
        out.update(dates=[f"{d:%Y-%m}" for d in monthly_night.index],
                   series=[dict(key="night", label="night", values=rlist(monthly_night, 3),
                                smooth=rlist(roll(monthly_night), 3)),
                           dict(key="day", label="day", values=rlist(monthly_day, 3),
                                smooth=rlist(roll(monthly_day), 3))])
    else:
        monthly_all = residual.resample("ME").mean()
        out.update(dates=[f"{d:%Y-%m}" for d in monthly_all.index],
                   series=[dict(key="all", label="all hours", values=rlist(monthly_all, 3),
                                smooth=rlist(roll(monthly_all), 3))])

    # The step across the hardware change, stated rather than left to the eye. Three complete years
    # either side, so an outage at the changeover does not sit inside a compared window. It is the
    # residual the exported product carries - the uncorrected column is not shown.
    if v.source_flag and (df[v.source_flag] == 0).any():
        break_year = int(df.index[df[v.source_flag] == 0][0].year)
        pre = (both.index.year >= break_year - 3) & (both.index.year <= break_year - 1)
        post = (both.index.year >= break_year + 1) & (both.index.year <= break_year + 3)
        rows = []
        windows = [("all hours", np.ones(len(both), bool))]
        if split:
            windows += [("night", night.to_numpy()), ("day", (~night).to_numpy())]
        for wname, wmask in windows:
            before, after = residual[pre & wmask].mean(), residual[post & wmask].mean()
            rows.append(dict(window=wname, before=r(before), after=r(after), step=r(after - before)))
        out.update(break_year=break_year, steps=rows)

    yearly = []
    for y in sorted(set(both.index.year)):
        sel = residual.index.year == y
        row = dict(year=int(y), mean=r(residual[sel].mean()), sd=r(residual[sel].std()),
                   n=int(sel.sum()))
        if split:
            row.update(night=r(residual[sel & night.to_numpy()].mean()),
                       day=r(residual[sel & (~night).to_numpy()].mean()))
        yearly.append(row)
    out["yearly"] = yearly
    return out


# ----------------------------------------------------------------------------------------------
# Render
# ----------------------------------------------------------------------------------------------

def render(payload, out_path):
    """Inline the assets and the payload into one self-contained HTML file."""
    template = (ASSETS / "template.html").read_text(encoding="utf-8")
    css = (ASSETS / "dashboard.css").read_text(encoding="utf-8")
    js = (ASSETS / "dashboard.js").read_text(encoding="utf-8")

    # `</script>` inside the JSON would end the tag early, and `<!--` would open a comment.
    data = (json.dumps(payload, allow_nan=False, separators=(",", ":"))
            .replace("</", "<\\/").replace("<!--", "<\\!--"))
    m = payload["meta"]

    html = (template
            .replace("/*__CSS__*/", css)
            .replace("/*__DATA__*/", data)
            .replace("/*__JS__*/", js)
            .replace("__TITLE__", f"{m['site']} \u2014 {m['title'].lower()} "
                                  f"{m['first_year']}\u2013{m['last_year']}"))

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    return out_path


def build(key, out=None, outdir=None, use_reference=True, quiet=False):
    """Build one variable's dashboard and return the path it was written to."""
    v = Variable(key, VARIABLES[key])
    say = (lambda *a: None) if quiet else print

    say(f"[{key}] reading {v.path.name} ...")
    df, corrections = load_product(v)
    say(f"  {len(df):,} records, {v.first_year}\u2013{v.last_year}, integrity checks passed")
    if corrections:
        say(f"  correction: {corrections['n_changed']:,} of {corrections['n']:,} records changed, "
            f"{corrections['dmin']:+.4f} to {corrections['dmax']:+.4f} {v.units}, "
            f"{corrections['distinct']:,} distinct values")

    payload = build_payload(v, df, corrections, use_reference=use_reference)
    if payload["reference"]:
        say(f"  reference {payload['reference']['station']}: "
            f"{payload['reference']['n']:,} overlapping measured half-hours")

    path = render(payload, out or Path(outdir or OUTDIR) / f"METEO_{key}_dashboard.html")
    say(f"  written: {path}  ({path.stat().st_size / 1024:.0f} kB)")
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--var", help="variable key, see --list")
    parser.add_argument("--all", action="store_true", help="build every registered variable")
    parser.add_argument("--list", action="store_true", help="list the registered variables")
    parser.add_argument("--out", help="output HTML file (single variable only)")
    parser.add_argument("--outdir", help="output directory; the default is the external data "
                                         "folder. Use it with --all to build a whole set into "
                                         "the site output tree")
    parser.add_argument("--no-reference", action="store_true",
                        help="skip the reference-station comparison")
    parser.add_argument("--open", dest="open_browser", action="store_true",
                        help="open the finished dashboard in the default browser")
    args = parser.parse_args(argv)

    if args.list or not (args.var or args.all):
        print(f"{'key':<12} {'units':<14} {'product':<44} available")
        for key, cfg in VARIABLES.items():
            path = PRODUCTS / cfg["file"]
            print(f"{key:<12} {cfg['units']:<14} {cfg['file']:<44} "
                  f"{'yes' if path.exists() else 'MISSING'}")
        return 0

    if args.all:
        if args.out:
            parser.error("--out names one file; use --outdir with --all")
        failed = []
        for key in VARIABLES:
            try:
                build(key, outdir=args.outdir, use_reference=not args.no_reference)
            except (AssertionError, SystemExit, KeyError, ValueError) as exc:
                # One variable's product being absent or malformed must not stop the rest, but it
                # has to be reported rather than swallowed.
                print(f"[{key}] FAILED: {exc}")
                failed.append(key)
        if failed:
            print(f"\n{len(failed)} of {len(VARIABLES)} failed: {', '.join(failed)}")
            return 1
        return 0

    if args.var not in VARIABLES:
        parser.error(f"unknown variable {args.var!r}; known keys: {', '.join(VARIABLES)}")
    path = build(args.var, out=args.out, outdir=args.outdir,
                 use_reference=not args.no_reference)
    if args.open_browser:
        webbrowser.open(path.resolve().as_uri())
    return 0


if __name__ == "__main__":
    sys.exit(main())
