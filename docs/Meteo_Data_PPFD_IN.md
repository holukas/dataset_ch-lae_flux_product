# Photosynthetic photon flux density at 47 m

Half-hourly incoming photosynthetic photon flux density at 47 m on the CH-LAE tower, 2004
to September 2026, gap-filled to completeness. The file is
`03_METEO_PPFD_IN_GAPFILLED_2004-2026.09` (parquet and CSV): **398,832 records** on a
continuous 30-minute index `TIMESTAMP_MIDDLE` (middle of the half-hour, UTC+01:00, no
daylight saving), from 2004-01-01 00:15 to 2026-09-30 23:45.

The [interactive dashboard](dashboards/METEO_PPFD_IN_dashboard.html) summarises the
product on one page. It is still built from the 2004-2025 version of the product and ends in December 2025.

Method, evidence and checks:

- [`03_METEO_PPFD_IN`](notebooks/10_METEO/30_PRODUCTS/03_METEO_PPFD_IN_2004-2026.09.html):
  builds the product (merge of the two screenings, 2012 corrections, nighttime offset,
  gap-filling), identifies the sensor and tests it at both hardware changes.
- [`RADIATION_SENSOR_CONTINUITY`](notebooks/10_METEO/30_PRODUCTS/RADIATION_SENSOR_CONTINUITY.html):
  compares four radiation sensors and places the decline described below on this sensor
  rather than on either reference.
- [Meteo Product Chain](Meteo_Product_Chain.html): this product depends on `SW_IN`, which
  is built first.

::: {.callout-important title="The sensor lost response between 2022 and 2024"}

Against both of its independent references the 47 m quantum sensor reads about 3 to 3.5 %
lower in 2026 than in 2021, and about 6 to 7 % below its 2006-2010 level. The fall has not
continued since 2024: 2025 and 2026 lie within 0.4 % of 2024.

