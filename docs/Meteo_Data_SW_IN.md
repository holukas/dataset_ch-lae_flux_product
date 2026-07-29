# Incoming shortwave radiation at 47 m

Half-hourly incoming shortwave radiation measured at 47 m on the CH-LAE tower,
2004-2025, complete and gap-filled. The file is
`01_METEO_SW_IN_GAPFILLED_2004-2025` (parquet and CSV): **385,728 records** on a
continuous 30-minute middle-timestamp index (named `TIMESTAMP_MIDDLE` in the
file) in local time (UTC+1, no daylight saving), from 2004-01-01 00:15 to
2025-12-31 23:45.

The [**interactive dashboard**](dashboards/METEO_SW_IN_dashboard.html) summarises
the exported product on one page: coverage and provenance, seasonality,
distributions, extremes and trends, with a table view behind every chart. It is a
standalone file and can be downloaded and opened without a network connection.

The notebooks behind this page carry the full method, the evidence and the
checks:

- [`01_METEO_SW_IN`](notebooks/10_METEO/30_PRODUCTS/01_METEO_SW_IN_2004-2025.html)
  — builds the product: the merge of the two screenings, the 2012 corrections,
  the nighttime offset, the gap-filling, and the evidence that the record is
  homogeneous across both hardware changes.
- [`RADIATION_SENSOR_CONTINUITY`](notebooks/10_METEO/30_PRODUCTS/RADIATION_SENSOR_CONTINUITY.html)
  — compares four radiation sensors and attributes every level change in the
  record to a particular instrument.
- [`Meteo_Product_Chain`](Meteo_Product_Chain.html) — where this product sits in
  the chain. It is the one meteo product several others depend on: `TA`,
  `PPFD_IN` and `VPD` all read it.

::: {.callout-note title="One column, no homogenised variant"}

Unlike `TA`, this series needs no homogenisation. The same sensor was read through the same calibration across the January 2016 acquisition change, and the December 2021 replacement of the radiometer did not move the level either. There is therefore a single value column and no `_HOMOGENIZED` counterpart.

