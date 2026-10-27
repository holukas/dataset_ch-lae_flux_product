# Soil water content at the forest floor

Half-hourly volumetric soil water content at five depths of the `FF1` soil profile at CH-LAE,
2004-2025. The file is `09_METEO_SWC_FF1_2004-2025` (parquet and CSV): **373,728 records** on a
continuous 30-minute index, `TIMESTAMP_MIDDLE` (middle of the half-hour), in local time
(UTC+01:00, no daylight saving), from 2004-09-07 00:15 to 2025-12-31 23:45. Values are in
**% VWC**. The index begins in September 2004 because the soil record begins then.

The series ends on 31 December 2025. It is part of [FP2026.1](Dataset_Versions.html) and of the
[merged meteo product](notebooks/10_METEO/30_PRODUCTS/99_METEO_MERGED_2004-2026.09.html), where it
is `NaN` from 1 January 2026; the extension to 30 September 2026 is in progress.

The interactive dashboards summarise one depth each (coverage, provenance, seasonality,
distributions, extremes and trends). They are standalone files and work offline:
[0.05](dashboards/METEO_SWC_0.05_dashboard.html) /
[0.1](dashboards/METEO_SWC_0.1_dashboard.html) /
[0.2](dashboards/METEO_SWC_0.2_dashboard.html) /
[0.3](dashboards/METEO_SWC_0.3_dashboard.html) /
[0.5](dashboards/METEO_SWC_0.5_dashboard.html) m.

Notebooks:

- [`09_METEO_SWC_FF1`](notebooks/10_METEO/30_PRODUCTS/09_METEO_SWC_FF1_2004-2025.html): builds
  the product, splices the sensor generations and tests the older era for internal breaks.
- The screening notebooks of the current profile, one per depth, which screen the raw
  high-resolution record before this product reads it:
  [0.05](notebooks/10_METEO/20_SCREENING/SWC/SWC_FF1_0.05_1_2020-2025.html) /
  [0.1](notebooks/10_METEO/20_SCREENING/SWC/SWC_FF1_0.1_1_2020-2025.html) /
  [0.2](notebooks/10_METEO/20_SCREENING/SWC/SWC_FF1_0.2_1_2020-2025.html) /
  [0.3](notebooks/10_METEO/20_SCREENING/SWC/SWC_FF1_0.3_1_2020-2025.html) /
  [0.5](notebooks/10_METEO/20_SCREENING/SWC/SWC_FF1_0.5_1_2020-2025.html) m, and the shared
  [profile download](notebooks/10_METEO/20_SCREENING/SWC/SWC_FF1_PROFILE_2020-2025.html) they use
  as a cross-check reference.
- [`Meteo_Product_Chain`](Meteo_Product_Chain.html): where this product sits in the chain.

::: {.callout-important title="Which column to use"}

No column is homogeneous across April 2020, when the whole soil profile was replaced. The step
between the two profiles is **+7.6 to +10.7 % VWC**, depending on depth. It is an instrument
change, not weather.

- Within one profile, use `SWC_FF1_<d>_1`, which is what the probe recorded.
- Across April 2020, use `SWC_FF1_<d>_1_HOMOGENIZED`. Read *The 2020 profile replacement* first:
  this column rests on climatology alone and is a derived estimate, not a measurement.
- At **0.5 m there is no homogenised column**, because that depth has only one profile.

**Nothing in this product is gap-filled.** Coverage over the full period ranges from 80.8 % at
0.05 m to 96.0 % at 0.2 m. A missing record is `NaN`, never `0`.

:::

## Columns

Fourteen columns: per depth, one measured value, one homogenised column and one flag, except at
0.5 m, which has no homogenised column. The columns are grouped by depth. `<d>` is one of `0.05`,
`0.1`, `0.2`, `0.3`, `0.5`.

