# Air temperature at 47 m

Half-hourly air temperature at 47 m on the CH-LAE tower, 2004 to September 2026,
gap-filled to completeness. The file is `02_METEO_TA_GAPFILLED_2004-2026.09`
(parquet and CSV): **398,832 records** on a continuous 30-minute middle-timestamp
index (named `TIMESTAMP_MIDDLE` in the file) in local time (UTC+1, no daylight
saving), from 2004-01-01 00:15 to 2026-09-30 23:45. 2026 is a partial year
(January to September).

The [**interactive dashboard**](dashboards/METEO_TA_dashboard.html) summarises the
product on one page: coverage and provenance, seasonality, distributions, extremes
and trends, with a table view behind every chart. It is standalone and works
offline.

Method, evidence and checks:

- [`02_METEO_TA`](notebooks/10_METEO/30_PRODUCTS/02_METEO_TA_2004-2026.09.html):
  builds the product: screening, gap-filling, the 2016 correction, and the
  treatment of the May 2025 change and the June 2026 probe change.
- [`TA_HOMOGENIZATION_OPTIONS`](notebooks/10_METEO/30_PRODUCTS/TA_HOMOGENIZATION_OPTIONS.html):
  the candidate corrections for the 2016 break, and why this one was chosen.
- [`METEO_TA` overview](notebooks/90_OVERVIEW/METEO_TA.html): the finished
  product year by year, with the residual steps recomputed on each run.

::: {.callout-important title="Which column to use"}

