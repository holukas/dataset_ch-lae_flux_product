# Relative humidity at 47 m

Half-hourly relative humidity at 47 m on the CH-LAE tower, 2004 to September 2026,
complete. The file is `04_METEO_RH_CORRECTED_2004-2026.09` (parquet and CSV):
**398,832 records** on a continuous 30-minute middle-timestamp index (named
`TIMESTAMP_MIDDLE` in the file) in local time (UTC+1, no daylight saving), from
2004-01-01 00:15 to 2026-09-30 23:45. 2026 is a partial year (January to
September).

The [**interactive dashboard**](dashboards/METEO_RH_dashboard.html) summarises the
product on one page: coverage and provenance, seasonality, distributions, extremes
and trends, with a table view behind every chart. It is standalone and works
offline.

Method, evidence and checks:

- [`04_METEO_RH`](notebooks/10_METEO/30_PRODUCTS/04_METEO_RH_2004-2026.09.html):
  builds the product: the merge of the two screenings, the 2012 corrections, the
  `RH > 100 %` correction, the identification of the probes and their states, the
  2016 and 2026 transfers, and the two reconstruction passes.
- [`02_METEO_TA`](notebooks/10_METEO/30_PRODUCTS/02_METEO_TA_2004-2026.09.html): the
  same probe delivers `TA`, and the dates of every probe change and probe state are
  derived there. Notebook `04` reads its product for the vapour pressure of the
  2025 and 2026 analyses, so `02` runs first.
- [`Meteo_Product_Chain`](Meteo_Product_Chain.html): where this product sits in the
  chain. `VPD` is computed from it.

::: {.callout-important title="Which column to use"}

