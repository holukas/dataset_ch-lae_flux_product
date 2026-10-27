# Soil temperature at the forest floor

Half-hourly soil temperature at seven depths of the `FF1` profile at CH-LAE, 2004-2025. The file
is `10_METEO_TS_FF1_2004-2025` (parquet and CSV): **373,728 records** on a continuous 30-minute
index, `TIMESTAMP_MIDDLE` (middle of the half-hour), in local time (UTC+01:00, no daylight
saving), from 2004-09-07 00:15 to 2025-12-31 23:45. Values are in **°C**. The index begins in
September 2004 because the soil record begins then.

The series ends on 31 December 2025. It is part of [FP2026.1](Dataset_Versions.html) and of the
[merged meteo product](notebooks/10_METEO/30_PRODUCTS/99_METEO_MERGED_2004-2026.09.html), where it
is `NaN` from 1 January 2026; the extension to 30 September 2026 is in progress. Both carry the
seven overall columns and their flags, not the eighteen individual channels.

The interactive dashboards summarise one depth each (coverage, provenance, seasonality,
distributions, extremes and trends). They are standalone files and work offline:
[0.05](dashboards/METEO_TS_0.05_dashboard.html) /
[0.1](dashboards/METEO_TS_0.1_dashboard.html) /
[0.15](dashboards/METEO_TS_0.15_dashboard.html) /
[0.2](dashboards/METEO_TS_0.2_dashboard.html) /
[0.3](dashboards/METEO_TS_0.3_dashboard.html) /
[0.5](dashboards/METEO_TS_0.5_dashboard.html) /
[0.6](dashboards/METEO_TS_0.6_dashboard.html) m. Each covers only the whole years its depth
measured, so 0.15 m ends in 2020 and 0.2 m and 0.6 m begin in 2021.

Notebooks:

- [`10_METEO_TS_FF1`](notebooks/10_METEO/30_PRODUCTS/10_METEO_TS_FF1_2004-2025.html): builds the
  product. It reconciles the channels, splices the sensor generations, fills the gaps and tests
  the record for breaks.
- [`TS_FF1_SCREENED_30MIN`](notebooks/10_METEO/30_PRODUCTS/TS_FF1_SCREENED_30MIN_2004-2025.html):
  downloads the screened channels the product is built from.
- [`TS_FF1_GAPFILL_ML_COMPARISON`](notebooks/10_METEO/30_PRODUCTS/TS_FF1_GAPFILL_ML_COMPARISON.html):
  the comparison that chose the gap-filling method.
- The thirteen screening notebooks of the current profile, one per channel, under
  `10_METEO/20_SCREENING/TS/` in the [notebook index](notebooks/index.html).
- [`Meteo_Data_SWC`](Meteo_Data_SWC.html): soil water content of the same profile. Its June 2015
  break is attributed using this variable.
- [`Meteo_Product_Chain`](Meteo_Product_Chain.html): where this product sits in the chain.

::: {.callout-important title="Which column to use"}

The file holds two kinds of column.

- **`TS_FF1_<d>_HOMOGENIZED_GAPFILLED`** is the column to analyse: one reconciled, gap-filled
  series per depth, with the sensor-generation step removed where it could be measured.
- **The eighteen individual channels** (`TS_FF1_0.05_2`, `TS_PRF_FF1_0.05_1`, ...) are the
  screened measurements, one sensor each, with gaps where that sensor was down. Use them when you
  need the record of a single instrument.

**Filter on `FLAG_..._METHOD` before analysis.** At 0.3 m and 0.5 m about **47 % of the overall
column is modelled**, because those depths had no sensor between March 2010 and April 2020.

**Do not compute a diurnal or seasonal amplitude across April 2020.** The levels are reconciled,
the amplitudes are not: they differ by a factor of three at 0.05 m.

:::

## Columns

Thirty-five columns: eighteen individual channels, seven overall columns, seven `METHOD` flags and
three `SUSPECT` flags. `<d>` is one of `0.05`, `0.1`, `0.15`, `0.2`, `0.3`, `0.5`, `0.6`.

