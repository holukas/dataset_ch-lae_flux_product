# Variables

The main variables of FP2026.1: column name, unit and meaning. All are half-hourly. The index
`TIMESTAMP_MIDDLE` marks the middle of each half-hour, in UTC+01:00 all year (no daylight
saving). The `_INFO.md` file that comes with the dataset lists all 548 columns with unit and
description; this page covers the columns most users need.

## Fluxes

The fluxes come from the enclosed-path LI-7200 (`IRGA72`). In FP2026.2, in progress, the same
columns hold the fluxes of the open-path LI-7500 (`IRGA75`) for 2004-2015, and `FLAG_FLUX_SOURCE`
gives the analyser of each half-hour (`75` or `72`). FP2026.2 also adds the `GPP` and `RECO` of the
partitioning ([Level 4.2](L4.2.md)). The column names follow the
processing levels of the [post-processing chain](FPC.qmd). For example,
`NEE_L3.1_L3.3_CUT_50_QCF_gfXG` is `NEE` after [Level 3.1](L3.1.md) (storage term) and
[Level 3.3](L3.3.md) (USTAR filter, scenario `CUT_50`), from records with quality flag 0 or 1
(`QCF`), gap-filled with XGBoost (`gfXG`).

: Gap-filled fluxes, the columns for most analyses. {#tbl-vars-flux}

| Column | Unit | Meaning | Page |
|---|---|---|---|
| `NEE_L3.1_L3.3_CUT_<nn>_QCF_gfXG` | µmol m^-2^ s^-1^ | Net ecosystem exchange of CO~2~: `FC` plus the storage term. Negative values are uptake by the ecosystem. One column per USTAR scenario, `<nn>` = `16`, `50`, `84`. | [L4.1](L4.1.md) |
| `NEE_L3.1_L3.3_CUT_50_QCF_gfXG_RANDUNC` | µmol m^-2^ s^-1^ | Random uncertainty of `NEE`, 1 sigma (Pastorello et al. 2020). | [L4.1](L4.1.md) |
| `NEE_L3.1_L3.3_CUT_50_QCF_gfXG_USTARUNC` | µmol m^-2^ s^-1^ | USTAR uncertainty: half the difference between the `CUT_84` and `CUT_16` series. | [L4.1](L4.1.md) |
| `NEE_L3.1_L3.3_CUT_50_QCF_gfXG_JOINTUNC` | µmol m^-2^ s^-1^ | Random and USTAR uncertainty combined. | [L4.1](L4.1.md) |
| `LE_L3.1_L3.3_CUT_NONE_QCF_gfXG` | W m^-2^ | Latent heat flux. No storage term, no USTAR filter. | [L4.1](L4.1.md) |
| `ET_L3.1_L3.3_CUT_NONE_QCF_gfXG` | mm (30 min)^-1^ | Evapotranspiration, computed from the gap-filled `LE`. | [L4.1](L4.1.md) |
| `H_L3.1_L3.3_CUT_NONE_QCF_gfXG` | W m^-2^ | Sensible heat flux from the sonic anemometer. No storage term, no USTAR filter. | [L4.1](L4.1.md) |
| `FLAG_<column>_ISFILLED` | - | 0 where the value was measured, otherwise filled. | [L4.1](L4.1.md) |

Each gap-filled column also exists with `_gfMDS` instead of `_gfXG`, filled with MDS. These are
for comparison only; use the XGBoost columns. The three USTAR thresholds are 0.272, 0.304 and
0.340 m s^-1^ ([Level 3.3](L3.3.md)).

: Measured fluxes and auxiliary columns. {#tbl-vars-flux-aux}

| Column | Unit | Meaning | Page |
|---|---|---|---|
| `NEE_L3.1_L3.3_CUT_<nn>_QCF` | µmol m^-2^ s^-1^ | Measured `NEE` after all quality tests and the USTAR filter, not gap-filled. `_QCF0` instead of `_QCF` keeps the records with quality flag 0 only. | [L3.3](L3.3.md) |
| `LE_L3.1_L3.3_CUT_NONE_QCF`, `H_L3.1_L3.3_CUT_NONE_QCF` | W m^-2^ | Measured `LE` and `H` after all quality tests, not gap-filled (also with `_QCF0`). | [L3.2](L3.2.md) |
| `FC` | µmol m^-2^ s^-1^ | CO~2~ flux from EddyPro (Level 1), without storage term and without quality filtering. | [L1](L1.md) |
| `SC_SINGLE_gfRMED_L3.1` | µmol m^-2^ s^-1^ | CO~2~ storage term from the concentration at the measurement height, gap-filled with a rolling median, as added to `FC` to give `NEE`. | [L3.1](L3.1.md) |
| `LE`, `H` | W m^-2^ | Latent and sensible heat flux from EddyPro (Level 1), without quality filtering. | [L1](L1.md) |
| `USTAR` | m s^-1^ | Friction velocity. | [L3.3](L3.3.md) |
| `FLAG_L2_<flux>_QCF`, `FLAG_L3.1_<flux>_QCF`, ... | - | Overall quality flag after each level: 0 best, 1 good, 2 rejected. | [L2](L2.md) |
| `SW_IN_POT`, `DAYTIME`, `NIGHTTIME` | W m^-2^, -, - | Potential incoming shortwave radiation for the middle of the half-hour, and the day and night flags derived from it (1 where the condition holds). | - |

The other Level-1 columns are the EddyPro output: the fluxes after each correction stage, the
quality tests, wind and turbulence statistics, footprint distances and raw-data statistics.

::: {.callout-note title="Two units for ET"}

The gap-filled `ET_..._gfXG` and `ET_..._gfMDS` are in mm per half-hour. The Level-1 column `ET`
from EddyPro is in mm h^-1^.

:::

## Meteorological variables

Measured at the tower at 47 m (`T1_47_1`) or in the soil profile at the forest floor
(`FF1_<depth>`, depth in metres). Each variable has its own page with its columns, flags,
coverage and known limitations. The provenance flags (`FLAG_<column>_ISFILLED`, `_SOURCE` and
others) are defined there.

: Meteorological variables. {#tbl-vars-meteo}

| Variable | Columns | Unit | Page |
|---|---|---|---|
| Incoming shortwave radiation | `SW_IN_T1_47_1_gfXG` | W m^-2^ | [SW_IN](Meteo_Data_SW_IN.md) |
| Air temperature | `TA_T1_47_1_gfXG`, `TA_T1_47_1_HOMOGENIZED_gfXG` | °C | [TA](Meteo_Data_TA.md) |
| Photosynthetic photon flux density | `PPFD_IN_T1_47_1_gfXG` | µmol m^-2^ s^-1^ | [PPFD_IN](Meteo_Data_PPFD_IN.md) |
| Relative humidity | `RH_T1_47_1`, `RH_T1_47_1_HOMOGENIZED` | % | [RH](Meteo_Data_RH.md) |
| Air pressure | `PA_T1_47_1` | kPa | [PA](Meteo_Data_PA.md) |
| Incoming longwave radiation | `LW_IN_T1_47_1` | W m^-2^ | [LW_IN](Meteo_Data_LW_IN.md) |
| Vapour pressure deficit | `VPD_T1_47_1`, `VPD_T1_47_1_HOMOGENIZED` | kPa | [VPD](Meteo_Data_VPD.md) |
| Precipitation | `PREC_TOT_T1_47_1`, `PREC_TOT_T1_47_1_HOMOGENIZED` | mm (30 min)^-1^ | [PREC](Meteo_Data_PREC.md) |
| Soil water content (volumetric), five depths | `SWC_FF1_<depth>_1`, and `SWC_FF1_<depth>_1_HOMOGENIZED` except at 0.5 m | % | [SWC](Meteo_Data_SWC.md) |
| Soil temperature, seven depths | `TS_FF1_<depth>_HOMOGENIZED_GAPFILLED` | °C | [TS](Meteo_Data_TS.md) |
| Soil heat flux, positive into the soil | `G_FF1_0.05_HOMOGENIZED` | W m^-2^ | [G](Meteo_Data_G.md) |
| Outgoing (reflected) shortwave radiation | `SW_OUT_T1_47_1` | W m^-2^ | [SW_OUT](Meteo_Data_SW_OUT.md) |
| Outgoing (emitted) longwave radiation | `LW_OUT_T1_47_1` | W m^-2^ | [LW_OUT](Meteo_Data_LW_OUT.md) |

Column suffixes: `_HOMOGENIZED` is corrected for sensor changes, so the record is consistent over
time; `_gfXG` and `_GAPFILLED` are gap-filled. `PREC`, `SWC`, `TS`, `G`, `SW_OUT` and `LW_OUT`
end on 31 December 2025 and are empty in 2026.
