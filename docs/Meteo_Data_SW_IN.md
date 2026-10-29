# Incoming shortwave radiation at 47 m

Half-hourly incoming shortwave radiation at 47 m on the CH-LAE tower, 2004 to September
2026, gap-filled to completeness. The file is `01_METEO_SW_IN_GAPFILLED_2004-2026.09`
(parquet and CSV): **398,832 records** on a continuous 30-minute index `TIMESTAMP_MIDDLE`
(middle of the half-hour, UTC+01:00, no daylight saving), from 2004-01-01 00:15 to
2026-09-30 23:45.

The [interactive dashboard](dashboards/METEO_SW_IN_dashboard.html) summarises the product
on one page.

Method, evidence and checks:

- [`01_METEO_SW_IN`](notebooks/10_METEO/30_PRODUCTS/01_METEO_SW_IN_2004-2026.09.html):
  builds the product (merge of the two screenings, 2012 corrections, nighttime offset,
  gap-filling) and shows that the record is homogeneous across both hardware changes.
- [`RADIATION_SENSOR_CONTINUITY`](notebooks/10_METEO/30_PRODUCTS/RADIATION_SENSOR_CONTINUITY.html):
  compares four radiation sensors and attributes each level change in the record to one
  instrument.
- [`METEO_SW_IN` overview](notebooks/90_OVERVIEW/METEO_SW_IN.html): the product year by
  year, 2004-2025.
- [Meteo Product Chain](Meteo_Product_Chain.html): `TA` and `PPFD_IN` use this product as
  a gap-filling driver.

::: {.callout-note title="One column, no homogenised variant"}

