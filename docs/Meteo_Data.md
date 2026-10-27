# Meteo Data

Thirteen meteo products from the CH-LAE tower and forest-floor soil profile, each a
half-hourly file with its value columns and provenance flags. Products `01` to `07` run to
30 September 2026; products `08` to `13` still end on 31 December 2025. This page covers
what all products share. Each variable has its own page with its columns, units, coverage,
flag codes and known limitations.

## Pages for the individual variables

An entry without a working link is a page or dashboard not yet written, not a variable
missing from the dataset.

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
| `G` | soil heat flux, three plates | [Soil heat flux at the forest floor](Meteo_Data_G.html) | [`G`](dashboards/METEO_G_dashboard.html) |
| `SW_OUT` | outgoing shortwave radiation | [Outgoing shortwave radiation at 47 m](Meteo_Data_SW_OUT.html) | [`SW_OUT`](dashboards/METEO_SW_OUT_dashboard.html) |
| `LW_OUT` | outgoing longwave radiation | [Outgoing longwave radiation at 47 m](Meteo_Data_LW_OUT.html) | [`LW_OUT`](dashboards/METEO_LW_OUT_dashboard.html) |

A dashboard is one standalone page per exported series: coverage and provenance,
seasonality, distributions, extremes, trends and, where one exists, the comparison against
the reference station, with a table view behind every chart. It works offline. Where a
product exports both a measured and a `_HOMOGENIZED` column, the dashboard uses the
homogenised one and names it at the top.

## The merged file and FP2026.1

Notebook `99` joins all thirteen products onto one half-hourly index. The file is
`99_METEO_MERGED_2004-2026.09` (parquet and CSV): 398,832 records from 2004-01-01 00:15 to
2026-09-30 23:45, with 61 columns, 31 data series and 30 flag columns. The values are exactly
what each product notebook exported; the merge computes and corrects nothing.

- **`01` to `07`** (`SW_IN`, `TA`, `PPFD_IN`, `RH`, `PA`, `LW_IN`, `VPD`) run to
  30 September 2026.
- **`08` to `13`** (`PREC`, `SWC`, `TS`, `G`, `SW_OUT`, `LW_OUT`) still end on
  31 December 2025. Their columns are `NaN` from January to September 2026 until their
  notebooks are extended.
- For `TS` and `G` the merged file carries only the reconciled series, one per depth and
  one plate mean. The individual channels and plates stay in the product files.

The file `99_METEO_MERGED_2004-2026.09_INFO.md`, written beside the data, lists every
column with its unit, range and flag codes, and the reason each series has gaps. Read the
column list there; this page does not repeat it.

**FP2026.1 carries all 61 meteo columns** of the merged file, cut to the FP2026.1 period,
1 January 2016 to 30 September 2026. The six products that end in 2025 are therefore empty
in FP2026.1 for January to September 2026. See [Dataset versions](Dataset_Versions.html).

## Calendar explorer

**[Every month of the record on one grid](dashboards/METEO_CALENDAR_explorer.html)**

One tile per month, coloured by the selected metric and marked with what was notable in
that month. The grid is drawn at three resolutions: months, meteorological seasons, and
single days. The daily raster is the only one of the three that does not split a spell at a
boundary. Open a month for its statistics against the calendar-month normal, its rank among
the same month of the other years, and a calendar of its days; open a day for its
statistics, flags and diurnal course.

The explorer aggregates and compares the exported products and corrects nothing. A month
with too few measured records carries no badge and is not ranked. The normal is a period
average over the whole record, not a stationary climate, so the trend of each calendar month
is shown with it, together with the estimator, the coverage rule and the significance test.
The file is standalone and works offline.

## The meteo products

