# Outgoing shortwave radiation at 47 m

Half-hourly outgoing (reflected) shortwave radiation at 47 m on the CH-LAE tower, 2005-2025,
exported as measured. The file is `12_METEO_SW_OUT_2005-2025` (parquet and CSV): **355,872
records** on a continuous 30-minute middle-timestamp index (named `TIMESTAMP_MIDDLE` in the
file) in local time (UTC+1, no daylight saving), from 2005-09-14 00:15 to 2025-12-31 23:45. The
first measurement is at 2005-09-14 11:15.

Method, evidence and checks:

- [`12_METEO_SW_OUT`](notebooks/10_METEO/30_PRODUCTS/12_METEO_SW_OUT_2005-2025.html) — builds
  the product: the merge of the two screenings and the measurement that shows them to be on one
  scale, the 2012 corrections, the nighttime offset, and the identification of the instrument
  and the conversion constant behind each part of the record.
- [`SW_OUT_T1_47_1`](notebooks/10_METEO/20_SCREENING/SW_OUT/SW_OUT_T1_47_1_2020-2025.html) — the
  screening of the current era, which corrects the raw record before this product reads it.
- [`01_METEO_SW_IN`](notebooks/10_METEO/30_PRODUCTS/01_METEO_SW_IN_2004-2025.html) — the
  incoming channel of the same radiometer. It is this product's only diagnostic partner, because
  `SW_OUT / SW_IN` is the surface albedo, and it is also the denominator of every albedo figure
  quoted below.
- [`Meteo_Data_LW_OUT`](Meteo_Data_LW_OUT.html) — the outgoing longwave channel of the same
  instrument head, which shares the December 2021 boundary.
- [`Meteo_Product_Chain`](Meteo_Product_Chain.html) — where this product sits in the chain.

::: {.callout-important title="One value column, and which flag matters"}

The file carries **two** flags for one value column, because the record has two boundaries and
they fall on different dates.

- **`FLAG_SW_OUT_T1_47_1_INSTRUMENT` is the one that marks a real break.** The radiometer was
  replaced on 14 December 2021, and the two instruments convert this channel differently. Filter
  on it before comparing values across that date, and drop code `2`, the weeks in which the new
  instrument was still read through the old instrument's constant, before using December 2021 or
  early January 2022 at all.
- **`FLAG_SW_OUT_T1_47_1_SOURCE` is provenance, not a warning.** It names the screening that
  produced each value. The two screenings were measured against each other on two years of
  simultaneous records and agree to 0.03 %, so a trend or a multi-year mean may be taken straight
  across the boundary between them. There is **no `_HOMOGENIZED` column** for the same reason.

**Nothing is gap-filled**, so the value column contains `NaN` and a non-null record is a
measurement. Nighttime values are exactly `0`, which is a physical statement rather than a gap.

:::

## What the values are

The exported numbers are **upwelling shortwave irradiance** above the canopy. This stand
reflects roughly a tenth of the shortwave that falls on it, so the values are an order of
magnitude smaller than `SW_IN`: the daylight median is **22.0 W m^-2^**, the daylight mean
32.4 W m^-2^, and the largest half-hour of the record is 236.2 W m^-2^. Over the whole record,
including nights, the median is 0.2 W m^-2^.

Dividing this variable by `SW_IN` gives the surface albedo, which is what most analyses want.
Over the 157,444 half-hours with an incoming flux above 20 W m^-2^ and a measured reflected
flux, the **median ratio is 0.112**. Thirty-five of them (0.022 %) give a ratio above 1.05; they
sit at low incoming flux and 28 fall between December and March, which is what snow on the
upward-facing sensor and a low sun produce.

## Columns