This series needs no homogenisation. The same sensor was read through the same
calibration across the January 2016 acquisition change, and the December 2021 replacement
of the radiometer did not move the level either. There is one value column and no
`_HOMOGENIZED` column. A slow departure of the sensor from its references from 2013 is
described under [Known limitations](#known-limitations).

:::

## Columns

Every record carries a value, and the flag is defined at every record.

: Columns of `01_METEO_SW_IN_GAPFILLED_2004-2026.09`. {#tbl-swin-cols}

| column | unit | description |
|---|---|---|
| `SW_IN_T1_47_1_gfXG` | W m^-2^ | Incoming shortwave radiation, gaps filled. Complete, non-negative, exactly zero at night. |
| `FLAG_SW_IN_T1_47_1_ISFILLED` | - | Whether the value was measured, and if not, which method produced it. |

### `FLAG_SW_IN_T1_47_1_ISFILLED`

Filter on `== 0` for measured records. Every other code marks a filled value. Code `4` is
not used.

: Fill codes and their record counts. {#tbl-swin-isfilled}

| code | meaning | records | share |
|---|---|---|---|
| 0 | observed | 364,830 | 91.5 % |
| 1 | daytime gap, filled by the XGBoost model | 17,411 | 4.4 % |
| 2 | daytime gap, filled by the timestamp-only fallback model | 697 | 0.2 % |
| 3 | nighttime gap, set to zero | 15,894 | 4.0 % |

Code `3` is not an estimate: the sun is below the horizon and the value is zero. Codes `0`
and `3` together are 95.5 % of the record.

## Coverage

The tower measurement begins on **2005-09-14 11:15**, when the radiometer was wired to the
tower logger. Everything before that is modelled.

: Years in which measured coverage is not near-complete. Every other year from 2006 to
September 2026 is at least 95 % measured. {#tbl-swin-coverage}

| year | measured | why |
|---|---|---|
| 2004 | 0 % | before the radiometer was connected to this logger |
| 2005 | 30 % | the record begins on 14 September |
| 2012 | 93 % | logger clock error, power-supply failure and storm damage |
| 2016 | 94 % | the January outage during which the logger was replaced |

In 2012 a logger clock error shifted one block of August by 15.5 hours, and a tower
power-supply failure in late July and August and storm damage in late October and November
left records that could not be repaired. The clock error was corrected, the other two
periods were removed, and all of it was gap-filled.

## How the gaps were filled

Daytime gaps are filled by an XGBoost model, trained separately for **2004-2018** and
**2019-2026**. The split is where the NABEL sensor at 49 m on the same tower ends, so that
no model is trained on one driver set and applied to the other. Until 2018 the drivers are
NABEL and MeteoSwiss Lägern (2.5 km away); from 2019 only Lägern remains, so the later fills
rest on the more distant sensor. Code `2` marks the half-hours where a driver was
missing; 571 of its 697 records are in January 2004, before the MeteoSwiss record begins.
Drivers enter as measured, never gap-filled. Nighttime gaps are set to zero. A
reference is used only as a driver and never replaces a measured value.

## Known limitations {#known-limitations}

- **The sensor reads about 3 % high relative to its references from 2013.** NABEL at 49 m,
  MeteoSwiss Lägern and the co-located PAR sensor all show it at once, which places the
  change on this radiometer. It develops over about three years rather than at a date, and
  the fieldbook records no maintenance or calibration of this radiometer between its
  installation in 2005 and its removal in 2021. The change is within the field uncertainty
  of a pyranometer of this class and is **not corrected**, because there is neither a
  boundary at which to apply a correction nor a known fault to justify one. Allow for a few
  per cent when comparing the middle of the record with its beginning.
- **The MeteoSwiss gap-filling driver changed level in October 2010.** `SW_IN_LAE_MS`, the
  only driver after 2018, steps by about 5 % on 6 October 2010, when that station's
  radiation instrumentation was rebuilt. Both tower radiation sensors and NABEL step
  against it together. The fills are not affected, because a driver supplies the state of
  the sky, which a scale change does not alter. **Do not read a difference between this
  product and MeteoSwiss Lägern as evidence about the tower across that date.**
- **Nighttime values are exactly zero, not measurements.** The small drifting nighttime
  offset of the pyranometer was removed per day before gap-filling. For instrument noise or
  the offset itself, use the screened database series.
- **2004 and most of 2005 are entirely modelled.** They precede the measurement and are
  filled from NABEL and MeteoSwiss Lägern. These are the least constrained parts of the
  record.
- **January 2004 is a model artefact and reads far too high.** The MeteoSwiss reference
  begins on 1 February 2004, so every daytime half-hour of January 2004 is filled by the
  timestamp-only fallback model (code `2`), which uses the date and time but no measurement
  of the sky. The month totals 325 MJ m^-2^, about 2.7 times the mean January of
  2005-2025 (119 MJ m^-2^) and twice the brightest of them (161 MJ m^-2^ in 2022). It is
  **not corrected**. Exclude January 2004 from radiation totals, anomalies and rankings.
  `PPFD_IN` of the same month is filled the same way (see
  [Photosynthetic photon flux density at 47 m](Meteo_Data_PPFD_IN.html)).

## The hardware changes of 2016 and 2021

**The January 2016 acquisition change did nothing measurable to this series.** It is
recorded here because the same changeover moved `TA_T1_47_1` by 1.3 °C. For `TA` the sensor
and its conversion changed; for shortwave radiation neither did. Every surviving logger
program, three CR10X programs of 2005-2006 and the CR1000 program installed at the
changeover, reads the same Kipp & Zonen CNR1 (serial number 020484) on a 25 mV differential
channel at multiplier `99.7009` (the reciprocal of its sensitivity) and offset `0`. Across
2016 every ratio among the three shortwave sensors changes by less than in an ordinary year.
The largest change, 1.4 %, is in the pair that does not involve the tower. Notebook `01`
asserts this on every run.

**The December 2021 replacement of the radiometer did not move the level either.** A CNR4
replaced the CNR1, with a sensitivity of 13.89 instead of 10.03 µV/W/m². The date coincides
with the change of screening software, so the two possible causes of a step cannot be
separated, but neither produces one.
