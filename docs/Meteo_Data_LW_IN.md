# Incoming longwave radiation at 47 m

Half-hourly incoming (downwelling) longwave radiation at 47 m on the CH-LAE tower,
2005-2025, exported as measured. The file is `06_METEO_LW_IN_2005-2025` (parquet and
CSV): **355,872 records** on a continuous 30-minute middle-timestamp index (named
`TIMESTAMP_MIDDLE` in the file) in local time (UTC+1, no daylight saving), from
2005-09-14 00:15 to 2025-12-31 23:45.

The [**interactive dashboard**](dashboards/METEO_LW_IN_dashboard.html) summarises the
product on one page: coverage and provenance, seasonality, distributions, extremes
and trends, with a table view behind every chart. It is standalone and works offline.

Method, evidence and checks:

- [`06_METEO_LW_IN`](notebooks/10_METEO/30_PRODUCTS/06_METEO_LW_IN_2005-2025.html) —
  builds the product: the merge of the two screenings, the 2012 corrections, the
  identification of the instrument from the logger programs and the maintenance
  record, and the measurement of the calibration change described below.
- [`01_METEO_SW_IN`](notebooks/10_METEO/30_PRODUCTS/01_METEO_SW_IN_2004-2025.html) —
  the other channel of the same radiometer. It establishes the instrument's identity
  and dates its replacement, and it is the reference for what the January 2016 and
  December 2021 hardware changes did to the shortwave side.
- [`02_METEO_TA`](notebooks/10_METEO/30_PRODUCTS/02_METEO_TA_2004-2025.html) — the
  air-temperature product, which notebook `06` uses as its only diagnostic driver.
- [`Meteo_Product_Chain`](Meteo_Product_Chain.html) — where this product sits in the
  chain.

::: {.callout-important title="The record changes level on 7 June 2016"}

This series is **not homogeneous**. Until 7 June 2016 the pyrgeometer's signal was
converted with the calibration factor of the *pyranometer* in the same instrument,
10.03 instead of 12.83 µV/W/m². On that date the site's logger program was
corrected, and everything recorded before it **reads too low**.

The size of the error is not a constant. It is proportional to the difference
between the value and $\sigma T_a^4$, so it is largest under a clear sky and
approximately zero under low overcast: about **9 W m^-2^ in the middle of the
distribution and up to some 22 W m^-2^ on a clear, dry night**.

