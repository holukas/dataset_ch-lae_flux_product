# Outgoing longwave radiation at 47 m

Half-hourly outgoing (upwelling) longwave radiation at 47 m on the CH-LAE tower, 2005-2025,
exported as measured. The file is `13_METEO_LW_OUT_2005-2025` (parquet and CSV): **355,872
records** on a continuous 30-minute index, `TIMESTAMP_MIDDLE` (middle of the half-hour), in local
time (UTC+01:00, no daylight saving), from 2005-09-14 00:15 to 2025-12-31 23:45. The first
measurement is at 2005-09-14 13:15.

The series ends on 31 December 2025. It is part of [FP2026.1](Dataset_Versions.html) and of the
[merged meteo product](notebooks/10_METEO/30_PRODUCTS/99_METEO_MERGED_2004-2026.09.html), where it
is `NaN` from 1 January 2026; the extension to 30 September 2026 is in progress.

The [interactive dashboard](dashboards/METEO_LW_OUT_dashboard.html) summarises coverage,
provenance, seasonality, distributions, extremes and trends. Read its trend together with the
instrument card: the record steps in June 2016 and again in December 2021, neither step is
corrected, and a trend over the whole record includes both.

Notebooks:

- [`13_METEO_LW_OUT`](notebooks/10_METEO/30_PRODUCTS/13_METEO_LW_OUT_2005-2025.html): builds the
  product. It compares the two screenings where they overlap, applies the 2012 corrections, removes
  the excursion during the radiometer exchange, and identifies the instrument and calibration
  factor behind each part of the record.
- [`LW_OUT_T1_47_1`](notebooks/10_METEO/20_SCREENING/LW_OUT/LW_OUT_T1_47_1_2020-2025.html): the
  screening of the current era, which dates the radiometer exchange to the minute.
- [`06_METEO_LW_IN`](notebooks/10_METEO/30_PRODUCTS/06_METEO_LW_IN_2005-2026.09.html): the second
  pyrgeometer of the same instrument. Together the two give the net longwave exchange, but they are
  separate detectors with separate calibration factors, so each era question is tested again here.
- [`02_METEO_TA`](notebooks/10_METEO/30_PRODUCTS/02_METEO_TA_2004-2026.09.html): air temperature,
  which gives the Stefan-Boltzmann emission used in every check on this page. Its homogenised
  column is used, because the checks cross January 2016.
- [`Meteo_Data_SW_OUT`](Meteo_Data_SW_OUT.html): the outgoing shortwave channel of the same
  instrument, with the same December 2021 boundary.
- [`Meteo_Product_Chain`](Meteo_Product_Chain.html): where this product sits in the chain.

::: {.callout-important title="The record steps at the December 2021 radiometer exchange"}

The CNR1 was replaced by a CNR4 on 14 December 2021, and the series changes at that date by more
than in any year without a change. The change of screening software falls close to the same date
but is ruled out, because the two screenings give the same values where they overlap. The cause is
the instrument.

The step is **not corrected, and there is no homogenised column**: its cause is known, its size is
not, and a correction would need calibration data the site does not hold. Filter on
`FLAG_LW_OUT_T1_47_1_SOURCE` before comparing the two eras, and drop code `3`, the 24 days in which
the new instrument was read with the old instrument's constant.

**Nothing is gap-filled**, so the value column contains `NaN` and every non-null record is a
measurement.

:::

## What the values are

The values are **upwelling longwave irradiance**: the thermal emission of the canopy seen from
47 m, plus the small part of the downwelling flux that the canopy reflects. The median is
**356.7 W m^-2^**, the mean 359.1 W m^-2^, and the range 239.6 to 503.5 W m^-2^.

A pyrgeometer's voltage measures only the *net* exchange between the viewed surface and the
instrument body, so the instrument's own emission is added to obtain the irradiance. Every value in
this file includes it; the converted voltage alone would differ by some 300 to 400 W m^-2^.

A wrong calibration factor therefore scales only the **net** signal, not the added emission term.
For a downward-facing pyrgeometer above a canopy the net signal is small: a few W m^-2^ in the
median and a few tens at the extremes, against several hundred in the file. The factor error that
costs `LW_IN` about 8 W m^-2^ in the middle of its distribution is worth much less here, which is
why the checks below use percentiles of the net signal rather than the level.

