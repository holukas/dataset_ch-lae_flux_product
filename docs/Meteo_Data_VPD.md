# Vapour pressure deficit at 47 m

Half-hourly vapour pressure deficit at 47 m on the CH-LAE tower, 2004-2025,
complete. The file is `07_METEO_VPD_2004-2025` (parquet and CSV): **385,728
records** on a continuous 30-minute middle-timestamp index (named
`TIMESTAMP_MIDDLE` in the file) in local time (UTC+1, no daylight saving), from
2004-01-01 00:15 to 2025-12-31 23:45.

`VPD` is not measured. It is computed from air temperature and relative humidity by
formula, so its properties are inherited from those two products rather than from an
instrument of its own.

Method, evidence and checks:

- [`07_METEO_VPD`](notebooks/10_METEO/30_PRODUCTS/07_METEO_VPD_2004-2025.html) —
  computes the product, and measures what the January 2016 acquisition change leaves
  in it.
- [`02_METEO_TA`](notebooks/10_METEO/30_PRODUCTS/02_METEO_TA_2004-2025.html) — the
  temperature input, and the correction applied to it.
- [`04_METEO_RH`](notebooks/10_METEO/30_PRODUCTS/04_METEO_RH_2004-2025.html) — the
  humidity input, and why no corrected version of it exists.
- [`Meteo_Product_Chain`](Meteo_Product_Chain.html) — where this product sits in the
  chain.

::: {.callout-important title="Not homogeneous across 21 January 2016"}

Air temperature and relative humidity at 47 m come from **one probe**, replaced
together with its logger on 21 January 2016. Both inputs change level at that date.

The temperature input is corrected: this product uses the homogenised `TA`, so its
temperature term is on one consistent level across the whole record. **The humidity
input is not corrected**, because no defensible correction for it exists, see
[Relative humidity at 47 m](Meteo_Data_RH.html).

What remains is a step of roughly **17 % of the mean VPD** at that date, measured
against MeteoSwiss Lägern. Any statistic crossing 21 January 2016 contains it. Use
`FLAG_VPD_T1_47_1_SOURCE` to stay inside one probe generation. Comparisons within an
era are unaffected by the step, though see the limitation on drift below.

:::

## Columns

Every one of the 385,728 records carries a value, and both flags are defined
everywhere.