The 47 m record comes from three probes, and the second of them changed state twice
before it was replaced (see [Sensor history](#sensor-history)). The measured column
steps **upwards by 2.1 to 3.3 percentage points of RH** at the 21 January 2016
probe change, and by **3.9 to 4.1** on the half-hours away from saturation; it
becomes drier at the 5 June 2026 probe change, increasingly so with the humidity.

- Inside one probe state, use `RH_T1_47_1`, which is what the probe reported.
- Across 21 January 2016 or 5 June 2026 (period means, trends, year rankings,
  anomalies) use `RH_T1_47_1_HOMOGENIZED`, which puts the other probes on the level
  of the CS215. It removes the steps at the probe changes, not the drift within each
  era (see [Known limitations](#known-limitations)).
- Where provenance has to be certain, select `FLAG_RH_T1_47_1_SOURCE` in
  `{0, 1, 4, 6}`. Codes `6` and `7` carry the probe's heating in sun in both
  columns; exclude code `7` wherever the sun-dependent part of `RH` matters.

See [What happened in 2016](#what-happened-in-2016).

:::

## Columns

Every one of the 398,832 records carries a value, and both flags are defined
everywhere. The two value columns share the same flags.

: Columns of `04_METEO_RH_CORRECTED_2004-2026.09`. {#tbl-rh-cols}

| column | unit | description |
|---|---|---|
| `RH_T1_47_1` | % | Relative humidity, corrected and gap-free, every probe as measured. Bounded to `[0, 100]`. Not homogeneous across 2016-01-21 or 2026-06-05. |
| `FLAG_RH_T1_47_1_MISSING` | - | Whether the value was measured at 47 m, and if not, which sensor it was reconstructed from. |
| `RH_T1_47_1_HOMOGENIZED` | % | The same series on the level of the CS215. Bounded to `[0, 100]`. |
| `FLAG_RH_T1_47_1_SOURCE` | - | Which probe, and which state of it, stands behind the record. |

### `FLAG_RH_T1_47_1_MISSING`

Filter on `== 0` for genuine 47 m measurements. The series is complete, so every
other code marks a value transferred from another instrument. Nothing in this
product is modelled: a reconstructed value is another measurement of the same
quantity, corrected by a monthly offset fitted within the probe state it belongs
to.

: Provenance codes, their record counts and their share of the 398,832 records. {#tbl-rh-missing}

| code | meaning | records | share |
|---|---|---|---|
| 0 | measured at 47 m | 382,181 | 95.83 % |
| 3 | reconstructed from NABEL at 49 m on the same tower | 15,729 | 3.94 % |
| 4 | reconstructed from MeteoSwiss Lägern, 2.5 km away | 922 | 0.23 % |

Codes `1` (never measured) and `2` (removed as faulty) are defined in the notebook
but do not occur in this file: the two references between them cover every gap.

Code `3` carries approximately **3 % RH** of uncertainty, established by
leave-one-year-out validation against the years both sensors measured. Code `4` is
weaker still, since Lägern is 2.5 km away on the ridge at 845 m, about 100 m above
the tower sensor (the tower stands at about 690 m, the sensor 47 m above the
ground). It occurs almost only after the NABEL sensor ends in 2018: 877 of its 922
records fall in 2019 (759), 2023 (9), 2024 (107), 2025 (1) and 2026 (1), the
records of 2025 and 2026 being the two probe half-hours. The other 45 are short
NABEL gaps in 2004 (6), 2005 (24), 2011 (10) and 2016 (5).

### `FLAG_RH_T1_47_1_SOURCE`

The codes are those of notebook `02`, and notebook `04` asserts that the two flags
agree on every record.

: Probe and probe-state codes, their record counts and the period each covers
(`TIMESTAMP_MIDDLE`). {#tbl-rh-source}

| code | probe and state | period | records |
|---|---|---|---|
| 0 | Campbell CS215 on SDI-12, normal state | 2016-01-21 14:15 to 2024-10-21 23:45 | 153,428 |
| 1 | Rotronic MP101A, single-ended analog | 2004-09-20 10:45 to 2015-12-31 23:45 | 197,739 |
| 2 | acquisition changeover, probe generation undetermined | 2016-01-01 00:15 to 2016-01-21 13:45 | 988 |
| 3 | before the tower record begins | 2004-01-01 00:15 to 2004-09-20 10:15 | 12,645 |
| 4 | Campbell HygroVUE10 on SDI-12 | 2026-06-05 11:45 to 2026-09-30 23:45 | 5,641 |
| 5 | probe handling or probe swap half-hour | 2025-05-16 09:45 and 2026-06-05 11:15 | 2 |
| 6 | Campbell CS215 after the handling of 16 May 2025, reads high in sun | 2025-05-16 10:15 to 2026-06-05 10:45 | 18,482 |
| 7 | Campbell CS215 with excess daytime heating, reads low in sun | 2024-10-22 00:15 to 2025-05-16 09:15 | 9,907 |

Codes `2`, `3` and `5` mark records that no probe at this height stands behind.
Code `2` is the changeover outage: the tower recorded nothing for 20 days while the
logger was rebuilt, and those records are reconstructed from NABEL. The two code-`5`
half-hours are removed and reconstructed from Lägern with the offset of the state
before each. Select `FLAG_RH_T1_47_1_SOURCE` in `{0, 1, 4, 6}` where the probe has
to be certain, and a single code to stay inside one probe state.

## Coverage

The tower measurement begins on **2004-09-20 10:45**. Everything before that is
reconstructed from NABEL. From 2005 onwards every year is at least 92.8 % measured.

: The years in which measured coverage is not near-complete. Every other year of
2005-2025 is at least 99 % measured. {#tbl-rh-coverage}

| year | measured | why |
|---|---|---|
| 2004 | 28.0 % | the record begins on 20 September |
| 2009 | 97.2 % | scattered outages |
| 2012 | 92.8 % | logger clock error, power-supply failure and storm damage |
| 2016 | 94.3 % | the January outage during which the probe and logger were replaced |
| 2019 | 95.7 % | an outage after the NABEL reference ends, filled from MeteoSwiss |

The 2012 faults are the largest interruption inside the measured period. A logger
clock error shifted one block of August 2012 by 15.5 hours; a tower power-supply
failure in late July and August, and storm damage in late October and November, left
records that could not be repaired. The clock error was corrected, the other two
periods were removed, and all of it was reconstructed from NABEL.

## Sensor history {#sensor-history}

`TA_T1_47_1` and `RH_T1_47_1` arrive from one probe in one sensor call, so every
date below is the same in notebook `02`, where most of them are derived. The field
name and its database tags did not change at any of them.

- **Rotronic MP101A, to 31 December 2015 (code `1`).** Six CR10X programs spanning
  2004-2006 name it and its analog conversion.
- **Campbell CS215, from 21 January 2016 (code `0`).** Named by the CR1000 program
  installed at the changeover, read over SDI-12.
- **The same CS215 with excess daytime heating, 22 October 2024 to 16 May 2025
  (code `7`).** Dated in notebook `02` from the daytime excess of the 47 m
  temperature over the 35 m profile sensor of the same tower, which grows in the
  weeks after the fieldbook records intake tubing attached at the 47 m sonic
  anemometer on 19 September 2024.
- **The same CS215 after 16 May 2025 (code `6`).** The probe was handled during a
  site visit that day; the fieldbook records the heating connection of the tower
  inlet found melted and disconnected. See
  [The May 2025 change](#the-may-2025-change).
- **Campbell HygroVUE10, from 5 June 2026 (code `4`).** The fieldbook adds it at
  this location on that day. See
  [The June 2026 probe change](#the-june-2026-probe-change).

The homogenised column treats each state as follows.

: What `RH_T1_47_1_HOMOGENIZED` applies to each source code. {#tbl-rh-homog}

| source code | correction |
|---|---|
| 1, 2, 3 | the 2016 transfer, which depends on the humidity, added to every record |
| 0, 5, 6, 7 | none: the CS215 is the reference level |
| 4 | the HygroVUE10 transfer, made in vapour pressure and converted back with the homogenised `TA` of notebook `02` |

## What happened in 2016 {#what-happened-in-2016}

The probe and its acquisition system were replaced together. The logger programs of
the two eras name them directly: six CR10X programs spanning 2004-2006 all measure a
**Rotronic MP101A** on a single-ended analog channel at the same conversion, and the
CR1000 program installed at the changeover measures a **Campbell CS215** over
SDI-12. Air temperature and relative humidity arrive from that one probe in one
sensor call, which is why the same date splits both variables.

**The change moved the series, and the move is on the tower.** Three humidity series
span the changeover: the tower probe, a NABEL probe at 49 m on the same mast, and
MeteoSwiss Lägern 2.5 km away. Both comparisons that contain the tower probe step
upwards at January 2016 by roughly ten times what they move in an ordinary year, and
the comparison between the two references does not move at all.

: The change in each pairwise difference across January 2016, in percentage points
of RH, against what the same comparison does from one year to the next in an
ordinary year. {#tbl-rh-step}

| comparison | change across 2016 | ordinary year | away from saturation |
|---|---|---|---|
| tower minus NABEL 49 m | +3.32 | 0.29 | +4.14 |
| tower minus MeteoSwiss Lägern | +2.12 | 0.22 | +3.85 |
| NABEL 49 m minus MeteoSwiss Lägern | -0.35 | 0.61 | -0.24 |

**The 100 % ceiling hides part of it.** Relative humidity cannot exceed 100 %, and
this record lies mostly in humid air: the measured series has a median of 82.8 % RH,
and 11.1 % of its half-hours are at or above 99.9 %. Where both probes are already against that bound the step has nowhere to
go, so the whole-record figure understates it: on the half-hours where nothing is
near the ceiling the step is 1.2 to 1.8 times as large. Measured against the humidity
itself, it is 3.2 to 6.3 percentage points below 85 % RH and at most 1.1 above 95 %
RH.

**The probe that was replaced had drifted.** Independently of any reference, 1,931
half-hours of the analog era (0.99 % of its 195,606 measured records) read above
100 % RH, physically impossible and the
signature of a capacitive humidity element that has aged. Their share grows through
that era and reaches 3.6 % of 2015, the last full year before the replacement. The
SDI-12 era has none.

**The step is present at every hour**, and is larger at night (+4.3 % RH against
NABEL) than in daylight (+2.2 % RH). That rules out the radiation-shield mechanism
that accounts for part of the `TA` step, which acts only in sunshine.

The maintenance record adds little for this date: the January 2016 visit report
carries no device tag, and the fieldbook registers no temperature or humidity device
at the 47 m location before the HygroVUE10 of June 2026. The identification rests on
the logger programs and on the data.

### The 2016 transfer {#the-2016-transfer}

Because the step depends on the humidity, no constant removes it. The homogenised
column raises the MP101A era by a **transfer that varies with the humidity**: per
humidity bin, the difference between the eras is added to the earlier one.

**Fitted on the era means, such a transfer is not stable.** Both eras drift against
Lägern, in opposite directions and by more over their own length than the step
between them. In the 60 to 80 % RH band, over January to September of each year,
the MP101A era drifts by -0.34 percentage points of RH per year (-3.44 over
2005-2015) and the CS215 era by +0.44 per year (+3.07 over 2017-2024), 6.51 in
total against a step of 5.46 between the era means. Estimates from the first and
the second half of each era therefore differ by up to 4.93 % RH, the size of the
correction, and summer and winter by up to 4.72 % RH.

**Fitted at the break, it is.** The transfer is fitted against NABEL on tower minus
NABEL, binned on the NABEL humidity: the MP101A over 2013-2015 against the CS215 from
February 2016 to July 2018, the end of NABEL's independent record. Close to the
break the drift has had little time to act, and shorter windows change the result by
less than the year-to-year noise of each bin plus a year of drift: from 40 % RH
upwards by at most 1.27 % RH, never more than 0.95 of that bin's tolerance. Each bin's
correction is attached to the MP101A's own reading in that bin, interpolated between
bins, and the result is capped at 100 %, so a saturated MP101A record stays
saturated.

The transfer raises the MP101A era by 0 to 5.51 % RH, by 2.98 % RH on average over
its measured records. It is largest in the middle of the humidity range and close to
zero near saturation. Scored against Lägern, which entered no fit, the mean step
across the break over the humidity bins falls from +4.21 to +0.83 % RH, within a
tolerance of 1.81 % RH: Lägern's own year-to-year change (0.71) plus the drift the
fitting windows contain (1.10).

Every record before the changeover (codes `1`, `2` and `3`) receives the transfer,
reconstructed records included, because their reconstruction offsets are fitted on
the MP101A era and put them on its level.

## The May 2025 change {#the-may-2025-change}

The CS215 reports `RH` relative to its own temperature, so a probe that is too warm
in sun reads a lower `RH` for the same amount of water vapour. Whether the change of
16 May 2025 is of that kind or a change of the humidity element is decided in
**vapour pressure**, computed from each sensor's own `RH` and `TA`: a temperature
error moves `RH` and leaves vapour pressure in place.

Over the 30 days either side of the handling, against the same calendar dates of the
normal CS215 summers 2022-2024, `RH` in sun rises by +4.43 % RH against Lägern,
outside the range of the normal years (-3.07 to +1.13 % RH), while the vapour
pressure changes by +0.13 hPa, within theirs (+0.13 to +0.45 hPa), and the tower
temperature in sun falls by 1.57 °C against Lägern. Against the normal years `RH` moves by +5.17 %
RH, which at 17.9 °C corresponds to 1.06 hPa of vapour pressure; the vapour pressure
moves by -0.20 hPa, 19 % of that. The change is in the probe's temperature, not in
its humidity element.

`RH_T1_47_1_HOMOGENIZED` therefore leaves codes `6` and `7` as measured, as it leaves
code `0`. A correction of these records would be a correction of the probe
temperature, which belongs to notebook `02`. In sun, code `7` reads low and code `6`
higher than the normal CS215, in both columns: against Lägern, `RH` in sun is +0.18 %
RH under code `7` and +4.62 % RH under code `6`, where the normal CS215 summers on
the same dates give +0.18 to +3.37 and -0.20 to +3.12 % RH.

## The June 2026 probe change {#the-june-2026-probe-change}

On **5 June 2026** a Campbell HygroVUE10 (SDI-12) replaced the CS215. The swap is
dated to the half-hour by a gap in the raw 1-minute record from 11:10 to 11:31; the
half-hour 11:00 to 11:30 is removed and reconstructed (source code `5`). In vapour
pressure against Lägern the HygroVUE10 reads drier than the normal CS215, by
1.27 hPa over 12 June to 30 September, against a year-to-year scatter of 0.19 hPa
among the CS215 summers. In `RH` as measured it lies 2.3 to 4.6 % RH below the CS215
summers between 30 and 90 % RH.

The HygroVUE10 also differs from the CS215 in its radiation behaviour (it reads
cooler in sun, notebook `02`), so a transfer in % RH would mix the humidity elements
with the temperature sensors. The transfer is therefore made in **vapour pressure**:

1. Vapour pressure `e` from each sensor's own `RH` and `TA`, on two season-matched
   samples: the HygroVUE10 from 12 June to 30 September 2026, after its
   configuration change of 11 June, and the normal CS215 (code `0`) on the same
   calendar dates of 2022 to 2024.
2. The HygroVUE10-minus-CS215 difference `Delta_e` is fitted as a line in the Lägern
   vapour pressure (5,328 HygroVUE10 and 15,885 CS215 records). It runs from
   -0.90 hPa at 8 hPa to -1.66 hPa at 20 hPa. After the transfer the residual over
   all hours of the sample is -0.08 hPa, against -1.27 hPa before and a tolerance of
   0.19 hPa, and no vapour pressure bin exceeds 0.09 hPa. In a month hold-out, each
   month predicted by fits without it, the residuals are -0.17 hPa in June,
   -0.32 hPa in July, -0.01 hPa in August and +0.19 hPa in September, all within a
   tolerance of 0.37 hPa pooled over the months.
3. `RH_HOMOGENIZED = 100 * (e - Delta_e) / e_s(TA_HOMOGENIZED)`, where `e_s` is the
   saturation vapour pressure at the homogenised `TA` of notebook `02` for the same
   record, capped to `[0, 100]`.

**What the homogenised `RH` refers to.** From June 2026 it is relative to the
homogenised temperature of notebook `02`, not to the CS215's own temperature. That
temperature carries no radiative excess, so in sun the homogenised `RH` lies above
what a CS215 would read, and at night close to it: against the CS215 summers it lies
0.74 % RH higher in sun, 0.30 % RH higher at night and 0.60 % RH higher over all
hours. Per
Lägern humidity bin it lies 0.03 to 1.25 % RH higher between 30 and 90 % RH and
2.52 % RH higher above 90 %. On its records the homogenised column adds 3.92 % RH on
average, at most 8.21 % RH.

## Known limitations {#known-limitations}

- **The homogenised column removes the steps, not the drift.** Against MeteoSwiss
  Lägern the MP101A era drifts downwards by 0.34 and the CS215 era upwards by 0.44
  percentage points of RH per year, so each era travels further over its own length
  than the 2016 step (see [The 2016 transfer](#the-2016-transfer)). A trend computed from either column, or a
  comparison of years far from the break, therefore still contains sensor movement.
  The drift is not corrected: it is not attributed to either station, and after the
  NABEL sensor stops in 2018 there is no third humidity series at this site to
  attribute it with. Correcting it towards MeteoSwiss would replace the measurement
  with the reference.
- **The 2016 transfer depends on the reference.** Fitted against Lägern over the
  same windows instead of NABEL, it would raise the measured MP101A records of
  2013-2015 by +3.36 instead of +2.82 % RH on average, 0.54 % RH more, and by up to
  2.44 % RH more just below saturation (at a reading of 95 %), where NABEL finds
  almost no step and Lägern a large one. That difference is the uncertainty of the
  homogenised column across 2016, and it is largest in humid conditions. Shorter
  fitting windows give a smaller correction between 40 and 85 % RH, by 0.61 to
  0.69 % RH on average, so part of what the fitted windows attribute to the probes
  may be drift.
- **Codes `6` and `7` carry the probe's heating.** Both are temperature effects that
  remain in both value columns: in sun code `7` reads low and code `6` high against
  the normal CS215.
- **The HygroVUE10 transfer rests on one summer and one reference.** It is fitted on
  June to September 2026 against Lägern and applied as fitted to the whole
  HygroVUE10 era, including the transitional week of 5 to 11 June. Its month
  hold-out residuals follow the season, from -0.32 hPa in July to +0.19 hPa in
  September: within the summer the transfer leaves the early months slightly too
  dry and the late ones slightly too wet. Its behaviour
  outside the summer is untested, and it is to be refitted once the HygroVUE10
  record includes a winter.
- **Which probe is correct is not settled here.** The homogenised column is on the
  level of the CS215; the evidence does not establish an absolute accuracy for any
  of the probes.
- **`VPD` inherits the humidity steps.**
  [`07_METEO_VPD`](notebooks/10_METEO/30_PRODUCTS/07_METEO_VPD_2004-2025.html) has
  not yet been updated to this version of the product: it covers 2004-2025 and is
  computed from the homogenised `TA` and the measured `RH`, so its temperature term
  is put on one level and its humidity term is not. What remains there is a step of
  about 17 % of the mean VPD. VPD across 2016 or June 2026 is to be computed from the
  two homogenised columns together. See
  [Vapour pressure deficit at 47 m](Meteo_Data_VPD.html).
- **Reconstructed records are estimates, not measurements.** Code `3` carries
  approximately 3 % RH of uncertainty against a sensor-to-sensor agreement of about
  2 % RH in summer; code `4` more. January to September 2004 is reconstructed
  throughout and is the least constrained part of the record.
- **Values near 100 % are corrected, not restored.** A drifting probe loses
  resolution close to saturation. Where the analog era read above 100 % a daily offset
  was subtracted and the remainder clipped, which removes the impossible values but
  does not recover the information they stood for. Analyses of saturation frequency
  should expect the eras to differ for this reason as well as for the step.
- **The NABEL reference is not independent after July 2018.** From August 2018 the
  ingested `RH_NABEL_T1_49_1` column reproduces the tower column exactly. Nothing in
  this file is derived from those months, since the notebook cuts the reference
  there, but a user comparing this product against that NABEL column directly would be
  comparing it against itself.
- **2026 is a partial year.** The record ends on 30 September 2026, so a 2026 annual
  mean covers January to September only.
