# Outgoing longwave radiation at 47 m

Half-hourly outgoing (upwelling) longwave radiation at 47 m on the CH-LAE tower, 2005-2025,
exported as measured. The file is `13_METEO_LW_OUT_2005-2025` (parquet and CSV): **355,872
records** on a continuous 30-minute middle-timestamp index (named `TIMESTAMP_MIDDLE` in the
file) in local time (UTC+1, no daylight saving), from 2005-09-14 00:15 to 2025-12-31 23:45. The
first measurement is at 2005-09-14 13:15.

The [**interactive dashboard**](dashboards/METEO_LW_OUT_dashboard.html) summarises the product
on one page: coverage and provenance, seasonality, distributions, extremes and trends, with a
table view under every chart. Read its trend with the instrument card beside it: the record
steps at June 2016 and again at December 2021, and neither step is corrected, so a trend taken
across the whole record carries both.

Method, evidence and checks:

- [`13_METEO_LW_OUT`](notebooks/10_METEO/30_PRODUCTS/13_METEO_LW_OUT_2005-2025.html) — builds
  the product: the comparison of the two screenings where they overlap, the 2012 corrections,
  the removal of the radiometer-exchange excursion, and the identification of the instrument and
  the calibration factor behind each part of the record.
- [`LW_OUT_T1_47_1`](notebooks/10_METEO/20_SCREENING/LW_OUT/LW_OUT_T1_47_1_2020-2025.html) — the
  screening of the current era, which dates the radiometer exchange to the minute.
- [`06_METEO_LW_IN`](notebooks/10_METEO/30_PRODUCTS/06_METEO_LW_IN_2005-2025.html) — the second
  pyrgeometer of the same instrument. Together the two products are the site's net longwave
  exchange, but they are separate detectors with separate calibration factors, so a finding
  about one says nothing definite about the other, and every era question is asked again here.
- [`02_METEO_TA`](notebooks/10_METEO/30_PRODUCTS/02_METEO_TA_2004-2025.html) — the
  air-temperature product, which supplies the Stefan-Boltzmann yardstick that every check on this
  page rests on. Its homogenised column is used, because the checks cross January 2016.
- [`Meteo_Data_SW_OUT`](Meteo_Data_SW_OUT.html) — the outgoing shortwave channel of the same
  instrument head, which shares the December 2021 boundary.
- [`Meteo_Product_Chain`](Meteo_Product_Chain.html) — where this product sits in the chain.

::: {.callout-important title="The record steps at the December 2021 radiometer exchange"}

The CNR1 was replaced by a CNR4 on 14 December 2021, and this series changes at that date by
more than it changes in any year where nothing happened. The change of screening software falls
close to the same date, but it is excluded as the cause, because the two screenings carry the
same numbers where they overlap. What remains is the instrument.

The step is **not corrected and no homogenised column is provided**: a step whose cause is
established is not the same as a step whose size is known, and correcting it would require
calibration figures the site does not hold. Filter on `FLAG_LW_OUT_T1_47_1_SOURCE` before
comparing the two eras, and drop code `3`, the 24 days in which the new instrument was read
through the old instrument's constant.

**Nothing is gap-filled**, so the value column contains `NaN` and a non-null record is a
measurement.

:::

## What the values are

The exported numbers are **upwelling longwave irradiance**: the thermal emission of the canopy
as seen from 47 m, plus the small part of the downwelling flux that the canopy reflects. The
median is **356.7 W m^-2^**, the mean 359.1, and the range 239.6 to 503.5 W m^-2^.

A pyrgeometer's voltage measures only the *net* exchange between the surface it views and the
instrument's own body, so the instrument's own emission has to be added to obtain the
irradiance. Every value in this file already includes it. A reader who mistook these values for
the converted raw voltage would be wrong by some 300 to 400 W m^-2^.

That construction also sets the scale of everything else on this page. A wrong calibration
factor scales the **net** signal and leaves the added emission term alone, and for a
downward-facing pyrgeometer above a canopy that net signal is small — a few W m^-2^ in the
median and a few tens at its extremes, against several hundred in the file. The same factor
error that costs `LW_IN` about 9 W m^-2^ in the middle of its distribution is therefore worth
far less here, which is why the checks below work on percentiles of the net signal rather than
on the level.

Two physical checks close the notebook, and both pass. The ratio of the measured value to the
Stefan-Boltzmann emission at air temperature has a nighttime median of **0.979** (5th to 95th
percentile 0.963 to 0.996) and a daytime median of 0.990, as a canopy radiating near the
temperature of the air around it must. And the site loses longwave radiation on most half-hours:
the median of `LW_IN − LW_OUT` is **−46.4 W m^-2^**, and 81 % of nighttime and 85 % of daytime
half-hours are net losses. That second check is what would catch the two channels having been
transposed somewhere between the logger and this file.