The measured column is **not homogeneous**. The 47 m record comes from three
instruments, and the second of them changed state twice before it was replaced
(see [Sensor history](#sensor-history)).

- Inside one sensor state, use `TA_T1_47_1_gfXG`, which is what the instrument
  reported.
- Across 21 January 2016, 16 May 2025 or 5 June 2026 (period means, trends, year
  rankings, anomalies, daily maxima, threshold-day counts) use
  `TA_T1_47_1_HOMOGENIZED_gfXG`. The 2016 step alone exceeds the climate signal
  over this record.
- Where provenance has to be certain, select `FLAG_TA_T1_47_1_SOURCE` in
  `{0, 1, 4, 6}`. Exclude code `7` from daytime statistics (daily maxima, diurnal
  ranges): it remains too warm in sun after homogenisation.

:::

## Columns

Both value columns are complete and both flags are defined at every record. The
two value columns share the same flags, since the correction changes values, not
provenance.

: Columns of `02_METEO_TA_GAPFILLED_2004-2026.09`. {#tbl-ta-cols}

| column | unit | description |
|---|---|---|
| `TA_T1_47_1_gfXG` | °C | Air temperature as the instrument reported it, gaps filled. Inhomogeneous across 2016-01-21, 2025-05-16 and 2026-06-05. |
| `FLAG_TA_T1_47_1_ISFILLED` | - | Whether the value was measured, and if not, which method produced it. |
| `TA_T1_47_1_HOMOGENIZED_gfXG` | °C | The same series corrected so that the sensor eras can be compared. |
| `FLAG_TA_T1_47_1_SOURCE` | - | Which sensor, and which state of it, stands behind the record. |

### `FLAG_TA_T1_47_1_ISFILLED`

Filter on `== 0` for measured records. The series is complete, so every other code
marks a modelled value. Code `3` is not used.

: Fill codes and their record counts. {#tbl-ta-isfilled}

| code | meaning | records | share |
|---|---|---|---|
| 0 | observed | 382,167 | 95.82 % |
| 1 | gap-filled by XGBoost | 14,914 | 3.74 % |
| 2 | gap-filled from timestamp information only (fallback) | 43 | 0.01 % |
| 4 | linear interpolation across a short gap (up to 1 h) | 178 | 0.04 % |
| 5 | reconstructed from NABEL at 49 m on the same tower | 1,530 | 0.38 % |

Codes above `0` account for 4.18 % of the product. Gap-filling is split into five periods, at each sensor change and at the end of
the NABEL record in 2018, so that no model is trained across a change of sensor.
The 1,530 code-`5` records are almost all January 2004 (1,488 records), plus one
in February 2004 and 41 in July 2012.

### `FLAG_TA_T1_47_1_SOURCE`

: Sensor and sensor-state codes, their record counts and the period each covers
(`TIMESTAMP_MIDDLE`). {#tbl-ta-source}

| code | sensor and state | period | records |
|---|---|---|---|
| 0 | Campbell CS215 on SDI-12, normal state | 2016-01-21 14:15 to 2024-10-21 23:45 | 153,428 |
| 1 | Rotronic MP101A, single-ended analog | 2004-09-20 10:45 to 2015-12-31 23:45 | 197,739 |
| 2 | acquisition changeover, sensor era undetermined | 2016-01-01 00:15 to 2016-01-21 13:45 | 988 |
| 3 | before the tower record begins | 2004-01-01 00:15 to 2004-09-20 10:15 | 12,645 |
| 4 | Campbell HygroVUE10 on SDI-12 | 2026-06-05 11:45 to 2026-09-30 23:45 | 5,641 |
| 5 | probe handling or probe swap half-hour | 2025-05-16 09:45 and 2026-06-05 11:15 | 2 |
| 6 | Campbell CS215 after the handling of 16 May 2025 | 2025-05-16 10:15 to 2026-06-05 10:45 | 18,482 |
| 7 | Campbell CS215 with excess daytime heating | 2024-10-22 00:15 to 2025-05-16 09:15 | 9,907 |

Codes `2`, `3` and `5` mark records that no instrument on this tower stands
behind; the measured value of the two code-`5` half-hours is removed and modelled.
Select `FLAG_TA_T1_47_1_SOURCE` in `{0, 1, 4, 6}` where provenance has to be
certain, and a single code to stay inside one sensor state.

***

## Sensor history {#sensor-history}

The field name `TA_T1_47_1` and its database tags did not change at any of the
following dates.

- **Rotronic MP101A, to 31 December 2015 (code `1`).** Read as a single-ended analog
  voltage by a CR10X logger. The logger programs name the sensor and its
  conversion.
- **Campbell CS215, from 21 January 2016 (code `0`).** Read over SDI-12 by the CR1000
  logger installed at the changeover, whose program names the sensor. The 20 days
  between the two are an outage (code `2`).
- **The same CS215 with excess daytime heating, 22 October 2024 to 16 May 2025
  (code `7`).** On 19 September 2024 the fieldbook records intake tubing from the
  tower attached at the 47 m sonic anemometer. In the following weeks the daytime
  excess of the 47 m probe over the 35 m profile sensor of the same tower grows
  beyond any value it reaches earlier; a rule on that excess dates the onset.
- **The same CS215 after 16 May 2025 (code `6`).** On that day the probe was
  handled during a site visit, and the daytime excess disappears. See
  [The May 2025 change](#the-may-2025-change).
- **Campbell HygroVUE10, from 5 June 2026 (code `4`).** It replaced the CS215. See
  [The June 2026 probe change](#the-june-2026-probe-change).

The homogenised column treats each state as follows.

: What `TA_T1_47_1_HOMOGENIZED_gfXG` applies to each source code. {#tbl-ta-homog}

| source code | correction |
|---|---|
| 1, 2, 3 | the constant of the 2016 change, +1.3197 °C, added to every record |
| 0, 7 | the shield term of the CS215, subtracted: zero at night, at most 0.59 °C |
| 6 | a constant night term, +0.058 °C, subtracted at all hours; no shield term |
| 4 | the HygroVUE10 transfer onto the normal CS215, then the shield term of the CS215 |
| 5 | as the period the half-hour belongs to (the handling record as code `7`, the swap record as code `6`) |

## The 2016 sensor change

On 21 January 2016 a Rotronic MP101A, read as an analog voltage, was replaced by a
Campbell CS215 read over a digital line, together with the logger that read it.
Two things changed at once, and `TA_T1_47_1_HOMOGENIZED_gfXG` corrects both.

**The old chain read too cold, day and night.** It carried a constant zero-point
error of about -11 mV, which at 10 mV per °C left it reading roughly 1.1 °C below
an aspirated reference on the same tower; the new sensor reads about 0.2 °C above
that reference. The gap between the two eras is **+1.3197 °C**, added to every
record before the changeover.

**The two sensors warm differently in sunshine.** Both sit in passive shields,
which heat up in sun, and the newer one heats more. This part of the step appears
only in daylight, so no constant can remove it. It was measured against NABEL, an
aspirated fan-ventilated sensor at 49 m on the same tower, and subtracted from the
later era. It is **zero at night** and reaches **-0.59 °C** at most.

Both corrections were fitted against NABEL and then scored against MeteoSwiss
Lägern, a station 2.5 km away that entered neither of them:

: The step across the sensor change, measured against MeteoSwiss, 2013-2015
against 2017-2019. {#tbl-ta-steps}

| window | as measured | after both corrections |
|---|---|---|
| night | +1.31 °C | -0.01 °C |
| day | +1.69 °C | +0.06 °C |
| all hours | +1.51 °C | +0.03 °C |

The correction raises the earlier era by the constant and lowers the sunlit records
of the later eras by the shield term (by 0.15 °C on average over the 2017-2025
annual means of measured records), so over the whole record it more than halves the
apparent warming. From the complete columns, the difference between the 2005-2015
and 2017-2025 period means falls from +2.39 °C to +0.92 °C, and the Theil-Sen trend
over annual means from +1.76 to +0.77 °C decade^-1^. Computed from measured records
only, the same figures are +2.47 °C and +1.00 °C, and +1.80 and +0.77 °C decade^-1^:
the two ways differ by 0.08 °C in the period difference and by at most
0.04 °C decade^-1^ in the trend. Notebook `02` reports both.

## The May 2025 change {#the-may-2025-change}

On **16 May 2025** the raw 1-minute record of the 47 m probe jumps by about 5 °C
within ten minutes, between 09:32 and 09:42, while the 35 m sensor of the same
tower does not change: the probe was handled. The fieldbook records a site visit on
that day, with the heating connection of the tower inlet found melted and
disconnected. The half-hour 09:30 to 10:00 is removed and modelled (source code
`5`).

The change is attributed to the 47 m probe with two pairs: the 47 m probe against
the 35 m sensor, and the 35 m sensor against MeteoSwiss Lägern. The second pair
contains no 47 m measurement and changes at the handling by an ordinary amount
(-0.36 °C above 500 W m^-2^, 14 days after against 14 days before); the first changes
in sun by -1.11 °C, more than at any other day of the half-year around it.

- **Code `7`**, the heated state from 22 October 2024, receives the shield term of
  the normal CS215 and nothing more. In strong sun it remains too warm by up to
  0.92 °C after homogenisation.
- **Code `6`**, from 16 May 2025, no longer carries the daytime excess of the normal
  CS215 and receives no shield term. Its night level is compared with the normal
  CS215 of 2022-2024 against Lägern, matched month by month over March to
  September, and the difference is removed as a constant. That constant is
  +0.058 °C, smaller than its uncertainty of 0.22 °C (the year-to-year scatter of
  the same quantity among the reference years). After the correction, code `6` lies
  within 0.13 °C of the normal CS215 at night and in every radiation class. In a
  month hold-out, each month corrected with the term derived from the others
  departs from the normal CS215 by at most 0.215 °C, against up to 0.57 °C between
  one reference year and the others in the same month.

## The June 2026 probe change {#the-june-2026-probe-change}

On **5 June 2026** a Campbell HygroVUE10 (SDI-12) replaced the CS215 at 47 m. Three
observations date the change: the raw 1-minute record has a gap from 11:10 to 11:31
that day; the fieldbook adds the HygroVUE10 at this location on 5 June and records a
change of its SDI-12 configuration with a new logger program on 11 June; and the
residual against MeteoSwiss Lägern changes level from that day, most in sun. The
swap half-hour 11:00 to 11:30 is removed and modelled (source code `5`).

NABEL ended in 2018, so Lägern is the only reference spanning this change. The
transfer is fitted on two season-matched samples: the HygroVUE10 from 12 June to
30 September 2026 (5 to 11 June, before the configuration change, enter no fit), and
the normal CS215 (code `0`) on the same calendar dates of 2022 to 2024. It has two
terms:

- **A radiation term**, zero in the dark. In sun the HygroVUE10 reads cooler than
  the normal CS215 by an amount that grows with radiation, to 0.98 °C at
  600 W m^-2^.
- **A night term**, a constant. At night the HygroVUE10 reads 0.11 °C cooler than
  the mean of the CS215 summers, less than the scatter among those summers
  (0.19 °C).

After both terms the HygroVUE10 lies within 0.05 °C of the CS215 level at night and
in every radiation class of the fitting sample. A month hold-out, in which each
month is refitted without itself and predicted, tests the transfer on data it was
not fitted to: the held-out months depart from the CS215 level by at most 0.18 °C,
against up to 0.58 °C before the correction and up to 0.38 °C between one CS215
summer and the others in the same month. The shield term of the CS215 is then
applied, so the HygroVUE10 era ends on the same reference level as the other eras.

## Known limitations

- **A small difference in the shape of the day remains across 2016.** The shield
  correction is fitted on the three years NABEL overlaps the CS215 (2016-2018) and
  applied to the CS215 until May 2025 and, through the transfer, to the HygroVUE10
  era, so it is an extrapolation after 2018. Measured against MeteoSwiss on
  2013-2015 against 2016-2018, the homogenised column still carries a daily-maximum
  step of +0.21 °C, a diurnal-range step of +0.18 °C and a daily-minimum step of
  +0.03 °C. The same statistics on the measured column step by up to +1.90 °C.
  **Daily maxima and diurnal ranges are the quantities most exposed to what
  remains.**
- **The heated CS215 (code `7`) is under-corrected in sun.** Daytime values and daily
  maxima from 22 October 2024 to 16 May 2025 are biased warm, by up to 0.92 °C in
  strong sun. The onset of code `7` is dated by a rule on a statistic over a
  month-long window; the excess grows gradually, so records shortly before the
  onset may already carry part of it.
- **The night term of code `6` is smaller than its uncertainty** (+0.058 °C against
  0.22 °C). It is applied
  because the change is established, not because the night difference is resolved,
  and it rests on one reference 2.5 km away.
- **The HygroVUE10 transfer rests on one summer and one reference.** It is fitted on
  12 June to 30 September 2026 against Lägern and applied as fitted to every
  HygroVUE10 record, including 5 to 11 June. Its behaviour in winter, under snow or
  rime and at low sun is untested. The CS215 level it is fitted to is a mean of
  three summers that differ among themselves at night by up to 0.19 °C, more than
  the night term of 0.11 °C.
- **The record is made self-consistent, not absolutely accurate.** The later eras
  are standardised onto the earlier one's shield behaviour, so the earlier era's own
  warm bias in sunshine (about +0.4 °C at strong radiation, relative to an aspirated
  sensor) remains in all of them. What is removed is the change in that bias at each
  sensor change, not the bias itself.
- **The records reconstructed from NABEL carry too little scatter.** The 1,530
  code-`5` values come from a line fitted on NABEL, so they sit approximately
  0.05 °C from it where a real measurement sits approximately 0.25 °C from it.
  Their means are sound; variance, extremes and any statistic of spread computed
  over January 2004 are understated.
- **2004 is 72 % modelled.** The tower record begins 2004-09-20 10:45. January 2004
  is reconstructed from NABEL rather than gap-filled, because the MeteoSwiss
  reference does not begin until 1 February 2004. The year carries source code `3`
  throughout its first nine months and is the least constrained in the record.
- **2026 is a partial year.** The record ends on 30 September 2026, so a 2026 annual
  mean covers January to September only.
