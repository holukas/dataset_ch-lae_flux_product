# Air pressure at 47 m

Half-hourly atmospheric pressure at 47 m on the CH-LAE tower, September 2005 to September
2026, exported as measured. The file is `05_METEO_PA_2005-2026.09` (parquet and CSV):
**369,552 records** on a continuous 30-minute index `TIMESTAMP_MIDDLE` (middle of the
half-hour, UTC+01:00, no daylight saving), from 2005-09-02 00:15 to 2026-09-30 23:45.

The [interactive dashboard](dashboards/METEO_PA_dashboard.html) summarises the product on
one page. It is still built from the 2004-2025 version of the product and ends in December 2025.

Method, evidence and checks:

- [`05_METEO_PA`](notebooks/10_METEO/30_PRODUCTS/05_METEO_PA_2005-2026.09.html): builds
  the product: unit harmonisation of the two screenings, 2012 corrections, identification
  of the barometer from the logger programs, the check of the absolute level against the
  barometric formula, and the two hardware boundaries.
- [Meteo Product Chain](Meteo_Product_Chain.html): no other meteo product is computed from
  this one.

::: {.callout-note title="One column, no flag, gaps left in"}

This product is not gap-filled. There is one value column and no flag column. About 1 % of
the record is missing: a non-null value is a measurement and a `NaN` is a real gap.

