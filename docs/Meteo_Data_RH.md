# Relative humidity at 47 m

Half-hourly relative humidity at 47 m on the CH-LAE tower, 2004-2025, complete. The
file is `04_METEO_RH_CORRECTED_2004-2025` (parquet and CSV): **385,728 records** on
a continuous 30-minute middle-timestamp index (named `TIMESTAMP_MIDDLE` in the file)
in local time (UTC+1, no daylight saving), from 2004-01-01 00:15 to
2025-12-31 23:45.

The [**interactive dashboard**](dashboards/METEO_RH_dashboard.html) summarises the
product on one page: coverage and provenance, seasonality, distributions, extremes
and trends, with a table view behind every chart. It is standalone and works
offline.

Method, evidence and checks:

- [`04_METEO_RH`](notebooks/10_METEO/30_PRODUCTS/04_METEO_RH_2004-2025.html) — builds
  the product: the merge of the two screenings, the 2012 corrections, the
  `RH > 100 %` correction, the identification of the two probe generations and the
  step between them, and the two reconstruction passes.
- [`02_METEO_TA`](notebooks/10_METEO/30_PRODUCTS/02_METEO_TA_2004-2025.html) — the
  same probe delivers `TA`, and the January 2016 replacement moved that variable too.
  What was done about it there is the closest available model for what a homogenised
  `RH` would require.
- [`Meteo_Product_Chain`](Meteo_Product_Chain.html) — where this product sits in the
  chain. `VPD` is computed from it.

::: {.callout-important title="Not homogeneous across 21 January 2016"}

The 47 m probe was replaced on **21 January 2016**, together with the logger that
read it: a Rotronic MP101A read as an analog voltage gave way to a Campbell CS215
read over a digital line. The exported series steps **upwards by 2.1 to
3.3 percentage points of RH** at that date, and by **3.9 to 4.1** on the half-hours
away from saturation. The earlier era reads too dry.

**There is no homogenised column.** The step is not one number: it is 3 to 6
percentage points over the drier half of the range and close to nothing near 100 %
RH, so no constant correction reaches both ends. A correction that varies with the
humidity was built, tested and rejected, because both eras drift internally by more
than the step between them and no fixed transfer is right for any particular year.
Anything crossing that date must be restricted to one probe generation using
`FLAG_RH_T1_47_1_SOURCE`, or must carry the step as an uncertainty.

