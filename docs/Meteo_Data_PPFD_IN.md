# Photosynthetic photon flux density at 47 m

Half-hourly incoming photosynthetic photon flux density at 47 m on the CH-LAE
tower, 2004-2025, gap-filled to completeness. The file is
`03_METEO_PPFD_IN_GAPFILLED_2004-2025` (parquet and CSV): **385,728 records** on a
continuous 30-minute middle-timestamp index (named `TIMESTAMP_MIDDLE` in the file)
in local time (UTC+1, no daylight saving), from 2004-01-01 00:15 to
2025-12-31 23:45.

The [**interactive dashboard**](dashboards/METEO_PPFD_IN_dashboard.html) summarises
the product on one page: coverage and provenance, seasonality, distributions,
extremes and trends, with a table view behind every chart. It is standalone and
works offline.

Method, evidence and checks:

- [`03_METEO_PPFD_IN`](notebooks/10_METEO/30_PRODUCTS/03_METEO_PPFD_IN_2004-2025.html)
  — builds the product: the merge of the two screenings, the 2012 corrections, the
  nighttime offset, the gap-filling, and the section identifying the sensor and
  testing it at both hardware changes.
- [`RADIATION_SENSOR_CONTINUITY`](notebooks/10_METEO/30_PRODUCTS/RADIATION_SENSOR_CONTINUITY.html)
  — compares four radiation sensors and attributes every level change in the record
  to a particular instrument. It is what places the decline described below on this
  sensor rather than on either reference.
- [`Meteo_Product_Chain`](Meteo_Product_Chain.html) — where this product sits in the
  chain. It depends on `SW_IN`, which has to be built first.

::: {.callout-important title="The sensor has been losing response since 2022"}

The 47 m quantum sensor reads progressively lower against both of its independent
references from 2022 onwards: about 3 to 4 % lower over 2021-2025, and 6 to 7 %
below its 2006-2010 level by the end of the record, which arrives before the
decline has levelled off.

