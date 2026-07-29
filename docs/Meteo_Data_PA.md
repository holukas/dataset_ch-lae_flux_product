# Air pressure at 47 m

Half-hourly atmospheric pressure measured at 47 m on the CH-LAE tower,
2005-2025, exported as measured. The file is `05_METEO_PA_2005-2025` (parquet
and CSV): **356,448 records** on a continuous 30-minute middle-timestamp index
(named `TIMESTAMP_MIDDLE` in the file) in local time (UTC+1, no daylight
saving), from 2005-09-02 00:15 to 2025-12-31 23:45.

The notebooks behind this page carry the full method, the evidence and the
checks:

- [`05_METEO_PA`](notebooks/10_METEO/30_PRODUCTS/05_METEO_PA_2004-2025.html)
  — builds the product: the unit harmonisation of the two screenings, the 2012
  corrections, the identification of the barometer from the logger programs, the
  check of the absolute level against the barometric formula, and the two
  hardware boundaries.
- [`Meteo_Product_Chain`](Meteo_Product_Chain.html) — where this product sits in
  the chain. No other meteo product is computed from it.

::: {.callout-note title="One column, no flag, and gaps left in"}

`SW_IN`, `TA` and `PPFD_IN` are complete, gap-filled products with a provenance
flag. This one is not. There is a single value column, no flag column, and about
1 % of the record is missing: a non-null value is a measurement and a `NaN` is a
real gap. Code that assumes a complete series has to handle the gaps explicitly.

