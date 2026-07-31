# Meteo Data

TODO IN PROGRESS

## Calendar explorer

**[Every month of the record on one grid](dashboards/METEO_CALENDAR_explorer.html)**

Twenty-one years by twelve months, one tile per month, coloured by the metric
selected and badged with what was notable in that month. Open a month for its
statistics against the calendar-month normal, its rank among the same month of every
other year, and a calendar of its days; open a day for that day's statistics, its
flags and its diurnal course. The page aggregates and compares the exported products
and corrects nothing. A month too sparsely measured to support a claim carries no
badge and is ranked against nothing. The file is standalone and works offline.

## Pages for the individual variables

Every meteo parameter has its own page, carrying its columns, units, coverage,
flag codes and known limitations, and linking the notebooks that produced it.
This page stays general: the conventions shared by all products, what they
contain, and how they are built. A limitation belongs to a variable and is
documented on that variable's page.

The list below is the full set of parameters. Pages are added as they are
written, so an entry without a link is a page not yet written rather than a
variable missing from the dataset.

Each parameter also has an **interactive dashboard**: one self-contained page
summarising the exported product year by year, with coverage and provenance,
seasonality, distributions, extremes, trends, and the comparison against the
reference station where one exists. Every chart carries a table view of the same
numbers, and the file is standalone and works offline.

