# Data dashboards

Interactive summaries of the finished products, one page per series. Each is a
complete standalone HTML file with its own charts and styling: it opens without a
server, works offline, and can be sent to somebody who has neither this site nor
the data.

They are built from the exported product files rather than from the database, so
a dashboard shows exactly the record a user of the dataset would receive. They
are regenerated at every deploy, which means a dashboard cannot describe an older
version of the product than the one currently published.

***

## Calendar explorer

**[Every month of the record on one grid](dashboards/METEO_CALENDAR_explorer.html)**

Twenty-one years by twelve months, one tile per month, coloured by the metric you
select and badged with what was notable in that month. The same grid is drawn at
three resolutions: months, meteorological seasons, and a raster of every day of
the record. The daily raster is the only one of the three that never cuts a spell
in half at a boundary, so a heatwave or a drought that ran across a month end is
visible there and split in the other two.

It reads the meteorological products today, which is why it currently sits beside
the meteo dashboards. It is a calendar over whatever the dataset carries rather
than a meteorological page, so it will move once the flux products land.

***

## Per-variable dashboards

Each one covers a single exported series year by year: coverage and provenance,
seasonality, distributions, extremes, trends, and the comparison against an
independent reference station where one exists. Every chart carries a table view
of the same numbers underneath it, so a figure can be read as values rather than
only as a picture.

The soil profiles get one dashboard per depth rather than one for the profile,
because a depth is the unit that has its own sensor history, its own gaps and its
own limitations.

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

## What a dashboard is not

A dashboard summarises a product; it does not document one. What was corrected,
what was left alone and what is still open belong to the variable, so they live on
that variable's page under [Meteorological data](Meteo_Data.md), and the evidence
behind each decision lives in the notebook that page links to.

So read a dashboard to see what the record looks like, and read the variable page
before drawing a conclusion from it.