Two physical checks pass. The ratio of the measured value to the Stefan-Boltzmann emission at air
temperature has a nighttime median of **0.979** (5th to 95th percentile 0.963 to 0.996) and a
daytime median of 0.990, as expected for a canopy radiating near air temperature. And the site
loses longwave radiation in most half-hours: the median of `LW_IN − LW_OUT` is
**−46.4 W m^-2^**, and 81 % of nighttime and 85 % of daytime half-hours are net losses. The second
check would detect the two channels having been swapped anywhere between the logger and this file.

## Columns

: Columns of `13_METEO_LW_OUT_2005-2025`. {#tbl-lwout-cols}

| column | unit | description |
|---|---|---|
| `LW_OUT_T1_47_1` | W m^-2^ | Outgoing longwave radiation, as measured. Contains `NaN`. |
| `FLAG_LW_OUT_T1_47_1_SOURCE` | - | Which instrument and calibration factor produced the value. Defined at every record. |

There is **no `ISFILLED` flag**, because nothing is filled. `PA`, `LW_IN` and `SW_OUT` are exported
the same way.

### `FLAG_LW_OUT_T1_47_1_SOURCE`

: Provenance codes and their record counts. Shares are of the 348,958 measured records. {#tbl-lwout-source}

| code | meaning | period | records | measured | share |
|---|---|---|---|---|---|
| 0 | CNR4, this channel with its own factor of 11.33 µV/W/m^2^ | from 2022-01-07 | 69,840 | 69,724 | 20.0 % |
| 1 | CNR1, under the logger program of 7 June 2016 | 2016-06-07 to 2021-12-13 | 96,768 | 95,996 | 27.5 % |
| 2 | CNR1 at 10.03 µV/W/m^2^, the pyranometer's factor | to 2016-06-06 | 188,112 | 182,102 | 52.2 % |
| 3 | changeover, calibration undetermined | 2021-12-14 to 2022-01-06 | 1,152 | 1,136 | 0.3 % |

::: {.callout-note title="These codes differ from those of `LW_IN`"}

The two files number their eras differently, and the start of the changeover code differs by one
day. Here code `1` is the era from the June 2016 logger program, and all of 14 December 2021 carries
the undetermined code, because the exchange happened during that day.
[`LW_IN`](Meteo_Data_LW_IN.html) assigns that day to the CNR1 and starts its undetermined code on
the next day. Do not carry a code from one file to the other.

:::

## Coverage

Of the 355,872 records, **348,958 have a value (98.1 %)**. Of 972 gaps, 933 are one hour or
shorter and nine exceed a day.

: The five longest gaps. {#tbl-lwout-gaps}

| from | to | days | cause |
|---|---|---|---|
| 2015-08-17 | 2015-09-27 | 41.1 | outage of this channel alone |
| 2016-01-01 | 2016-01-21 | 20.6 | site-wide outage during the tower logger replacement |
| 2019-11-04 | 2019-11-19 | 15.8 | station outage |
| 2012-10-28 | 2012-11-09 | 13.0 | removed in this product: storm damage and stressed cables |
| 2012-07-29 | 2012-08-10 | 12.6 | removed in this product: tower power-supply failure |

The longest gap affects this channel only. The incoming channel of the same radiometer measured
through those six weeks (99.0 % coverage in 2015), and `SW_OUT` has no gap there either. The cause
is not known.

Five years are below 97 % measured: 2015 at 88.1 %, 2012 at 92.3 %, 2016 at 94.3 %, 2019 at 95.7 %
and 2009 at 96.6 %. 2005 is a partial year, beginning in September.

This product removed three sets of records: **1,202** inside the two 2012 windows of documented
logger-wide fault, as in notebooks `01` to `03` and `06`; **one** record outside the physical range
of 150 to 600 W m^-2^; and **ten** half-hours during the radiometer exchange that fell outside the
range of the same time of day on the seven days either side, when the instrument was unmounted and
no longer viewing the canopy. The **August 2012 clock error** is corrected by the same +15.5 h shift
as the other tower variables. Unlike `LW_IN`, this variable can confirm the size of the shift,
because the canopy heats in the sun and its emission follows.

***

## The two screenings agree

The MeteoScreeningTool and the diive screening cover **35,032 of the same half-hours**, and on
those records they give the same series: median difference 0.000 W m^-2^, RMS difference
0.011 W m^-2^, largest single difference 2.06 W m^-2^, correlation 1.000. The join between them
changes no value, and the change of screening is ruled out as the cause of the step at the turn of
2022. `LW_IN` has no such overlap.

## The June 2016 calibration change reached this channel

On 7 June 2016 a new logger program changed a radiometer calibration factor from 10.03 to
12.83 µV/W/m^2^, the change that leaves more than half of `LW_IN` reading low. The maintenance
record names one factor without saying which channels received it, so the question was tested in
the data.

The statistic is the 2nd percentile of the nighttime net signal (measured value minus the
Stefan-Boltzmann emission at air temperature), where a conversion error is largest. It moves from
**−15.9 W m^-2^ in 2006-2015 to −11.3 W m^-2^ in 2017-2021**, a ratio of 0.721 that is the same at
every percentile of the tail, as expected for a change of conversion. The documented factor change
predicts 0.782; the two agree well within the year-to-year scatter of the statistic. Where the
canopy is at air temperature and the net signal is near zero, no conversion factor can act, and the
corresponding statistic moves by only 0.07 % across the date. A change in the canopy or the weather
would not produce this pattern.

**Effect on the values.** Before 7 June 2016 the net signal is too large in magnitude by roughly a
quarter. Values therefore read low at night, when the canopy is cooler than the instrument, and
high during the day. Because the net signal is small, the error is a few W m^-2^ at most, compared
with about 8 W m^-2^ for the incoming channel. It is **not corrected**, because that would need the
radiometer's body temperature, which this product does not read. Code `2` marks the affected era,
more than half the record.

## The December 2021 exchange and the 24 days after it

Measured the same way, the first half of 2022 gives an envelope ratio of **0.710** against the three
preceding years, outside the 0.808 to 1.050 that the statistic shows in years without a boundary.
The record therefore steps at the exchange. The screenings agree, so the cause is the instrument or
the weather, and the CNR1 was replaced by the CNR4 on that date. Nothing is corrected; the flag
separates the two instruments.

From 14 December 2021 to 7 January 2022 the CNR4 was read by a logger program written for the CNR1,
so its values were converted with the wrong sensitivity. Which of two candidate sensitivities was
applied is not known: the program that set it does not survive, and the June 2016 entry does not
say whether its new factor reached this channel. Both candidates were computed; neither is adopted.
The error is small, because the constant scales the net signal, not the reported irradiance. Over
the window the net signal has a median of −0.7 W m^-2^ and a 5th to 95th percentile range of −3.6 to
+2.7 W m^-2^, so the worst case over both candidates is **1.6 W m^-2^ on a single half-hour, 0.5 %
of the reported value**. Code `3` marks the interval, so it can be dropped where an unambiguous
calibration is needed.

## Known limitations

- **The record is not homogeneous across December 2021.** The step is measured and attributed to
  the instrument, but its size in W m^-2^ is not established. Filter on the source flag before
  comparing the two eras, and treat a trend across that date as containing the change.
- **More than half of the record was converted with the pyranometer's factor.** Everything before
  7 June 2016 carries code `2` and reads low at night by roughly a quarter of the net signal, a few
  W m^-2^. It is not corrected, because that would need the radiometer's body temperature.
- **The 24 days of the changeover have an unverified conversion**, with an error of at most
  1.6 W m^-2^ and the applied constant not identified. Code `3` marks them.
- **There is no independent reference at the site.** MeteoSwiss Lägern measures no longwave, NABEL
  has no pyrgeometer, and the below-canopy sensor views a different surface. Every statement above
  rests either on the physics of the measurement, with the Stefan-Boltzmann emission at air
  temperature as the yardstick, or on the overlap between the two screenings. This is weaker
  evidence than a second instrument; where it does not suffice, the product notebook says so.
- **The physical checks use air temperature in place of two temperatures that are not measured**:
  the canopy temperature and the radiometer body temperature. This is adequate to estimate the size
  of an effect, not to correct the data.
- **The January 2016 acquisition change did not move this series.** It is listed because the same
  change moved `TA_T1_47_1` by 1.3 °C and because it is easily confused with the June date five
  months later. Every surviving logger program applies the same conversion across it, and the data
  show no change.
- **The series contains gaps and is not gap-filled.** Code that assumes a complete series will fail
  or propagate `NaN`. If a complete series is needed, for example for four-component net radiation
  or energy-balance closure, fill it downstream, and do not train one model across a calibration
  boundary.
- **The six-week gap of August and September 2015 has no known cause**, and it makes 2015 the least
  complete year. No other channel of the same instrument shares it.
- **The 2012 windows were removed without evidence from this series**, as in `06`. They rest on a
  documented logger-wide fault, and this variable has no reference that could show a level error
  there.
