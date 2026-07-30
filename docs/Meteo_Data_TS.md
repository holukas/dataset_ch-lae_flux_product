# Soil temperature at the forest floor

Half-hourly soil temperature at seven depths of the `FF1` profile at CH-LAE, 2004-2025.
The file is `10_METEO_TS_FF1_2004-2025` (parquet and CSV): **373,728 records** on a
continuous 30-minute middle-timestamp index (named `TIMESTAMP_MIDDLE` in the file) in local
time (UTC+1, no daylight saving), from 2004-09-07 00:15 to 2025-12-31 23:45. Values are in
**°C**. The index begins with the soil record rather than on 1 January, because there is no
soil temperature at this plot before September 2004.

The **interactive dashboards** summarise one depth each on a single page — coverage and
provenance, seasonality, distributions, extremes and trends, with a table view behind every
chart. They are standalone and work offline:
[0.05](dashboards/METEO_TS_0.05_dashboard.html) /
[0.1](dashboards/METEO_TS_0.1_dashboard.html) /
[0.15](dashboards/METEO_TS_0.15_dashboard.html) /
[0.2](dashboards/METEO_TS_0.2_dashboard.html) /
[0.3](dashboards/METEO_TS_0.3_dashboard.html) /
[0.5](dashboards/METEO_TS_0.5_dashboard.html) /
[0.6](dashboards/METEO_TS_0.6_dashboard.html) m. Each covers only the whole years its own
depth measured, so 0.15 m ends in 2020 and 0.2 m and 0.6 m begin in 2021.

Method, evidence and checks:

- [`10_METEO_TS_FF1`](notebooks/10_METEO/30_PRODUCTS/10_METEO_TS_FF1_2004-2025.html) —
  builds the product: reconciles the channels, splices the sensor generations, fills the gaps
  and tests the record for breaks.
- [`TS_FF1_SCREENED_30MIN`](notebooks/10_METEO/30_PRODUCTS/TS_FF1_SCREENED_30MIN_2004-2025.html)
  — downloads the screened channels the product is built from.
- [`TS_FF1_GAPFILL_ML_COMPARISON`](notebooks/10_METEO/30_PRODUCTS/TS_FF1_GAPFILL_ML_COMPARISON.html)
  — the experiment that chose the gap-filling method and rejected the alternatives.
- The thirteen screening notebooks of the current profile, under
  [`20_SCREENING/TS/`](notebooks/index.html), one per channel.
- [`Meteo_Data_SWC`](Meteo_Data_SWC.html) — the soil water content of the same profile, whose
  June 2015 break is settled using this variable.
- [`Meteo_Product_Chain`](Meteo_Product_Chain.html) — where this product sits in the chain.

::: {.callout-important title="Which column to use"}

The file holds two kinds of column per depth.

- **`TS_FF1_<d>_HOMOGENIZED_GAPFILLED`** is the one to analyse: one reconciled, gap-filled
  series per depth, with the sensor-generation step removed where it could be measured.
- **The eighteen individual channels** (`TS_FF1_0.05_2`, `TS_PRF_FF1_0.05_1`, …) are the raw
  screened measurements, one sensor each, with gaps where that sensor was down. Use these
  when you need the truth of one instrument.

**Filter on `FLAG_…_METHOD` before analysis.** At 0.3 m and 0.5 m about **47 % of the overall
column is modelled**, not measured, because those depths had no sensor between March 2010 and
April 2020.

**Do not compute a diurnal or seasonal amplitude across April 2020.** The levels are
reconciled; the amplitudes are not, and they differ by a factor of three at 0.05 m.

:::

## Columns

Thirty-five columns: eighteen individual channels, seven overall columns, seven `METHOD`
flags and three `SUSPECT` flags. `<d>` is one of `0.05`, `0.1`, `0.15`, `0.2`, `0.3`, `0.5`,
`0.6`.

