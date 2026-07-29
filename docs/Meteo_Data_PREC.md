# Precipitation at 47 m

Half-hourly precipitation from the rain gauge at 47 m on the CH-LAE tower,
2004-2025. The file is `08_METEO_PREC_GAPFILLED_2004-2025` (parquet and CSV):
**385,728 records** on a continuous 30-minute middle-timestamp index (named
`TIMESTAMP_MIDDLE` in the file) in local time (UTC+1, no daylight saving), from
2004-01-01 00:15 to 2025-12-31 23:45. Values are sums over each half hour in mm, on
the gauge's 0.1 mm tipping-bucket grid. Divide by 0.5 h for a rate.

The [**interactive dashboard**](dashboards/METEO_PREC_dashboard.html) summarises the
product on one page: coverage and provenance, seasonality, distributions, extremes
and trends, with a table view behind every chart. It is standalone and works
offline.

Method, evidence and checks:

- [`08_METEO_PREC`](notebooks/10_METEO/30_PRODUCTS/08_METEO_PREC_2004-2025.html) —
  builds the product, and tests every hardware boundary in the record.
- [`MeteoSwiss_OED_PREC`](notebooks/10_METEO/10_REFERENCE/MeteoSwiss_OED_PREC_2004-2025.html)
  — the Ehrendingen gauge, which is both the diagnostic and the fill source.
- [`MeteoSwiss_REGIONAL_PREC`](notebooks/10_METEO/10_REFERENCE/MeteoSwiss_REGIONAL_PREC_2004-2025.html)
  — the thirteen stations within 21 km that decide which gauge moved in 2018.
- [`Meteo_Product_Chain`](Meteo_Product_Chain.html) — where this product sits in the
  chain.

::: {.callout-important title="Which column to use"}

The measured column is **not homogeneous across mid-2018**, when the gauge moved from
one acquisition system to another. Annual totals average 830 mm before the change and
1,003 mm after it.

- Inside one era, use `PREC_TOT_T1_47_1`, which is what the gauge recorded.
- Across mid-2018, use `PREC_TOT_T1_47_1_HOMOGENIZED`. A total spanning the change
  taken from the measured column is dominated by the acquisition change rather than
  by the weather.

Neither column is complete: 0.58 % of records are `NaN`, all of them before June
2014, and a missing record is not a dry one.

:::

## Columns

Both value columns are `NaN` at the same records. The flags apply to either, since
the homogenisation changes values and not provenance.