There is also no `_HOMOGENIZED` column, although the record does change level at
the January 2016 acquisition change. The step is small and is described under
[Known limitations](#known-limitations), together with what to do about it.

:::

## Columns

: Columns of `05_METEO_PA_2005-2025`. {#tbl-pa-cols}

| column | unit | description |
|---|---|---|
| `PA_T1_47_1` | kPa | Atmospheric pressure at 47 m, measured and corrected. Gaps are `NaN`. |

The unit is **kPa**, the FLUXNET convention. The database stores the two
screenings of this measurement in different units — `kPa` before 2022 and `Pa`
after — because the two loggers wrote different units. The notebook harmonises
them from the magnitude of the data and refuses to proceed if that verdict
disagrees with the unit tag the database carries.

Measured values range from **89.45 to 95.54 kPa**, with a median of 93.31 kPa.

## Coverage

**352,438 of the 356,448 records carry a value, 98.9 %.** The record begins on
2005-09-02, when the archive of this logger begins; the barometer itself was
already in service, but no earlier data are held. There is no `PA` for 2004 and
for the first eight months of 2005, and none is reconstructed, so the index of
this product starts later than that of `SW_IN`, `TA` and `PPFD_IN`.

Gaps are short except where a logger was out of service. Of 415 separate gaps,
399 are one hour or shorter; the longest is the 20.6-day outage of January 2016
during which the tower logger was replaced.

: The years in which measured coverage is not near-complete. Every other full
year of 2006-2025 is at least 99.3 % measured. {#tbl-pa-coverage}

| year | measured | why |
|---|---|---|
| 2005 | 99.4 % of 2 Sep to 31 Dec | the record begins on 2 September |
| 2009 | 97.0 % | outages |
| 2010 | 98.9 % | outages |
| 2012 | 94.1 % | power-supply failure and storm damage |
| 2016 | 94.3 % | the January outage during which the logger was replaced |
| 2019 | 95.7 % | outages |

The 2012 faults are the largest interruption inside the measured period. A
logger clock error shifted one block of August 2012 by 15.5 hours and was
corrected; a tower power-supply failure in late July and August and storm damage
in late October and November left values that were biased rather than missing,
and those periods were removed. The removal windows were derived from this
variable's own disagreement with the independent hut barometer rather than
copied from the other products, so they do not coincide exactly with the windows
used for `SW_IN`, `TA` and `PPFD_IN`. Anything that assumed the four products
exclude identical periods should use each product's own missingness instead.

## What the sensor is, and what the absolute level rests on

The instrument is a **Vaisala PTB101B** barometer. Every logger program that has
ever measured it — the six CR10X programs of 2004-2006 and the CR1000 program
installed in January 2016 — converts its signal with the same multiplier and the
same offset, spanning 600 to 1060 hPa, which is that barometer's own range. The
maintenance record does not name the instrument once in twenty-one years: it has
never been replaced, calibrated or cleaned as far as the record goes, and it is
not in the device inventory.

Pressure is the one meteo variable here whose **absolute** level can be checked
against physics rather than only against another sensor, and it passes. The
barometric formula, with nothing fitted to the tower data, predicts the
difference between this barometer and each reference from that reference's own
pressure, temperature and humidity. It places the barometer within 5 m of its
nominal elevation using MeteoSwiss Lägern (2.5 km away at 845 m, about 110 m
above the barometer) and within 9 m using the NABEL barometer at the hut, and
the two references agree with each other to 4 m. It also reproduces the annual
wave in the difference between two barometers at different heights — 87 Pa
measured against 79 Pa predicted, the two cycles correlating at 0.99. A unit
error, a wrong offset or a lost factor of ten would fail this by orders of
magnitude.

## What the January 2016 acquisition change did

It moved the level by about **0.09 kPa**, and this is the one hardware change in
the record that did something measurable.

The barometer and its conversion did not change. What changed is how the logger
read the signal: the CR10X excited the sensor and measured it single-ended,
while the CR1000 measures it differentially. A single-ended measurement carries
whatever offset sits between the sensor's ground and the logger's, and a
differential measurement does not.

The change is placed on the tower rather than on a reference by the pattern of
three barometers. Both differences involving the tower move across 2016, by
−0.0884 and −0.0888 kPa, while the difference between the two references moves
by −0.0001 kPa. Which era is the correct one is settled absolutely rather than by
preference: the later era sits on the barometric prediction against both
references and the earlier era sits about 0.1 kPa above it. **The record before
21 January 2016 therefore reads approximately 0.09 kPa high.**

The step is bracketed by the 20.6-day outage that ends on 21 January 2016 and
cannot be dated more finely. The logger program on disk is dated 18 January 2016
and the maintenance record names that same program file, so the record, the
program and the maintenance log agree on the date independently of one another.

The December 2021 change of screening software, which coincides with a hardware
change for some other variables, does nothing here: the difference against
MeteoSwiss changes less across that boundary than it does in an ordinary year.

## Known limitations {#known-limitations}

- **The record is not homogeneous across 21 January 2016, and is not corrected.**
  The values before that date read approximately 0.09 kPa high, as described
  above. No homogenised column is provided. Three considerations stand behind
  that: the step is one part in a thousand of the value and under ten metres of
  air, so air density and the flux quantities computed from it change by the same
  one part in a thousand; a second, rescaled column would change the set of
  columns this product and the merged product ship; and a residual drift of the
  same size, described in the next point, would remain after any homogenisation.
  Analyses that need one absolute level across the whole record should subtract
  0.09 kPa from the records before 21 January 2016 — the later era is the one to
  keep — and analyses within a year, or of pressure changes rather than pressure
  levels, are unaffected.

- **A slow drift of about 0.1 kPa over twenty years cannot be attributed.**
  Beyond the two dated events, the difference between this barometer and
  MeteoSwiss Lägern falls by approximately 0.1 kPa across the record. Slightly
  more than half of that falls after mid-2018, when the second barometer at the
  site stops, so there is no witness that can say which of the two instruments is
  moving. It develops over years rather than stepping at a date, so there is no
  boundary at which a correction could be applied.

- **The MeteoSwiss Lägern pressure series changed level in October 2010.** The
  same rebuild of that station's instrumentation that moved its radiation record
  moved its pressure record: `PA_LAE_MS` steps by approximately 0.06 to 0.07 kPa
  relative to both barometers at this site, which is what places the change
  there. It does not affect this product, which never uses Lägern to correct a
  value, but **a difference between this product and MeteoSwiss Lägern must not
  be read as evidence about the tower across that date.**

- **The NABEL hut barometer is not an independent record after July 2018.** The
  database series `PA_NABEL_H1_2_1` runs nominally to the end of 2018, but from
  3 July 2018 its values simply repeat the tower series to five decimal places.
  The notebook detects this and truncates the reference there. Anything else
  reading that series should do the same: comparing the tower against it over
  those months returns perfect agreement and means nothing.

- **The record does not begin until September 2005.** Anything joining this
  product to `SW_IN`, `TA` or `PPFD_IN`, whose index starts on 2004-01-01, has to
  cope with a shorter series rather than assuming a common period.