It is **not corrected**, for the reasons under
[Known limitations](#known-limitations). A trend or a period comparison spanning
the last years of this record therefore contains the sensor's own decline as well
as any change in the light. Comparisons within a year are unaffected, as is any use
of a single half-hour.

:::

::: {.callout-note title="One column, no homogenised variant"}

One instrument over the whole record, read through the same conversion by two
acquisition systems, with no step at either hardware boundary. There is a single
value column and no `_HOMOGENIZED` counterpart. The gradual decline above is not
something a boundary correction could address.

:::

## Columns

Every one of the 385,728 records carries a value, and the flag is defined
everywhere.

: Columns of `03_METEO_PPFD_IN_GAPFILLED_2004-2025`. {#tbl-ppfd-cols}

| column | unit | description |
|---|---|---|
| `PPFD_IN_T1_47_1_gfXG` | µmol m^-2^ s^-1^ | Incoming photosynthetic photon flux density, gaps filled. Complete, non-negative, exactly zero at night. |
| `FLAG_PPFD_IN_T1_47_1_ISFILLED` | - | Whether the value was measured, and if not, which method produced it. |

### `FLAG_PPFD_IN_T1_47_1_ISFILLED`

Filter on `== 0` for measured records. The series is complete, so every other code
marks a modelled value.

: Fill codes and their record counts. {#tbl-ppfd-isfilled}

| code | meaning | records | share |
|---|---|---|---|
| 0 | observed | 369,124 | 95.7 % |
| 1 | daytime gap, filled by the XGBoost model | 8,374 | 2.2 % |
| 2 | daytime gap, filled by the timestamp-only fallback model | 600 | 0.2 % |
| 3 | nighttime gap, set to zero by physics | 7,543 | 2.0 % |
| 4 | short daytime gap, filled by linear interpolation | 87 | 0.02 % |

Code `3` is not an estimate: the sun is below the horizon and the value is zero by
physics. Counting codes `0` and `3` together as not modelled raises the
non-modelled share to 97.7 %.

The filled records are not spread thinly through the series. They fall in about 160
runs, dominated by the period before the measurement begins and by a small number
of outages, so filtering on the flag removes whole periods rather than a sprinkling
of half-hours. Sixteen of the twenty-two years carry fewer than a hundred filled
records each.

## Coverage

The tower measurement begins on **2004-09-20 10:45**. Everything before that is
modelled.

: The years in which measured coverage is not near-complete. Every other year of
2005-2025 is at least 95 % measured. {#tbl-ppfd-coverage}

| year | measured | why |
|---|---|---|
| 2004 | 28 % | the record begins on 20 September |
| 2012 | 93 % | logger clock error, power-supply failure and storm damage |
| 2016 | 94 % | the January outage during which the logger was replaced |

The 2012 faults are the largest interruption inside the measured period. A logger
clock error shifted one block of August 2012 by 15.5 hours; a tower power-supply
failure in late July and August, and storm damage in late October and November,
left records that could not be repaired. The clock error was corrected, the other
two periods were removed, and all of it was gap-filled. The three windows are the
same ones notebooks `01` and `02` remove, because the fault is in the logger and
the power supply and therefore affects every variable on that system.

The January 2016 outage runs from 1 January to 21 January 14:15, when the
replacement logger came online.

## How the gaps were filled

Daytime gaps are filled by an XGBoost model over the whole record. There is no
period split, unlike `SW_IN` and `TA`: all three drivers span the full record, so no
model is ever asked to predict a period whose drivers it did not see.

The drivers are the gap-filled `SW_IN` from notebook `01`, potential radiation
computed from the site coordinates, and MeteoSwiss Lägern global radiation. The
tower pyranometer is by far the strongest (same height, same mast, r^2^ 0.99) but
it is itself gap-filled, and `PPFD_IN` gaps tend to coincide with `SW_IN` gaps
because both sensors sit on the same logger. MeteoSwiss Lägern covers that case: an
independent measurement of the sky 2.5 km away, at the cost of considerably more
scatter. Code `2` marks the few half-hours where neither radiation driver was
available.

Nighttime gaps are set to zero rather than modelled. The exported series is always
the tower sensor; a reference is a driver and never overwrites a measured value.

## Known limitations {#known-limitations}

- **The sensor has been losing response since 2022, and it had not levelled off by
  the end of the record.** It falls against the co-located tower pyranometer and
  against MeteoSwiss Lägern together, by 3.3 % and 3.7 % respectively between 2021
  and 2025, reaching 6.1 and 7.4 % below its 2006-2010 level in the last year of the
  record. Both references moving together is what places the change on this
  instrument; `RADIATION_SENSOR_CONTINUITY` reaches the same conclusion from four
  sensors at once. It is **not corrected**, because it develops over years rather
  than stepping at a date, so there is no boundary at which a correction could be
  applied, and because no maintenance record identifies a cause, so any correction
  would be a rescaling towards a reference rather than the repair of a known fault.
  The likeliest explanation for a falling response in a quantum sensor left in the
  field for twenty years is the sensor itself: soiling, or ageing of its diffuser and
  detector. **Analyses that span the last years of this record should allow for
  several per cent on this account, or use a reference-normalised quantity.**
  Gap-filled records inherit the state of the sensor at the time they were filled and
  neither add the bias nor remove it.

- **A comparison against `SW_IN` across 2013 carries that sensor's drift, not this
  one's.** The 47 m pyranometer rises by about 3 % against its own references from
  2013, and the ratio between the two tower radiation series moves accordingly. The
  change is on the pyranometer, see
  [Incoming shortwave radiation at 47 m](Meteo_Data_SW_IN.html), but it is visible in
  any quantity that divides one of these products by the other, such as a
  photon-to-energy ratio computed over the whole record.

- **The MeteoSwiss series used to fill the gaps changed level in October 2010.**
  `SW_IN_LAE_MS` steps by about 5 % on 6 October 2010, when that station's radiation
  instrumentation was rebuilt. This is a property of the reference, not of the tower.
  It does not degrade the fills, since a driver supplies the state of the sky and a
  scale change does not alter which half-hours were cloudy. It does mean that **a
  difference between this product and MeteoSwiss Lägern must not be read as evidence
  about the tower across that date.**

- **Nighttime values are exactly zero, not measurements.** The sensor reads a small
  positive offset at night: about 4.2 µmol m^-2^ s^-1^ before the 2016 logger
  replacement and 2.5 µmol m^-2^ s^-1^ after it. It is an instrument offset rather
  than light, and it was removed per day before gap-filling, which sets every
  measured nighttime record to exactly zero. Analyses of instrument noise or of the
  offset itself must go back to the screened database series.

- **2004 is 72 % modelled.** The tower record begins 2004-09-20 10:45, and everything
  before it rests on the `SW_IN` product, which is itself reconstructed for that
  period. Those records are a fill built on a fill and carry the uncertainty of both
  steps. The flag marks them.

## What the January 2016 changes did

Nothing measurable to this series. Two things happened that month: the tower logger
was replaced, which moved `TA_T1_47_1` by 1.3 °C, and the fieldbook records **a new
Kipp & Zonen PAR sensor being installed on 8 January 2016**.

**That sensor is not this column.** The CR1000 logger program measures two
incoming-PAR instruments at 47 m and names both. `PPFD_IN_T1_47_1`, the series
exported here, is a Delta-T sunshine sensor, which delivers a signal already scaled
to µmol m^-2^ s^-1^ and is therefore read at a multiplier of exactly 1. The Kipp &
Zonen PAR LITE installed that January is `PPFD_IN_T1_47_2`, read at the reciprocal
of its own calibrated sensitivity, and its record begins on 2016-01-21 14:15 and
never reaches back before that date. The maintenance record alone cannot make this
distinction, because it files both instruments under the same operation tag.

The Delta-T sensor was installed in August 2004 and appears in every surviving
logger program from then on, at the same multiplier of 1 and offset of 0 in both the
CR10X and the CR1000 era. The maintenance record shows no replacement and no
calibration of it in twenty-one years; two cleanings, in December 2016 and April
2021, are the whole of its documented history.

The data agree. Across 2016 the ratio of this sensor to the tower pyranometer
changes by +0.4 % and to MeteoSwiss Lägern by +0.5 %, both smaller than the change
the same measurement finds in an ordinary year. The comparison against MeteoSwiss is
the one that carries the argument: a change confined to this tower's acquisition
system could move both tower sensors together and leave their ratio flat, but it
could not move their ratio against a station 2.5 km away. The one thing that
demonstrably did change is the sensor's nighttime offset, which the per-day
correction removes on both sides of the date.

The `mst` and `diive` screenings meet at the end of 2021, and that boundary carries
no step either. Notebook `03` asserts all of this on every run, so a future change to
the product that reintroduced a step would fail rather than export quietly.
