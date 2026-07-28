# Air temperature at 47 m

Half-hourly air temperature measured at 47 m on the CH-LAE tower, 2004-2025,
complete and gap-filled. The file is
`02_METEO_TA_GAPFILLED_2004-2025` (parquet and CSV), written by notebook
[`02_METEO_TA`](notebooks/10_METEO/30_PRODUCTS/02_METEO_TA_2004-2025.html),
which carries the full method and the evidence behind every decision described
here.

The product holds **385,728 records** on a continuous 30-minute middle-timestamp
index (named `TIMESTAMP_MIDDLE` in the file) in local time (UTC+1, no daylight
saving), from 2004-01-01 00:15 to 2025-12-31 23:45.

::: {.callout-important title="Which column to use"}

The measured column is **not homogeneous across 21 January 2016**. On that date
the sensor and its acquisition system were replaced together, and the earlier
era reads approximately 1.3 °C too cold.

- Analyses that stay inside one sensor era may use `TA_T1_47_1_gfXG`, which is
  what the instrument reported.
- Analyses that **cross 21 January 2016** — period means, trends, year
  rankings, anomalies against a multi-year reference — must use
  `TA_T1_47_1_HOMOGENIZED_gfXG`. The step exceeds the climate signal over this
  record.

:::

## Columns

Both value columns are complete: every one of the 385,728 records carries a
value, and the flag columns are defined everywhere.

: Columns of `02_METEO_TA_GAPFILLED_2004-2025`. {#tbl-ta-cols}

| column | unit | description |
|---|---|---|
| `TA_T1_47_1_gfXG` | °C | Air temperature as the instrument reported it, gaps filled. Inhomogeneous across 2016-01-21. |
| `FLAG_TA_T1_47_1_ISFILLED` | - | Provenance of the value: measured or which method produced it. |
| `TA_T1_47_1_HOMOGENIZED_gfXG` | °C | The same series with the pre-2016 era raised by +1.3197 °C onto the level of the later era. |
| `FLAG_TA_T1_47_1_SOURCE` | - | Which sensor generation stands behind the record. |

Both value columns share the same two flag columns: homogenisation changes
values, never provenance.

### `FLAG_TA_T1_47_1_ISFILLED`

Filter on `== 0` to select measured records. The series is complete, so every
other code marks a value a model produced. Code `3` is not used.

: Fill codes and their record counts. {#tbl-ta-isfilled}

| code | meaning | records | share |
|---|---|---|---|
| 0 | observed | 369,065 | 95.7 % |
| 1 | gap-filled by XGBoost | 14,912 | 3.9 % |
| 2 | gap-filled from timestamp information only (fallback) | 43 | 0.01 % |
| 4 | linear interpolation across a short gap | 178 | 0.05 % |
| 5 | reconstructed from NABEL at 49 m on the same tower | 1,530 | 0.4 % |

Codes above `0` account for 4.3 % of the product. The code-`5` records are
almost entirely January 2004 (1,488 records), with one further record in
February 2004 and 41 in July 2012.

### `FLAG_TA_T1_47_1_SOURCE`

: Sensor-era codes, their record counts and the period each covers. {#tbl-ta-source}

| code | sensor era | period | records |
|---|---|---|---|
| 0 | Campbell CS215 on SDI-12 | 2016-01-21 14:15 to 2025-12-31 23:45 | 174,356 |
| 1 | Rotronic MP101A, single-ended analog | 2004-09-20 10:45 to 2015-12-31 23:45 | 197,739 |
| 2 | acquisition changeover, sensor era undetermined | 2016-01-01 00:15 to 2016-01-21 13:45 | 988 |
| 3 | before the tower record begins | 2004-01-01 00:15 to 2004-09-20 10:15 | 12,645 |

Codes `2` and `3` mark records that no instrument on this tower stands behind.
Select `FLAG_TA_T1_47_1_SOURCE <= 1` where provenance has to be certain.

## The 2016 acquisition break

On 21 January 2016 a Rotronic MP101A read as a single-ended analog voltage
(10 mV per °C) was replaced by a Campbell CS215 on SDI-12. The old measurement
chain carried a constant zero-point error of about -11 mV, so the pre-2016
record reads approximately 1.3 °C too cold relative to the later era.

The offset was established against two independent references: NABEL at 49 m on
the same tower, which spans the break and runs to 2018, and MeteoSwiss Lägern
2.5 km away. NABEL minus MeteoSwiss changes by only 0.06 °C across the break, so
it is the tower sensor that moved, not the references. The homogenised column
adds a constant +1.3197 °C to every record before the changeover, including the
2016 changeover interval and the reconstructed months of 2004.

The size of the effect on record-scale statistics, with 2016 excluded from both
periods because the changeover happened inside it:

: Difference between the 2005-2015 and 2017-2025 period means, and the Theil-Sen trend over annual means 2005-2025, computed both ways. {#tbl-ta-break}

| computed from | series | period difference | Theil-Sen |
|---|---|---|---|
| measured records only | as measured | +2.475 °C | +1.802 °C decade^-1^ |
| measured records only | homogenised | +1.155 °C | +0.873 °C decade^-1^ |
| the exported complete columns | as measured | +2.390 °C | +1.757 °C decade^-1^ |
| the exported complete columns | homogenised | +1.070 °C | +0.865 °C decade^-1^ |

Neither way of computing them is more correct. Measured-only figures are free of
the gap-filling model but are seasonally biased wherever a year's gaps cluster
in one season; figures from the complete columns have no sampling bias but carry
the model. The difference between the two rows of a pair measures how far the
gap-filling moves these statistics.

## Known limitations

- **The homogenisation corrects a constant offset and nothing else.** The CS215
  is passively shielded and the MP101A was less affected by the same error, so a
  constant offset cannot make the two eras identical in shape. Measured on
  2013-2015 against 2016-2018, the homogenised column still carries a residual
  daytime step of approximately +0.7 °C, a daily-amplitude step of approximately
  +0.8 °C and a monthly-mean step of approximately +0.2 °C; over the full eras
  these are roughly half as large. **Daily maxima, diurnal ranges and
  threshold-day counts such as summer days and hot days remain inhomogeneous
  across 2016 and should not be compared across it.**
- **The records reconstructed from NABEL carry too little scatter.** The 1,530
  code-`5` values come from a line fitted on NABEL, so they sit approximately
  0.05 °C from it where a real measurement sits approximately 0.25 °C from it.
  Their means are sound; variance, extremes and any statistic of spread computed
  over January 2004 are understated.
- **2004 is 72 % modelled.** The tower record begins 2004-09-20 10:45. January
  2004 is reconstructed from NABEL rather than gap-filled, because the
  MeteoSwiss reference does not begin until 1 February 2004. The year carries
  source code `3` throughout its first nine months and is the least constrained
  in the record.
- **The mechanism of the offset is inferred.** The class of error is
  established, but whether the 11 mV originated in the probe's zero trim or in a
  ground offset in the cabling is not.
