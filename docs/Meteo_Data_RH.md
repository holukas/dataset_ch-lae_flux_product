# Relative humidity at 47 m

Half-hourly relative humidity at 47 m on the CH-LAE tower, 2004 to September 2026,
complete. The file is `04_METEO_RH_CORRECTED_2004-2026.09` (parquet and CSV):
**398,832 records** on a continuous 30-minute index `TIMESTAMP_MIDDLE` (middle of the
half-hour, UTC+01:00, no daylight saving), from 2004-01-01 00:15 to 2026-09-30 23:45. 2026
is a partial year (January to September).

The [interactive dashboard](dashboards/METEO_RH_dashboard.html) summarises the product on
one page. It is still built from the 2004-2025 version of the product and ends in December 2025. That version has no homogenised column, so the dashboard shows `RH_T1_47_1` as measured.

Method, evidence and checks:

- [`04_METEO_RH`](notebooks/10_METEO/30_PRODUCTS/04_METEO_RH_2004-2026.09.html): builds
  the product: merge of the two screenings, 2012 corrections, the `RH > 100 %` correction,
  the identification of the probes and their states, the 2016 and 2026 transfers, and the
  two reconstruction passes.
- [`02_METEO_TA`](notebooks/10_METEO/30_PRODUCTS/02_METEO_TA_2004-2026.09.html): the same
  probe delivers `TA`, and the dates of every probe change and probe state are derived
  there. Notebook `04` reads its product, so `02` runs first.
- [Meteo Product Chain](Meteo_Product_Chain.html): `VPD` is computed from this product.

::: {.callout-important title="Which column to use"}

