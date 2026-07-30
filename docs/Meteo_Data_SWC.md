# Soil water content at the forest floor

Half-hourly volumetric soil water content at five depths of the `FF1` soil profile at
CH-LAE, 2004-2025. The file is `09_METEO_SWC_FF1_2004-2025` (parquet and CSV):
**373,728 records** on a continuous 30-minute middle-timestamp index (named
`TIMESTAMP_MIDDLE` in the file) in local time (UTC+1, no daylight saving), from
2004-09-07 00:15 to 2025-12-31 23:45. Values are in **% VWC**. The index begins with the
soil record rather than on 1 January, because there is no soil moisture at this plot
before September 2004.

The **interactive dashboards** summarise one depth each on a single page — coverage and
provenance, seasonality, distributions, extremes and trends, with a table view behind
every chart. They are standalone and work offline:
[0.05](dashboards/METEO_SWC_0.05_dashboard.html) /
[0.1](dashboards/METEO_SWC_0.1_dashboard.html) /
[0.2](dashboards/METEO_SWC_0.2_dashboard.html) /
[0.3](dashboards/METEO_SWC_0.3_dashboard.html) /
[0.5](dashboards/METEO_SWC_0.5_dashboard.html) m.

Method, evidence and checks:

- [`09_METEO_SWC_FF1`](notebooks/10_METEO/30_PRODUCTS/09_METEO_SWC_FF1_2004-2025.html) —
  builds the product, splices the sensor generations, and tests the older era for internal
  breaks.
- The screening notebooks of the current profile, one per depth, which correct the raw
  high-resolution record before this product reads it:
  [0.05](notebooks/10_METEO/20_SCREENING/SWC/SWC_FF1_0.05_1_2020-2025.html) /
  [0.1](notebooks/10_METEO/20_SCREENING/SWC/SWC_FF1_0.1_1_2020-2025.html) /
  [0.2](notebooks/10_METEO/20_SCREENING/SWC/SWC_FF1_0.2_1_2020-2025.html) /
  [0.3](notebooks/10_METEO/20_SCREENING/SWC/SWC_FF1_0.3_1_2020-2025.html) /
  [0.5](notebooks/10_METEO/20_SCREENING/SWC/SWC_FF1_0.5_1_2020-2025.html) m, and the
  [profile download](notebooks/10_METEO/20_SCREENING/SWC/SWC_FF1_PROFILE_2020-2025.html)
  they share as a cross-check reference.
- [`Meteo_Product_Chain`](Meteo_Product_Chain.html) — where this product sits in the chain.

::: {.callout-important title="Which column to use"}

No column is homogeneous across April 2020, when the whole soil profile was replaced. The
step between the two profiles is **+7.6 to +10.7 % VWC** depending on depth, and it is an
instrument change, not weather.

- Inside one profile, use `SWC_FF1_<d>_1`, which is what the probe recorded.
- Across April 2020, use `SWC_FF1_<d>_1_HOMOGENIZED` — but read *The 2020 profile
  replacement* below first, because that column rests on climatology alone and is a derived
  estimate rather than a measurement.
- At **0.5 m there is no homogenised column**, because that depth has only one profile.

**Nothing in this product is gap-filled**, and coverage varies strongly by depth, from
80.8 % at 0.05 m to 96.0 % at 0.2 m over the full period. A missing record is `NaN`, never
`0`.

:::

## Columns

Fourteen columns: one measured value, one homogenised twin and one flag per depth, except at
0.5 m, which has no homogenised twin. They are grouped by depth in the file, so a value and
its provenance stay adjacent. `<d>` is one of `0.05`, `0.1`, `0.2`, `0.3`, `0.5`.