Two things a user should still know about are described under [Known limitations](#known-limitations): a slow departure of the sensor from its references from 2013, and a level change in the MeteoSwiss series used to fill the gaps.

:::

## Columns

Every one of the 385,728 records carries a value, and the flag is defined
everywhere.

: Columns of `01_METEO_SW_IN_GAPFILLED_2004-2025`. {#tbl-swin-cols}

| column | unit | description |
|---|---|---|
| `SW_IN_T1_47_1_gfXG` | W m^-2^ | Incoming shortwave radiation, gaps filled. Complete, non-negative, exactly zero at night. |
| `FLAG_SW_IN_T1_47_1_ISFILLED` | - | Whether the value was measured, and if not, which method produced it. |

### `FLAG_SW_IN_T1_47_1_ISFILLED`

Filter on `== 0` to select measured records. The series is complete, so every
other code marks a value a model produced. Code `4` is not used.

: Fill codes and their record counts. {#tbl-swin-isfilled}

| code | meaning | records | share |
|---|---|---|---|
| 0 | observed | 351,726 | 91.2 % |
| 1 | daytime gap, filled by the XGBoost model | 17,411 | 4.5 % |
| 2 | daytime gap, filled by the timestamp-only fallback model | 697 | 0.2 % |
| 3 | nighttime gap, set to zero by physics | 15,894 | 4.1 % |

Code `3` is not an estimate in the usual sense: the sun is below the horizon and
the value is zero by physics. Treating codes `0` and `3` together as "not
modelled" is reasonable for most purposes and raises the non-modelled share to
95.3 %.

**Fill quality is not uniform across the record.** Until 2018 two independent
radiation measurements drive the model — NABEL at 49 m on the same tower, and
MeteoSwiss Lägern 2.5 km away. From 2019 only Lägern remains, so the fills of
the later period lean on the more distant sensor. Code `2` marks the few
half-hours where neither driver was available and only the timestamp was left.

## Coverage

The tower measurement begins on **2005-09-14 11:15**, the date the radiometer
was wired to the tower logger. Everything before that is modelled. From 2006
onwards the record is close to complete, and only four years fall below 95 %
measured.

: The years in which measured coverage is not near-complete. Every other year of
2006-2025 is at least 95 % measured. {#tbl-swin-coverage}

| year | measured | why |
|---|---|---|
| 2004 | 0 % | before the radiometer was connected to this logger |
| 2005 | 30 % | the record begins on 14 September |
| 2012 | 93 % | logger clock error, power-supply failure and storm damage |
| 2016 | 94 % | the January outage during which the logger was replaced |

The 2012 faults are the largest interruption inside the measured period. A
logger clock error shifted one block of August 2012 by 15.5 hours; a tower
power-supply failure in late July and August, and storm damage in late October
and November, left records that could not be repaired. The clock error was
corrected, the other two periods were removed, and all of it was gap-filled.
Notebook `01` carries the day-by-day evidence.

## How the gaps were filled

Daytime gaps are filled by an XGBoost model, separately for **2004-2018** and
**2019-2025**. The split is not at a hardware change — it is where the NABEL
sensor stops, and therefore where the model loses a driver. Training one model
across that boundary would let records on one side be predicted by a
relationship fitted mostly on the other.

Both drivers enter the model **as measured**, never gap-filled, so the target is
never used to predict itself. Nighttime gaps are not modelled at all: they are
set to zero, which is what the sun being below the horizon means.

The exported series is always the tower sensor. A reference is a driver, and
never overwrites a measured value.

## Known limitations {#known-limitations}

- **The sensor departs from its references by a few per cent from 2013.** From
  2013 the tower radiometer reads about 3 % high relative to NABEL at 49 m,
  MeteoSwiss Lägern, and the co-located PAR sensor — all three at once, which is
  what places the change on this instrument rather than on any of them. It
  develops over about three years rather than stepping at a date, no maintenance
  record covers it, and the fieldbook records no calibration of this radiometer
  between its installation in 2005 and its removal in 2021. It is within the
  field uncertainty of a pyranometer of this class over that interval and is
  **not corrected**, because a correction could neither be applied at a boundary
  nor justified by a known fault. Analyses comparing the middle of the record
  against its beginning should allow for a few per cent on that account.

- **The MeteoSwiss series used to fill the gaps changed level in October 2010.**
  `SW_IN_LAE_MS`, the gap-filling driver and the only one after 2018, steps by
  about 5 % on 6 October 2010, when that station's radiation instrumentation was
  rebuilt. This is a property of the reference, not of the tower: the two tower
  sensors and NABEL's all step against it together and not against each other.
  It does not degrade the fills, because a driver supplies the state of the sky
  and a scale change does not alter which half-hours were cloudy. It does mean
  that **a difference between this product and MeteoSwiss Lägern must not be
  read as evidence about the tower across that date.**

- **Nighttime values are exactly zero, not measurements.** A pyranometer reads a
  small drifting offset at night. It is an instrument offset rather than
  radiation, and it was removed per day before gap-filling, which sets every
  measured nighttime record to exactly zero. Analyses of instrument noise or of
  the offset itself must go back to the screened database series, not to this
  product.

- **2004 and most of 2005 are entirely modelled.** They precede the measurement
  and rest on MeteoSwiss Lägern alone, which itself begins on 1 February 2004.
  These are the least constrained parts of the record.

## What the January 2016 acquisition change did

Nothing measurable. It is recorded here because the same changeover moved
`TA_T1_47_1` by 1.3 °C, which makes it a reasonable thing to ask about.

The difference is that `TA` changed sensor *and* conversion at once, while
shortwave radiation changed neither. Every surviving logger program — three
CR10X programs spanning 2005-2006 and the CR1000 program installed at the
changeover — measures the same Kipp & Zonen CNR1, serial number 020484, on a
25 mV differential channel at multiplier `99.7009` and offset `0`. That
multiplier is the reciprocal of the sensitivity of that instrument. Replacing
the logger changed how the voltage was digitised and nothing about what it
meant.

The data agree. Across 2016 every ratio among the three shortwave sensors
changes by less than the same measurement changes in an ordinary year; the
largest is 1.4 %, and it belongs to the pair that does not involve the tower at
all. Notebook `01` asserts this on every run, so a future change to the product
that reintroduced a step would fail rather than export quietly.

The radiometer itself was replaced in December 2021, a CNR1 giving way to a
CNR4 with a sensitivity a third larger. That boundary coincides with the change
of screening software, so the two possible causes of a step cannot be separated
from each other — but neither produces one, which is what the product needs.