: Columns of `09_METEO_SWC_FF1_2004-2025`. {#tbl-swc-cols}

| column | unit | description |
|---|---|---|
| `SWC_FF1_<d>_1` | % VWC | Soil water content as the probe recorded it, screened. Not homogeneous across April 2020. |
| `SWC_FF1_<d>_1_HOMOGENIZED` | % VWC | The same series with the pre-2020 era shifted onto the level of the current profile. A derived estimate. Absent at 0.5 m. |
| `FLAG_SWC_FF1_<d>_1_SOURCE` | - | Which sensor generation measured the value. |

A value is present exactly where its flag is greater than `0`, and the homogenised column is
present exactly where the measured one is.

### `FLAG_SWC_FF1_<d>_1_SOURCE`

The codes name a **sensor generation**. Any code above `0` means the depth measured the value;
filter on `> 0` for measurements.

: Source codes and their record counts per depth. {#tbl-swc-source}

| code | sensor generation | 0.05 m | 0.1 m | 0.2 m | 0.3 m | 0.5 m |
|---|---|---|---|---|---|---|
| 0 | no measurement: a gap, or before this depth's record begins | 71,670 | 36,422 | 14,865 | 50,638 | 275,140 |
| 1 | EC-20 profile, screened with the MeteoScreeningTool | 207,596 | 238,767 | 260,311 | 239,424 | 0 |
| 2 | TEROS 12 `FF1` profile, installed 19 March 2020 | 94,462 | 98,539 | 98,552 | 69,152 | 98,588 |
| 3 | TEROS 12 replacement probe, 40 cm downslope | 0 | 0 | 0 | 14,514 | 0 |

Code `1` runs from 2004 until each probe failed, between December 2018 and March 2020. Code `2`
begins on 2020-04-10 at every depth. Code `3` exists at 0.3 m only, from 2025-03-04. At 0.5 m,
2004-2020 is code `0` throughout, because the older profile had no probe at that depth.

## Coverage

Coverage differs by depth more than for any other meteo variable, because each probe failed at
its own time and none was replaced until the whole profile was.

: Coverage and gap structure since each depth's own record begins. A gap is measured as the interval between the values surrounding it. {#tbl-swc-cov}

| depth | record begins | coverage | gaps | gaps > 30 d | longest gap | ends | range | mean |
|---|---|---|---|---|---|---|---|---|
| 0.05 m | 2004-09-07 | 80.8 % | 100 | 6 | 695 d | 2015-06-03 | 7.7-39.7 | 23.5 |
| 0.1 m | 2004-09-07 | 90.3 % | 105 | 3 | 480 d | 2020-04-10 | 0.8-41.7 | 22.9 |
| 0.2 m | 2004-09-07 | 96.0 % | 108 | 2 | 92 d | 2009-06-11 | 7.3-39.0 | 23.6 |
| 0.3 m | 2004-09-07 | 86.5 % | 70 | 6 | 328 d | 2025-03-04 | 3.3-36.4 | 21.1 |
| 0.5 m | 2020-04-10 | 98.2 % | 31 | 0 | 14 d | 2024-04-23 | 18.9-31.7 | 24.1 |

Means and ranges mix the two profiles and are for orientation only. The three longest gaps are
not station outages. At 0.1 m, 480 days pass between the old probe failing and the new profile
starting; at 0.3 m, 328 days pass until the replacement probe of 2025. The 695 days at 0.05 m are
unexplained (see *Known limitations*).

***

## The 2020 profile replacement

The five TEROS 12 probes of the current profile were installed on 19 March 2020 and began
reporting on 10 April 2020. The EC-20 probes they replaced had failed one by one over the
preceding year and a half, so **the two generations do not overlap at any depth**. The interval
between them runs from 22 days at 0.2 m to 480 days at 0.1 m and is not filled.

No other measurement spans the break: there is no second profile and no weather-service
reference, and all depths changed on the same day. The step therefore cannot be calibrated as the
2018 precipitation step was. The `_HOMOGENIZED` columns shift the older era onto the current level
with **additive calendar-month offsets fitted on climatology alone**. This assumes the two periods
had the same monthly soil-moisture climate. Use these columns for continuity and trend work that
has to cross 2020. Do not read a homogenised pre-2020 value as an estimate of the water content at
the time.

The homogenised columns are **not on one common reference period**. Each is shifted onto its own
depth's current-profile era, which at 0.3 m ends at the April 2024 probe failure and elsewhere runs
to the end of 2025. Within a depth this has no effect; a difference *between* depths across 2020
includes it.

## The 2015 break in the older era

On **25 June 2015, between 08:15 and 09:15**, all four depths of the older profile drop by about
**3.9 % VWC** at once and stay at the lower level. The maintenance record has work on the
forest-floor logger's wiring that morning. Three weeks earlier it records the replacement of the
plot's power supply and loose connectors on the soil-moisture probes. These probes were read as a
voltage scaled by a fixed multiplier, so a poor connection shifts the reported level directly.
Soil temperature on the same logger does not change at that time (see
[`Meteo_Data_TS`](Meteo_Data_TS.html)), which confines the event to the soil-moisture wiring.

The break is not corrected, because a larger problem lies underneath it. Through 2005-2015 both
the wettest and the driest conditions of each year rise steadily at every depth, by **+0.5 to
+1.2 % VWC per year** (5 to 9 % VWC in total), while precipitation over the same decade trends
slightly downward. The driest half-hour of a year is set by the soil, so a dry end that nearly
doubles points to the instruments, not to the weather. The site inventory flags three of the four
old probes as defective. A drift has no date at which a
correction could be applied and no reference to fit against, so it is documented and not removed,
as for the tower pyranometer ([`SW_IN`](Meteo_Data_SW_IN.html)) and the PAR sensor
([`PPFD_IN`](Meteo_Data_PPFD_IN.html)).

**A level comparison within the pre-2020 era across June 2015 is not a comparison of
measurements**, and a trend fitted through that era is dominated by instrument drift, not by
climate.

## No break in January 2016

The January 2016 tower renewal moved air temperature, relative humidity and air pressure, and a
program change in June 2016 left much of the longwave record reading low. This profile is not
affected. It is on the forest-floor datalogger, the tower program contains no soil-moisture
instruction, the profile lost no records while the tower logger was replaced, and neither the
level nor any single half-hour changes at the date. The notebook asserts all three.

## Known limitations

- **Depths are not replicates.** Each is a single probe at one point. The probes share a logger, a
  power supply and an SDI-12 bus, so they fail together, but they measure different soil, and
  differences between them are real.
- **0.3 m carries three sensor generations and steps twice.** The 2020 probe stopped communicating
  in April 2024 and took the whole profile's SDI-12 port down with it, which is why every depth has
  a gap in April 2024. Its last value is at `2024-04-09 16:45`. The 328-day gap that follows ends
  with a replacement probe installed on 4 March 2025, **40 cm downslope** in different soil, which
  reads about 3 % VWC high relative to the other depths. Code `3` marks it; the measured column keeps
  the step and the homogenised column removes it.
- **The pre-2020 era was screened once, with the deprecated MeteoScreeningTool, and never
  re-screened.** Values outside the physical range are removed here. These are failed sensor reads,
  which this hardware stores as a fixed negative value instead of a gap. A probe that stopped
  responding to rain while still reporting plausible values would not be caught. The per-depth
  screening notebooks run that test for the current profile only.
- **The two largest gaps of the older era are power failures** documented in the site record:
  10 March to 11 June 2009, and 6 March to 28 May 2010, when a fuse slipped out and the
  battery-powered forest-floor logger lost power. There is no site record for the forest floor
  before 2006, so gaps in the first two years cannot be explained.
- **The nearly two-year gap at 0.05 m** (July 2013 to June 2015) has no explanation in the site
  record and, unlike the 2009 and 2010 gaps, affects one depth only. It is why 0.05 m has the lowest
  coverage and the longest gap of the five depths.
- **Sub-daily timestamps in August 2012 are uncertain.** A logger clock error that month is
  corrected in the tower products. Whether the forest-floor logger had the same error is not
  recorded, and soil moisture has no diurnal cycle to check it against. No shift is applied.
- **FLUXNET's `SWC_F_MDS_1..4` are not this product.** They splice the same two profiles with the
  2020 step passed through unchanged, and fill some periods with a constant value. Use the source
  flag to keep the generations apart.