: Columns of `07_METEO_VPD_2004-2025`. {#tbl-vpd-cols}

| column | unit | description |
|---|---|---|
| `VPD_T1_47_1` | kPa | Vapour pressure deficit, computed and gap-free. Not homogeneous across 2016-01-21. |
| `FLAG_VPD_T1_47_1_ISFILLED` | - | What the record was computed from. |
| `FLAG_VPD_T1_47_1_SOURCE` | - | Which probe generation stands behind the record. |

Values range from **0 to 4.345 kPa**, with a median of 0.179 kPa. `VPD` is zero at
saturation and cannot be negative.

There is deliberately **no `_HOMOGENIZED` column**. That name would assert the record
is comparable across January 2016, and it is not: only one of the two inputs can be
put on a single level.

### What it is computed from

`VPD` is the difference between the saturation vapour pressure at the air
temperature and the actual vapour pressure, so it follows from `TA` and `RH` alone.
The Magnus coefficients are those used by ReddyProc.

: The two inputs. {#tbl-vpd-inputs}

| input | column used | from |
|---|---|---|
| air temperature | `TA_T1_47_1_HOMOGENIZED_gfXG` | notebook `02` |
| relative humidity | `RH_T1_47_1` | notebook `04` |

The temperature input is the **homogenised** column, and the choice affects more
than accuracy: the two pre-2016 input errors act on `VPD` in opposite directions.
The earlier `TA` reads about 1.3 °C too cold, which lowers saturation vapour
pressure and pulls `VPD` down; the earlier `RH` reads a few percentage points too
dry, which pushes `VPD` up. A `VPD` computed from the uncorrected temperature
therefore reports a 2016 step about **three times smaller**, not because that series
is better, but because one error masks the other. The masking depends on the
particular temperature and humidity and is not a property to rely on, so the product
uses the best available estimate of each input and states the residual step openly.

### `FLAG_VPD_T1_47_1_ISFILLED`

Filter on `== 0` for records computed from two genuine 47 m measurements. Every
record is computed by the formula, none is modelled, but a computed record need not
rest on two measurements.

: Provenance codes and their record counts. {#tbl-vpd-isfilled}

| code | meaning | records | share |
|---|---|---|---|
| 0 | measured `TA` and measured `RH` | 369,056 | 95.7 % |
| 5 | measured `RH`, gap-filled `TA` | 23 | 0.01 % |
| 6 | `RH` reconstructed from NABEL at 49 m | 15,729 | 4.1 % |
| 7 | `RH` reconstructed from MeteoSwiss Lägern | 920 | 0.2 % |

Code `6` outranks `5` because it is the larger error: `RH` enters the formula
linearly and a reconstructed value carries approximately 3 % RH of uncertainty.
Codes `1`, `2` and `4` are reserved for modelled values and do not occur.

### `FLAG_VPD_T1_47_1_SOURCE`

Carried over unchanged from notebooks `02` and `04`, which describe the same probe
and whose flags are identical record for record.

: Probe generations and their record counts. {#tbl-vpd-source}

| code | probe and acquisition | period | records |
|---|---|---|---|
| 0 | Campbell CS215 on SDI-12 | 2016-01-21 14:15 to 2025-12-31 23:45 | 174,356 |
| 1 | Rotronic MP101A, single-ended analog | 2004-09-20 10:45 to 2015-12-31 23:45 | 197,739 |
| 2 | acquisition changeover, generation undetermined | 2016-01-01 00:15 to 2016-01-21 13:45 | 988 |
| 3 | before the tower record begins | 2004-01-01 00:15 to 2004-09-20 10:15 | 12,645 |

## Coverage

The series is complete. What varies is how much of each year rests on two
measurements rather than on a reconstructed humidity.

: The years in which fewer than 99 % of records are computed from two measurements.
Every other year of 2005-2025 is at least 99 %. {#tbl-vpd-coverage}

| year | computed from two measurements | why |
|---|---|---|
| 2004 | 28.0 % | the tower humidity record begins on 20 September |
| 2009 | 97.2 % | scattered outages |
| 2012 | 92.8 % | logger clock error, power-supply failure and storm damage |
| 2016 | 94.3 % | the January outage during which the probe and logger were replaced |
| 2019 | 95.7 % | an outage after the NABEL reference ends |

## Known limitations

- **The record is not homogeneous across 21 January 2016.** The residual step is
  approximately 17 % of the mean `VPD`, against a year-to-year variation of about
  2 % in the same statistic. It is what the uncorrectable humidity step leaves behind
  after the temperature term has been put on one level. Restrict anything crossing
  that date to one probe generation using `FLAG_VPD_T1_47_1_SOURCE`, or carry the
  step as an uncertainty. Computing `VPD` from the *uncorrected* `TA` instead would
  report a step about three times smaller, because the two input errors have opposite
  signs on `VPD` and one masks the other. That is a smaller number, not a better
  product: this one uses the best available estimate of each input.
- **Both humidity eras also drift internally.** Against MeteoSwiss Lägern the earlier
  era moves approximately −0.31 percentage points of RH per year and the later era
  approximately +0.50, so a `VPD` trend computed entirely inside one era still
  contains sensor movement. Over the length of each era this drift amounts to more
  than the 2016 step itself. It is not corrected, because it is not attributed to
  either station and, after the NABEL sensor stops in 2018, there is no third humidity
  series at the site to attribute it with.
- **The step is largest where `VPD` is largest.** The humidity error is biggest in the
  drier half of the range and vanishes near saturation, so warm dry afternoons, the
  conditions that produce high `VPD`, carry more of it than the record-wide figure
  suggests.
- **Reconstructed humidity propagates.** 4.3 % of records rest on a humidity
  transferred from another instrument rather than measured at 47 m. Filter on
  `FLAG_VPD_T1_47_1_ISFILLED == 0` where that matters.
- **The temperature correction has its own limits.** The homogenised `TA` puts the two
  eras on one level; it does not make either absolutely accurate. Both 47 m sensors
  sit in passive radiation shields that heat in sunlight, and what `02` removes is the
  difference between the two shields' responses, not the heating itself.