: Columns of `10_METEO_TS_FF1_2004-2025`. {#tbl-ts-cols}

| column | unit | description |
|---|---|---|
| `TS_FF1_<d>_HOMOGENIZED_GAPFILLED` | °C | One series per depth: the depth's sensors reconciled into one record, the generation step removed where measurable, gaps filled from the other depths. |
| `FLAG_..._METHOD` | - | Whether each value was measured, and by which generation, or modelled. |
| `FLAG_..._SUSPECT` | - | `1` where the early profile disagreed with itself. Only at 0.05, 0.1 and 0.15 m. |
| eighteen `TS_FF1_*` / `TS_PRF_FF1_*` | °C | The individual screened channels, one sensor each. Never gap-filled. |

### `FLAG_TS_FF1_<d>_HOMOGENIZED_GAPFILLED_METHOD`

Keep `METHOD` `1` or `2` for measured values only.

: Method codes and their record counts per depth. {#tbl-ts-method}

| code | meaning | 0.05 m | 0.1 m | 0.15 m | 0.2 m | 0.3 m | 0.5 m | 0.6 m |
|---|---|---|---|---|---|---|---|---|
| 0 | no value | 21,398 | 21,398 | 104,050 | 274,381 | 21,398 | 21,398 | 274,381 |
| 1 | measured, current profile | 99,347 | 98,611 | 0 | 98,571 | 98,692 | 98,590 | 98,617 |
| 2 | measured, early profile | 252,848 | 252,880 | 269,389 | 0 | 88,151 | 88,188 | 0 |
| 3 | modelled, nearest contributing depth ≤ 0.15 m away | 98 | 802 | 252 | 0 | 164,795 | 0 | 0 |
| 4 | modelled, nearest contributing depth further away | 37 | 37 | 37 | 776 | 692 | 165,552 | 730 |

Codes `3` and `4` record how far away the nearest contributing depth was. They are not a quality
ranking: the fill uses every available depth at once, so a `4` is not necessarily worse than a `3`.

### `FLAG_TS_FF1_<d>_HOMOGENIZED_GAPFILLED_SUSPECT`

`1` marks the period in which the three channels of the early profile disagreed with each other
beyond their own seasonal norm. The flag exists at three depths and covers 8,121 to 20,297
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

The spans differ because the sensors did: **0.15 m exists only in the early profile**, **0.2 m and
0.6 m only from 2020**, and the other depths span the whole record.

Where one depth has no value, no depth has: **5.7 % of records are missing at every depth at
once**, during station outages of the early era. The four longest are 124 days from February
2011, 93 days from March 2009, 83 days from March 2010 and 63 days from May 2007. The site record
names two of them: a failed logger, and a fuse that slipped out of the battery-powered
forest-floor station.

***

## The 2020 profile replacement

The early profile was a five-sensor Campbell 107 probe stick. The forest-floor logger programs
name its sensors at 5, 10, 15, 30 and 50 cm, which are the five depths with an early record. It was
replaced in March 2020 by the current sensors, which began reporting on 10 April 2020.

Unlike soil water content, the two generations here **overlap**, for 347 days, until the old
stick stopped at the March 2021 logger rebuild. The overlap measures the level difference: about
0.6 K at 0.05 m and 0.4 K at 0.1 m. `HOMOGENIZED` in the column name refers to its removal.

::: {.callout-warning title="Levels are reconciled, amplitudes are not"}

The early sensors were much more closely coupled to the surface than the current ones at the same
nominal depth. At 0.05 m the median summer daily amplitude is **3.13 K in the early era and 0.90 K
in the current one**, and the median annual range 25.4 K against 18.0 K. At 0.1 m the daily
amplitude is 1.27 K against 0.59 K.

A daily or seasonal amplitude computed across April 2020 is therefore dominated by the sensor
change. Annual and daily *means* are comparable across it; amplitudes are not.

:::

**At 0.3 m and 0.5 m there is no homogenisation**, because the generations do not overlap: the
early sensors at those depths stopped on 2010-03-06, ten years before the new ones were installed.
The early era there keeps its own level, and a trend across April 2020 includes the sensor change.
The climatological offsets used for soil water content are not used here, so that measured and
climatological offsets are not mixed in one product.

## The early profile disagrees with itself, 2009-2012

Between January 2009 and May 2012 the three early channels depart from their own seasonal norm by
1.5 to 3.5 K, for months at a time and in opposite pairs: one runs warm while another runs cold.
In the other thirteen years they agree to within a few tenths of a kelvin.

The period covers the years in which the forest-floor logger repeatedly lost power, and it ends
around a logger program of April 2012 described as having *"corrected multipliers and offset"*.
Which channel is wrong is **not determined**: with three sensors, one that moves shifts the
comparison for all three, and there is no fourth soil sensor and no external reference. The
records are kept, flagged `SUSPECT`, and not corrected.

## The gap-fill

Gaps in the overall columns are filled from the **other depths of the same profile**, with a
least-squares fit made separately for each sensor generation, so a fill does not introduce a
sensor step. The fit uses every available depth, each with rolling means over 3 h to 120 d, and a day-of-year
term. It was
validated by holding out whole years and by predicting the deep depths from the shallow ones alone.

Each depth is filled only within its own measured span and is not extrapolated. This is why
0.2 m and 0.6 m have no values before 2020 and 0.15 m none after March 2021. Within a span, the
only remaining gaps are the station outages. The individual channels are never filled.

## Known limitations

- **Amplitudes are not comparable across April 2020.** The early sensors were more closely coupled
  to the surface than the current ones at the same nominal depth, so the diurnal and seasonal
  amplitude changes with the hardware, by a factor of three at 0.05 m. No correction is applied to
  the amplitudes.
- **Records between January 2009 and May 2012 carry the `SUSPECT` flag.** The three early
  channels differ from one another by 1.5 to 3.5 K over that period, and which of them is wrong
  cannot be established. Filter on the flag before using those years quantitatively.
- **The deep columns have no usable diurnal cycle.** At 0.5 m and 0.6 m the sensors report in
  steps of 0.1 K, and the median summer daily amplitude at those depths is 0.10 K, one reporting
  step. A diurnal cycle in the deep columns reflects the instrument resolution, not the soil.
- **Nearly half of 0.3 m and 0.5 m is modelled.** Both are 47 % modelled over the file, almost
  all of it in the ten years between March 2010 and April 2020 when no sensor existed at those
  depths. These values are estimates from the other depths.
- **Depths are not replicates.** They share a logger, a power supply and a data bus, so they fail
  together, but they measure different soil, and differences between them are real.
- **The early era was screened once, with the deprecated MeteoScreeningTool, and never
  re-screened.** The thirteen screening notebooks cover the current channels only. The product
  notebook checks the early era for physical consistency but does not re-screen it.
- **Some early field names do not describe their content.** Ten `TS_PRF_FF1_*` names hold the
  current profile, re-screened by the old tool under a shifted replicate index. Three
  `TS_FF1_0.05_*` names in the early era are separate probes installed beside the soil heat-flux
  plates, at effective depths of about 0.15, 0.22 and 0.31 m rather than 0.05 m. All thirteen are
  excluded from this product. In the raw database, do not take these names at face value.
- **There is no 1.0 m or 1.5 m depth**, although the database has fields for them. Their only
  records are a two-year block with 1,559 values of exactly `0.00 °C` and excursions to `211 °C`,
  never screened.
- **Sub-daily timestamps in August 2012 are uncertain.** A logger clock error that month is
  corrected in the tower products. Whether the forest-floor logger had the same error is not
  recorded. No shift is applied here.
- **The site record before 2011 is not found by a date filter**, because it was pasted into the
  maintenance system as one entry. There is no site record for 2004 and 2005, so statements about
  the first two years rest on the data alone.

## Two dates that do not affect this product

- **January 2016.** The tower renewal moved air temperature by 1.32 °C and stepped humidity and
  pressure. It did not reach this profile, which is on the forest-floor logger; the tower program
  takes no soil temperature. The record shows no outage, no unusual half-hour and no level change
  at the date. The level test for a change common to every channel resolves about ±0.75 K, and
  finds no change within that.
- **25 June 2015.** Soil water content steps by about 3.9 % VWC at the forest-floor rewiring that
  morning. Soil temperature does not move: at every channel it lies in the middle of the
  distribution of comparable mornings. This shows the event was confined to the soil-moisture
  wiring, and the [soil water content page](Meteo_Data_SWC.html) relies on it.
