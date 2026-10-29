# Vapour pressure deficit at 47 m

Half-hourly vapour pressure deficit at 47 m on the CH-LAE tower, 2004 to September 2026,
complete. The file is `07_METEO_VPD_2004-2026.09` (parquet and CSV): **398,832 records** on
a continuous 30-minute index `TIMESTAMP_MIDDLE` (middle of the half-hour, UTC+01:00, no
daylight saving), from 2004-01-01 00:15 to 2026-09-30 23:45. 2026 is a partial year
(January to September).

`VPD` is not measured. It is computed by formula from air temperature and relative
humidity, so it inherits the properties of those two products.

The [interactive dashboard](dashboards/METEO_VPD_dashboard.html) summarises the product on
one page.

Method, evidence and checks:

- [`07_METEO_VPD`](notebooks/10_METEO/30_PRODUCTS/07_METEO_VPD_2004-2026.09.html):
  computes both columns and measures what the probe changes leave in each.
- [`02_METEO_TA`](notebooks/10_METEO/30_PRODUCTS/02_METEO_TA_2004-2026.09.html): the
  temperature input and its homogenisation.
- [`04_METEO_RH`](notebooks/10_METEO/30_PRODUCTS/04_METEO_RH_2004-2026.09.html): the
  humidity input and its homogenisation.
- [`METEO_VPD` overview](notebooks/90_OVERVIEW/METEO_VPD.html): the product year by year,
  2004-2025.
- [Meteo Product Chain](Meteo_Product_Chain.html): where this product sits in the chain.

::: {.callout-important title="Which column to use"}

`TA` and `RH` at 47 m come from **one probe**, which changed on 21 January 2016 (Rotronic
MP101A to Campbell CS215) and on 5 June 2026 (to a Campbell HygroVUE10). Both inputs
change level at these dates, so `VPD` does as well.

- `VPD_T1_47_1` is computed from the measured `TA` and `RH`. It is the `VPD` the probe
  reported and matches the measured `TA` and `RH` passed to EddyPro in the biomet file
  ([Level 1](L1.md)). Use it together with those columns, and inside one probe state.
