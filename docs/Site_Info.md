# Site information

CH-LAE (Lägeren) is a managed mixed deciduous mountain forest on the south-facing
slope of the Lägern, in the Jura mountain range that marks the northern boundary
of the Swiss Plateau, north-west of Zurich [@etzold_carbon_2011]. The stand is
diverse in species, diameter class and tree age, and has a complex canopy
structure [@etzold_carbon_2011; @shekhar_contrasting_2024]. Eddy covariance
measurements started in **April 2004** and are ongoing.

This page draws on the
[Swiss FluxNet site page for CH-LAE](https://www.swissfluxnet.ethz.ch/index.php/sites/site-info-ch-lae/)
and on two published site descriptions, @etzold_carbon_2011 and
@shekhar_contrasting_2024. Every value below names its source; where sources
disagree, both are given. Details of the eddy covariance setup — sonic
anemometer, gas analysers, sensor separations and the setup periods the flux runs
are organised by — are listed per year in [Yearly Notes](Yearly_Notes.md); the
dataset itself is described in [Overview](Overview.md).

![The CH-LAE tower in December 2019. The instrument platform carrying the eddy covariance system and the meteorological sensors stands clear of a leafless deciduous canopy with scattered conifers; the Swiss Plateau below is under fog. Photo: Markus Staudinger, Grassland Sciences Group, ETH Zurich](images/CH-LAE_2019_tower_byMarkusStaudinger_1620x1080.jpg){#fig-site-tower}

## Location and terrain

: Site identification and position. Coordinates, elevation and IGBP class are
from the Swiss FluxNet site page; slope, region and altitudinal zone are from
@etzold_carbon_2011. {#tbl-site-location}

| property | value |
|---|---|
| site code | CH-LAE |
| FLUXNET ID | CH-Lae |
| site name | Lägeren, Canton of Aargau, Switzerland |
| latitude | 47°28'42.0" N (47.478333) |
| longitude | 8°21'51.8" E (8.364389) |
| elevation | 689 m a.s.l. |
| IGBP class | Mixed forest (MF) |
| geographical region | Swiss Jura |
| altitudinal zone | montane |
| slope | 27°, south-facing |

The slope is the property of this site that most affects the flux measurement.
Advection on it contributes measurably to the carbon budget, and the site has
been used as a study case for that term [@etzold_contribution_2010]. That work is
also the origin of the constant friction-velocity threshold of 0.3 m s^-1^ that
later studies of this site have applied [@shekhar_contrasting_2024]; the
threshold used in the present dataset is documented under [QCF](QCF.md), not
here.

::: {.callout-note title="Published positions differ from the values above"}

The position in @tbl-site-location is the correct one. Some published
descriptions of the site give slightly different values: **682 m a.s.l.** instead
of 689 m [@etzold_carbon_2011; @shekhar_contrasting_2024], and coordinates about
50 m away, 47°28'40.8" N, 8°21'55.2" E [@etzold_carbon_2011]. The prose of the
Swiss FluxNet page separately describes the site as being at 800 m a.s.l., which
characterises the mountain rather than the tower. Use the values in the table.

:::

The tower position on a map:
[OpenStreetMap](https://www.openstreetmap.org/?mlat=47.478333&mlon=8.364389#map=15/47.478333/8.364389)
· [Swiss national map (swisstopo)](https://map.geo.admin.ch/?swisssearch=47.478333,8.364389)
· [Google Maps](https://www.google.com/maps/search/?api=1&query=47.478333,8.364389).
The swisstopo map carries the relief and the forest cover, which show the slope
and the extent of the stand better than a street map does.

![The view from the top of the tower on 17 April 2014, over the canopy and onto the Swiss Plateau, with snow-covered mountains on the horizon. The stand is in early leaf flush, the broadleaves light green against the dark conifers. In the foreground are the tower's own instrument booms, among them a cup anemometer and a shielded temperature and humidity sensor.](images/CH-LAE_2014_2014-04-17_panorama_IMAG0013-14.jpg){#fig-site-panorama}

## Climate

Published long-term means for the site differ, because they cover different
periods and rest on different measurements. Both are given here rather than one.

: Long-term air temperature and precipitation means, with the period and source
of each. {#tbl-site-climate-means}

| period | mean annual air temperature | mean annual precipitation | source |
|---|---|---|---|
| 1989-2009 | 7.4 °C | 1000 mm | @etzold_carbon_2011, from MeteoSwiss |
| 2004-2020 | 8.67 °C | 801 mm | @shekhar_contrasting_2024 |
| 2005-2020 | 8.6 °C | not given | Swiss FluxNet site page |

The two temperature means are consistent with a warming record rather than in
conflict: the Swiss FluxNet page reports 7.8 °C over 2005-2012 against 9.4 °C
over 2013-2020, a difference of 1.6 °C between the two halves of that period. The
two precipitation figures are **not** directly comparable — they cover different
years and do not come from the same gauge — so neither should be used as *the*
site value without saying which it is.

::: {.callout-warning title="To do: recompute the climate figures from this dataset"}

Every climate value on this page — the means above, the extremes below, and the
growing-season conditions — comes from an external source or a published study,
and each covers a period that ends before this dataset does. They are to be
recomputed over **2004-2025** from the products documented here: air temperature
from [`02_METEO_TA`](Meteo_Data_TA.md), precipitation from
[`08_METEO_PREC`](Meteo_Data_PREC.md), vapour pressure deficit from
[`07_METEO_VPD`](Meteo_Data_VPD.md) and soil water content from
[`09_METEO_SWC`](Meteo_Data_SWC.md). Recomputed values will be cited as
**this dataset** and will state their own period.

Once they exist, the tables are to hold **only** this dataset's numbers; the
published values are then dropped rather than kept alongside. The papers remain
cited on this page, so a figure quoted from one of them can still be traced to
its source.

:::

: Temperature extremes reported on the Swiss FluxNet site page for 2005-2020.
{#tbl-site-climate-extremes}

| property | value |
|---|---|
| highest recorded temperature | 33.5 °C (25 July 2019) |
| lowest recorded temperature | -17.2 °C (7 February 2012) |

The site air temperature record is affected by a sensor and acquisition change in
January 2016; see [Air temperature](Meteo_Data_TA.md) for what that means for a
comparison of early against late years. Measured precipitation at the tower is
documented under [Precipitation](Meteo_Data_PREC.md).

Three MeteoSwiss stations lie close enough to serve as references: **Lägern**
(845 m a.s.l., 2.5 km), **Ehrendingen** (428 m a.s.l., 3.8 km) and
**Zürich/Kloten** (426 m a.s.l.). Which of them covers which variable is not
uniform — Lägern measures no precipitation and no longwave radiation, and
Ehrendingen measures precipitation only. The reference used for each product is
named on that product's page under [Meteorological data](Meteo_Data.md).

### Growing season and dryness

@shekhar_contrasting_2024 characterise the site's growing season and its
water-related conditions over 2005-2022. These are useful for judging which years
in the record are climatically unusual.

: Growing-season conditions over 2005-2022, after @shekhar_contrasting_2024. The
growing season is day of year 115-275, approximately 25 April to 2 October.
{#tbl-site-gs}

| property | value |
|---|---|
| mean soil moisture | 0.21 m^3^ m^-3^ |
| 10th percentile of soil moisture | 0.14 m^3^ m^-3^ |
| mean vapour pressure deficit | 1.1 kPa |
| 90th percentile of vapour pressure deficit | 2.1 kPa |

Days below the soil-moisture percentile occurred mainly in **2006, 2009, 2015 and
2018**, and days that were both soil-dry and air-dry fell largely in **2015, 2018
and 2022**; 2015 had the most extreme-dryness days of any year in that period
[@shekhar_contrasting_2024]. Soil moisture and vapour pressure deficit at the
site are negatively correlated (*r* = -0.36), more strongly so than at the
subalpine site the same study compares against.

## Vegetation and stand structure

The stand is dominated by European beech (*Fagus sylvatica* L.), with ash
(*Fraxinus excelsior* L.) and Norway spruce (*Picea abies* (L.) Karst.) the other
abundant species [@etzold_carbon_2011]. Canopy composition has been quantified as
beech 40 %, ash 19 %, sycamore maple (*Acer pseudoplatanus* L.) 13 %, European
silver fir (*Abies alba* Mill.) 8 % and Norway spruce 4 %
[@paul-limoges_below-canopy_2017; @shekhar_contrasting_2024]. The Swiss FluxNet
site page additionally lists *Tilia cordata* Mill., *Quercus robur* L. and
*Ulmus glabra* Huds. as present. In spring, bear's garlic (*Allium ursinum* L.)
forms a dense understorey, growing from about March to June
[@etzold_carbon_2011; @shekhar_contrasting_2024].

: Stand characteristics. {#tbl-site-stand}

| property | value | source |
|---|---|---|
| mean height of dominant trees | 30.6 m | @etzold_carbon_2011; Swiss FluxNet |
| top-height diameter | 72.18 cm (quadratic mean of the 100 thickest trees per hectare) | Swiss FluxNet |
| stem density, DBH ≥ 12 cm | 503 trees (2011) | Swiss FluxNet |
| leaf area index | 4.1 ± 0.3 m^2^ m^-2^ (June 2006) | Swiss FluxNet |
| maximum leaf area index | 1.7-5.5 m^2^ m^-2^ | @etzold_carbon_2011 |
| age of dominant *Fagus sylvatica* | 52-155 years | @etzold_carbon_2011 |
| age of dominant *Picea abies* | 105-185 years | @etzold_carbon_2011 |
| maximum age, *Fagus sylvatica* | approximately 150 years | Swiss FluxNet |
| maximum age, *Picea abies* | 120-170 years | Swiss FluxNet |

The eddy covariance system and the meteorological sensors of this dataset are
mounted at 47 m, well above the mean canopy height of about 30 m
[@etzold_carbon_2011; @shekhar_contrasting_2024].

## Soil and geology

The bedrock is limestone, marl and sandstone, with transition zones between them
(Swiss FluxNet site page). Soils are **rendzic leptosols** (rendzinas) and
**haplic cambisols** in the World Reference Base classification
[@etzold_carbon_2011]. The litter layer is thin: leaf litter decomposes nearly
completely within one year (Swiss FluxNet site page).

: Soil properties reported by @etzold_carbon_2011. {#tbl-site-soil}

| property | value |
|---|---|
| soil pH | 4.0-7.5 |
| soil carbon stock, 0-20 cm | 8.4-9.6 kg m^-2^ |

The pH range is wide because the two soil types differ: rendzinas over limestone
are near-neutral to alkaline, the cambisols acidic. Soil moisture and soil
temperature measured at the forest floor are documented under
[Soil water content](Meteo_Data_SWC.md) and
[Soil temperature](Meteo_Data_TS.md).

## Management and footprint

The forest is a high forest, and the two halves of the flux footprint are managed
differently. The **southern** part has been managed under Forest Stewardship
Council certification since 1998; the **northern** part is a nature reserve in
which tree harvesting stopped around the late 1990s. Footprint modelling
indicates that the eddy covariance fluxes draw on both parts in roughly equal
proportion [@etzold_carbon_2011].

This matters when the fluxes are interpreted: the measurement is not of a single
management regime but an approximately even mixture of a managed and an unmanaged
stand. Management events recorded for the site are listed under
[Management data](Management_Data.md).

## Monitoring programmes and networks

The site belongs to several programmes beyond Swiss FluxNet, which is why more
than one measurement record exists at the same location:

- **Swiss FluxNet**, operated by the Grassland Sciences Group, ETH Zurich, which
  runs the eddy covariance system this dataset is built from
  [@shekhar_contrasting_2024].
- **NABEL**, the Swiss national air pollution monitoring network, which operates
  its own meteorological sensors on the same tower [@etzold_carbon_2011]. The
  NABEL air temperature and radiation measurements at 49 m are used as co-located
  references in the meteorological products; that series ends in mid-2018.
- **LWF**, the long-term forest ecosystem research programme of WSL
  (Swiss Federal Institute for Forest, Snow and Landscape Research)
  (Swiss FluxNet site page).
- **CarboEurope IP**, the European carbon flux network the site joined at the
  start of the measurements (Swiss FluxNet site page).

The site is not an ICOS station. @shekhar_contrasting_2024 name ICOS Class 1
status for the subalpine site CH-Dav, which they treat alongside CH-LAE, not for
CH-LAE itself.

## Further information

- [Swiss FluxNet site page for CH-LAE](https://www.swissfluxnet.ethz.ch/index.php/sites/site-info-ch-lae/)
  — the site description, and where the numbered notes referenced by the setup
  table in [Yearly Notes](Yearly_Notes.md) are defined.
- [EC raw binary format for CH-LAE](https://www.swissfluxnet.ethz.ch/index.php/sites/site-info-ch-lae/ec-raw-binary-format-ch-lae/)
  — the setup periods, their raw file ranges and the notes that document
  corrections and unusable periods.
- [CH-LAE FP2022 (2004-2022)](https://doi.org/10.3929/ethz-b-000582198) — the
  previous release of this dataset, in the ETH Research Collection
  [@hortnagl_ch-lae_2023].
- [Instrumentation](Instrumentation.md) — the instruments deployed at the site and
  their measurement periods.

## References

::: {#refs}
:::