The 47 m record comes from three probes, and the second of them changed state twice
before it was replaced (see [Sensor history](#sensor-history)). The measured column steps
**up by 2.1 to 3.3 percentage points of RH** at the 21 January 2016 probe change (3.9 to 4.1
on the half-hours away from saturation). At the 5 June 2026 probe change it becomes drier,
increasingly so with the humidity.

- Inside one probe state, use `RH_T1_47_1`, which is what the probe reported.
- Across 21 January 2016 or 5 June 2026 (period means, trends, year rankings, anomalies)
  use `RH_T1_47_1_HOMOGENIZED`, which puts the other probes on the level of the CS215. It
  removes the steps at the probe changes, not the drift within each era (see
  [Known limitations](#known-limitations)).
- Where provenance has to be certain, select `FLAG_RH_T1_47_1_SOURCE` in `{0, 1, 4, 6}`.
  Codes `6` and `7` carry the probe's heating in sun in both columns; exclude code `7`
  wherever the sun-dependent part of `RH` matters.

:::

## Columns

Every record carries a value, and both flags are defined at every record and describe both
value columns.

: Columns of `04_METEO_RH_CORRECTED_2004-2026.09`. {#tbl-rh-cols}

| column | unit | description |
|---|---|---|
| `RH_T1_47_1` | % | Relative humidity, corrected and gap-free, every probe as measured. Bounded to `[0, 100]`. Not homogeneous across 2016-01-21 or 2026-06-05. |
| `FLAG_RH_T1_47_1_MISSING` | - | Whether the value was measured at 47 m, and if not, which sensor it was reconstructed from. |
| `RH_T1_47_1_HOMOGENIZED` | % | The same series on the level of the CS215. Bounded to `[0, 100]`. |
| `FLAG_RH_T1_47_1_SOURCE` | - | Which probe, and which state of it, stands behind the record. |

### `FLAG_RH_T1_47_1_MISSING`

Filter on `== 0` for measurements at 47 m. Every other code marks a value transferred
from another instrument. Nothing in this product is modelled: a reconstructed value is
another measurement of the same quantity, corrected by a monthly offset fitted within the
probe state it belongs to.

: Provenance codes, their record counts and their share of the 398,832 records. {#tbl-rh-missing}

| code | meaning | records | share |
|---|---|---|---|
| 0 | measured at 47 m | 382,181 | 95.83 % |
| 3 | reconstructed from NABEL at 49 m on the same tower | 15,729 | 3.94 % |
| 4 | reconstructed from MeteoSwiss Lägern, 2.5 km away | 922 | 0.23 % |

Codes `1` (never measured) and `2` (removed as faulty) are defined in the notebook but do
not occur: the two references cover every gap.

Code `3` carries about **3 % RH** of uncertainty, from leave-one-year-out validation
against the years both sensors measured. Code `4` is weaker, since Lägern is 2.5 km away
on the ridge at 845 m, about 100 m above the tower sensor (the tower stands at about 690 m).
It occurs almost only after the NABEL sensor ends in 2018: 877 of its 922 records fall in
2019 (759), 2023 (9), 2024 (107), 2025 (1) and 2026 (1), the last two being the two probe
half-hours. The other 45 fill short NABEL gaps in 2004 (6), 2005 (24), 2011 (10) and
2016 (5).

### `FLAG_RH_T1_47_1_SOURCE`

The codes are those of notebook `02`, and notebook `04` asserts that the two flags agree
on every record.

: Probe and probe-state codes, their record counts and the period each covers
(`TIMESTAMP_MIDDLE`). {#tbl-rh-source}

| code | probe and state | period | records |
|---|---|---|---|
| 0 | Campbell CS215 on SDI-12, normal state | 2016-01-21 14:15 to 2024-10-21 23:45 | 153,428 |
| 1 | Rotronic MP101A, single-ended analog | 2004-09-20 10:45 to 2015-12-31 23:45 | 197,739 |
| 2 | acquisition changeover, probe undetermined | 2016-01-01 00:15 to 2016-01-21 13:45 | 988 |
| 3 | before the tower record begins | 2004-01-01 00:15 to 2004-09-20 10:15 | 12,645 |
| 4 | Campbell HygroVUE10 on SDI-12 | 2026-06-05 11:45 to 2026-09-30 23:45 | 5,641 |
| 5 | probe handling or probe swap half-hour | 2025-05-16 09:45 and 2026-06-05 11:15 | 2 |
| 6 | Campbell CS215 after the handling of 16 May 2025, reads high in sun | 2025-05-16 10:15 to 2026-06-05 10:45 | 18,482 |
| 7 | Campbell CS215 with excess daytime heating, reads low in sun | 2024-10-22 00:15 to 2025-05-16 09:15 | 9,907 |

No probe at this height stands behind codes `2`, `3` and `5`. During the changeover (code
`2`) the tower recorded nothing for 20 days, and those records are reconstructed from
NABEL. The two code-`5` half-hours are removed and reconstructed from Lägern with the offset
of the state before each. To stay inside one probe state, select a single code.

## Coverage

The tower measurement begins on **2004-09-20 10:45**. Everything before that is
reconstructed from NABEL.

: Years in which measured coverage is not near-complete. Every other year of 2005-2025 is
at least 99 % measured, and 2026 (January to September) is 100 % measured. {#tbl-rh-coverage}

| year | measured | why |
|---|---|---|
| 2004 | 28.0 % | the record begins on 20 September |
| 2009 | 97.2 % | scattered outages |
| 2012 | 92.8 % | logger clock error, power-supply failure and storm damage |
| 2016 | 94.3 % | the January outage during which the probe and logger were replaced |
| 2019 | 95.7 % | an outage after the NABEL reference ends, filled from MeteoSwiss |

In 2012 a logger clock error shifted one block of August by 15.5 hours, and a tower
power-supply failure in late July and August and storm damage in late October and November
left records that could not be repaired. The clock error was corrected, the other two
periods were removed, and all of it was reconstructed from NABEL.

## Sensor history {#sensor-history}

`TA_T1_47_1` and `RH_T1_47_1` arrive from one probe in one sensor call, so every date below
is the same as in notebook `02`, where most of them are derived. The field name and its
database tags did not change at any of them.

- **Rotronic MP101A, to 31 December 2015 (code `1`).** Six CR10X programs of 2004-2006 name
  it and its analog conversion.
- **Campbell CS215, from 21 January 2016 (code `0`).** Named by the CR1000 program
  installed at the changeover, read over SDI-12.
- **The CS215 with excess daytime heating, 22 October 2024 to 16 May 2025 (code `7`).**
  Dated in notebook `02` from the daytime excess of the 47 m temperature over the 35 m
  sensor of the same tower, which grows in the weeks after intake tubing was attached at
  the 47 m sonic anemometer on 19 September 2024.
- **The CS215 after 16 May 2025 (code `6`).** The probe was handled during a site visit
  that day; the fieldbook records the heating connection of the tower inlet found melted
  and disconnected. See [The May 2025 change](#the-may-2025-change).
- **Campbell HygroVUE10, from 5 June 2026 (code `4`).** The fieldbook adds it at this
  location that day. See [The June 2026 probe change](#the-june-2026-probe-change).

The fieldbook registers no temperature or humidity device at the 47 m location before the
HygroVUE10, so the 2016 identification rests on the logger programs and on the data.

: What `RH_T1_47_1_HOMOGENIZED` applies to each source code. {#tbl-rh-homog}

| source code | correction |
|---|---|
| 1, 2, 3 | the 2016 transfer, which depends on the humidity, added to every record; then the saturation ceiling above 90 % RH |
| 0, 5, 6, 7 | none: the CS215 is the reference level |
| 4 | the HygroVUE10 transfer, made in vapour pressure and converted back with the homogenised `TA` of notebook `02` |

## What happened in 2016 {#what-happened-in-2016}

The probe and its acquisition system were replaced together: a **Rotronic MP101A** on a
single-ended analog channel gave way to a **Campbell CS215** over SDI-12. Air temperature
and relative humidity come from that one probe, so the same date splits both variables.

**The step is on the tower.** Three humidity series span the changeover: the tower probe,
a NABEL probe at 49 m on the same mast, and MeteoSwiss Lägern. Both comparisons that
contain the tower probe step up at January 2016 by about ten times their ordinary
year-to-year change, and the comparison between the two references does not move.

: The change in each pairwise difference across January 2016, in percentage points of RH,
against the change of the same comparison between two ordinary years. {#tbl-rh-step}

| comparison | change across 2016 | ordinary year | away from saturation |
|---|---|---|---|
| tower minus NABEL 49 m | +3.32 | 0.29 | +4.14 |
| tower minus MeteoSwiss Lägern | +2.12 | 0.22 | +3.85 |
| NABEL 49 m minus MeteoSwiss Lägern | -0.35 | 0.61 | -0.24 |

**The 100 % ceiling hides part of the step.** The measured series has a median of
82.8 % RH, and 11.1 % of its half-hours are at or above 99.9 %. Where both probes are at
that bound the step cannot show, so the whole-record figure understates it: away from the
ceiling the step is 1.2 to 1.8 times as large. Below 85 % RH it is 3.2 to 6.3 percentage
points, above 95 % RH at most 1.1.

**The replaced probe had drifted.** 1,931 half-hours of the analog era (0.99 % of its
195,606 measured records) read above 100 % RH, the typical sign of an aged capacitive
humidity element. Their share grows through that era to 3.6 % of 2015. The SDI-12 era has
none.

**The step is present at every hour**, and is larger at night (+4.3 % RH against NABEL)
than in daylight (+2.2 % RH). The radiation-shield difference that explains part of the
`TA` step acts only in sunshine, so it does not explain this one.

### The 2016 transfer {#the-2016-transfer}

Because the step depends on the humidity, a constant cannot remove it. The homogenised
column raises the MP101A era by a **transfer that varies with the humidity**: per humidity
bin, the difference between the eras is added to the earlier one.

**Fitted on the era means, such a transfer is not stable.** Both eras drift against
Lägern, in opposite directions and by more over their own length than the step between
them. In the 60 to 80 % RH band, over January to September of each year, the MP101A era
drifts by -0.34 percentage points of RH per year (-3.44 over 2005-2015) and the CS215 era
by +0.44 per year (+3.07 over 2017-2024): 6.51 in total, against a step of 5.46 between the
era means. Estimates from the first and second half of each era differ by up to 4.93 % RH,
the size of the correction, and summer and winter by up to 4.72 % RH.

**Fitted at the break, it is stable.** The transfer is fitted on tower minus NABEL, binned
on the NABEL humidity: the MP101A over 2013-2015 against the CS215 from February 2016 to
July 2018, the end of NABEL's independent record. Close to the break the drift has had
little time to act. Shorter windows change the result by less than the year-to-year noise
of each bin plus a year of drift: from 40 % RH upwards by at most 1.27 % RH, never more than
0.95 of that bin's tolerance. Each bin's correction is attached to the MP101A's own reading
in that bin, interpolated between bins, and the result is capped at 100 %, so a saturated
MP101A record stays saturated.

The transfer raises the MP101A era by 0 to 5.51 % RH, most in the middle of the humidity
range and close to zero near saturation. Together with the
[saturation ceiling](#the-saturation-ceiling), the homogenised column adds 3.10 % RH on
average to the measured MP101A records. Scored against Lägern, which entered no fit, the mean step across the break
falls from +4.21 to +0.83 % RH, within a tolerance of 1.81 % RH (Lägern's own year-to-year
change, 0.71, plus the drift contained in the fitting windows, 1.10). Every record before
the changeover (codes `1`, `2` and `3`) receives the transfer, reconstructed records
included, because their reconstruction offsets put them on the MP101A level.

### The saturation ceiling {#the-saturation-ceiling}

In saturated air (Lägern at 99 % RH or more) the normal CS215 reads 100 %, the MP101A only
99.1 to 100 % depending on the year, also after the 2016 transfer, which is close to zero at
the top of the range. Without a correction, `VPD` from the homogenised column would reach
zero far less often before 2016 than after. The homogenised column therefore maps each
MP101A year's median reading in saturated air onto 100 % and scales the readings between
90 % RH and that ceiling linearly; readings below 90 % RH are unchanged. Lägern only marks
the saturated half-hours, it does not set the level. The change is at most 0.9 % RH. Just
below saturation the CS215 still reads wetter than the MP101A, by about 2 % RH at a Lägern
humidity of 90 to 95 %; that is the reference dependence of the 2016 transfer and is not
corrected.

## The May 2025 change {#the-may-2025-change}

The CS215 reports `RH` relative to its own temperature, so a probe that is too warm in sun
reads a lower `RH` for the same amount of water vapour. Whether the change of 16 May 2025
is of that kind or a change of the humidity element is decided in **vapour pressure**,
computed from each sensor's own `RH` and `TA`: a temperature error moves `RH` and leaves
vapour pressure unchanged.

Over the 30 days either side of the handling, against the same calendar dates of the
normal CS215 summers 2022-2024, `RH` in sun rises by +4.43 % RH against Lägern, outside the
range of the normal years (-3.07 to +1.13 % RH). The vapour pressure changes by +0.13 hPa,
within theirs (+0.13 to +0.45 hPa), and the tower temperature in sun falls by 1.57 °C
against Lägern. Against the normal years `RH` moves by +5.17 % RH, which at 17.9 °C
corresponds to 1.06 hPa; the vapour pressure moves by -0.20 hPa, 19 % of that. The change
is in the probe's temperature, not in its humidity element.

`RH_T1_47_1_HOMOGENIZED` therefore leaves codes `6` and `7` as measured, like code `0`. A
correction of these records would be a correction of the probe temperature, which is the
task of notebook `02`. Against Lägern, `RH` in sun is +0.18 % RH under code `7` and
+4.62 % RH under code `6`, where the normal CS215 summers on the same dates give +0.18 to
+3.37 and -0.20 to +3.12 % RH.

## The June 2026 probe change {#the-june-2026-probe-change}

On **5 June 2026** a Campbell HygroVUE10 (SDI-12) replaced the CS215. A gap in the raw
1-minute record from 11:10 to 11:31 dates the swap; the half-hour 11:00 to 11:30 is removed
and reconstructed (source code `5`). In vapour pressure against Lägern the HygroVUE10
reads drier than the normal CS215, by 1.27 hPa over 12 June to 30 September, against a
year-to-year scatter of 0.19 hPa among the CS215 summers. In `RH` as measured it lies 2.3
to 4.6 % RH below the CS215 summers between 30 and 90 % RH.

The HygroVUE10 also reads cooler than the CS215 in sun (notebook `02`), so a transfer in
% RH would mix the humidity elements with the temperature sensors. The transfer is
therefore made in **vapour pressure**:

1. Vapour pressure `e` is computed from each sensor's own `RH` and `TA`, on two
   season-matched samples: the HygroVUE10 from 12 June to 30 September 2026, after its
   configuration change of 11 June, and the normal CS215 (code `0`) on the same calendar
   dates of 2022 to 2024.
2. The HygroVUE10-minus-CS215 difference `Delta_e` is fitted as a line in the Lägern
   vapour pressure (5,328 HygroVUE10 and 15,885 CS215 records). It runs from -0.90 hPa at
   8 hPa to -1.66 hPa at 20 hPa. After the transfer the residual over all hours of the
   sample is -0.08 hPa, against -1.27 hPa before and a tolerance of 0.19 hPa, and no vapour
   pressure bin exceeds 0.09 hPa. In a month hold-out (each month predicted by fits without
   it) the residuals are -0.17 hPa in June, -0.32 hPa in July, -0.01 hPa in August and
   +0.19 hPa in September, all within a tolerance of 0.37 hPa pooled over the months.
3. `RH_HOMOGENIZED = 100 * (e - Delta_e) / e_s(TA_HOMOGENIZED)`, where `e_s` is the
   saturation vapour pressure at the homogenised `TA` of notebook `02` for the same record,
   capped to `[0, 100]`.

**From June 2026 the homogenised `RH` refers to the homogenised temperature of notebook
`02`**, not to the probe's own temperature. That temperature carries no radiative excess,
so in sun the homogenised `RH` lies above what a CS215 would read, and at night close to
it. Against the CS215 summers it lies 0.74 % RH higher in sun, 0.30 % RH higher at night
and 0.60 % RH higher over all hours; per Lägern humidity bin, 0.03 to 1.25 % RH higher
between 30 and 90 % RH and 2.52 % RH higher above 90 %. On the HygroVUE10 records the
homogenised column adds 3.92 % RH on average, at most 8.21 % RH.

## Known limitations {#known-limitations}

- **The homogenised column removes the steps, not the drift.** Against MeteoSwiss Lägern
  the MP101A era drifts down by 0.34 and the CS215 era up by 0.44 percentage points of RH
  per year, so each era moves further over its own length than the 2016 step (see
  [The 2016 transfer](#the-2016-transfer)). A trend from either column, or a comparison of
  years far from the break, still contains sensor movement. The drift is not corrected: it
  cannot be attributed to either station, and after the NABEL sensor stops in 2018 there is
  no third humidity series at the site to attribute it with. Correcting it towards
  MeteoSwiss would replace the measurement with the reference.
- **The 2016 transfer depends on the reference.** Fitted against Lägern over the same
  windows instead of NABEL, it would raise the measured MP101A records of 2013-2015 by
  +3.36 instead of +2.82 % RH on average, 0.54 % RH more, and by up to 2.44 % RH more just
  below saturation (at a reading of 95 %), where NABEL finds almost no step and Lägern a
  large one. That difference is the uncertainty of the homogenised column across 2016, and
  it is largest in humid conditions. Shorter fitting windows give a correction smaller by
  0.61 to 0.69 % RH on average between 40 and 85 % RH, so part of what the fitting windows
  attribute to the probes may be drift.
- **Codes `6` and `7` carry the probe's heating** in both value columns: in sun code `7`
  reads low and code `6` high against the normal CS215.
- **The HygroVUE10 transfer rests on one summer and one reference.** It is fitted on June
  to September 2026 against Lägern and applied to the whole HygroVUE10 era, including the
  transitional week of 5 to 11 June. Its month hold-out residuals follow the season, from
  -0.32 hPa in July to +0.19 hPa in September, so the transfer leaves the early summer
  months slightly too dry and the late ones slightly too wet. Its behaviour outside the
  summer is untested, and it is to be refitted once the HygroVUE10 record includes a winter.
- **Which probe is correct is not settled.** The homogenised column is on the level of the
  CS215; the evidence does not establish an absolute accuracy for any of the probes.
- **`VPD` inherits these properties.** Notebook `07` computes `VPD_T1_47_1` from the
  measured `TA` and `RH` and `VPD_T1_47_1_HOMOGENIZED` from the two homogenised columns.
  Use the homogenised `VPD` across 2016 or June 2026. See
  [Vapour pressure deficit at 47 m](Meteo_Data_VPD.html).
- **Reconstructed records are estimates, not measurements.** Code `3` carries about
  3 % RH of uncertainty, against a sensor-to-sensor agreement of about 2 % RH in summer;
  code `4` more. January to September 2004 is reconstructed throughout and is the least
  constrained part of the record.
- **Values near 100 % are corrected, not restored.** A drifting probe loses resolution
  close to saturation. Where the analog era read above 100 %, a daily offset was subtracted
  and the remainder clipped, which removes the impossible values but does not recover the
  information they stood for. Saturation frequency differs between the eras for this
  reason as well as because of the step. The saturation ceiling of the homogenised column
  narrows the difference without removing it: with Lägern at 99 % RH or more, the
  homogenised MP101A reads 99.5 % or more on 69 % of the half-hours, the CS215 on 81 %
  (measured records, 2008 to October 2024).
- **The NABEL reference is not independent after July 2018.** From August 2018 the ingested
  `RH_NABEL_T1_49_1` column reproduces the tower column exactly. Nothing in this file is
  derived from those months, but a comparison of this product with that NABEL column over
  them compares the product with itself.
- **2026 is a partial year.** A 2026 annual mean covers January to September only.