Comparisons within one era are unaffected. See
[What happened in 2016](#what-happened-in-2016).

:::

## Columns

Every one of the 385,728 records carries a value, and both flags are defined
everywhere.

: Columns of `04_METEO_RH_CORRECTED_2004-2025`. {#tbl-rh-cols}

| column | unit | description |
|---|---|---|
| `RH_T1_47_1` | % | Relative humidity, corrected and gap-free. Bounded to `[0, 100]`. Not homogeneous across 2016-01-21. |
| `FLAG_RH_T1_47_1_MISSING` | - | Whether the value was measured at 47 m, and if not, which sensor it was reconstructed from. |
| `FLAG_RH_T1_47_1_SOURCE` | - | Which probe generation stands behind the record. |

### `FLAG_RH_T1_47_1_MISSING`

Filter on `== 0` for genuine 47 m measurements. The series is complete, so every
other code marks a value transferred from another instrument. Nothing in this
product is modelled: a reconstructed value is another measurement of the same
quantity, corrected by a monthly offset.

: Provenance codes and their record counts. {#tbl-rh-missing}

| code | meaning | records | share |
|---|---|---|---|
| 0 | measured at 47 m | 369,079 | 95.7 % |
| 3 | reconstructed from NABEL at 49 m on the same tower | 15,729 | 4.1 % |
| 4 | reconstructed from MeteoSwiss Lägern, 2.5 km away | 920 | 0.2 % |

Codes `1` (never measured) and `2` (removed as faulty) are defined in the notebook
but do not occur in this file: the two references between them cover every gap.

Code `3` carries approximately **3 % RH** of uncertainty, established by
leave-one-year-out validation against the years both sensors measured. Code `4` is
weaker still, since Lägern is 2.5 km away and 400 m lower, and is concentrated in
2019 (759 records) and 2024 (107 records), after the NABEL sensor ends.

### `FLAG_RH_T1_47_1_SOURCE`

: Probe generations, their record counts and the period each covers. {#tbl-rh-source}

| code | probe and acquisition | period | records |
|---|---|---|---|
| 0 | Campbell CS215 on SDI-12 | 2016-01-21 14:15 to 2025-12-31 23:45 | 174,356 |
| 1 | Rotronic MP101A, single-ended analog | 2004-09-20 10:45 to 2015-12-31 23:45 | 197,739 |
| 2 | acquisition changeover, probe generation undetermined | 2016-01-01 00:15 to 2016-01-21 13:45 | 988 |
| 3 | before the tower record begins | 2004-01-01 00:15 to 2004-09-20 10:15 | 12,645 |

Codes `2` and `3` mark records that no probe at this height stands behind. Code `2`
is the changeover outage: the tower recorded nothing for 20 days while the logger
was rebuilt, and those records are reconstructed from NABEL. Select
`FLAG_RH_T1_47_1_SOURCE <= 1` where the probe generation has to be certain, and
`== 0` or `== 1` to stay inside one of them.

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
| tower − NABEL 49 m | +3.32 | 0.29 | +4.14 |
| tower − MeteoSwiss Lägern | +2.12 | 0.22 | +3.85 |
| NABEL 49 m − MeteoSwiss Lägern | −0.35 | 0.61 | −0.24 |

**The 100 % ceiling hides part of it.** Relative humidity cannot exceed 100 %, and
this record sits at a median of 82.9 % RH with a large share of half-hours at
saturation. Where both probes are already against that bound the step has nowhere to
go, so the whole-record figure understates it: on the half-hours where nothing is
near the ceiling the step is 1.2 to 1.8 times as large. Measured against the humidity
itself, it is 3.2 to 6.3 percentage points below 85 % RH and at most 1.1 above 95 %
RH.

**The probe that was replaced had drifted.** Independently of any reference, 1,931
half-hours of the analog era read above 100 % RH, physically impossible and the
signature of a capacitive humidity element that has aged. Their share grows through
that era and reaches 3.6 % of 2015, the last full year before the replacement. The
SDI-12 era has none.

**The step is present at every hour**, and is larger at night (+4.3 % RH against
NABEL) than in daylight (+2.2 % RH). That rules out the radiation-shield mechanism
that accounts for part of the `TA` step, which acts only in sunshine.

The maintenance record adds little: GIN files no device at the 47 m T/RH location
for the whole of the exported period, the January 2016 visit report carries no device
tag, and the CS215 is named at this logger only in a wiring repair six years later.
The identification rests on the logger programs and on the data.

## Known limitations

- **The record is not homogeneous, and cannot be made so with a constant.** Any
  statistic crossing 21 January 2016 (period means, trends, year rankings, anomalies,
  threshold-hour counts) contains a step of 2 to 4 percentage points of RH. Because
  the step depends on the humidity itself and vanishes at saturation, no single
  offset removes it, and none is applied. The level-dependent transfer such a column
  would need was built and measured, and it does not hold: re-estimated from either
  half of its own eras it changes by as much as the correction itself, and summer and
  winter disagree by about as much again. Applying it would also push 19 % of
  early-era records past 100 %.
- **Both eras drift internally, by more than the step between them.** Against
  MeteoSwiss Lägern the earlier era moves approximately −0.31 percentage points of RH
  per year and the later era approximately +0.50, so each era travels further over
  its own length than the 2016 jump. A trend computed entirely inside one era
  therefore still contains sensor movement. The drift is not corrected: it is not
  attributed to either station, and after the NABEL sensor stops in 2018 there is no
  third humidity series at this site to attribute it with. Correcting it towards
  MeteoSwiss would replace the measurement with the reference.
- **Which era is correct is not settled here.** The evidence shows that the earlier
  probe drifted and that the later one reads moister; it does not establish an
  absolute accuracy for either. The product is the measurement with the probe
  generation named beside it.
- **`VPD` inherits this step, and it is the dominant term in it.**
  [`07_METEO_VPD`](notebooks/10_METEO/30_PRODUCTS/07_METEO_VPD_2004-2025.html) is
  computed from the homogenised `TA` and from this series, so its temperature term is
  put on one level and its humidity term cannot be. What remains is a step of about
  17 % of the mean VPD. The `RH` step is largest in the drier half of the range,
  which is where VPD is largest. See
  [Vapour pressure deficit at 47 m](Meteo_Data_VPD.html).
- **Reconstructed records are estimates, not measurements.** Code `3` carries
  approximately 3 % RH of uncertainty against a sensor-to-sensor agreement of about
  2 % RH in summer; code `4` more. January to September 2004 is reconstructed
  throughout and is the least constrained part of the record.
- **Values near 100 % are corrected, not restored.** A drifting probe loses
  resolution close to saturation. Where the analog era read above 100 % a daily offset
  was subtracted and the remainder clipped, which removes the impossible values but
  does not recover the information they stood for. Analyses of saturation frequency
  should expect the two eras to differ for this reason as well as for the step.
- **The NABEL reference is not independent after July 2018.** From August 2018 the
  ingested `RH_NABEL_T1_49_1` column reproduces the tower column exactly. Nothing in
  this file is derived from those months, since the notebook cuts the reference
  there, but a user comparing this product against that NABEL column directly would be
  comparing it against itself.