Each product notebook writes one file per variable as parquet and CSV. The notebooks are
numbered `01` to `13` in the order in which they may read one another: `02` and `03` read
`01`, `04` reads `02`, and `07` reads `02` and `04`. These numbers are used as shorthand
throughout the documentation. In the repository the notebooks are in
`workflow/10_METEO/30_PRODUCTS/`; on this site they are under
[Notebooks](notebooks/index.html) and are linked under
[How they are built](#how-they-are-built).

Two conventions apply to every product.

**Timestamps are `TIMESTAMP_MIDDLE`, local standard time (UTC+01:00), on a continuous
30-minute index with no daylight saving.** The timestamp marks the middle of the averaging
period, so `09:15` covers 09:00 to 09:30.

**Apply the provenance flag before analysis.** It says, record by record, whether a value
was measured, corrected, reconstructed or modelled. `PA` is the only product without a
flag. `PA`, `LW_IN`, `SWC`, `G`, `SW_OUT` and `LW_OUT` are not gap-filled, so their gaps are
`NaN`.

: Meteo variables in the product files. Coverage is the share of that file's own period
carrying a value; flag columns are defined at every record. `<d>` is the depth in metres. {#tbl-meteo-vars}

| variable | unit | period | coverage | provenance flag |
|---|---|---|---|---|
| `SW_IN_T1_47_1_gfXG` | W m^-2^ | 2004-Sep 2026 | 100 % | `ISFILLED` |
| `TA_T1_47_1_gfXG` | °C | 2004-Sep 2026 | 100 % | `ISFILLED` + `SOURCE` |
| `TA_T1_47_1_HOMOGENIZED_gfXG` | °C | 2004-Sep 2026 | 100 % | `ISFILLED` + `SOURCE` |
| `PPFD_IN_T1_47_1_gfXG` | µmol m^-2^ s^-1^ | 2004-Sep 2026 | 100 % | `ISFILLED` |
| `RH_T1_47_1` | % | 2004-Sep 2026 | 100 % | `MISSING` + `SOURCE` |
| `RH_T1_47_1_HOMOGENIZED` | % | 2004-Sep 2026 | 100 % | `MISSING` + `SOURCE` |
| `PA_T1_47_1` | kPa | 2005-Sep 2026 | 98.9 % | none, gaps left in |
| `LW_IN_T1_47_1` | W m^-2^ | 2005-Sep 2026 | 98.7 % | `SOURCE`, gaps left in |
| `VPD_T1_47_1` | kPa | 2004-Sep 2026 | 100 % | `ISFILLED` + `SOURCE` |
| `VPD_T1_47_1_HOMOGENIZED` | kPa | 2004-Sep 2026 | 100 % | `ISFILLED` + `SOURCE` |
| `PREC_TOT_T1_47_1` | mm (30 min) | 2004-2025 | 99.4 % | `SOURCE` + `ISFILLED` |
| `PREC_TOT_T1_47_1_HOMOGENIZED` | mm (30 min) | 2004-2025 | 99.4 % | `SOURCE` + `ISFILLED` |
| `SWC_FF1_<d>_1`, depths 0.05 / 0.1 / 0.2 / 0.3 / 0.5 m | % VWC | 2004-2025 | 26-96 % | `SOURCE` |
| `SWC_FF1_<d>_1_HOMOGENIZED`, the four depths above 0.5 m | % VWC | 2004-2025 | 81-96 % | `SOURCE` |
| `TS_FF1_<d>_HOMOGENIZED_GAPFILLED`, depths 0.05 / 0.1 / 0.15 / 0.2 / 0.3 / 0.5 / 0.6 m | °C | 2004-2025 | 27-94 % | `METHOD` + `SUSPECT` |
| eighteen individual `TS_FF1_*` / `TS_PRF_FF1_*` channels | °C | 2004-2025 | 21-72 % | none, raw as screened |
| `G_FF1_0.05_<n>`, three plates | W m^-2^ | 2004-2025 | 73-96 % | `SOURCE` |
| `G_FF1_0.05_HOMOGENIZED`, the plate mean | W m^-2^ | 2004-2025 | 95.6 % | `NPLATES` |
| `SW_OUT_T1_47_1` | W m^-2^ | 2005-2025 | 98.8 % | `INSTRUMENT` + `SOURCE` |
| `LW_OUT_T1_47_1` | W m^-2^ | 2005-2025 | 98.1 % | `SOURCE`, gaps left in |

Flag names are given by their suffix; the full column is `FLAG_<variable>_<suffix>`.

### The derived columns

A `_HOMOGENIZED` or `_GAPFILLED` column sits beside the measured one rather than replacing
it, so the measured record remains available.

**`_HOMOGENIZED`** removes a step that a hardware change left in the values, so the eras
on either side can be compared. It does not make either era more accurate: it removes the
change in the instrument's bias, not the bias itself. `TA` and `RH` carry one because their
probe and acquisition system were replaced together in January 2016 and the probe again in
June 2026, and `VPD` because it is computed from them. `PREC` carries one because its
acquisition system changed in 2018, and `SWC` one per depth because the soil profile was
replaced in 2020. Most rescale the earlier era onto the level of the later one. `TA` also
corrects the difference between the radiation shields of the probes, which acts only in
daylight.

**`_GAPFILLED`** means a model produced some of the values. For `TS` the model is a
regression on the other depths of the profile, and the `METHOD` flag says which values are
measured and which are modelled.

### Known limitations

The limitations of each product are on that variable's page under *Known limitations*:
the dates across which the record is not homogeneous, the columns that are estimates rather
than measurements, and what a trend or period comparison over the series contains besides
the weather. @tbl-meteo-pages links every page.

Two limitations belong to a reference rather than to a product and recur on several pages.
The MeteoSwiss Lägern station changed level in October 2010, when its instrumentation was
rebuilt. The NABEL series on the same tower stop being independent records in mid-2018.
Neither changes a value in any file, but both change what a comparison against those
series means.

### How they are built {#how-they-are-built}

Every product reads the quality-screened half-hourly record from the database, joins the
older `mst` screening to the newer `diive` one, applies the site's shared 2012 repairs where
the variable was on the affected logger, and is checked before it is written. Independent
references do the validation and, where a product is filled, much of the filling:
MeteoSwiss Lägern 2.5 km away, NABEL at 49 m on the same tower until 2018, the MeteoSwiss
gauge at Ehrendingen for rain, and for `PREC` every MeteoSwiss station within 21 km. The
soil products have no external reference and are checked against the other depths of their
own profile. [Meteo Product Chain](Meteo_Product_Chain.html) shows which product reads which.

Each notebook documents its own decisions and the evidence behind them:
[`01` `SW_IN`](notebooks/10_METEO/30_PRODUCTS/01_METEO_SW_IN_2004-2026.09.html),
[`02` `TA`](notebooks/10_METEO/30_PRODUCTS/02_METEO_TA_2004-2026.09.html),
[`03` `PPFD_IN`](notebooks/10_METEO/30_PRODUCTS/03_METEO_PPFD_IN_2004-2026.09.html),
[`04` `RH`](notebooks/10_METEO/30_PRODUCTS/04_METEO_RH_2004-2026.09.html),
[`05` `PA`](notebooks/10_METEO/30_PRODUCTS/05_METEO_PA_2005-2026.09.html),
[`06` `LW_IN`](notebooks/10_METEO/30_PRODUCTS/06_METEO_LW_IN_2005-2026.09.html),
[`07` `VPD`](notebooks/10_METEO/30_PRODUCTS/07_METEO_VPD_2004-2026.09.html),
[`08` `PREC`](notebooks/10_METEO/30_PRODUCTS/08_METEO_PREC_2004-2025.html),
[`09` `SWC`](notebooks/10_METEO/30_PRODUCTS/09_METEO_SWC_FF1_2004-2025.html),
[`10` `TS`](notebooks/10_METEO/30_PRODUCTS/10_METEO_TS_FF1_2004-2025.html),
[`11` `G`](notebooks/10_METEO/30_PRODUCTS/11_METEO_G_FF1_2004-2025.html),
[`12` `SW_OUT`](notebooks/10_METEO/30_PRODUCTS/12_METEO_SW_OUT_2005-2025.html),
[`13` `LW_OUT`](notebooks/10_METEO/30_PRODUCTS/13_METEO_LW_OUT_2005-2025.html), and
[`99`](notebooks/10_METEO/30_PRODUCTS/99_METEO_MERGED_2004-2026.09.html), the merge.
Unnumbered notebooks beside them export nothing and each settle one question, such as
[`RADIATION_SENSOR_CONTINUITY`](notebooks/10_METEO/30_PRODUCTS/RADIATION_SENSOR_CONTINUITY.html);
the variable pages link the ones that bear on them.