: Columns of `10_METEO_TS_FF1_2004-2025`. {#tbl-ts-cols}

| column | unit | description |
|---|---|---|
| `TS_FF1_<d>_HOMOGENIZED_GAPFILLED` | °C | One series per depth: the depth's sensors reconciled into one record, the generation step removed where measurable, gaps filled from the other depths. |
| `FLAG_…_METHOD` | - | Whether each value was measured and by which generation, or modelled. |
| `FLAG_…_SUSPECT` | - | `1` where the early profile disagreed with itself. Only at 0.05, 0.1 and 0.15 m. |
| eighteen `TS_FF1_*` / `TS_PRF_FF1_*` | °C | The individual screened channels, one sensor each. Never gap-filled. |

### `FLAG_TS_FF1_<d>_HOMOGENIZED_GAPFILLED_METHOD`

Keep `METHOD ∈ {1, 2}` for measured values only.

: Method codes and their record counts per depth. {#tbl-ts-method}

| code | meaning | 0.05 m | 0.1 m | 0.15 m | 0.2 m | 0.3 m | 0.5 m | 0.6 m |
|---|---|---|---|---|---|---|---|---|
| 0 | no value | 21,398 | 21,398 | 104,050 | 274,381 | 21,398 | 21,398 | 274,381 |
| 1 | measured, current profile | 99,347 | 98,611 | 0 | 98,571 | 98,692 | 98,590 | 98,617 |
| 2 | measured, early profile | 252,848 | 252,880 | 269,389 | 0 | 88,151 | 88,188 | 0 |
| 3 | modelled, nearest contributing depth ≤ 0.15 m away | 98 | 802 | 252 | 0 | 164,795 | 0 | 0 |
| 4 | modelled, nearest contributing depth further off | 37 | 37 | 37 | 776 | 692 | 165,552 | 730 |

Codes `3` and `4` are provenance, not a quality ranking: they record how far the nearest
contributing depth was, and since the fill uses every available depth at once a `4` is not
necessarily worse than a `3`.

### `FLAG_TS_FF1_<d>_HOMOGENIZED_GAPFILLED_SUSPECT`

`1` marks the period where the early profile's three channels disagreed with each other
beyond their own seasonal norm. It exists at three depths only, and covers 8,121 to 20,297
records between January 2009 and May 2012. **Filter on it before using the early era
quantitatively.**

## Coverage

: Coverage per depth, over the full file and within each depth's own measured span. {#tbl-ts-cov}

| depth | span | coverage of the file | coverage within its span | measured | modelled | range |
|---|---|---|---|---|---|---|
| 0.05 m | 2004-09-07 to 2025-12-31 | 94.3 % | 94.3 % | 99.96 % | 0.04 % | −3.6 to 28.8 |
| 0.1 m | 2004-09-07 to 2025-12-31 | 94.3 % | 94.3 % | 99.8 % | 0.2 % | −0.7 to 22.8 |
| 0.15 m | 2004-09-07 to 2021-03-24 | 72.2 % | 93.0 % | 99.9 % | 0.1 % | 0.1 to 19.9 |
| 0.2 m | 2020-04-10 to 2025-12-31 | 26.6 % | 99.0 % | 99.2 % | 0.8 % | 1.8 to 19.2 |
| 0.3 m | 2004-09-07 to 2025-12-31 | 94.3 % | 94.3 % | 53.0 % | 47.0 % | 1.2 to 18.9 |
| 0.5 m | 2004-09-07 to 2025-12-31 | 94.3 % | 94.3 % | 53.0 % | 47.0 % | 1.7 to 17.2 |
| 0.6 m | 2020-04-10 to 2025-12-31 | 26.6 % | 99.0 % | 99.3 % | 0.7 % | 3.6 to 16.9 |

The spans differ because the holes in the ground do: **0.15 m is early-only**, **0.2 m and
0.6 m exist only from 2020**, and the rest span the whole record. These are facts about which
sensors existed when, not gaps.

Where a depth has no value at all, no depth does: **5.7 % of records are missing at every
depth at once**, whole-station outages of the early era. The four longest are 124 days from
February 2011, 93 days from March 2009, 83 days from March 2010 and 63 days from May 2007.
Two of them are named in the site record as a dead logger and a fuse that slipped out of the
battery-powered forest-floor station.

***

## The 2020 profile replacement

The early profile was a five-sensor Campbell 107 probe stick, identified from the
forest-floor logger programs, which name its sensors at 5, 10, 15, 30 and 50 cm — exactly the
five depths that carry an early record. It was replaced in March 2020 by the current
instruments, which began reporting on 10 April.

Unlike soil water content, the two generations here **do overlap**, for 347 days until the old
stick stopped at the March 2021 logger rebuild. That overlap is what makes the level
difference a measurement rather than an assumption: about 0.6 K at 0.05 m and 0.4 K at 0.1 m.
The `HOMOGENIZED` part of the column name refers to removing it.

::: {.callout-warning title="Levels are reconciled; amplitudes are not"}
The early sensors were far better coupled to the surface than today's at the same nominal
depth. At 0.05 m the median summer daily amplitude is **3.13 K in the early era against
0.90 K in the current one**, and the median annual range 25.4 K against 18.0 K. At 0.1 m it is
1.27 K against 0.59 K.

A daily or seasonal amplitude computed across April 2020 is therefore dominated by the sensor
change, not by climate. Annual and daily *means* are comparable; amplitudes are not.
:::

**At 0.3 m and 0.5 m there is no homogenisation at all**, because the generations do not
overlap there — the early sensors at those depths stopped on 2010-03-06, ten years before the
new ones went in. The early era at those depths therefore sits at its own level, and a trend
across April 2020 still carries the sensor change. The climatological route used for soil
water content is deliberately refused here: mixing measured and climatological offsets in one
product would make them indistinguishable.

## The early profile disagrees with itself, 2009-2012

Between January 2009 and May 2012 the three early channels depart from their own seasonal
norm by 1.5 to 3.5 K, for months at a time and in mirror-image pairs — one running warm while
another runs cold. Across the other thirteen years they agree to a few tenths of a kelvin.

The period brackets the years when the forest-floor logger was repeatedly losing power, and
ends around a logger program of April 2012 described as having *"corrected multipliers and
offset"*. Which of the three channels is wrong is **not determined**: with only three sensors,
one moving shifts the comparison for all three, and there is no fourth soil sensor and no
external reference to break the tie. The affected records are kept, flagged `SUSPECT`, and not
corrected.

## The gap-fill

Gaps in the overall columns are filled from the **other depths of the same profile**, by a
least-squares fit made separately for each sensor generation — so a fill never introduces a
sensor step — using every available depth plus its thermal memory and a day-of-year term. It
was validated by holding out whole years and by predicting the deep depths from the shallow
ones alone.

It **interpolates and does not extrapolate**: each depth is filled only within its own
measured span, which is why 0.2 m and 0.6 m have no values before 2020 and 0.15 m none after
March 2021. Inside a span the only gaps left are the whole-station outages. The individual
channels are never filled.

## Known limitations

- **Amplitudes are not comparable across April 2020.** The earlier sensors were more
  closely coupled to the surface than the present ones at the same nominal depth, so the
  diurnal and seasonal amplitude changes with the hardware, by a factor of three at
  0.05 m. The levels are reconciled between the two generations; the amplitudes are not,
  and no correction is applied to them.
- **Records between January 2009 and May 2012 carry the `SUSPECT` flag.** The early
  profile's three channels differ from one another by 1.5 to 3.5 K over that period and
  the available evidence cannot establish which of them is in error. Filter on the flag
  before using those years quantitatively.
- **The deep columns have no usable diurnal cycle.** At 0.5 m and 0.6 m the sensors report to
  0.1 K, and the median summer daily amplitude at those depths *is* 0.10 K — one reporting
  step. A diurnal cycle read off the deep columns is the instrument's resolution, not the
  soil.
- **Nearly half of 0.3 m and 0.5 m is modelled.** Both are 47 % modelled over the file,
  essentially all of it the ten-year hole between March 2010 and April 2020 when no sensor
  existed at those depths. The values there are good estimates from the other depths, but they
  are estimates.
- **Depths are not replicates.** They share a logger, a power supply and a data bus, so they
  fail together; they do not measure the same soil, and their disagreement is information.
- **The early era was screened once, with the deprecated MeteoScreeningTool, and never
  re-screened.** The thirteen screening notebooks cover the current channels only. The product
  notebook checks the early era for physical consistency but cannot re-screen it.
- **Some early field names are not what they are called.** Ten `TS_PRF_FF1_*` names are the
  modern profile re-screened by the old tool under a shifted replicate index, and three
  `TS_FF1_0.05_*` names in the early era are separate probes installed beside the soil
  heat-flux plates, at effective depths of roughly 0.15, 0.22 and 0.31 m rather than 0.05 m.
  All thirteen are excluded from this product. Going back to the raw database, do not read
  those names as what they say.
- **There is no 1.0 m or 1.5 m depth**, although the database has fields for them: the only
  records are a two-year block containing 1,559 values of exactly `0.00 °C` and excursions to
  `211 °C`, which nothing has screened.
- **August 2012 sub-daily timestamps carry the same uncertainty as the tower variables.** A
  logger clock error that month is corrected in the tower products; whether the forest-floor
  logger shared it is not recorded. Nothing is applied here.
- **The site record before 2011 is invisible to a simple date filter**, having been pasted into
  the maintenance system as one entry. 2004 and 2005 have no site record at all, so statements
  about the first two years rest on physical evidence alone.

## Two dates that do not affect this product

- **The January 2016 site renewal did not reach this profile**, although it moved air
  temperature by 1.32 °C and stepped humidity and pressure. It replaced the tower installation;
  this station is on the forest-floor logger, whose program takes no soil temperature, and the
  record shows no outage, no unusual half-hour and no level change at the date. The level test
  able to see a change common to every channel resolves about ±0.75 K, and within that nothing
  happens.
- **The forest-floor rewiring of 25 June 2015 left this variable untouched.** Soil *water
  content* steps by about 3.9 % VWC at that half-hour; soil temperature does not move, sitting
  in the middle of the distribution of comparable mornings at every channel. That contrast is
  what shows the event was confined to the soil-moisture wiring, and it is the evidence the
  [soil water content page](Meteo_Data_SWC.html) rests its attribution on.
