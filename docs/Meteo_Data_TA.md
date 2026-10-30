# Air temperature at 47 m

Half-hourly air temperature at 47 m on the CH-LAE tower, 2004 to September 2026,
gap-filled to completeness. The file is `02_METEO_TA_GAPFILLED_2004-2026.09` (parquet and
CSV): **398,832 records** on a continuous 30-minute index `TIMESTAMP_MIDDLE` (middle of the
half-hour, UTC+01:00, no daylight saving), from 2004-01-01 00:15 to 2026-09-30 23:45. 2026
is a partial year (January to September).

The [interactive dashboard](dashboards/METEO_TA_dashboard.html) summarises the product on
one page. It is still built from the 2004-2025 version of the product and ends in December 2025.

Method, evidence and checks:

- [`02_METEO_TA`](notebooks/10_METEO/30_PRODUCTS/02_METEO_TA_2004-2026.09.html): builds
  the product: screening, gap-filling, the 2016 correction, and the treatment of the
  May 2025 change and the June 2026 probe change.
- [`TA_HOMOGENIZATION_OPTIONS`](notebooks/10_METEO/30_PRODUCTS/TA_HOMOGENIZATION_OPTIONS.html):
  the candidate corrections for the 2016 break, and why this one was chosen.
- [`METEO_TA` overview](notebooks/90_OVERVIEW/METEO_TA.html): the product year by year,
  2004-2025, from the current product file. The partial year 2026 is left out.

::: {.callout-important title="Which column to use"}

