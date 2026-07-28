# Air temperature at 47 m

Half-hourly air temperature measured at 47 m on the CH-LAE tower, 2004-2025,
complete and gap-filled. The file is `02_METEO_TA_GAPFILLED_2004-2025` (parquet
and CSV): **385,728 records** on a continuous 30-minute middle-timestamp index
(named `TIMESTAMP_MIDDLE` in the file) in local time (UTC+1, no daylight
saving), from 2004-01-01 00:15 to 2025-12-31 23:45.

The notebooks behind this page carry the full method, the evidence and the
checks:

- [`02_METEO_TA`](notebooks/10_METEO/30_PRODUCTS/02_METEO_TA_2004-2025.html) —
  builds the product: screening, gap-filling, and the 2016 correction.
- [`TA_HOMOGENIZATION_OPTIONS`](notebooks/10_METEO/30_PRODUCTS/TA_HOMOGENIZATION_OPTIONS.html)
  — the ways the 2016 break could have been corrected, and why this one was
  chosen.
- [`METEO_TA` overview](notebooks/90_DATASET_OVERVIEW/METEO_TA.html) — the
  finished product year by year, with the residual steps recomputed on each run.

::: {.callout-important title="Which column to use"}

The measured column is **not homogeneous across 21 January 2016**, when the
sensor and its acquisition system were replaced together.

- Analyses that stay inside one sensor era may use `TA_T1_47_1_gfXG`, which is
  what the instrument reported.
- Analyses that **cross 21 January 2016** — period means, trends, year
  rankings, anomalies, daily maxima, threshold-day counts — must use
  `TA_T1_47_1_HOMOGENIZED_gfXG`. The step exceeds the climate signal over this
  record.

:::

## Columns

Both value columns are complete: every one of the 385,728 records carries a
value, and the flag columns are defined everywhere. The two value columns share
the same two flags, because the correction changes values, never provenance.

: Columns of `02_METEO_TA_GAPFILLED_2004-2025`. {#tbl-ta-cols}

| column | unit | description |
|---|---|---|
| `TA_T1_47_1_gfXG` | °C | Air temperature as the instrument reported it, gaps filled. Inhomogeneous across 2016-01-21. |
| `FLAG_TA_T1_47_1_ISFILLED` | - | Whether the value was measured, and if not, which method produced it. |
| `TA_T1_47_1_HOMOGENIZED_gfXG` | °C | The same series corrected so that the two sensor eras can be compared. |
| `FLAG_TA_T1_47_1_SOURCE` | - | Which sensor generation stands behind the record. |

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

***

## What happened in 2016, and what was corrected

On 21 January 2016 the 47 m sensor and its acquisition system were replaced
together: a Rotronic MP101A, read as an analog voltage, gave way to a Campbell
CS215 read over a digital line. Two things changed at once, and
`TA_T1_47_1_HOMOGENIZED_gfXG` corrects both.

**The old chain read too cold, day and night.** It carried a constant
zero-point error of about -11 mV, which at 10 mV per °C left it reading roughly
1.1 °C below an aspirated reference on the same tower; the new sensor reads
about 0.2 °C above that reference. The gap between the two eras is
**+1.3197 °C**, and that is added to every record before the changeover.

**The two sensors warm differently in sunshine.** Both sit in passive shields,
which heat up in sun, and the newer one heats more. This part of the step
appears only in daylight, so no constant can remove it. It was measured against
NABEL — an aspirated, fan-ventilated sensor at 49 m on the same tower — and is
subtracted from the later era. It is **zero at night** and reaches **-0.59 °C**
at most.

Both corrections were established against NABEL and then checked against
MeteoSwiss Lägern, a station 2.5 km away that entered neither of them:

: The step across the sensor change, measured against MeteoSwiss. {#tbl-ta-steps}

| window | as measured | after both corrections |
|---|---|---|
| night | +1.31 °C | -0.01 °C |
| day | +1.69 °C | +0.06 °C |
| all hours | +1.51 °C | +0.03 °C |

Over the whole record the correction more than halves the apparent warming: the
difference between the 2005-2015 and 2017-2025 period means falls from +2.39 °C
to +0.91 °C, and the Theil-Sen trend over annual means from +1.76 to
+0.76 °C decade^-1^. Those figures come from the complete columns; computed from
measured records only they differ by less than 0.1 °C, and both are reported in
notebook `02`.

## Known limitations

- **A small difference in the shape of the day remains.** The shield correction
  is fitted on the three years NABEL overlaps the newer sensor and applied over
  ten, so it is an extrapolation after 2018. Measured against MeteoSwiss on
  2013-2015 against 2016-2018, the homogenised column still carries a
  daily-maximum step of +0.21 °C, a diurnal-range step of +0.18 °C and a
  daily-minimum step of +0.03 °C; over the full eras all three are smaller. The
  same statistics on the measured column step by up to +1.90 °C. **Daily maxima
  and diurnal ranges are the quantities most exposed to what remains.**
- **The record is made self-consistent, not absolutely accurate.** The later era
  is standardised onto the earlier one, so the earlier era's own warm bias in
  sunshine — about +0.4 °C at strong radiation, relative to an aspirated sensor
  — remains in both. What is removed is the *change* in that bias at the sensor
  swap, not the bias itself.
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