: Columns of `09_METEO_SWC_FF1_2004-2025`. {#tbl-swc-cols}

| column | unit | description |
|---|---|---|
| `SWC_FF1_<d>_1` | % VWC | Soil water content as the probe recorded it, screened. Not homogeneous across April 2020. |
| `SWC_FF1_<d>_1_HOMOGENIZED` | % VWC | The same series with the pre-2020 era shifted onto the level of the current profile. A derived estimate. Absent at 0.5 m. |
| `FLAG_SWC_FF1_<d>_1_SOURCE` | - | Which sensor generation measured the value. |

A value is present exactly where its flag is greater than `0`, and the homogenised column is
present exactly where the measured one is.

### `FLAG_SWC_FF1_<d>_1_SOURCE`

The codes name a **sensor generation**, not a gap-filling model: any code above `0` means
this depth measured this value. Filter on `> 0` for measurements.

: Source codes and their record counts per depth. {#tbl-swc-source}

| code | sensor generation | 0.05 m | 0.1 m | 0.2 m | 0.3 m | 0.5 m |
|---|---|---|---|---|---|---|
| 0 | no measurement: a gap, or before this depth's record begins | 71,670 | 36,422 | 14,865 | 50,638 | 275,140 |
| 1 | EC-20 profile, screened with the MeteoScreeningTool | 207,596 | 238,767 | 260,311 | 239,424 | 0 |
| 2 | TEROS 12 `FF1` profile, installed 19 March 2020 | 94,462 | 98,539 | 98,552 | 69,152 | 98,588 |
| 3 | TEROS 12 replacement probe, 40 cm downslope | 0 | 0 | 0 | 14,514 | 0 |

Code `1` runs from 2004 to each probe's own death, between December 2018 and March 2020.
Code `2` begins on 2020-04-10 at every depth. Code `3` exists at 0.3 m only, from
2025-03-04. The whole of 2004-2020 is code `0` at 0.5 m, because the older profile had no
probe at that depth — no instrument, rather than missing data.

## Coverage

Coverage differs by depth more than for any other meteo variable, because each probe failed
on its own schedule and was not replaced until the whole profile was.

: Coverage and gap structure since each depth's own record begins. A gap is measured as the interval between the values surrounding it. {#tbl-swc-cov}

| depth | record begins | coverage | gaps | gaps > 30 d | longest gap | ends | range | mean |
|---|---|---|---|---|---|---|---|---|
| 0.05 m | 2004-09-07 | 80.8 % | 100 | 6 | 695 d | 2015-06-03 | 7.7-39.7 | 23.5 |
| 0.1 m | 2004-09-07 | 90.3 % | 105 | 3 | 480 d | 2020-04-10 | 0.8-41.7 | 22.9 |
| 0.2 m | 2004-09-07 | 96.0 % | 108 | 2 | 92 d | 2009-06-11 | 7.3-39.0 | 23.6 |
| 0.3 m | 2004-09-07 | 86.5 % | 70 | 6 | 328 d | 2025-03-04 | 3.3-36.4 | 21.1 |
| 0.5 m | 2020-04-10 | 98.2 % | 31 | 0 | 14 d | 2024-04-23 | 18.9-31.7 | 24.1 |

Means and ranges mix the two profiles and are given for orientation only. Three of the five
longest gaps are hardware rather than downtime: 0.1 m waits 480 days between its old probe
dying and the new profile starting, 0.3 m waits 328 days for its replacement in 2025, and the
695 days at 0.05 m are the unexplained absence discussed under *Known limitations*.

***

## The 2020 profile replacement

The five TEROS 12 probes of the current profile were installed on 19 March 2020 and began
reporting on 10 April. The EC-20 probes they replaced had failed one by one over the
preceding year and a half, so **the two generations never overlap at any depth**: the
interval between them runs from 22 days at 0.2 m to 480 days at 0.1 m. That interval is a
dead probe, not an outage, and it is not filled.

Because nothing measured through the break — no second profile, no weather service, and not
the other depths, which changed on the same day — the step cannot be calibrated the way the
precipitation step at 2018 can. The `_HOMOGENIZED` columns shift the older era onto the
current level using **additive calendar-month offsets fitted on climatology alone**, which
assumes the two periods had the same monthly soil-moisture climate. Use them for continuity
and trend work that has to cross 2020. Do not read a homogenised pre-2020 value as an
estimate of what the soil held at the time.

The four homogenised columns are also **not on one reference period**: each is shifted onto
its own depth's current-profile era, and at 0.3 m that era ends at the April 2024 probe
failure while elsewhere it runs to the end of 2025. Within a depth this changes nothing;
differencing *between* depths across 2020 carries the difference.

## The 2015 break in the older era

The older era is not one level either, and this matters for anyone using it. On **25 June
2015, between 08:15 and 09:15**, all four depths drop by about **3.9 % VWC** at once and stay
down. The maintenance record has people working on the forest-floor logger's wiring that
morning, and three weeks earlier it records the plot's power supply being replaced and the
soil-moisture probes' connectors being found loose. These probes were read as a voltage
scaled by a fixed multiplier, so a poor connection in that path shifts the reported level
directly.

The break is not corrected, because removing it alone would leave a larger problem in place.
Underneath it, both the wettest and the driest conditions of each year rise steadily at every
depth through 2005-2015, by **+0.5 to +1.2 % VWC per year** — five to nine % VWC in total —
while precipitation over the same decade trends slightly downward. The driest half-hour of a
year is a property of the soil, so a record whose dry end nearly doubles is not tracking the
weather. It is consistent with the site inventory, which flags three of the four old probes
as defective. A drift has no date at which a correction could be applied and no reference to
fit against, so it is documented rather than removed, as for the tower pyranometer on the
[`SW_IN` page](Meteo_Data_SW_IN.html) and the PAR sensor on the
[`PPFD_IN` page](Meteo_Data_PPFD_IN.html).

The practical consequence: **a level comparison inside the pre-2020 era across June 2015 is
not a comparison of measurements**, and a trend fitted through that era is dominated by
instrument drift rather than by climate.

## No break at the January 2016 site renewal

The January 2016 tower renewal moved air temperature, relative humidity and air pressure, and
a program change that June left much of the longwave record reading low. It did **not** affect
this profile, which is on the forest-floor datalogger rather than the tower one: the tower
program contains no soil-moisture instruction at all, the profile lost no records while the
tower logger was replaced, and neither the level nor any individual half-hour moves at the
date. The notebook asserts all three, so the question is settled rather than open.

## Known limitations

- **Depths are not replicates.** Each is a single probe at one point in one profile. They
  share a logger, a power supply and an SDI-12 bus, so they fail together; but they do not
  measure the same soil, and their disagreement is information rather than error.
- **0.3 m carries three sensor generations and steps twice.** The original probe stopped
  communicating in April 2024 and, in failing, took the whole profile's SDI-12 port down,
  which is why every depth has an April 2024 gap. Its last value in this file is
  `2024-04-09 16:45`, and the 328-day gap that follows ends when a replacement went in on
  4 March 2025 **40 cm down the slope**, in different soil, reading about 3 % VWC high
  relative to its neighbours. Code `3` marks it; the measured column keeps the step and the
  homogenised column removes it.
- **The pre-2020 era was screened once, with the deprecated MeteoScreeningTool, and never
  re-screened.** Values outside the physical range are removed here — failed sensor reads,
  which that hardware stores as a fixed negative constant rather than as a gap — but a probe
  that stopped responding to rainfall while still reporting plausible values would not be
  caught. The per-depth screening notebooks run that test for the current profile only.
- **The two largest gaps in the older era were power failures**, documented in the site
  record: 10 March to 11 June 2009 and 6 March to 28 May 2010, when a fuse slipped out and
  the battery-powered forest-floor logger lost power. The forest floor had no site record at
  all before 2006, so the first two years of the soil record are unadjudicable in principle.
- **The nearly two-year absence at 0.05 m** (July 2013 to June 2015) has no explanation
  anywhere in the site record, and unlike the 2009 and 2010 gaps it affects one depth only.
  It is why 0.05 m has the lowest coverage and the longest gap of the five depths.
- **Sub-daily timestamps in August 2012 carry the same uncertainty as the tower variables.**
  A logger clock error that month is corrected in the tower products. Whether the
  forest-floor logger shared it is not recorded, and the fault is undetectable in soil
  moisture, which has no diurnal cycle to align against. Nothing is applied.
- **FLUXNET's `SWC_F_MDS_1..4` are not this product.** They splice the same two profiles with
  the 2020 step passed straight through, and flat-fill some stretches at a constant value.
  The source flag exists so that this product cannot be used the same way by accident.