: Columns of `08_METEO_PREC_GAPFILLED_2004-2025`. {#tbl-prec-cols}

| column | unit | description |
|---|---|---|
| `PREC_TOT_T1_47_1` | mm (30 min)^-1^ | Precipitation as the gauge recorded it, with the fillable gaps taken from Ehrendingen. Inhomogeneous across mid-2018. |
| `PREC_TOT_T1_47_1_HOMOGENIZED` | mm (30 min)^-1^ | The same series with the pre-2018 era rescaled onto the level of the later era. A derived estimate, not a measurement. |
| `FLAG_PREC_TOT_T1_47_1_SOURCE` | - | Which acquisition chain and screened record a measured value came from. |
| `FLAG_PREC_TOT_T1_47_1_ISFILLED` | - | Whether the record is a measurement at all. |

The flags are complementary: `ISFILLED == 0` exactly where `SOURCE > 0`, and the
value is `NaN` exactly where `ISFILLED == 2`.

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

Codes `3`, `4` and `5` are one acquisition chain, split only by which screened record
delivered the values; where records `4` and `5` overlap they agree value for value
over two full years. Select `SOURCE >= 3` for the homogeneous later series and
`SOURCE > 0` for every gauge measurement. Code `2` covers the ten weeks of the
changeover, which two maintenance entries bracket and 19 rain days cannot resolve.

### `FLAG_PREC_TOT_T1_47_1_ISFILLED`

Filter on `== 0` for measured records. Code `1` is another gauge's measurement,
rescaled; code `2` is a gap that could not be filled.

: Fill codes and their record counts. {#tbl-prec-isfilled}

| code | meaning | records | share |
|---|---|---|---|
| 0 | measured at the tower | 382,572 | 99.18 % |
| 1 | filled from MeteoSwiss Ehrendingen, rescaled by a monthly factor | 932 | 0.24 % |
| 2 | still missing: no sub-daily reference exists | 2,224 | 0.58 % |

The 932 filled records add 56.4 mm and only 96 of them are wet; 759 of them fill the
16-day outage of November 2019. The 2,224 unfillable records all lie before
2014-06-04 10:15, because Ehrendingen has no sub-daily data before September 2014.

***

## The 2018 acquisition change

One instrument measured throughout, a Lambrecht `15188H` at 47 m. In mid-2018 it was
moved from EMPA's acquisition system to the ETH `CR1000` logger, and the recorded
amounts rise by about a fifth. The break is in the measurement chain, not in the
instrument.

The later era is the one to trust. Against every MeteoSwiss precipitation station
within 21 km the early era reads low, at ratios of 0.74 to 0.91, while the later era
agrees with the network at 0.91 to 1.05. Against the ensemble's elevation gradient
the early era sits 25 % below what a gauge on this ridge should catch and the later
era 10 % below, where roughly 10 % is ordinary wind under-catch for an exposed ridge
top.

`PREC_TOT_T1_47_1_HOMOGENIZED` lifts the early era onto the later one with a factor
per calendar month, fitted against those stations. The factors run from 1.07 to 1.44,
equivalent to 1.21 applied uniformly, and they bring the mean annual total of the
complete early years from 830 mm to 991 mm against 1,003 mm for the later era. The
later era is copied through unchanged. Neither era is absolutely calibrated: the
correction makes the record self-consistent across 2018 without removing the
under-catch both eras carry.

## No second break in 2016

January 2016 moved three other tower variables when the datalogger was replaced, and
a program change that June left more than half the longwave record reading low.
Precipitation is unaffected, because the gauge was not on that logger; it stayed on
EMPA's acquisition until 2018. No surviving tower program records the gauge at all,
and the 20.6-day outage that pressure and longwave both suffer while the logger is
replaced is absent here, with all 988 half-hours measured. The catch ratio against
the regional stations confirms it at both dates, and finds nothing at any later
boundary either, including the change of screening tool in January 2020.

## Known limitations

- **Winter totals are biased low, and the bias changes at 2018.** The gauge misses
  snow as it falls and releases part of it days later on melt, so winter sub-daily
  timing is unreliable in both eras. On days below 2 °C the catch ratio averages 0.62
  before 2018 and 0.56 after, but individual winters vary by more than that. The
  maintenance record has the heating disconnected on 8 August 2018, the day the gauge
  was rewired, still inactive in January 2024, and a new transformer fitted in July
  2024; none of the three dates shows up in the data, so nothing is corrected. A
  winter total spanning 2018 mixes the acquisition change with a change in snow
  catch, which is why the largest monthly factors are the winter ones.
- **The homogenisation cannot correct a single bucket tip.** Homogenised values are
  rounded back onto the 0.1 mm grid, and 0.1 mm times any monthly factor rounds to
  0.1 mm again, so 6,580 records are identical in both columns: 32 % of the wet
  half-hours in the early era, though only 5 % of its rainfall. Totals are
  unaffected, but a count of wet half-hours or a light-rain intensity statistic is
  not homogenised, and the factor delivered overall is 1.19 rather than the 1.21
  fitted.
- **Filled records are good for sums, not for timing.** A filled value is the
  Ehrendingen gauge's measurement, 3.8 km away and 260 m lower, rescaled. On
  synthetic gaps the summed rainfall is right to within 2.2 % at every gap length,
  but the median error on one gap's total is 14 % for a two-week gap and about 35 %
  for a one-hour gap, so short gaps are the unreliable ones. At half-hourly
  resolution the correlation is 0.7, about a quarter of the half-hours a fill marks
  wet were dry at the tower, and about 30 % of wet half-hours are missed.
- **`GAPFILLED` in the filename does not mean complete.** Unlike `SW_IN`, `TA` and
  `PPFD_IN`, this product still contains `NaN`, and code that assumes otherwise will
  break on it or propagate `NaN` silently.
- **2008 is the only badly incomplete year, at 93.2 % coverage.** A 24.6-day outage
  in May and June falls inside the unfillable period; Ehrendingen recorded 58.5 mm
  over that window. Every other year carries a value for at least 98.3 % of its
  records.
- **Zeros are data.** 91.2 % of records carrying a value are exactly `0`, the correct
  value for no rain rather than a sentinel. The largest half hour in the record is
  27.7 mm, on 2023-07-12.
