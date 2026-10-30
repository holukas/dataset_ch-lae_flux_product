# Data dashboards

Interactive summaries of the meteorological products, one page per series. Each
dashboard is a standalone HTML file with its own charts and styling. It opens
without a server, works offline, and can be shared with someone who has neither
this site nor the data.

The dashboards are built from the exported product files, not from the database.
They are rebuilt at every deploy of this site.

::: {.callout-note title="The dashboards end in December 2025"}

The dashboards are still built from the product versions that end on
31 December 2025. They do not yet show January to September 2026, although
`SW_IN`, `TA`, `PPFD_IN`, `RH`, `PA`, `LW_IN` and `VPD` in FP2026.1 run to
30 September 2026. The products were re-run when they were extended, so some
values before 2026 also differ from the dataset: gap-filled values of `SW_IN`, `TA`
and `PPFD_IN`, the homogenised `TA`, mainly in 2025, and above all `VPD`. The annual means
of `VPD` in the current product are lower than on its dashboard, by about 0.03 kPa
in 2004-2015 and by 0.005 to 0.007 kPa from 2016. There are no dashboards for the
fluxes yet.

:::

***

## Calendar explorer

**[Every month of the record on one grid](dashboards/METEO_CALENDAR_explorer.html)**

The years 2005 to 2025 by twelve months, one tile per month, coloured by the
selected metric and marked with what was notable in that month. The same grid is
drawn at three resolutions: months, meteorological seasons, and every day of the
record. The daily raster is the only one of the three that never splits a spell
at a boundary, so a heatwave or a drought that ran across a month end is visible
as one event there and split in the other two.

The explorer currently reads only the meteorological products.

***

## Per-variable dashboards

Each dashboard covers a single exported series year by year: coverage and
provenance, seasonality, distributions, extremes, trends, and the comparison
against an independent reference station where one exists. Every chart has a
table of the same numbers below it.

The soil profiles have one dashboard per depth, because each depth has its own
sensor history, gaps and limitations.

### Tower, 47 m

| parameter | dashboard |
|---|---|
| `SW_IN` | [Incoming shortwave radiation](dashboards/METEO_SW_IN_dashboard.html) |
| `SW_OUT` | [Outgoing shortwave radiation](dashboards/METEO_SW_OUT_dashboard.html) |
| `LW_IN` | [Incoming longwave radiation](dashboards/METEO_LW_IN_dashboard.html) |
| `LW_OUT` | [Outgoing longwave radiation](dashboards/METEO_LW_OUT_dashboard.html) |
| `PPFD_IN` | [Photosynthetic photon flux density](dashboards/METEO_PPFD_IN_dashboard.html) |
| `TA` | [Air temperature](dashboards/METEO_TA_dashboard.html) |
| `RH` | [Relative humidity](dashboards/METEO_RH_dashboard.html) |
| `VPD` | [Vapour pressure deficit](dashboards/METEO_VPD_dashboard.html) |
| `PA` | [Air pressure](dashboards/METEO_PA_dashboard.html) |
| `PREC` | [Precipitation](dashboards/METEO_PREC_dashboard.html) |

: Tower dashboards. {#tbl-dash-tower}

### Forest floor

| parameter | dashboard |
|---|---|
| `G` | [Soil heat flux](dashboards/METEO_G_dashboard.html) |
| `SWC` | soil water content at [0.05](dashboards/METEO_SWC_0.05_dashboard.html), [0.1](dashboards/METEO_SWC_0.1_dashboard.html), [0.2](dashboards/METEO_SWC_0.2_dashboard.html), [0.3](dashboards/METEO_SWC_0.3_dashboard.html) and [0.5 m](dashboards/METEO_SWC_0.5_dashboard.html) |
| `TS` | soil temperature at [0.05](dashboards/METEO_TS_0.05_dashboard.html), [0.1](dashboards/METEO_TS_0.1_dashboard.html), [0.15](dashboards/METEO_TS_0.15_dashboard.html), [0.2](dashboards/METEO_TS_0.2_dashboard.html), [0.3](dashboards/METEO_TS_0.3_dashboard.html), [0.5](dashboards/METEO_TS_0.5_dashboard.html) and [0.6 m](dashboards/METEO_TS_0.6_dashboard.html) |

: Forest-floor dashboards. {#tbl-dash-soil}

***

## Dashboards and variable pages

A dashboard summarises a product; it does not document it. What was corrected,
what was left unchanged and what is still open are described on the page of each
variable under [Meteorological data](Meteo_Data.md), and the evidence for each
decision is in the notebook that page links to. Read the variable page before
drawing conclusions from a dashboard.
