# Variables

The variables of the CH-LAE flux product: name, unit and what each stands for. All are
half-hourly, with the timestamp in the middle of the averaging period, in local time (UTC+1, no
daylight saving). Columns, coverage, flags and known limitations of each variable are on its page.

::: {.callout-note title="In progress"}
This list holds what is settled so far. The column names of the published file, and which
auxiliary series it carries (storage terms, friction velocity, the quality flags of each level),
are not decided yet.
:::

## Fluxes

: Flux variables. {#tbl-vars-flux}

| Variable | Unit | Stands for | Page |
|---|---|---|---|
| `NEE` | µmol m^-2^ s^-1^ | Net ecosystem exchange of CO~2~: the CO~2~ flux plus the storage term below the measurement height. Negative values are uptake by the ecosystem. | [L3.1](L3.1.md), [L4.1](L4.1.md) |
| `FC` | µmol m^-2^ s^-1^ | CO~2~ flux measured by eddy covariance, without the storage term. | [L2](L2.md) |
| `SC` | µmol m^-2^ s^-1^ | CO~2~ storage term: the change of the CO~2~ concentration below the measurement height, from a single point. | [L3.1](L3.1.md) |
| `LE` | W m^-2^ | Latent heat flux, the energy carried by the water vapour flux. Turbulent flux without storage term. | [L3.2](L3.2.md), [L4.1](L4.1.md) |
| `ET` | mm (30 min) | Evapotranspiration: `LE` divided by the latent heat of vaporisation, as a water amount per half-hour. | [L4.1](L4.1.md) |
| `H` | W m^-2^ | Sensible heat flux, from the sonic anemometer. Turbulent flux without storage term. | [L3.2](L3.2.md), [L4.1](L4.1.md) |
| `USTAR` | m s^-1^ | Friction velocity, a measure of turbulence. `NEE` is filtered at three thresholds. | [L3.3](L3.3.md) |
| `GPP`, `RECO` | µmol m^-2^ s^-1^ | Gross primary production and ecosystem respiration from partitioning `NEE`. Not part of FP2026.1. | [L4.2](L4.2.md) |

Suffixes of the flux columns:

| Suffix | Meaning |
|---|---|
| `_CUT_16`, `_CUT_50`, `_CUT_84` | `NEE` filtered at the 16th, 50th and 84th percentile USTAR threshold. |
| `_QCF` | Records that passed the quality tests (quality flag 0 or 1). |
| `_QCF0` | Highest-quality records only (quality flag 0), for analyses without gap-filled values. |
| `_gfXG`, `_gfMDS` | Gap-filled with XGBoost (the method of this dataset) or with MDS (for comparison). |
| `_RANDUNC` | Random uncertainty of the gap-filled `NEE`, 1 sigma, µmol m^-2^ s^-1^. |
| `_USTARUNC` | USTAR uncertainty: half the difference between the `CUT_84` and `CUT_16` series. |
| `_JOINTUNC` | Random and USTAR uncertainty combined. |
| `FLAG_..._ISFILLED` | 0 where the value was measured, otherwise how it was filled. |

## Meteorological variables

Measured at the 47 m tower level unless the name says `FF1` (forest floor).

: Meteorological variables. {#tbl-vars-meteo}

| Variable | Unit | Stands for | Page |
|---|---|---|---|
| `SW_IN` | W m^-2^ | Incoming shortwave radiation | [SW_IN](Meteo_Data_SW_IN.md) |
| `SW_OUT` | W m^-2^ | Outgoing (reflected) shortwave radiation | [SW_OUT](Meteo_Data_SW_OUT.md) |
| `LW_IN` | W m^-2^ | Incoming longwave radiation | [LW_IN](Meteo_Data_LW_IN.md) |
| `LW_OUT` | W m^-2^ | Outgoing (emitted) longwave radiation | [LW_OUT](Meteo_Data_LW_OUT.md) |
| `PPFD_IN` | µmol m^-2^ s^-1^ | Incoming photosynthetic photon flux density | [PPFD_IN](Meteo_Data_PPFD_IN.md) |
| `TA` | °C | Air temperature | [TA](Meteo_Data_TA.md) |
| `RH` | % | Relative humidity | [RH](Meteo_Data_RH.md) |
| `VPD` | kPa | Vapour pressure deficit | [VPD](Meteo_Data_VPD.md) |
| `PA` | kPa | Air pressure | [PA](Meteo_Data_PA.md) |
| `PREC` | mm (30 min) | Precipitation | [PREC](Meteo_Data_PREC.md) |
| `SWC` | % | Soil water content (volumetric), forest floor, five depths | [SWC](Meteo_Data_SWC.md) |
| `TS` | °C | Soil temperature, forest floor, seven depths | [TS](Meteo_Data_TS.md) |
| `G` | W m^-2^ | Soil heat flux, forest floor, three plates | [G](Meteo_Data_G.md) |

Suffixes of the meteorological columns:

| Suffix | Meaning |
|---|---|
| `_T1_47_1`, `_FF1_<d>_1` | Location: tower level at 47 m, or forest floor profile at depth `<d>` in metres. |
| `_HOMOGENIZED` | Corrected for sensor changes, so the record is consistent over time. |
| `_gfXG`, `_GAPFILLED` | Gaps filled; the flag says which values are measured. |
| `FLAG_<variable>_<suffix>` | Provenance flag, e.g. `ISFILLED` or `SOURCE`; defined on each variable's page. |