- `VPD_T1_47_1_HOMOGENIZED` is computed from the homogenised `TA` and `RH`, which put every
  probe state on the level of the normal CS215. Use it for anything that crosses
  January 2016 or June 2026 (period means, trends, year rankings, anomalies). It is the
  `VPD` of the flux post-processing chain, which uses it with the homogenised `TA` for
  gap-filling and partitioning ([Level 4.1](L4.1.md), [Level 4.2](L4.2.md)). In
  saturated air it reaches zero before and after 2016, because the homogenised `RH` lifts
  the MP101A's readings in saturated air to 100 %
  ([RH, saturation ceiling](Meteo_Data_RH.md#the-saturation-ceiling)).

**Changed from the 2004-2025 version of this product.** There, `VPD_T1_47_1` was computed
from the homogenised `TA` and the measured `RH`, and no homogenised `VPD` existed. That
mixed basis is no longer exported. The column name `VPD_T1_47_1` now stands for the measured
pair.

:::

## Columns

Both value columns are complete, and both flags are defined at every record and describe
both value columns.

: Columns of `07_METEO_VPD_2004-2026.09`. {#tbl-vpd-cols}

| column | unit | description |
|---|---|---|
| `VPD_T1_47_1` | kPa | Vapour pressure deficit from the measured `TA` and `RH`. Not homogeneous across 2016-01-21 or 2026-06-05. |
| `FLAG_VPD_T1_47_1_ISFILLED` | - | What the record was computed from. |
| `VPD_T1_47_1_HOMOGENIZED` | kPa | Vapour pressure deficit from the homogenised `TA` and `RH`. |
| `FLAG_VPD_T1_47_1_SOURCE` | - | Which probe, and which state of it, stands behind the record. |

`VPD_T1_47_1` ranges from **0 to 4.104 kPa** (median 0.176 kPa), `VPD_T1_47_1_HOMOGENIZED`
from **0 to 4.183 kPa** (median 0.156 kPa). `VPD` is zero at saturation and cannot be
negative.

: The input pairs. {#tbl-vpd-inputs}

| value column | air temperature | relative humidity |
|---|---|---|
| `VPD_T1_47_1` | `TA_T1_47_1_gfXG` (notebook `02`) | `RH_T1_47_1` (notebook `04`) |
| `VPD_T1_47_1_HOMOGENIZED` | `TA_T1_47_1_HOMOGENIZED_gfXG` (notebook `02`) | `RH_T1_47_1_HOMOGENIZED` (notebook `04`) |

`VPD` is the saturation vapour pressure at the air temperature minus the actual vapour
pressure. The Magnus coefficients are those used by ReddyProc. In the CS215 states (source
codes `0`, `5`, `6`, `7`) the homogenised `RH` equals the measured one and the homogenised
`TA` is not warmer than the measured one, so the homogenised `VPD` is never higher than the
measured `VPD` there. On average the homogenised column is lower by 0.006 kPa in the normal
CS215 state, by 0.015 kPa in the MP101A era and by 0.071 kPa in the HygroVUE10 era.

### `FLAG_VPD_T1_47_1_ISFILLED`

Filter on `== 0` for records computed from two measurements at 47 m. Every record is
computed by the formula and none is modelled, but a computed record does not always rest on
two measurements.

: Provenance codes and their record counts. {#tbl-vpd-isfilled}

| code | meaning | records | share |
|---|---|---|---|
| 0 | measured `TA` and measured `RH` | 382,158 | 95.82 % |
| 5 | measured `RH`, gap-filled `TA` | 23 | 0.01 % |
| 6 | `RH` reconstructed from NABEL at 49 m | 15,729 | 3.94 % |
| 7 | `RH` reconstructed from MeteoSwiss Lägern | 922 | 0.23 % |

Codes `6` and `7` take precedence over `5` because a reconstructed `RH` is the larger
error: it carries about 3 % RH of uncertainty and enters the formula linearly.

### `FLAG_VPD_T1_47_1_SOURCE`

Carried over unchanged from notebooks `02` and `04`, whose source flags are identical
record for record. The codes are described on
[Air temperature at 47 m](Meteo_Data_TA.html#sensor-history).

: Probe and probe-state codes, their record counts and the period each covers
(`TIMESTAMP_MIDDLE`). {#tbl-vpd-source}

| code | probe and state | period | records |
|---|---|---|---|
| 0 | Campbell CS215 on SDI-12, normal state | 2016-01-21 14:15 to 2024-10-21 23:45 | 153,428 |
| 1 | Rotronic MP101A, single-ended analog | 2004-09-20 10:45 to 2015-12-31 23:45 | 197,739 |
| 2 | acquisition changeover, probe undetermined | 2016-01-01 00:15 to 2016-01-21 13:45 | 988 |
| 3 | before the tower record begins | 2004-01-01 00:15 to 2004-09-20 10:15 | 12,645 |
| 4 | Campbell HygroVUE10 on SDI-12 | 2026-06-05 11:45 to 2026-09-30 23:45 | 5,641 |
| 5 | probe handling or probe swap half-hour | 2025-05-16 09:45 and 2026-06-05 11:15 | 2 |
| 6 | Campbell CS215 after the handling of 16 May 2025 | 2025-05-16 10:15 to 2026-06-05 10:45 | 18,482 |
| 7 | Campbell CS215 with excess daytime heating | 2024-10-22 00:15 to 2025-05-16 09:15 | 9,907 |

## Coverage

Both columns are complete. What varies is how much of each year rests on two measurements.

: Years in which fewer than 99 % of records are computed from two measurements. Every other
year of 2005-2025 is at least 99 %, and 2026 (January to September) is 99.99 %. {#tbl-vpd-coverage}

| year | computed from two measurements | why |
|---|---|---|
| 2004 | 28.0 % | the tower record begins on 20 September |
| 2009 | 97.2 % | scattered outages |
| 2012 | 92.8 % | logger clock error, power-supply failure and storm damage |
| 2016 | 94.3 % | the January outage during which the probe and logger were replaced |
| 2019 | 95.7 % | the November outage after the NABEL reference ended |

The 2019 gap is the longest after 2018: the 47 m humidity sensor was down from
4 November 2019 04:45 to 19 November 2019 23:45, 759 records. `RH` there is reconstructed
from MeteoSwiss Lägern, and `VPD` carries code `7`.

## The probe changes in `VPD`

Notebook `07` compares both columns with a `VPD` computed by the same formula from the
MeteoSwiss Lägern `TA` and `RH`, using only records computed from two measurements (code
`0`), split into day and night. Only the change in the tower-minus-Lägern difference
across a probe change is evidence, not the difference itself.

: The step in the tower-minus-Lägern `VPD` difference from the MP101A (2005-2015) to the
normal CS215 (from 2017), against the median change of the same difference between two
ordinary consecutive years. {#tbl-vpd-step-2016}

| column | step, day | ordinary year, day | step, night | ordinary year, night |
|---|---|---|---|---|
| `VPD_T1_47_1` | -0.0023 kPa | 0.0101 kPa | -0.0287 kPa | 0.0071 kPa |
| `VPD_T1_47_1_HOMOGENIZED` | +0.0004 kPa | 0.0131 kPa | -0.0130 kPa | 0.0083 kPa |

**January 2016 is an independent test**, because the 2016 transfers of `02` and `04` were
fitted against NABEL, not against Lägern. The homogenised column steps less than the
measured one by day and by night. The measured column's small daytime step is not evidence
of homogeneity: the two errors of the MP101A act on `VPD` in opposite directions (its `TA`
reads about 1.3 °C too cold, which lowers `VPD`, and its `RH` reads too dry, which raises
it), so they partly cancel. The earlier mixed basis, homogenised `TA` with measured `RH`,
stepped by about -0.051 kPa by day and by night, the most of the three.

**June 2026 is not an independent test.** The HygroVUE10 transfers of `02` and `04` were
fitted against Lägern on the same samples (the HygroVUE10 from 12 June to 30 September 2026
against the normal CS215 on the same dates of 2022-2024). Across this change the measured
column steps by +0.055 kPa by day and +0.117 kPa at night, against a mean `VPD` of the
HygroVUE10 sample of 1.39 kPa by day and 1.11 kPa at night. The homogenised column steps by
+0.021 and +0.018 kPa, which is expected by construction.

## Known limitations

- **The measured column is not homogeneous across 21 January 2016 or 5 June 2026.** Use
  `VPD_T1_47_1_HOMOGENIZED` for anything that crosses either date, or stay inside one probe
  state with `FLAG_VPD_T1_47_1_SOURCE`.
- **A small night step remains in the homogenised column at 2016.** It is -0.013 kPa
  against an ordinary-year change of 0.008 kPa, less than half the step of the measured
  column (-0.029 kPa).
- **Just below saturation the MP101A era remains slightly too dry.** At a Lägern humidity
  of 90 to 95 % the CS215 reads about 2 % RH wetter than the homogenised MP101A, so the
  homogenised `VPD` of humid half-hours before 2016 is slightly high. The saturation
  ceiling of the homogenised `RH` does not remove this difference
  ([RH, saturation ceiling](Meteo_Data_RH.md#the-saturation-ceiling)).
- **The June 2026 homogenisation rests on one summer and one reference.** The `TA` and `RH`
  transfers behind it are fitted on June to September 2026 against Lägern, are untested
  outside summer, and are to be refitted once the HygroVUE10 record includes a winter. See
  [Air temperature at 47 m](Meteo_Data_TA.html) and
  [Relative humidity at 47 m](Meteo_Data_RH.html).
- **Both humidity eras drift.** Against MeteoSwiss Lägern the MP101A era drifts by
  -0.34 and the CS215 era by +0.44 percentage points of RH per year, more over each era than
  the 2016 step. The homogenised `RH` removes the steps, not this drift, so a `VPD` trend
  in either column, even inside one era, contains sensor movement.
- **The homogenised `TA` is self-consistent, not absolutely accurate.** All eras are put on
  the radiation-shield behaviour of the MP101A, whose warm bias in sun (about +0.4 °C at
  strong radiation) remains. A warm bias in `TA` raises `VPD`.
- **Reconstructed humidity propagates.** 4.17 % of records rest on a humidity transferred
  from another instrument (codes `6` and `7`). Filter on `FLAG_VPD_T1_47_1_ISFILLED == 0`
  where that matters.
- **2026 is a partial year.** It holds January to September and a dry, clear summer, so its
  annual statistics are not comparable with full years.
