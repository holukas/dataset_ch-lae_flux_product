# Outgoing shortwave radiation at 47 m

Half-hourly outgoing (reflected) shortwave radiation at 47 m on the CH-LAE tower, 2005-2025,
exported as measured. The file is `12_METEO_SW_OUT_2005-2025` (parquet and CSV): **355,872
records** on a continuous 30-minute index, `TIMESTAMP_MIDDLE` (middle of the half-hour), in local
time (UTC+01:00, no daylight saving), from 2005-09-14 00:15 to 2025-12-31 23:45. The first
measurement is at 2005-09-14 11:15.

The series ends on 31 December 2025. It is part of [FP2026.1](Dataset_Versions.html) and of the
[merged meteo product](notebooks/10_METEO/30_PRODUCTS/99_METEO_MERGED_2004-2026.09.html), where it
is `NaN` from 1 January 2026; the extension to 30 September 2026 is in progress.

The [interactive dashboard](dashboards/METEO_SW_OUT_dashboard.html) summarises coverage,
provenance, seasonality, distributions, extremes and trends. Its instrument card shows how much of
each year came from the CNR1, the changeover window and the CNR4.

Notebooks:

- [`12_METEO_SW_OUT`](notebooks/10_METEO/30_PRODUCTS/12_METEO_SW_OUT_2005-2025.html): builds the
  product. It merges the two screenings and shows that they are on one scale, applies the 2012
  corrections and the nighttime offset, and identifies the instrument and conversion constant
  behind each part of the record.
- [`SW_OUT_T1_47_1`](notebooks/10_METEO/20_SCREENING/SW_OUT/SW_OUT_T1_47_1_2020-2025.html): the
  screening of the current era.
- [`01_METEO_SW_IN`](notebooks/10_METEO/30_PRODUCTS/01_METEO_SW_IN_2004-2026.09.html): the
  incoming channel of the same radiometer. `SW_OUT / SW_IN` is the surface albedo, which is the
  only diagnostic available for this product and the basis of every albedo figure below.
- [`Meteo_Data_LW_OUT`](Meteo_Data_LW_OUT.html): the outgoing longwave channel of the same
  instrument, with the same December 2021 boundary.
- [`Meteo_Product_Chain`](Meteo_Product_Chain.html): where this product sits in the chain.

::: {.callout-important title="One value column, and which flag matters"}

The file has **two** flags for one value column, because the record has two boundaries on
different dates.

- **`FLAG_SW_OUT_T1_47_1_INSTRUMENT` marks a real break.** The radiometer was replaced on
  14 December 2021, and the two instruments convert this channel differently. Filter on this flag
  before comparing values across that date. Drop code `2`, the weeks in which the new instrument
  was still read with the old instrument's constant, before using December 2021 or early January
  2022.
- **`FLAG_SW_OUT_T1_47_1_SOURCE` is provenance only.** It names the screening that produced each
  value. The two screenings agree to 0.03 % on two years of simultaneous records, so trends and
  multi-year means may be taken across the boundary between them. For the same reason there is
  **no `_HOMOGENIZED` column**.

**Nothing is gap-filled**, so the value column contains `NaN` and every non-null record is a
measurement. Nighttime values are exactly `0`, which is a physical value, not a gap.

:::

## What the values are

The values are **upwelling shortwave irradiance** above the canopy. The stand reflects roughly a
tenth of the incoming shortwave, so the values are an order of magnitude smaller than `SW_IN`: the
daylight median is **22.0 W m^-2^**, the daylight mean 32.4 W m^-2^, and the largest half-hour
236.2 W m^-2^. Over the whole record, nights included, the median is 0.2 W m^-2^.

Dividing by `SW_IN` gives the surface albedo. Over the 157,444 half-hours with an incoming flux
above 20 W m^-2^ and a measured reflected flux, the **median ratio is 0.112**. Thirty-five of them
(0.022 %) give a ratio above 1.05. They occur at low incoming flux, and 28 fall between December
and March, as expected from snow on the upward-facing sensor and a low sun.

## Columns