## Columns

: Columns of `13_METEO_LW_OUT_2005-2025`. {#tbl-lwout-cols}

| column | unit | description |
|---|---|---|
| `LW_OUT_T1_47_1` | W m^-2^ | Outgoing longwave radiation, as measured. Contains `NaN`. |
| `FLAG_LW_OUT_T1_47_1_SOURCE` | - | Which instrument and which calibration factor produced the value. Defined at every record. |

There is **no `ISFILLED` flag**, because nothing is filled. `PA`, `LW_IN` and `SW_OUT` are the
other meteo products exported this way.

### `FLAG_LW_OUT_T1_47_1_SOURCE`

: Provenance codes and their record counts. Shares are of the 348,958 measured records. {#tbl-lwout-source}

| code | meaning | period | records | measured | share |
|---|---|---|---|---|---|
| 0 | CNR4, this channel on its own factor of 11.33 µV/W/m^2^ | from 2022-01-07 | 69,840 | 69,724 | 20.0 % |
| 1 | CNR1, under the logger program of 7 June 2016 | 2016-06-07 to 2021-12-13 | 96,768 | 95,996 | 27.5 % |
| 2 | CNR1 at 10.03 µV/W/m^2^, the pyranometer's factor | to 2016-06-06 | 188,112 | 182,102 | 52.2 % |
| 3 | changeover, calibration undetermined | 2021-12-14 to 2022-01-06 | 1,152 | 1,136 | 0.3 % |

::: {.callout-note title="These codes are not the codes of `LW_IN`"}

The two files number their eras differently, and the boundary between codes `2` and `3` also
sits one day apart. Here code `1` is the era beginning with the June 2016 logger program, and
the whole of 14 December 2021 carries the undetermined code, because the exchange happened
during that day. [`LW_IN`](Meteo_Data_LW_IN.html) gives that day to the CNR1 and starts its
undetermined code on the following one. Do not carry a code from one file to the other.

:::

## Coverage

Of the 355,872 records, **348,958 carry a value (98.1 %)**. There are 972 gaps; 933 are one hour
or shorter and nine exceed a day.

: The five longest gaps. {#tbl-lwout-gaps}

| from | to | days | what it is |
|---|---|---|---|
| 2015-08-17 | 2015-09-27 | 41.1 | an outage of this channel alone |
| 2016-01-01 | 2016-01-21 | 20.6 | the site-wide outage during which the tower logger was replaced |
| 2019-11-04 | 2019-11-19 | 15.8 | a station outage |
| 2012-10-28 | 2012-11-09 | 13.0 | removed here: storm damage and stressed cables |
| 2012-07-29 | 2012-08-10 | 12.6 | removed here: the tower power-supply failure |

The longest gap is peculiar to this variable. The incoming channel of the same radiometer
measured through those six weeks, and reaches 99.0 % coverage for 2015 as a whole; `SW_OUT` has
no gap there either. Nothing in this product establishes what took the outgoing longwave channel
out.

Five years fall below 97 % measured: 2015 at 88.1 %, 2012 at 92.3 %, 2016 at 94.3 %, 2019 at
95.7 % and 2009 at 96.6 %. 2005 is a partial year by construction, beginning in September.

Three sets of records were removed by this product: **1,202** inside the two 2012 windows of
documented, logger-wide fault, following notebooks `01` to `03` and `06`; **one** record outside
the physical band of 150 to 600 W m^-2^; and **ten** half-hours of the radiometer exchange that
fell outside the range spanned by the same time of day on the seven days either side, when the
instrument was unmounted and no longer looking at the canopy. The **August 2012 clock error** is
corrected by the same +15.5 h shift as the other tower variables, and unlike `LW_IN` this
variable can verify the size of the shift, because the canopy heats in the sun and its emission
follows.

***

## The two screenings agree

The MeteoScreeningTool and the diive screening cover **35,032 of the same half-hours**, and on
those records they are the same series: the median difference is 0.000 W m^-2^, the RMS
difference 0.011 W m^-2^, the largest single difference 2.06 W m^-2^, and the correlation 1.000.
The two screenings reached the same numbers by different routes, so the splice between them
changes no value, and the change of screening is ruled out as a cause of anything the record does
at the turn of 2022. `LW_IN` had no such overlap and could not make that argument.

## The June 2016 calibration change reached this channel

On 7 June 2016 a new logger program corrected a radiometer calibration factor from 10.03 to
12.83 µV/W/m^2^ — the same change that leaves more than half of `LW_IN` reading low. Whether it
also reached the outgoing channel could not be settled from the maintenance record, which names
one factor without saying which channels it was written to, so it was put to the data.

The statistic is the 2nd percentile of the nighttime net signal — the measured value minus the
Stefan-Boltzmann emission at air temperature — which is where a conversion error is largest. It moves from **−15.9 W m^-2^ in 2006-2015 to −11.3 W m^-2^ in 2017-2021**, a
ratio of 0.721 that is the same at every percentile of the tail, as a change of conversion must
be. The documented factor change predicts 0.782, and the two agree well inside the year-to-year
scatter of the same statistic. The companion statistic, taken where the canopy sits at air
temperature and the net signal goes to zero so that no conversion factor can act, moves by
0.07 % across the same date. A change in the canopy or the weather has no reason to produce that
pattern.

**What this means for the values.** Before 7 June 2016 the reported net signal is too large in
magnitude by roughly a quarter, so the values read low at night, when the canopy is cooler than
the instrument, and high by day. Because the net signal is small, the error is a few W m^-2^ at
most rather than the 9 W m^-2^ the same factor costs the incoming channel. It is **not
corrected**: undoing it needs the radiometer's body temperature, a channel this product does not
read. Code `2` marks the affected era, which is more than half the record.

## The December 2021 exchange and the 24 days after it

Measured the same way, the first half of 2022 gives an envelope ratio of **0.710** against the
three preceding years, outside the 0.808 to 1.050 that the same statistic produces in years
holding no boundary. The record therefore steps at the exchange. Because the two screenings were
shown to agree, the change of screening is excluded, which leaves the instrument or the weather;
the CNR1 was replaced by a CNR4 on that date. Nothing is corrected, and the flag separates the
two instruments instead.

Between 14 December 2021 and 7 January 2022 the CNR4 was connected to a logger program written
for the CNR1, so its values were converted with the wrong sensitivity. Which of the two
candidate sensitivities was applied is not established: the program that set it does not
survive, and the June 2016 entry does not say whether its new factor reached this channel. Both
candidates were computed and neither is adopted. The resulting error is nevertheless small,
because the constant scales the net signal and not the irradiance the file reports: over that window the net signal has a
median of −0.7 W m^-2^ and a 5th-to-95th-percentile range of −3.6 to +2.7 W m^-2^, so the worst
case over both candidates is **1.6 W m^-2^ on a single half-hour, 0.5 % of the reported value**.
Code `3` isolates the interval, so a reader who needs an unambiguous calibration can drop
24 days out of a twenty-year record.

## Known limitations

- **The record is not homogeneous across December 2021.** The step is measured, its cause is
  attributed to the instrument, and its size in watts is not established. Filter on the source
  flag before comparing the two eras, and treat a trend computed across that date as containing
  the change.
- **More than half the record was converted with the pyranometer's factor.** Everything before
  7 June 2016 carries code `2` and reads low at night by roughly a quarter of the net signal,
  which is a few W m^-2^. It is not corrected, because correcting it would need the radiometer's
  body temperature.
- **The 24 days of the changeover carry an unverified conversion**, bounded above at 1.6 W m^-2^
  and not identified. Code `3` marks them.
- **There is no independent reference for this variable at the site.** MeteoSwiss Lägern carries
  no longwave channel, NABEL has no pyrgeometer, and the below-canopy sensor measures a different
  surface. Every statement above rests either on the physics of the measurement, using the
  Stefan-Boltzmann emission at air temperature as the yardstick, or on the overlap between the
  two screenings. That is weaker evidence than a second instrument, and where it does not reach,
  the product notebook says so.
- **The tests against physics use air temperature in place of two temperatures they cannot
  measure**: the canopy's, and the radiometer's own body. Both substitutions are good enough to
  put a size on an effect and not good enough to write a correction back into the data.
- **The January 2016 acquisition change did not move this series.** It is recorded here because
  the same changeover moved `TA_T1_47_1` by 1.3 °C, and because it is easy to confuse with the
  June date five months later. Every surviving logger program applies the same conversion across
  it, and the data show no change.
- **The series contains gaps and is not gap-filled.** Code that assumes a complete series will
  break or silently propagate `NaN`. If a complete series is needed — for a four-component net
  radiation, or for an energy-balance closure — fill it downstream, and do not train one model
  across a calibration boundary.
- **The six-week gap of August and September 2015 has no established cause**, and it is why 2015
  is the least complete year of the record. No other channel of the same instrument shares it.
- **The 2012 windows were removed without evidence from this series**, as in `06`. A documented,
  logger-wide fault covers them, and this variable has no reference that could reveal a level
  error if one were present.
