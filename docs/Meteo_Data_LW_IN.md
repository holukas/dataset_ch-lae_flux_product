# Incoming longwave radiation at 47 m

Half-hourly incoming (downwelling) longwave radiation at 47 m on the CH-LAE tower,
September 2005 to September 2026, exported as measured. The file is
`06_METEO_LW_IN_2005-2026.09` (parquet and CSV): **368,976 records** on a continuous
30-minute index `TIMESTAMP_MIDDLE` (middle of the half-hour, UTC+01:00, no daylight saving),
from 2005-09-14 00:15 to 2026-09-30 23:45. 2026 holds January to September only.

The [interactive dashboard](dashboards/METEO_LW_IN_dashboard.html) summarises the product
on one page. It is still built from the 2004-2025 version of the product and ends in December 2025.

Method, evidence and checks:

- [`06_METEO_LW_IN`](notebooks/10_METEO/30_PRODUCTS/06_METEO_LW_IN_2005-2026.09.html):
  builds the product: merge of the two screenings, 2012 corrections, identification of the
  instrument from the logger programs and the maintenance record, and the measurement of
  the calibration change described below.
- [`01_METEO_SW_IN`](notebooks/10_METEO/30_PRODUCTS/01_METEO_SW_IN_2004-2026.09.html): the
  shortwave channel of the same radiometer. It establishes the instrument's identity, dates
  its replacement, and shows what the January 2016 and December 2021 hardware changes did
  to the shortwave side.
- [`02_METEO_TA`](notebooks/10_METEO/30_PRODUCTS/02_METEO_TA_2004-2026.09.html): the air
  temperature product, the only diagnostic driver of notebook `06`.
- [Meteo Product Chain](Meteo_Product_Chain.html): where this product sits in the chain.

::: {.callout-important title="The record changes level on 7 June 2016"}

This series is **not homogeneous**. Until 7 June 2016 the pyrgeometer signal was converted
with the calibration factor of the *pyranometer* in the same instrument, 10.03 instead of
12.83 µV/W/m². On that date the logger program was corrected. Everything recorded before it
**reads too low**.

The error is proportional to the difference between the value and $\sigma T_a^4$, so it is
largest under a clear sky and close to zero under low overcast: about **8 W m^-2^ in the
middle of the distribution and up to about 23 W m^-2^ on a clear, dry night** (17 % of the
nighttime difference before the change, at its median and at its 2nd percentile).