: Columns of `12_METEO_SW_OUT_2005-2025`. {#tbl-swout-cols}

| column | unit | description |
|---|---|---|
| `SW_OUT_T1_47_1` | W m^-2^ | Outgoing shortwave radiation, as measured and corrected. Contains `NaN`; exactly `0` at night. |
| `FLAG_SW_OUT_T1_47_1_SOURCE` | - | Which screening produced the value. Defined at every record. |
| `FLAG_SW_OUT_T1_47_1_INSTRUMENT` | - | Which radiometer produced the value, and with which conversion constant. Defined at every record. |

There is **no `ISFILLED` flag**, because nothing is filled. `PA`, `LW_IN` and `LW_OUT` are exported
the same way.

### `FLAG_SW_OUT_T1_47_1_SOURCE`

: Screening codes and their record counts. Shares are of the 351,612 measured records. {#tbl-swout-source}

| code | meaning | records | measured | share |
|---|---|---|---|---|
| 0 | diive screening, from 2022 | 70,048 | 70,048 | 19.9 % |
| 1 | MeteoScreeningTool, to the end of 2021, shown to be on the same scale | 282,776 | 281,564 | 80.1 % |
| 2 | neither screening supplied this half-hour | 3,048 | 0 | 0 % |

Code `2` is not the same as a gap. A half-hour that a screening supplied and this product then
removed (for example a record inside the 2012 fault windows) keeps that screening's code and is
`NaN`. Code `2` means that no value was ever supplied.

### `FLAG_SW_OUT_T1_47_1_INSTRUMENT`

: Instrument codes and their record counts. Shares are of the measured records. {#tbl-swout-instrument}

| code | meaning | period | records | measured | share |
|---|---|---|---|---|---|
| 0 | CNR4, this channel with its own constant of 14.38 µV/W/m^2^ | from 2022-01-07 | 69,840 | 69,760 | 19.8 % |
| 1 | CNR1, one constant of 10.03 µV/W/m^2^ for all four channels | to 2021-12-14 13:15 | 284,907 | 280,729 | 79.8 % |
| 2 | changeover: CNR4 installed, CNR1 constant still in the logger program | 2021-12-14 13:45 to 2022-01-06 23:45 | 1,125 | 1,123 | 0.3 % |

There is **no code for either 2016 date**. The tower logger was replaced in January 2016 and a
radiometer calibration factor was corrected in June 2016, and neither moved this channel (see *The
two 2016 dates*).

## Coverage

Of the 355,872 records, **351,612 have a value (98.8 %)**. Most gaps are short: of 452 gaps, 431
are one hour or shorter and seven exceed a day.

: The five longest gaps. {#tbl-swout-gaps}

| from | to | days | cause |
|---|---|---|---|
| 2016-01-01 | 2016-01-21 | 20.6 | site-wide outage during the tower logger replacement |
| 2019-11-04 | 2019-11-19 | 15.8 | station outage |
| 2012-10-28 | 2012-11-09 | 13.0 | removed in this product: storm damage and stressed cables |
| 2012-07-29 | 2012-08-10 | 12.6 | removed in this product: tower power-supply failure |
| 2009-08-05 | 2009-08-15 | 9.8 | station outage |

Four years are below 98 % measured: 2012 at 92.7 %, 2016 at 94.3 %, 2019 at 95.7 % and 2009 at
96.9 %. The 2012 figure results from this product: 1,212 records were removed inside the two
windows of documented logger-wide fault, as in notebooks `01` to `03` and `06`.

Two corrections change values. The **August 2012 clock error** is corrected by the same +15.5 h
shift as the other tower variables. Unlike `LW_IN`, this variable can confirm the shift, because
reflected shortwave follows the sun and its correlation with potential radiation shows whether the
block is on the solar clock. The **nighttime zero offset** is removed per day over the whole
record, because only the newer screening had removed it; without this step the first sixteen years
would carry an offset that the last four do not.

***

## The two screenings

The two screenings read different inputs: the MeteoScreeningTool read delivered CSV files, the
diive screening reads the raw record. They could therefore have converted the same voltages with
different constants. They overlap for two full years on the same instrument, which allows a direct
comparison.

On 14,542 well-illuminated half-hours that both report, spread over 24 calendar months, the
**factor between them is 0.99970 (0.03 %)**, and the ratio of their standard deviations is
0.99955. The smallest conversion difference known at this site is 3.5 %, 118 times larger. The two
eras are therefore joined without rescaling, and no `_HOMOGENIZED` column is exported.

## The two 2016 dates

The tower logger was replaced in January 2016. In June 2016 a new logger program changed a
radiometer calibration factor from 10.03 to 12.83 µV/W/m^2^; this is the change that notebook `06`
finds in `LW_IN`. Had that factor reached the outgoing shortwave channel, the albedo would have
stepped by about a fifth, because only one of the two constants in the ratio would have changed.

It did not. The season-controlled albedo moves by **−1.0 % across both 2016 dates**, compared with
−5.3 % for a placebo pair of periods within the earlier era and −21.8 % expected from a factor
change on this channel alone. The record is homogeneous across both dates. The product notebook
asserts this, so a re-run that finds such a step fails instead of exporting it.

## The December 2021 radiometer exchange

The CNR1 was replaced by a CNR4 on 14 December 2021, and the conversion changed with it. The CNR1
logger programs convert all four channels with a single constant, so at least three of the four
were converted with a constant that is not their own. The two shortwave channels of the CNR4 each
have their own constant, and these differ by 3.5 %.

**The size of the resulting step cannot be determined from this product.** The season-controlled
albedo differs by 4.2 % between the two instruments, but the same statistic differs by 10.0 %
between two periods of the CNR4 era in which nothing changed. The growing-season albedo of the
stand varies from year to year by more than the instrument difference, so the CNR1's channel
mismatch cannot be separated from it with the years available. Nothing is corrected: that would
require the CNR1's two detector sensitivities, which were not recorded at this site.

Code `2` isolates the weeks between the installation of the CNR4 and the update of its constants
in the logger program. Compared with MeteoSwiss Lägern, which measures the incoming channel
independently, the changeover window is **8.3 % away from an ordinary winter**. If the CNR1
constant had still been in force, it would be 38.5 % away; these are 2.1 and 7.5 interquartile
widths of the between-winter scatter. This is evidence against the old constant having been in
force, but not proof that the window is correct. Seven winters can rule out an error of tens of
per cent, not a small one, and the test applies to the incoming channel, whose constant in the same
program was a different number. The window keeps its own code either way.

## Known limitations

- **The record is not homogeneous across 14 December 2021**, and the size of the step is not
  known. Filter on `FLAG_SW_OUT_T1_47_1_INSTRUMENT` before comparing values or albedos across that
  date, and treat any trend across it as containing an unquantified instrument change.
- **The 24 days of the changeover have an unverified conversion.** Code `2` marks them. The
  MeteoSwiss comparison argues against the old constant, but does not establish which constant was
  applied.
- **The CNR1 era carries an unquantified channel mismatch.** All four channels were converted with
  one constant, although each detector has its own factory calibration. Because both shortwave
  channels were divided by the same number, it cancels in their ratio, so the CNR1-era albedo does
  not depend on the absolute scale. The real difference between the two detectors does not cancel:
  the reflected flux of that era, and its albedo, include the difference between the two
  sensitivities. It is a fixed scale error within the era, not a break, so comparisons within the
  era are not affected.
- **The series contains gaps and is not gap-filled.** Code that assumes a complete series will
  fail or propagate `NaN`. Nothing else measures what this canopy reflects: MeteoSwiss Lägern and
  NABEL measure incoming shortwave only, and the site's other outgoing shortwave sensor is below the
  canopy. If a complete series is needed, fill it downstream, and do not train one model across the
  December 2021 boundary.
- **There is no independent reference.** Every quantitative statement above uses the ratio to the
  incoming channel of the same instrument. This ratio cancels anything that scaled both channels
  together (a supply voltage, a dirty dome), and therefore cannot detect it.
- **The 2012 windows were removed without evidence from this series.** They rest on the
  documented logger-wide fault, as in `01` to `03` and `06`. The albedo can detect a fault in the
  reflected channel alone, not one that moved both channels of the instrument together, as a
  power-supply problem does.
- **Coverage counts nighttime zeros as measurements.** In the diive era the screening set every
  nighttime value to zero, including gaps. This is physically correct, but from 2022 a nighttime
  record is a known value rather than a delivered measurement, and the coverage of those years is
  not strictly comparable with that of the earlier era.
- **A candidate removal window in July 2024 is still in the data.** The screening notebook lists
  2024-07-14 to 2024-07-19 for removal, but the removal was not committed. The albedo over the
  window is 2.6 % below the surrounding weeks, which is within how those weeks differ among
  themselves, and the maintenance record names no fault in this channel. The window is neither
  removed nor flagged; it is to be settled in the screening notebook.
- **The October 2010 rebuild of the MeteoSwiss Lägern station** changes nothing in this file, but
  it steps that station's incoming shortwave by about 5 %. A comparison of this product with Lägern
  across that date includes the step. The changeover test above uses only winters well after it.