The measured column is **not homogeneous**. The 47 m record comes from three probes, and
the second of them changed state twice before it was replaced (see
[Sensor history](#sensor-history)).

- Inside one probe state, use `TA_T1_47_1_gfXG`, which is what the probe reported.
- Across 21 January 2016, 16 May 2025 or 5 June 2026 (period means, trends, year rankings,
  anomalies, daily maxima, threshold-day counts) use `TA_T1_47_1_HOMOGENIZED_gfXG`. The
  2016 step alone is larger than the climate signal over this record.
- Where provenance has to be certain, select `FLAG_TA_T1_47_1_SOURCE` in `{0, 1, 4, 6}`.
  Exclude code `7` from daytime statistics (daily maxima, diurnal ranges): it remains too
  warm in sun after homogenisation.

:::

## Columns

Both value columns are complete, and both flags are defined at every record and describe
both value columns.

: Columns of `02_METEO_TA_GAPFILLED_2004-2026.09`. {#tbl-ta-cols}

| column | unit | description |
|---|---|---|
| `TA_T1_47_1_gfXG` | °C | Air temperature as the probe reported it, gaps filled. Not homogeneous across 2016-01-21, 2025-05-16 and 2026-06-05. |
| `FLAG_TA_T1_47_1_ISFILLED` | - | Whether the value was measured, and if not, which method produced it. |
| `TA_T1_47_1_HOMOGENIZED_gfXG` | °C | The same series with every probe state put on one level. |
| `FLAG_TA_T1_47_1_SOURCE` | - | Which probe, and which state of it, stands behind the record. |

### `FLAG_TA_T1_47_1_ISFILLED`

Filter on `== 0` for measured records. Every other code marks a filled value. Code `3` is
not used.

: Fill codes and their record counts. {#tbl-ta-isfilled}

| code | meaning | records | share |
|---|---|---|---|
| 0 | observed | 382,167 | 95.82 % |
| 1 | gap-filled by XGBoost | 14,914 | 3.74 % |
| 2 | gap-filled from timestamp information only (fallback) | 43 | 0.01 % |
| 4 | linear interpolation across a short gap (up to 1 h) | 178 | 0.04 % |
| 5 | reconstructed from NABEL at 49 m on the same tower | 1,530 | 0.38 % |

Gap-filling is split into five periods, at each probe change and at the end of the NABEL
record in 2018, so that no model is trained across a change of probe. Of the 1,530 code-`5`
records, 1,488 are in January 2004, one in February 2004 and 41 in July 2012.

### `FLAG_TA_T1_47_1_SOURCE`

: Probe and probe-state codes, their record counts and the period each covers
(`TIMESTAMP_MIDDLE`). {#tbl-ta-source}

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

No probe on this tower stands behind codes `2`, `3` and `5`. The measured value of the two
code-`5` half-hours is removed and modelled. To stay inside one probe state, select a single
code.

***

## Sensor history {#sensor-history}

The field name `TA_T1_47_1` and its database tags did not change at any of these dates.

- **Rotronic MP101A, to 31 December 2015 (code `1`).** Read as a single-ended analog
  voltage by a CR10X logger. The logger programs name the probe and its conversion.
- **Campbell CS215, from 21 January 2016 (code `0`).** Read over SDI-12 by the CR1000
  logger installed at the changeover, whose program names the probe. The 20 days between
  the two are an outage (code `2`).
- **The CS215 with excess daytime heating, 22 October 2024 to 16 May 2025 (code `7`).** On
  19 September 2024 the fieldbook records intake tubing attached at the 47 m sonic
  anemometer. In the following weeks the daytime excess of the 47 m probe over the 35 m
  sensor of the same tower grows beyond any earlier value; a rule on that excess dates the
  onset.
- **The CS215 after 16 May 2025 (code `6`).** The probe was handled during a site visit,
  and the daytime excess disappears. See [The May 2025 change](#the-may-2025-change).
- **Campbell HygroVUE10, from 5 June 2026 (code `4`).** It replaced the CS215. See
  [The June 2026 probe change](#the-june-2026-probe-change).

: What `TA_T1_47_1_HOMOGENIZED_gfXG` applies to each source code. {#tbl-ta-homog}

| source code | correction |
|---|---|
| 1, 2, 3 | the constant of the 2016 change, +1.3197 °C, added to every record |
| 0, 7 | the shield term of the CS215, subtracted: zero at night, at most 0.59 °C |
| 6 | a constant night term, +0.058 °C, subtracted at all hours; no shield term |
| 4 | the HygroVUE10 transfer onto the normal CS215, then the shield term of the CS215 |
| 5 | as the period the half-hour belongs to (the handling record as code `7`, the swap record as code `6`) |

## The 2016 sensor change

On 21 January 2016 the Rotronic MP101A, read as an analog voltage, was replaced by a
Campbell CS215 read over a digital line, together with the logger. Two things changed, and
`TA_T1_47_1_HOMOGENIZED_gfXG` corrects both.

**The old chain read too cold, day and night.** A constant zero-point error of about
-11 mV, at 10 mV per °C, left it reading about 1.1 °C below an aspirated reference on the
same tower; the new probe reads about 0.2 °C above that reference. The difference between
the two eras, **+1.3197 °C**, is added to every record before the changeover.

**The two probes warm differently in sunshine.** Both sit in passive radiation shields,
which heat up in sun, and the newer one heats more. This part of the step occurs only in
daylight, so a constant cannot remove it. It was measured against NABEL, an aspirated
sensor at 49 m on the same tower, and subtracted from the later era. It is **zero at night**
and **0.59 °C** at most.

Both corrections were fitted against NABEL and scored against MeteoSwiss Lägern (2.5 km
away), which entered neither fit.

: The step across the sensor change, measured against MeteoSwiss, 2013-2015 against
2017-2019. {#tbl-ta-steps}

| window | as measured | after both corrections |
|---|---|---|
| night | +1.31 °C | -0.01 °C |
| day | +1.69 °C | +0.06 °C |
| all hours | +1.51 °C | +0.03 °C |

The correction raises the earlier era by the constant and lowers the sunlit records of the
later eras by the shield term (by 0.15 °C on average over the 2017-2025 annual means of
measured records). Over the whole record it more than halves the apparent warming. From the
complete columns, the difference between the 2005-2015 and 2017-2025 period means falls from
+2.39 °C to +0.92 °C, and the Theil-Sen trend over annual means from +1.76 to
+0.77 °C decade^-1^. From measured records only, the same figures are +2.47 °C and +1.00 °C,
and +1.80 and +0.77 °C decade^-1^. Notebook `02` reports both.

## The May 2025 change {#the-may-2025-change}

On **16 May 2025** the raw 1-minute record of the 47 m probe jumps by about 5 °C between
09:32 and 09:42, while the 35 m sensor of the same tower does not change: the probe was
handled. The fieldbook records a site visit that day, with the heating connection of the
tower inlet found melted and disconnected. The half-hour 09:30 to 10:00 is removed and
modelled (source code `5`).

The change is placed on the 47 m probe by two comparisons. The 35 m sensor against
MeteoSwiss Lägern, which contains no 47 m measurement, changes by an ordinary amount at the
handling (-0.36 °C above 500 W m^-2^, 14 days after against 14 days before). The 47 m probe
against the 35 m sensor changes in sun by -1.11 °C, more than on any other day of the
surrounding half-year.

- **Code `7`**, the heated state from 22 October 2024, receives the shield term of the
  normal CS215 and nothing more. In strong sun it remains up to 0.92 °C too warm after
  homogenisation.
- **Code `6`**, from 16 May 2025, no longer has the daytime excess of the normal CS215 and
  receives no shield term. Its night level is compared with the normal CS215 of 2022-2024
  against Lägern, month by month over March to September, and the difference, +0.058 °C, is
  removed as a constant. Its uncertainty is 0.22 °C, the year-to-year scatter of the same
  quantity among the reference years. After the correction, code `6` lies within 0.13 °C of
  the normal CS215 at night and in every radiation class. In a month hold-out (each month
  corrected with the term derived from the others) it departs from the normal CS215 by at
  most 0.215 °C, against up to 0.57 °C between one reference year and the others in the
  same month.

## The June 2026 probe change {#the-june-2026-probe-change}

On **5 June 2026** a Campbell HygroVUE10 (SDI-12) replaced the CS215 at 47 m. The raw
1-minute record has a gap from 11:10 to 11:31 that day. The fieldbook adds the HygroVUE10
at this location on 5 June and records a change of its SDI-12 configuration with a new
logger program on 11 June. The residual against MeteoSwiss Lägern changes level from that
day, most in sun. The swap half-hour 11:00 to 11:30 is removed and modelled (source code
`5`).

NABEL ended in 2018, so Lägern is the only reference across this change. The transfer is
fitted on two season-matched samples: the HygroVUE10 from 12 June to 30 September 2026
(5 to 11 June, before the configuration change, enter no fit) and the normal CS215 (code
`0`) on the same calendar dates of 2022 to 2024. It has two terms:

- **A radiation term**, zero in the dark. In sun the HygroVUE10 reads cooler than the
  normal CS215 by an amount that grows with radiation, to 0.98 °C at 600 W m^-2^.
- **A night term**, a constant. At night the HygroVUE10 reads 0.11 °C cooler than the mean
  of the CS215 summers, less than the scatter among those summers (0.19 °C).

After both terms the HygroVUE10 lies within 0.05 °C of the CS215 level at night and in
every radiation class of the fitting sample. In a month hold-out (each month refitted
without itself and predicted) the held-out months depart from the CS215 level by at most
0.18 °C, against up to 0.58 °C before the correction and up to 0.38 °C between one CS215
summer and the others in the same month. The shield term of the CS215 is then applied, so
the HygroVUE10 era ends on the same reference level as the other eras.

## Known limitations

- **A small difference in the shape of the day remains across 2016.** The shield
  correction is fitted on the three years in which NABEL overlaps the CS215 (2016-2018) and
  applied until May 2025 and, through the transfer, to the HygroVUE10 era, so after 2018 it
  is an extrapolation. Against MeteoSwiss, 2013-2015 against 2016-2018, the homogenised
  column still carries a daily-maximum step of +0.21 °C, a diurnal-range step of +0.18 °C
  and a daily-minimum step of +0.03 °C; the measured column steps by up to +1.90 °C in the
  same statistics. **Daily maxima and diurnal ranges are most affected by what remains.**
- **The heated CS215 (code `7`) is under-corrected in sun.** Daytime values and daily
  maxima from 22 October 2024 to 16 May 2025 are biased warm, by up to 0.92 °C in strong
  sun. The excess grows gradually and its onset is dated by a rule over a month-long
  window, so records shortly before 22 October 2024 may already carry part of it.
- **The night term of code `6` is smaller than its uncertainty** (+0.058 °C against
  0.22 °C). It is applied because the change of probe state is established, not because the
  night difference is resolved, and it rests on one reference 2.5 km away.
- **The HygroVUE10 transfer rests on one summer and one reference.** It is fitted on
  12 June to 30 September 2026 against Lägern and applied as fitted to every HygroVUE10
  record, including 5 to 11 June. Its behaviour in winter, under snow or rime and at low
  sun is untested. The CS215 level it is fitted to is a mean of three summers that differ
  among themselves at night by up to 0.19 °C, more than the night term of 0.11 °C. It is to
  be refitted once the HygroVUE10 record includes a winter.
- **The record is made self-consistent, not absolutely accurate.** The later eras are
  standardised onto the shield behaviour of the MP101A, so its warm bias in sunshine (about
  +0.4 °C at strong radiation, relative to an aspirated sensor) remains in all of them.
- **Records reconstructed from NABEL have too little scatter.** The 1,530 code-`5` values
  come from a line fitted on NABEL, so they lie about 0.05 °C from it where a real
  measurement lies about 0.25 °C from it. Their means are sound; variance, extremes and
  other measures of spread over January 2004 are understated.
- **2004 is 72 % modelled.** The tower record begins 2004-09-20 10:45. January 2004 is
  reconstructed from NABEL because the MeteoSwiss reference begins only on 1 February 2004.
  The first nine months of 2004 carry source code `3` and are the least constrained part of
  the record.
- **2026 is a partial year.** A 2026 annual mean covers January to September only.