The decline is **not corrected** (see [Known limitations](#known-limitations)). A trend or
period comparison that spans the last years of the record contains it. Comparisons within
a year, and the use of single half-hours, are unaffected.

:::

There is one value column and no `_HOMOGENIZED` column: one instrument over the whole
record, read through the same conversion by two acquisition systems, with no step at either
hardware boundary.

## Columns

Every record carries a value, and the flag is defined at every record.

: Columns of `03_METEO_PPFD_IN_GAPFILLED_2004-2026.09`. {#tbl-ppfd-cols}

| column | unit | description |
|---|---|---|
| `PPFD_IN_T1_47_1_gfXG` | µmol m^-2^ s^-1^ | Incoming photosynthetic photon flux density, gaps filled. Complete, non-negative, exactly zero at night. |
| `FLAG_PPFD_IN_T1_47_1_ISFILLED` | - | Whether the value was measured, and if not, which method produced it. |

### `FLAG_PPFD_IN_T1_47_1_ISFILLED`

Filter on `== 0` for measured records. Every other code marks a filled value.

: Fill codes and their record counts. {#tbl-ppfd-isfilled}

| code | meaning | records | share |
|---|---|---|---|
| 0 | observed | 382,228 | 95.8 % |
| 1 | daytime gap, filled by the XGBoost model | 8,374 | 2.1 % |
| 2 | daytime gap, filled by the timestamp-only fallback model | 600 | 0.2 % |
| 3 | nighttime gap, set to zero | 7,543 | 1.9 % |
| 4 | short daytime gap, filled by linear interpolation | 87 | 0.02 % |

Code `3` is not an estimate: the sun is below the horizon and the value is zero. Codes `0`
and `3` together are 97.7 % of the record.

The 16,604 filled records fall in 159 runs. Most runs are single half-hours (126 of 159),
but eight runs of a day or longer hold 16,301 of the filled records: the period before the
measurement begins and a few outages. Filtering on the flag therefore removes mainly whole
periods. Seventeen of the 23 years (2026 to September) have fewer than a hundred filled
records, and seven have none.

## Coverage

The tower measurement begins on **2004-09-20 10:45**. Everything before that is modelled.

: Years in which measured coverage is not near-complete. Every other year of 2005-2025 is
at least 95 % measured, and 2026 (January to September) is 100 % measured. {#tbl-ppfd-coverage}

| year | measured | why |
|---|---|---|
| 2004 | 28 % | the record begins on 20 September |
| 2012 | 93 % | logger clock error, power-supply failure and storm damage |
| 2016 | 94 % | the January outage during which the logger was replaced |

In 2012 a logger clock error shifted one block of August by 15.5 hours, and a tower
power-supply failure in late July and August and storm damage in late October and November
left records that could not be repaired. The clock error was corrected, the other two
periods were removed, and all of it was gap-filled. The windows are the same as in `SW_IN`
and `TA`, because the fault was in the logger and the power supply. The January 2016
outage runs from 1 January to 21 January 14:15, when the replacement logger came online.

## How the gaps were filled

Daytime gaps are filled by one XGBoost model over the whole record; unlike `SW_IN` and
`TA` there is no period split, because all three drivers span the full record. The drivers
are the gap-filled `SW_IN` from notebook `01`, potential radiation computed from the site
coordinates, and MeteoSwiss Lägern global radiation. The tower pyranometer is the strongest
driver (same height, same mast, r^2^ 0.99), but it is itself gap-filled, and `PPFD_IN` gaps
tend to coincide with `SW_IN` gaps because both sensors are on the same logger. Lägern,
2.5 km away, covers that case with more scatter. Code `2` marks the half-hours where a
driver was missing; 571 of its 600 records are in January 2004, before the MeteoSwiss record
begins. Nighttime gaps are set to zero. A reference is used
only as a driver and never replaces a measured value.

## Known limitations {#known-limitations}

- **The sensor lost response between 2022 and 2024, and it has not recovered.** It falls
  against the co-located tower pyranometer and against MeteoSwiss Lägern together, by
  2.86 % and 3.45 % between 2021 and 2026, and reaches 5.63 % and 7.13 % below its
  2006-2010 level in 2026. The change over the last year (+0.4 % and +0.3 %) is within the
  ordinary year-to-year change of these ratios (0.6 % and 0.7 %), so one stable season does
  not yet show that the response has settled. Both references moving together places the
  change on this instrument, and `RADIATION_SENSOR_CONTINUITY` reaches the same conclusion
  from four sensors. It is **not corrected**: it develops over years, so there is no
  boundary at which to apply a correction, and no maintenance record identifies a cause, so
  a correction would be a rescaling towards a reference. The likely cause is the sensor
  itself after twenty years in the field (soiling, or ageing of the diffuser and detector).
  **Allow for several per cent in analyses that span the last years of the record, or use
  a reference-normalised quantity.** Gap-filled records inherit the state of the sensor at
  the time and neither add nor remove the bias.
- **A comparison against `SW_IN` across 2013 shows that sensor's drift, not this one's.**
  The 47 m pyranometer rises by about 3 % against its references from 2013 (see
  [Incoming shortwave radiation at 47 m](Meteo_Data_SW_IN.html)). Any ratio of the two
  products, such as a photon-to-energy ratio over the whole record, contains that change.
- **The MeteoSwiss gap-filling driver changed level in October 2010.** `SW_IN_LAE_MS`
  steps by about 5 % on 6 October 2010, when that station's radiation instrumentation was
  rebuilt. The fills are not affected, because a driver supplies the state of the sky.
  **Do not read a difference between this product and MeteoSwiss Lägern as evidence about
  the tower across that date.**
- **Nighttime values are exactly zero, not measurements.** The sensor reads a small
  positive offset at night: about 4.2 µmol m^-2^ s^-1^ before the 2016 logger replacement
  and 2.5 µmol m^-2^ s^-1^ from then to the end of 2021. From 2022 the `diive` screening
  has already removed it. The offset was removed per day before gap-filling. For instrument
  noise or the offset itself, use the screened database series.
- **2004 is 72 % modelled.** Everything before 2004-09-20 10:45 rests on the `SW_IN`
  product, which is itself reconstructed for that period. These records are a fill built on
  a fill and carry the uncertainty of both.
- **January 2004 is a model artefact and reads far too high.** The MeteoSwiss reference
  begins on 1 February 2004, so every daytime half-hour of January 2004 is filled by the
  timestamp-only fallback model (code `2`), as in `SW_IN`. The monthly mean is about twice
  the mean January of 2005-2025. It is **not corrected**. Exclude January 2004 from
  totals, anomalies and rankings (see
  [Incoming shortwave radiation at 47 m](Meteo_Data_SW_IN.html#known-limitations)).

## The January 2016 changes

They did nothing measurable to this series. Two things happened that month: the tower
logger was replaced, which moved `TA_T1_47_1` by 1.3 °C, and the fieldbook records **a new
Kipp & Zonen PAR sensor installed on 8 January 2016**.

**That sensor is not this column.** The CR1000 logger program reads two incoming-PAR
instruments at 47 m and names both. `PPFD_IN_T1_47_1`, exported here, is a Delta-T sunshine
sensor, whose signal is already scaled to µmol m^-2^ s^-1^ and is read at a multiplier of
exactly 1. The Kipp & Zonen PAR LITE installed that January is `PPFD_IN_T1_47_2`, read at
the reciprocal of its own sensitivity, and its record begins on 2016-01-21 14:15. The
maintenance record alone cannot make this distinction, because it files both instruments
under the same operation tag.

The Delta-T sensor was installed in August 2004 and appears in every surviving logger
program since, at multiplier 1 and offset 0 in both the CR10X and the CR1000 era. The
maintenance record shows no replacement and no calibration in twenty-two years, only two
cleanings, in December 2016 and April 2021.

Across 2016 the ratio of this sensor to the tower pyranometer changes by +0.4 % and to
MeteoSwiss Lägern by +0.5 %, both less than in an ordinary year. A change confined to the
tower acquisition system could move both tower sensors and leave their ratio flat, but it
could not move their ratio against a station 2.5 km away. Only the nighttime offset
changed, and the per-day correction removes it on both sides of the date. The `mst` and
`diive` screenings meet at the end of 2021 without a step either. Notebook `03` asserts all
of this on every run.