: Columns of `12_METEO_SW_OUT_2005-2025`. {#tbl-swout-cols}

| column | unit | description |
|---|---|---|
| `SW_OUT_T1_47_1` | W m^-2^ | Outgoing shortwave radiation, as measured and corrected. Contains `NaN`; exactly `0` at night. |
| `FLAG_SW_OUT_T1_47_1_SOURCE` | - | Which screening produced the value. Defined at every record. |
| `FLAG_SW_OUT_T1_47_1_INSTRUMENT` | - | Which radiometer produced the value, and with which conversion constant. Defined at every record. |

There is **no `ISFILLED` flag**, because nothing is filled. `PA`, `LW_IN` and `LW_OUT` are the
other meteo products exported this way.

### `FLAG_SW_OUT_T1_47_1_SOURCE`

: Screening codes and their record counts. Shares are of the 351,612 measured records. {#tbl-swout-source}

| code | meaning | records | measured | share |
|---|---|---|---|---|
| 0 | diive screening, from 2020 | 70,048 | 70,048 | 19.9 % |
| 1 | MeteoScreeningTool, measured to be on the same scale | 282,776 | 281,564 | 80.1 % |
| 2 | neither screening ever supplied this half-hour | 3,048 | 0 | 0 % |

Code `2` is not the same as a gap. A half-hour that one screening supplied and this product then
discarded — a record inside the 2012 damage windows, for instance — keeps that screening's code
and carries `NaN`. Code `2` says that nothing was ever offered for the slot.

### `FLAG_SW_OUT_T1_47_1_INSTRUMENT`

: Instrument codes and their record counts. Shares are of the measured records. {#tbl-swout-instrument}

| code | meaning | period | records | measured | share |
|---|---|---|---|---|---|
| 0 | CNR4, this channel on its own constant of 14.38 µV/W/m^2^ | from 2022-01-07 | 69,840 | 69,760 | 19.8 % |
| 1 | CNR1, one constant of 10.03 µV/W/m^2^ for all four channels of the head | to 2021-12-14 13:15 | 284,907 | 280,729 | 79.8 % |
| 2 | changeover: the CNR4 installed, the CNR1's constant still in the logger program | 2021-12-14 13:45 to 2022-01-06 23:45 | 1,125 | 1,123 | 0.3 % |

There is deliberately **no code for either 2016 date**. The tower logger was replaced in January
2016 and a radiometer calibration factor was corrected in June 2016, and neither moved this
channel; see *The two 2016 dates* below. A code for a boundary the data deny would invite a
reader to difference across it, find nothing, and then distrust the rest of the file.

## Coverage

Of the 355,872 records, **351,612 carry a value (98.8 %)**. The gaps are short: there are 452 of
them, 431 are one hour or shorter, and only seven exceed a day.

: The five longest gaps. {#tbl-swout-gaps}

| from | to | days | what it is |
|---|---|---|---|
| 2016-01-01 | 2016-01-21 | 20.6 | the site-wide outage during which the tower logger was replaced |
| 2019-11-04 | 2019-11-19 | 15.8 | a station outage |
| 2012-10-28 | 2012-11-09 | 13.0 | removed here: storm damage and stressed cables |
| 2012-07-29 | 2012-08-10 | 12.6 | removed here: the tower power-supply failure |
| 2009-08-05 | 2009-08-15 | 9.8 | a station outage |

Four years fall below 98 % measured: 2012 at 92.7 %, 2016 at 94.3 %, 2019 at 95.7 % and 2009 at
96.9 %. The 2012 figure is the one this product created: 1,212 records were removed inside the
two windows of documented, logger-wide fault, following notebooks `01` to `03` and `06`. The
albedo can detect a fault confined to the reflected channel, because the incoming channel is
then the reference, but it cannot see one that moved both channels of the same head together,
which is what a power-supply problem does. The windows are therefore removed on the strength of
the maintenance record rather than on evidence from this series.

Two corrections change values rather than removing them. The **August 2012 clock error** is
corrected by the same +15.5 h shift as the other tower variables, and unlike `LW_IN` this
variable can check it: reflected shortwave follows the sun, so the correlation against potential
radiation says whether the block has been put back on the sun's clock. The **nighttime
zero-offset** is removed per day over the whole record, because only the newer of the two
screenings had already done it; without that step the first sixteen years would carry an offset
that the last four do not.

***

## The two screenings

The two screenings did not read the same input files. The MeteoScreeningTool read delivered CSV
files, whereas the diive screening reads the raw record, so the two could in principle have
converted the same voltages with different constants. They overlap for two full years while both
describe the same instrument, which makes the question a measurement rather than an argument.

On 14,542 well-illuminated half-hours that both versions report, spread over 24 calendar months,
the **measured factor is 0.99970, a difference of 0.03 %**, and the ratio of their standard
deviations is 0.99955. The smallest conversion difference this site is known to have produced is
3.5 %, which is 118 times larger, so this is a measurement of no difference rather than a test
too blunt to find one. The two eras are spliced without rescaling, and no `_HOMOGENIZED` column
is exported: a duplicate column would invite a reader to difference it, get zero, and draw a
conclusion from that.

## The two 2016 dates

Two changes fall four months apart in 2016. The tower logger was replaced in January, and in
June a new logger program corrected a radiometer calibration factor from 10.03 to
12.83 µV/W/m^2^ — the change that notebook `06` finds in `LW_IN`. If that factor had reached the
outgoing shortwave channel, the albedo would have stepped by about a fifth, because only one of
the two constants in the ratio would have changed.

It did not. The season-controlled albedo moves by **−1.0 % across both 2016 dates**, against
−5.3 % for a placebo pair of periods inside the earlier era in which nothing happened, and
against the −21.8 % a change of factor on this channel alone would produce. The record is
homogeneous across both dates, which is why the instrument flag gives them no code. The product
notebook turns that negative result into an assertion, so a re-run that ever does find such a
step fails there rather than exporting a file that reports a calibration change as a change in
the canopy.

## The December 2021 radiometer exchange

The CNR1 was replaced by a CNR4 on 14 December 2021, and the conversion changed with it. The
CNR1's logger programs convert all four of its channels with a single constant, so at least
three of the four were converted with a constant that is not their own; the CNR4's two shortwave
channels each have their own, and they differ from each other by 3.5 %. That much is documented,
and it is why the instrument flag exists.

**How large the resulting step is, this product cannot say.** The season-controlled albedo
differs by 4.2 % between the two instruments, but the same statistic applied to two periods of
the CNR4 era, in which no instrument changed, differs by 10.0 %. The stand's growing-season
albedo moves from year to year by more than the two instruments do, so the older instrument's own
channel mismatch is not separable from that movement with the years available. Nothing is
corrected, because undoing the change would need the CNR1's two true detector sensitivities and
nothing at this site recorded them.

The weeks between the new instrument going up and its constants reaching the logger program are a
separate question, and code `2` isolates them. Measured against the MeteoSwiss Lägern station,
which sees the incoming channel independently, the changeover window sits **8.3 % away from an
ordinary winter**, whereas the CNR1's constant still being in force would put it 38.5 % away —
2.1 against 7.5 interquartile widths of the between-winter scatter. That is evidence against the
old constant having been in force, not a demonstration that the window is clean. Seven winters of
a midwinter statistic can rule out an error of tens of per cent and cannot rule out a small one,
and the test speaks for the incoming channel, whose constant was a different number in the same
program. The window keeps its own code either way.

## Known limitations

- **The record is not homogeneous across 14 December 2021**, and the size of the step is not
  established. Filter on `FLAG_SW_OUT_T1_47_1_INSTRUMENT` before comparing values or albedos
  across that date, and treat any trend computed across it as containing an unquantified
  instrument change.
- **The 24 days of the changeover carry an unverified conversion.** Code `2` marks them. The
  MeteoSwiss comparison argues against the old constant having been in force, but it does not
  establish which constant was.
- **The CNR1 era carries the instrument's own channel mismatch, and it is unquantified.** All
  four channels of that head were converted with a single constant, although the factory
  calibrates each detector separately. Because both shortwave channels were divided by the same
  number, that number cancels in their ratio, so the albedo of the CNR1 era does not depend on
  the instrument's absolute scale. What does not cancel is that the two detectors really do
  differ and were read as though they did not: the reflected flux of that era, and the albedo
  with it, carries the difference between the two sensitivities. It is a fixed scale error
  inside the era rather than a break, so it does not disturb comparisons made within it.
- **The series contains gaps and is not gap-filled.** Code that assumes a complete series will
  break or silently propagate `NaN`. Gap-filling would need something that measures what this
  canopy reflects, and nothing does: MeteoSwiss Lägern and NABEL carry the incoming channel only,
  and the site's other outgoing shortwave sensor sits below the canopy and sees a different
  quantity. If a complete series is needed, fill it downstream and do not train one model across
  the December 2021 boundary.
- **There is no independent reference for this variable.** Every quantitative statement above is
  made in the ratio against the incoming channel of the same instrument, which cancels anything
  that scaled both channels together — a supply voltage, a dirty dome — and therefore cannot see
  it either.
- **The 2012 windows were removed without evidence from this series.** They rest on the
  documented, logger-wide fault, as in `01` to `03` and `06`. Where the fault moved both channels
  of the head together, the albedo would not have shown it.
- **Coverage counts nighttime zeros as measurements.** In the diive era the screening set every
  nighttime position to zero, gaps included. That is physically right, since with no incoming
  shortwave there is none reflected, but it means a nighttime record from 2020 onwards is a known
  value rather than a delivered measurement, and the coverage of those years is not strictly
  comparable with the earlier era's.
- **A candidate window in July 2024 was left in the data.** The screening notebook records
  2024-07-14 to 2024-07-19 as a period to remove, but the removal was never committed, so those
  records are in this file. The albedo over the window is 2.6 % below the surrounding weeks,
  which is not enough to set it apart from how those weeks differ among themselves, and the
  maintenance record names nothing that would explain a fault in this channel. The window is
  neither removed nor flagged; settling it belongs in the screening notebook.
- **The October 2010 rebuild of the MeteoSwiss Lägern station** changes nothing in this file, but
  it steps that station's incoming shortwave by about 5 %. Any comparison of this product against
  Lägern that crosses that date carries the step. The changeover test above uses only winters
  well after it.