No correction and no homogenised column are provided (see
[Known limitations](#known-limitations)). Filter on `FLAG_LW_IN_T1_47_1_SOURCE` before
comparing the two eras, and treat any trend across mid-2016 as containing this change.

:::

## Columns

: Columns of `06_METEO_LW_IN_2005-2026.09`. {#tbl-lwin-cols}

| column | unit | description |
|---|---|---|
| `LW_IN_T1_47_1` | W m^-2^ | Incoming longwave radiation, as measured. Contains `NaN`. |
| `FLAG_LW_IN_T1_47_1_SOURCE` | - | Which instrument and which calibration factor produced the value. Defined at every record. |

There is **no `ISFILLED` flag**, because nothing is filled: a non-null value is a
measurement and a `NaN` is a real gap.

The values are **downwelling longwave irradiance**, median 316.15 W m^-2^, range 135.45 to
441.78 W m^-2^. A pyrgeometer's voltage measures the net exchange between the sky and the
instrument body, roughly -50 W m^-2^ at this site; the downwelling flux is that net signal
plus the instrument's own emission. That term is already included in every value. Reading
the raw converted voltage as the flux would be wrong by about 370 W m^-2^.

### `FLAG_LW_IN_T1_47_1_SOURCE`

: Provenance codes and their record counts over the 364,073 measured records. {#tbl-lwin-source}

| code | meaning | period | records | share |
|---|---|---|---|---|
| 0 | CNR4, its own calibration factor | from 2022-01-07 | 82,828 | 22.8 % |
| 1 | CNR1 at 12.83 µV/W/m^2^, the pyrgeometer's own factor | 2016-06-07 to 2021-12-14 | 96,037 | 26.4 % |
| 2 | CNR1 at 10.03 µV/W/m^2^, the pyranometer's factor; **reads low** | before 2016-06-07 | 184,104 | 50.6 % |
| 3 | changeover, era undetermined | 2021-12-15 to 2022-01-06 | 1,104 | 0.3 % |

Code `3` marks the three weeks between the installation of the CNR4 and the arrival of its
own constants in the logger program, during which the new instrument was read through the
old instrument's factor. Neither the maintenance record nor the data can assign this
interval to either side.

## Coverage

The measurement begins on **2005-09-14 13:15**, when the pyrgeometer channel was wired to
the tower logger. There is no longwave record before that date and none is reconstructed.
**364,073 of the 368,976 records carry a value (98.7 %).**

Of 998 gaps, 977 are one hour or shorter and eight exceed a day. The longest, 20.6 days
from 1 to 21 January 2016, is the site-wide outage during which the tower logger was
replaced; `PA` has the same gap.

: Years in which measured coverage is below 95 %. Every other year of 2006-2025 is at least
95 % measured, and January to September 2026 is complete. {#tbl-lwin-coverage}

| year | measured | why |
|---|---|---|
| 2012 | 92.3 % | logger clock error, power-supply failure and storm damage |
| 2016 | 94.3 % | the January outage during which the logger was replaced |

In 2012 a logger clock error shifted one block of August by 15.5 hours, and a tower
power-supply failure in late July and August and storm damage in late October and November
left records that were removed. `LW_IN` shows no sign of either fault in its own values, and
it has no independent reference that could reveal a level error. The removal therefore rests
on the documented logger-wide fault and is the conservative choice.

## Known limitations {#known-limitations}

- **The record is not homogeneous across 7 June 2016.** Values before that date read low by
  about 17 % of the difference between the value and $\sigma T_a^4$, over about half the
  record. This is **not corrected**. Undoing it requires splitting each stored value into
  the instrument's own emission and its net signal, which needs the radiometer body
  temperature. This product does not read that channel, and its treatment in the processing
  that produced the earlier values cannot be verified from the available files. Rescaling
  with air temperature as a proxy would put an unverified model into the exported numbers.
  The `SOURCE` flag marks the affected era instead.
- **The record also changes across December 2021, and the cause is not established.** The
  radiometer was replaced (CNR1 to CNR4) on 14 December 2021, and the screening software
  changed from `mst` to `diive` at the turn of the year. The two cannot be separated, and
  there is no reference against which to test either. The clear-sky part of the signal
  changes by about 11 %, about half the size of the June 2016 change, which accounts for
  most of the 6.5 W m^-2^ between the two periods once their temperature difference is
  removed. This is equally consistent with a change of instrument, a change of screening,
  and a gradual change in the lower atmosphere, which moved the same statistic in the same
  direction from 2019 to 2024 and reversed through 2025 and the dry year 2026. Nothing is
  corrected. Allow for a change of this order across that date; the `SOURCE` flag separates
  the two instruments.
- **The January 2016 acquisition change did *not* move this series.** It moved
  `TA_T1_47_1` by 1.3 °C and is easily confused with the June date five months later. The
  logger program installed at the changeover applies the same conversion as the programs
  before it, and the four months between the two 2016 dates behave like an ordinary year.
- **The series contains gaps and is not gap-filled.** Code that assumes a complete series
  will fail or propagate `NaN`.
- **There is no independent reference for this variable at the site.** MeteoSwiss Lägern
  has no longwave channel, NABEL has no pyrgeometer, and the below-canopy sensor installed
  in 2024 measures a different quantity. Every statement above rests on the physical
  relation between longwave radiation and air temperature rather than on a second
  instrument, so the evidence is weaker than for `SW_IN` or `TA`. Where it does not identify
  a cause, notebook `06` says so.
- **Summer 2026 was unusually dry and clear.** At MeteoSwiss Lägern, relative humidity was
  95 % or higher in 0.7 to 5.5 % of the half-hours of July to September 2026, against 4 to
  38 % in the same months of 2019-2025. With so few overcast nights, the overcast ceiling of
  nighttime apparent emissivity (its 95th percentile), one of the two checks in notebook
  `06`, falls to 0.93 to 0.95 in those months, below the same months of every earlier year.
  It falls in the same way when computed with the Lägern air temperature, so it reflects the
  weather, not the sensor.
- **Absolute accuracy is limited by the applied calibration.** Both CNR1 eras convert the
  pyrgeometer with a single factory constant and no correction for the dome. The two
  radiometer channels of the successor instrument differ by 28 % in sensitivity, the scale
  of the error removed in June 2016. What remains is the ordinary field uncertainty of an
  unventilated pyrgeometer, which is larger than for the shortwave channel of the same
  instrument.
