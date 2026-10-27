# Precipitation at 47 m

Half-hourly precipitation from the rain gauge at 47 m on the CH-LAE tower, 2004-2025. The file
is `08_METEO_PREC_GAPFILLED_2004-2025` (parquet and CSV): **385,728 records** on a continuous
30-minute index, `TIMESTAMP_MIDDLE` (middle of the half-hour), in local time (UTC+01:00, no
daylight saving), from 2004-01-01 00:15 to 2025-12-31 23:45. Values are sums over each half-hour
in mm, on the gauge's 0.1 mm tipping-bucket grid. Divide by 0.5 h for a rate.

The series ends on 31 December 2025. It is part of [FP2026.1](Dataset_Versions.html) and of the
[merged meteo product](notebooks/10_METEO/30_PRODUCTS/99_METEO_MERGED_2004-2026.09.html), where it
is `NaN` from 1 January 2026; the extension to 30 September 2026 is in progress.

The [interactive dashboard](dashboards/METEO_PREC_dashboard.html) summarises coverage,
provenance, seasonality, distributions, extremes and trends. It is a standalone file and works
offline.

Notebooks:

- [`08_METEO_PREC`](notebooks/10_METEO/30_PRODUCTS/08_METEO_PREC_2004-2025.html): builds the
  product and tests every hardware boundary in the record.
- [`MeteoSwiss_OED_PREC`](notebooks/10_METEO/10_REFERENCE/MeteoSwiss_OED_PREC_2004-2025.html):
  the Ehrendingen gauge, used both as diagnostic and as fill source.
- [`MeteoSwiss_REGIONAL_PREC`](notebooks/10_METEO/10_REFERENCE/MeteoSwiss_REGIONAL_PREC_2004-2025.html):
  the thirteen stations within 21 km that show which gauge moved in 2018.
- [`Meteo_Product_Chain`](Meteo_Product_Chain.html): where this product sits in the chain.

::: {.callout-important title="Which column to use"}

The measured column is **not homogeneous across mid-2018**, when the gauge moved from one
acquisition system to another. Annual totals average 830 mm before the change and 1,003 mm after
it.

- Within one era, use `PREC_TOT_T1_47_1`, which is what the gauge recorded.
- Across mid-2018, use `PREC_TOT_T1_47_1_HOMOGENIZED`. A total across the change taken from the
  measured column is dominated by the acquisition change, not by the weather.

Neither column is complete: 0.58 % of records are `NaN`, all of them before June 2014. A missing
record is not a dry one.

:::

## Columns

Both value columns are `NaN` at the same records. The flags apply to both, because the
homogenisation changes values and not provenance.