: The per-variable pages and dashboards. {#tbl-meteo-pages}

| parameter | measures | page | dashboard |
|---|---|---|---|
| `SW_IN` | incoming shortwave radiation | [Incoming shortwave radiation at 47 m](Meteo_Data_SW_IN.html) | [`SW_IN`](dashboards/METEO_SW_IN_dashboard.html) |
| `TA` | air temperature at 47 m | [Air temperature at 47 m](Meteo_Data_TA.html) | [`TA`](dashboards/METEO_TA_dashboard.html) |
| `PPFD_IN` | photosynthetic photon flux density | [Photosynthetic photon flux density at 47 m](Meteo_Data_PPFD_IN.html) | [`PPFD_IN`](dashboards/METEO_PPFD_IN_dashboard.html) |
| `RH` | relative humidity | [Relative humidity at 47 m](Meteo_Data_RH.html) | [`RH`](dashboards/METEO_RH_dashboard.html) |
| `PA` | air pressure | [Air pressure at 47 m](Meteo_Data_PA.html) | [`PA`](dashboards/METEO_PA_dashboard.html) |
| `LW_IN` | incoming longwave radiation | [Incoming longwave radiation at 47 m](Meteo_Data_LW_IN.html) | [`LW_IN`](dashboards/METEO_LW_IN_dashboard.html) |
| `VPD` | vapour pressure deficit | [Vapour pressure deficit at 47 m](Meteo_Data_VPD.html) | [`VPD`](dashboards/METEO_VPD_dashboard.html) |
| `PREC` | precipitation | [Precipitation at 47 m](Meteo_Data_PREC.html) | [`PREC`](dashboards/METEO_PREC_dashboard.html) |
| `SWC` | soil water content, five depths | [Soil water content at the forest floor](Meteo_Data_SWC.html) | [0.05](dashboards/METEO_SWC_0.05_dashboard.html) / [0.1](dashboards/METEO_SWC_0.1_dashboard.html) / [0.2](dashboards/METEO_SWC_0.2_dashboard.html) / [0.3](dashboards/METEO_SWC_0.3_dashboard.html) / [0.5](dashboards/METEO_SWC_0.5_dashboard.html) m |
| `TS` | soil temperature, seven depths | [Soil temperature at the forest floor](Meteo_Data_TS.html) | [0.05](dashboards/METEO_TS_0.05_dashboard.html) / [0.1](dashboards/METEO_TS_0.1_dashboard.html) / [0.15](dashboards/METEO_TS_0.15_dashboard.html) / [0.2](dashboards/METEO_TS_0.2_dashboard.html) / [0.3](dashboards/METEO_TS_0.3_dashboard.html) / [0.5](dashboards/METEO_TS_0.5_dashboard.html) / [0.6](dashboards/METEO_TS_0.6_dashboard.html) m |

A dashboard describes the column a user should analyse. Where a product exports
both a measured and a `_HOMOGENIZED` column, the dashboard uses the homogenised
one throughout and names it at the top.

## The meteo products

Ten notebooks turn the screened tower and soil measurements into one file per variable, written as parquet and CSV. Each file holds its value columns plus a provenance flag saying, half hour by half hour, whether the number was measured, corrected, reconstructed or modelled.

One notebook produces one variable. They are numbered `01` to `10` in the order in which they may read one another — `02` and `03` read `01`, and `07` reads `01`, `02` and `04` — and those numbers are used as shorthand throughout this documentation and inside the notebooks themselves. In the repository they are the folder `workflow/10_METEO/30_PRODUCTS/`; on this site they are rendered under [Notebooks](notebooks/index.html), and each is listed with its number and variable under [How they are built](#how-they-are-built) below.

Two conventions apply to every product.

**Timestamps are `TIMESTAMP_MID`, local time (UTC+1), on a continuous 30-minute index with no daylight saving.** The label sits in the middle of the averaging period, so `09:15` covers 09:00 to 09:30.

**The provenance flag distinguishes a measurement from an estimate and should be applied before analysis.** `PA` is the only product without one. Neither `PA` nor `LW_IN` is gap-filled and both retain their gaps; the `LW_IN` flag names the instrument and calibration behind each value rather than marking a fill.

: Meteo variables currently available. Coverage is the share of that file's own period carrying a value; flag columns are defined at every record. `<d>` is the depth in metres. {#tbl-meteo-vars}

| variable | unit | period | coverage | provenance flag |
|---|---|---|---|---|
| `SW_IN_T1_47_1_gfXG` | W m^-2^ | 2004-2025 | 100 % | `ISFILLED` |
| `TA_T1_47_1_gfXG` | °C | 2004-2025 | 100 % | `ISFILLED` + `SOURCE` |
| `TA_T1_47_1_HOMOGENIZED_gfXG` | °C | 2004-2025 | 100 % | `ISFILLED` + `SOURCE` |
| `PPFD_IN_T1_47_1_gfXG` | µmol m^-2^ s^-1^ | 2004-2025 | 100 % | `ISFILLED` |
| `RH_T1_47_1` | % | 2004-2025 | 100 % | `MISSING` + `SOURCE` |
| `PA_T1_47_1` | kPa | 2005-2025 | 98.9 % | none, gaps left in |
| `LW_IN_T1_47_1` | W m^-2^ | 2005-2025 | 98.6 % | `SOURCE`, gaps left in |
| `VPD_T1_47_1` | kPa | 2004-2025 | 100 % | `ISFILLED` + `SOURCE` |
| `PREC_TOT_T1_47_1` | mm (30 min) | 2004-2025 | 99.4 % | `SOURCE` + `ISFILLED` |
| `PREC_TOT_T1_47_1_HOMOGENIZED` | mm (30 min) | 2004-2025 | 99.4 % | `SOURCE` + `ISFILLED` |
| `SWC_FF1_<d>_1`, depths 0.05 / 0.1 / 0.2 / 0.3 / 0.5 m | % VWC | 2004-2025 | 26-96 % | `SOURCE` |
| `SWC_FF1_<d>_1_HOMOGENIZED`, the four depths above 0.5 m | % VWC | 2004-2025 | 81-96 % | `SOURCE` |
| `TS_FF1_<d>_HOMOGENIZED_GAPFILLED`, depths 0.05 / 0.1 / 0.15 / 0.2 / 0.3 / 0.5 / 0.6 m | °C | 2004-2025 | 27-94 % | `METHOD` + `SUSPECT` |
| eighteen individual `TS_FF1_*` / `TS_PRF_FF1_*` channels | °C | 2004-2025 | 21-72 % | none, raw as screened |

Flag names are given by their suffix; the full column is `FLAG_<variable>_<suffix>`.

### The derived columns

A `_HOMOGENIZED` or `_GAPFILLED` column sits beside the measured one rather than replacing it, so the measured record remains recoverable.

**`_HOMOGENIZED`** removes a step that a hardware change left in the raw values, so the eras either side become comparable. It does not make either era more accurate: what it removes is the *change* in the instrument's bias, not the bias itself. `TA` carries one because its sensor and acquisition system were replaced together in January 2016, `PREC` one because its acquisition system changed in 2018, `SWC` one per depth because the soil profile was replaced in 2020. Most are a rescaling of the earlier era onto the level of the later one; `TA` also corrects the difference between the two sensors' radiation shields, which acts only in daylight.

**`_GAPFILLED`** means a model produced some of the values. For `TS` the model is a regression on the remaining depths of the profile, and the `METHOD` flag identifies which values are measured and which are modelled.

### Known limitations

Every product carries limitations that are specific to it, and they are documented on
that variable's own page under *Known limitations*: which dates the record is not
homogeneous across, which columns are estimates rather than measurements, and what a
trend or a period comparison computed over that series contains besides the weather.
@tbl-meteo-pages links all ten pages.

Two limitations are properties of a reference rather than of a product, and recur on
several of those pages: the MeteoSwiss Lägern station changed level in October 2010, when its
instrumentation was rebuilt, and the NABEL series on the same tower stop being
independent records in mid-2018. Neither changes a value in any file, but both change
what a comparison against those series means.

### How they are built {#how-they-are-built}

Every product pulls the quality-screened half-hourly record from the database, joins the older `mst` screening to the newer `diive` one with `combine_first`, converts timestamps, applies the site's shared 2012 repairs where the variable sat on that logger, and writes out after a set of checks. Independent references do the validation and, where a product is filled, much of the filling: MeteoSwiss Lägern 2.5 km away, NABEL at 49 m on the same tower until 2018, the MeteoSwiss gauge at Ehrendingen for rain, and for `PREC` alone every MeteoSwiss station within 21 km. The soil products have no external reference and are checked against the other depths of their own profile.

Each notebook documents its own decisions and the evidence behind them, and each is named for the variable it produces:
[`01` `SW_IN`](notebooks/10_METEO/30_PRODUCTS/01_METEO_SW_IN_2004-2025.html),
[`02` `TA`](notebooks/10_METEO/30_PRODUCTS/02_METEO_TA_2004-2025.html),
[`03` `PPFD_IN`](notebooks/10_METEO/30_PRODUCTS/03_METEO_PPFD_IN_2004-2025.html),
[`04` `RH`](notebooks/10_METEO/30_PRODUCTS/04_METEO_RH_2004-2025.html),
[`05` `PA`](notebooks/10_METEO/30_PRODUCTS/05_METEO_PA_2005-2025.html),
[`06` `LW_IN`](notebooks/10_METEO/30_PRODUCTS/06_METEO_LW_IN_2005-2025.html),
[`07` `VPD`](notebooks/10_METEO/30_PRODUCTS/07_METEO_VPD_2004-2025.html),
[`08` `PREC`](notebooks/10_METEO/30_PRODUCTS/08_METEO_PREC_2004-2025.html),
[`09` `SWC`](notebooks/10_METEO/30_PRODUCTS/09_METEO_SWC_FF1_2004-2025.html),
[`10` `TS`](notebooks/10_METEO/30_PRODUCTS/10_METEO_TS_FF1_2004-2025.html).
A handful of unnumbered notebooks beside them export nothing and settle one question each, such as [`RADIATION_SENSOR_CONTINUITY`](notebooks/10_METEO/30_PRODUCTS/RADIATION_SENSOR_CONTINUITY.html); the variable pages link the ones that bear on them.