No correction is applied and no homogenised column is provided; the reasons are
under [Known limitations](#known-limitations). Filter on
`FLAG_LW_IN_T1_47_1_SOURCE` before comparing the two eras, and treat any trend
computed across mid-2016 as containing this change.

:::

## Columns

: Columns of `06_METEO_LW_IN_2005-2025`. {#tbl-lwin-cols}

| column | unit | description |
|---|---|---|
| `LW_IN_T1_47_1` | W m^-2^ | Incoming longwave radiation, as measured. Contains `NaN`. |
| `FLAG_LW_IN_T1_47_1_SOURCE` | - | Which instrument and which calibration factor produced the value. Defined at every record. |

There is **no `ISFILLED` flag**, because nothing is filled: a non-null value is a
measurement and a `NaN` is a real gap. `PA` is the only other meteo product exported
this way.

### `FLAG_LW_IN_T1_47_1_SOURCE`

: Provenance codes and their record counts over the 350,969 measured records. {#tbl-lwin-source}

| code | meaning | period | records | share |
|---|---|---|---|---|
| 0 | CNR4, its own calibration factor | from 2022-01-07 | 69,724 | 19.9 % |
| 1 | CNR1 at 12.83 µV/W/m^2^, the pyrgeometer's own factor | 2016-06-07 to 2021-12-14 | 96,037 | 27.4 % |
| 2 | CNR1 at 10.03 µV/W/m^2^, the pyranometer's factor — **reads low** | before 2016-06-07 | 184,104 | 52.5 % |
| 3 | changeover, era undetermined | 2021-12-15 to 2022-01-06 | 1,104 | 0.3 % |

Code `3` marks the three weeks between the installation of the CNR4 and the arrival
of its own constants in the logger program, during which the new instrument was read
through the old instrument's factor. Neither the maintenance record nor the data can
assign this interval to either side.

## Coverage

The measurement begins on **2005-09-14 13:15**, when the pyrgeometer channel was
wired to the tower logger; there is no longwave record before that date and none is
reconstructed. Of the 355,872 records, **350,969 carry a value (98.6 %)**.

The gaps are short. There are 998 of them; 977 are one hour or shorter and only
eight exceed a day. The longest, 20.6 days, runs from 1 to 21 January 2016, the
site-wide outage during which the tower logger was replaced, which `PA` shares
record for record.

: The two years in which measured coverage falls below 95 %. Every other year of
2006-2025 is at least 95 % measured. {#tbl-lwin-coverage}

| year | measured | why |
|---|---|---|
| 2012 | 92.3 % | logger clock error, power-supply failure and storm damage |
| 2016 | 94.3 % | the January outage during which the logger was replaced |

The 2012 faults are the largest interruption inside the measured period. A logger
clock error shifted one block of August 2012 by 15.5 hours; a tower power-supply
failure in late July and August, and storm damage in late October and November, left
records that were removed. Unlike the other tower variables, `LW_IN` shows no
internal sign of either fault: it has no independent reference that could reveal a
level error, and the removal therefore rests on the documented, logger-wide fault
rather than on evidence from this series. Notebook `06` states this and removes the
periods anyway, as the conservative choice.

## What the values are

The exported numbers are **downwelling longwave irradiance**, median 315.85 W m^-2^
and range 135.45 to 441.78 W m^-2^. A pyrgeometer's voltage measures the net
exchange between the sky and the instrument's own body, which at this site is
roughly -50 W m^-2^; the downwelling flux is that net signal plus the instrument's
own emission. That term is already included in every value in this file. A reader who
assumed the raw converted voltage would misread the file by some 370 W m^-2^.

## Known limitations {#known-limitations}

- **The record is not homogeneous across 7 June 2016.** The pyrgeometer's calibration
  factor was corrected on that date, and values before it read low by roughly 17 % of
  the difference between the value and $\sigma T_a^4$. This is more than half the
  record. It is **not corrected**, for a specific reason: undoing it requires
  splitting each stored value back into the instrument's own emission and its net
  signal, which needs the radiometer's body temperature, a channel this product does
  not read and one whose treatment in the processing chain that produced the earlier
  values cannot be verified from the files available. Rescaling with air temperature
  as a proxy would import an unverified model of that chain into the exported
  numbers. The `SOURCE` flag marks the affected era instead.

- **The record also changes across December 2021, and the cause is not established.**
  The radiometer was replaced (CNR1 to CNR4) on 14 December 2021, and the screening
  software changed from `mst` to `diive` at the turn of the year. The two fall on the
  same date and cannot be separated, and there is no reference against which either
  could be tested. What the data show is a change of about 11 % in the clear-sky part
  of the signal, roughly half the size of the June 2016 change, which accounts for
  most of the 6.5 W m^-2^ that separates the two periods once the temperature
  difference between them is removed. It is equally consistent with a change in the
  instrument, with the change of screening, and with the warming and moistening of
  the lower atmosphere that has been moving the same statistic since about 2017.
  Nothing is corrected. Analyses crossing that date should allow for a change of this
  order, and the `SOURCE` flag separates the two instruments.

- **The January 2016 acquisition change did *not* move this series.** It is recorded
  here because the same changeover moved `TA_T1_47_1` by 1.3 °C, and because it is
  easy to confuse with the June date five months later. The logger program installed
  at the changeover applies the same conversion as the programs before it, and the
  four months between the two 2016 dates behave like an ordinary year.

- **The series contains gaps and is not gap-filled.** Code that assumes a complete
  series will break or silently propagate `NaN`. `SW_IN`, `TA` and `PPFD_IN` are
  complete; this product is not.

- **There is no independent reference for this variable at the site.** MeteoSwiss
  Lägern carries no longwave channel, NABEL has no pyrgeometer, and the below-canopy
  sensor installed in 2024 measures a different quantity. Every statement above
  therefore rests on physics, the relation between longwave radiation and air
  temperature, rather than on a second instrument, and the evidence is correspondingly
  weaker than for `SW_IN` or `TA`. Where it does not reach far enough to identify a
  cause, notebook `06` says so.

- **Absolute accuracy is limited by the calibration that was applied.** Both eras of
  the CNR1 convert the pyrgeometer with a single factory constant and no correction
  for the instrument's own dome. The two radiometer channels of the successor
  instrument differ by 28 % in sensitivity, which is the scale of the error the June
  2016 entry removed; what remains after it is the ordinary field uncertainty of an
  unventilated pyrgeometer, which is larger than for the shortwave channel of the same
  instrument.