: Columns of `08_METEO_PREC_GAPFILLED_2004-2025`. {#tbl-prec-cols}

| column | unit | description |
|---|---|---|
| `PREC_TOT_T1_47_1` | mm (30 min)^-1^ | Precipitation as the gauge recorded it, with the fillable gaps taken from Ehrendingen. Inhomogeneous across mid-2018. |
| `PREC_TOT_T1_47_1_HOMOGENIZED` | mm (30 min)^-1^ | The same series with the pre-2018 era rescaled onto the level of the later era. A derived estimate, not a measurement. |
| `FLAG_PREC_TOT_T1_47_1_SOURCE` | - | Which acquisition chain and screened record a measured value came from. |
| `FLAG_PREC_TOT_T1_47_1_ISFILLED` | - | Whether the record is a measurement. |

The two flags are complementary: `ISFILLED == 0` exactly where `SOURCE > 0`, and the value is
`NaN` exactly where `ISFILLED == 2`.

### `FLAG_PREC_TOT_T1_47_1_SOURCE`

: Acquisition eras, the screened record each came from, and their record counts. {#tbl-prec-source}

| code | acquisition and screening | period | records |
|---|---|---|---|
| 0 | not measured at the tower: filled or missing | scattered, 2004-05-04 to 2025-09-26 | 3,156 |
| 1 | EMPA acquisition, diive screening | 2004-01-01 00:15 to 2018-05-28 23:45 | 250,327 |
| 2 | changeover in progress, era undetermined | 2018-05-29 00:15 to 2018-08-07 23:45 | 3,408 |
| 3 | ETH logger, diive screening | 2018-08-08 00:15 to 2018-12-31 23:45 | 7,008 |
| 4 | ETH logger, MeteoScreeningTool screening | 2019-01-01 00:15 to 2020-01-02 00:45 | 16,811 |
| 5 | ETH logger, diive screening | 2020-01-02 01:15 to 2025-12-31 23:45 | 105,018 |

Codes `3`, `4` and `5` are one acquisition chain, split only by the screened record that
delivered the values. Where records `4` and `5` overlap they agree value for value over two full
years. Select `SOURCE >= 3` for the homogeneous later series and `SOURCE > 0` for every gauge
measurement. Code `2` covers the ten weeks of the changeover: two maintenance entries bracket it,
and its 19 rain days are too few to assign it to either era.

### `FLAG_PREC_TOT_T1_47_1_ISFILLED`

Filter on `== 0` for measured records.

: Fill codes and their record counts. {#tbl-prec-isfilled}

| code | meaning | records | share |
|---|---|---|---|
| 0 | measured at the tower | 382,572 | 99.18 % |
| 1 | filled from MeteoSwiss Ehrendingen, rescaled by a monthly factor | 932 | 0.24 % |
| 2 | still missing: no sub-daily reference exists | 2,224 | 0.58 % |

The 932 filled records add 56.4 mm, and only 96 of them are wet; 759 of them fill the 16-day
outage of November 2019. The 2,224 unfilled records all lie before 2014-06-04 10:15, because
Ehrendingen has no sub-daily data before September 2014.

***

## The 2018 acquisition change

One instrument measured throughout, a Lambrecht `15188H` at 47 m. In mid-2018 it was moved from
EMPA's acquisition system to the ETH `CR1000` logger, and the recorded amounts rise by about a
fifth. The break is in the measurement chain, not in the instrument.

The later era is the one to trust. Against every MeteoSwiss precipitation station within 21 km,
the early era reads low (ratios 0.74 to 0.91), while the later era agrees with the network
(0.91 to 1.05). Against the elevation gradient of these stations, the early era is 25 % below
what a gauge on this ridge should catch and the later era 10 % below. About 10 % is ordinary wind
under-catch for an exposed ridge top.

`PREC_TOT_T1_47_1_HOMOGENIZED` lifts the early era onto the later one with one factor per
calendar month, fitted against those stations. The factors run from 1.07 to 1.44, equivalent to
1.21 applied uniformly. They raise the mean annual total of the complete early years from 830 mm
to 991 mm, against 1,003 mm for the later era. The later era is copied unchanged.

## No break in 2016

The January 2016 datalogger replacement moved three other tower variables, and a program change
in June 2016 left more than half of the longwave record reading low. Precipitation is not
affected: the gauge stayed on EMPA's acquisition until 2018 and no surviving tower program records
it. The 20.6-day outage that pressure and longwave show during the logger replacement is absent
here; all 988 half-hours are measured. The catch ratio against the regional stations shows no
step at either 2016 date, nor at any later boundary, including the change of screening tool in
January 2020.

## Known limitations

- **Neither column is absolutely calibrated, and both read low.** Against the regional stations'
  elevation gradient, the later era is about 10 % below what a gauge on this ridge should catch,
  which is ordinary wind under-catch for an exposed ridge top. The homogenisation lifts the early
  era onto the later one and stops there, so this 10 % remains in both columns. A total from this
  product is what the gauge caught, not what fell.
- **Winter totals are biased low, and the bias changes at 2018.** The gauge misses snow as it
  falls and releases part of it days later on melt, so sub-daily timing in winter is unreliable in
  both eras. On days below 2 °C the catch ratio averages 0.62 before 2018 and 0.56 after, but
  individual winters vary by more than that. The maintenance record has the gauge heating
  disconnected on 8 August 2018 (the day the gauge was rewired), still inactive in January 2024,
  and a new transformer fitted in July 2024. None of the three dates is visible in the data, so
  nothing is corrected. A winter total across 2018 mixes the acquisition change with a change in
  snow catch, which is why the winter months have the largest factors.
- **The homogenisation leaves light rain unchanged.** Homogenised values are rounded back onto the
  0.1 mm grid, and a small amount multiplied by 1.07 to 1.44 often rounds back to itself. In the
  early era, 9,146 of the 20,801 wet half-hours are identical in both columns, carrying 11 % of the
  rainfall: every 0.1 mm record, 55 % of the 0.2 mm records, 28 % of the 0.3 mm records, and none
  above 1 mm. Counts of wet half-hours and light-rain intensity statistics are therefore not
  homogenised. The factor delivered overall is 1.19 rather than the fitted 1.21, which is part of
  why the homogenised early era ends 1.2 % below the later level.
- **Filled records are suitable for sums, not for timing.** A filled value is the Ehrendingen
  measurement (3.8 km away, 260 m lower), rescaled. On synthetic gaps the summed rainfall is
  correct to within 2.2 % at every gap length, but the median error of one gap's total is 14 % for
  a two-week gap and about 35 % for a one-hour gap, so short gaps are the least reliable. At
  half-hourly resolution the correlation is 0.7; about a quarter of the half-hours a fill marks wet
  were dry at the tower, and about 30 % of wet half-hours are missed.
- **`GAPFILLED` in the file name does not mean complete.** Unlike `SW_IN`, `TA` and `PPFD_IN`,
  this product contains `NaN`. Code that assumes a complete series will fail or propagate `NaN`.
- **2008 is the only year with low coverage, 93.2 %.** A 24.6-day outage in May and June falls in
  the period that cannot be filled; Ehrendingen recorded 58.5 mm over that window. Every other year
  has a value for at least 98.3 % of its records.
- **Zeros are data.** 91.2 % of records with a value are exactly `0`, the correct value for no
  rain, not a missing-value code. The largest half-hour in the record is 27.7 mm, on 2023-07-12.