There is no `_HOMOGENIZED` column, although the record changes level by about 0.09 kPa at
the January 2016 acquisition change. See [Known limitations](#known-limitations) for what
to do about it.

:::

## Columns

: Columns of `05_METEO_PA_2005-2026.09`. {#tbl-pa-cols}

| column | unit | description |
|---|---|---|
| `PA_T1_47_1` | kPa | Atmospheric pressure at 47 m, measured and corrected. Gaps are `NaN`. |

The unit is **kPa**, the FLUXNET convention. The database stores the two screenings in
different units, `kPa` before 2022 and `Pa` after, because the two loggers wrote different
units. The notebook harmonises them from the magnitude of the data and stops if that result
disagrees with the database unit tag. Measured values range from **89.45 to 95.54 kPa**,
with a median of 93.31 kPa.

## Coverage

**365,542 of the 369,552 records carry a value, 98.9 %.** The record begins on 2005-09-02,
when the archive of this logger begins; the barometer was already in service, but no
earlier data are held. There is no `PA` for 2004 and the first eight months of 2005, and
none is reconstructed, so this product starts later than `SW_IN`, `TA` and `PPFD_IN`.

Of 415 gaps, 399 are one hour or shorter. The longest is the 20.6-day outage of January
2016, during which the tower logger was replaced.

: Years in which measured coverage is not near-complete. Every other full year of
2006-2025 is at least 99.3 % measured, and January to September 2026 is 100 % measured. {#tbl-pa-coverage}

| year | measured | why |
|---|---|---|
| 2005 | 99.4 % of 2 Sep to 31 Dec | the record begins on 2 September |
| 2009 | 97.0 % | a 9.8-day outage in August |
| 2010 | 98.9 % | outages |
| 2012 | 94.1 % | power-supply failure and storm damage |
| 2016 | 94.3 % | the January outage during which the logger was replaced |
| 2019 | 95.7 % | outages |

In 2012 a logger clock error shifted one block of August by 15.5 hours and was corrected.
A tower power-supply failure in late July and August and storm damage in late October and
November left biased values, and those periods were removed. The removal windows come from
this variable's own disagreement with the independent hut barometer, so they do not
coincide exactly with the windows of `SW_IN`, `TA` and `PPFD_IN`. Use each product's own
missing values rather than assuming the products exclude identical periods.

## The sensor and its absolute level

The instrument is a **Vaisala PTB101B** barometer. Every logger program that has measured
it, the six CR10X programs of 2004-2006 and the CR1000 program installed in January 2016,
converts its signal with the same multiplier and offset, spanning 600 to 1060 hPa, the
range of that barometer. The maintenance record does not name the instrument in twenty-one
years: as far as the record goes it was never replaced, calibrated or cleaned, and it is not
in the device inventory.

Pressure is the one meteo variable here whose **absolute** level can be checked against
physics, and it passes. The barometric formula, with nothing fitted to the tower data,
predicts the difference between this barometer and each reference from that reference's
own pressure, temperature and humidity. It places the barometer within 5 m of its nominal
elevation using MeteoSwiss Lägern (2.5 km away at 845 m, about 110 m above the barometer)
and within 9 m using the NABEL barometer at the hut; the two references agree with each
other to 4 m. It also reproduces the annual wave in the difference between two barometers
at different heights (89 Pa measured, 79 Pa predicted, correlation 0.98). A unit error, a
wrong offset or a lost factor of ten would fail this check by orders of magnitude.

## The January 2016 acquisition change

It moved the level by about **0.09 kPa**, the only hardware change in this record with a
measurable effect.

The barometer and its conversion did not change. The logger did: the CR10X measured the
sensor single-ended, the CR1000 measures it differentially. A single-ended measurement
includes any offset between the sensor's ground and the logger's; a differential one does
not.

Three barometers place the change on the tower. Both differences involving the tower move
across 2016, by -0.0884 and -0.0888 kPa, while the difference between the two references
moves by -0.0001 kPa. The barometric prediction shows which era is correct: averaged over
2016 to 2025, the later era agrees with the prediction against both references and the
earlier era lies about 0.1 kPa above it. Year by year, the departure of the later era from
the prediction against Lägern goes from +0.017 kPa in 2016 to -0.061 kPa in 2025 and
-0.074 kPa in January to September 2026 (the drift under
[Known limitations](#known-limitations)). **The record before
21 January 2016 therefore reads approximately 0.09 kPa high.**

The 20.6-day outage that ends on 21 January 2016 brackets the step, so it cannot be dated
more precisely. The logger program on disk is dated 18 January 2016, and the maintenance
record names the same program file.

The December 2021 change of screening software has no effect here: the difference against
MeteoSwiss changes less across that boundary than in an ordinary year.

## Known limitations {#known-limitations}

- **The record is not homogeneous across 21 January 2016, and is not corrected.** Values
  before that date read approximately 0.09 kPa high. No homogenised column is provided: the
  step is one part in a thousand of the value (under ten metres of air), so air density and
  the flux quantities computed from it change by the same one part in a thousand; a
  rescaled column would change the set of columns this product and the merged product ship;
  and a residual drift of the same size (next point) would remain after any homogenisation.
  **For one absolute level across the whole record, subtract 0.09 kPa from the records
  before 21 January 2016.** Analyses within a year, or of pressure changes rather than
  levels, are unaffected.
- **A slow drift of about 0.1 kPa over twenty years cannot be attributed.** Apart from the
  two dated events, the difference between this barometer and MeteoSwiss Lägern falls by
  approximately 0.1 kPa across the record. Slightly more than half of that falls after
  mid-2018, when the second barometer at the site stops, so no third instrument can show
  which of the two is moving. It develops over years, so there is no boundary for a
  correction, and the barometric formula cannot settle it because it is computed from
  Lägern's own pressure. January to September 2026 continues the drift: the difference
  against Lägern lies 0.023 kPa below the same months of 2025, the largest year-on-year
  change since 2016, but below the 0.04 kPa at which the notebook counts an event.
- **The MeteoSwiss Lägern pressure changed level in October 2010.** The rebuild of that
  station's instrumentation that moved its radiation record also moved `PA_LAE_MS`, by
  approximately 0.06 to 0.07 kPa relative to both barometers at this site. This product
  never uses Lägern to correct a value, but **do not read a difference between this product
  and MeteoSwiss Lägern as evidence about the tower across that date.**
- **The NABEL hut barometer is not independent after July 2018.** The database series
  `PA_NABEL_H1_2_1` runs nominally to the end of 2018, but from 3 July 2018 its values
  repeat the tower series to five decimal places. The notebook truncates the reference
  there. Any other use of that series should do the same.
- **The record begins in September 2005.** When joining this product to `SW_IN`, `TA` or
  `PPFD_IN`, whose index starts on 2004-01-01, expect a shorter series.
