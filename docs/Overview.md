# Overview

The CH-LAE flux product holds the half-hourly ecosystem fluxes and meteorological data of the
mixed forest site CH-LAE ([Site information](Site_Info.md)). The current version is
**FP2026.1**, released on 27 October 2026 and available on request from the
[Grassland Sciences group, ETH Zurich](https://gl.ethz.ch/). Release details are in
[Dataset Versions](Dataset_Versions.md).

## What FP2026.1 contains

| | |
|---|---|
| period | 1 January 2016 00:15 to 30 September 2026 23:45 |
| time step | 30 minutes |
| timestamp | `TIMESTAMP_MIDDLE`, the middle of each half-hour, in UTC+01:00 all year (no daylight saving) |
| size | 188,448 half-hours, 548 variables |
| files | `CH-LAE_FP2026.1_2016-2026.09` as parquet and CSV, and an `_INFO.md` file with the unit and description of every variable |

: FP2026.1 at a glance. {#tbl-overview-release}

- **Fluxes** from the enclosed-path LI-7200 gas analyser (`IRGA72`), measured from 11 January
  2016: `NEE`, `LE`, `ET` and `H`, quality-controlled and gap-filled, with the random, USTAR and
  joint uncertainty of `NEE`. The full Level-1 output of EddyPro is also included.
- **Meteorological data**: thirteen products, from radiation and air temperature at 47 m to soil
  water content and soil temperature at the forest floor. See [Meteo Data](Meteo_Data.md).

Column names and units are on [Variables](Variables.md). Use the columns gap-filled with XGBoost
(`_gfXG`). The MDS columns (`_gfMDS`) are for comparison only, because MDS fills long gaps poorly.
In April and May 2016, after the start-up period of the analyser was removed, MDS gives an `NEE`
of -235 gC m^-2^, against -113 gC m^-2^ with XGBoost.

## How the fluxes were produced

1. [Raw data](Raw_Data.md): the 20 Hz eddy covariance raw data, converted from binary to ASCII.
2. [Level 0](L0.md): preliminary flux runs, used to check the setup and to choose the time-lag
   ranges.
3. [Level 1](L1.md): final flux calculation with EddyPro, one run per setup period.
   [Level 1.1](L1.1.md), the correction of the open-path CO~2~ flux, applies only to the LI-7500
   fluxes of FP2026.2.
4. The [post-processing chain](FPC.qmd):
   [Level 2](L2.md) quality flags,
   [Level 3.1](L3.1.md) storage term (`NEE` only),
   [Level 3.2](L3.2.md) outlier removal,
   [Level 3.3](L3.3.md) USTAR filtering (`NEE` only, three fixed thresholds) and
   [Level 4.1](L4.1.md) gap-filling.
   [Level 4.2](L4.2.md), the partitioning of `NEE`, is not part of FP2026.1.

FP2026.1 was produced with the earlier, stricter test of negative nighttime `NEE` values. The tests
used since 30 October 2026 ([Level 3.2](L3.2.md)) apply to FP2026.2.

The dataset file is cut from a collection of all fluxes and meteorological data from 2004:
[`10_FLUXES_and_METEO_2004-2026.09`](notebooks/80_FINALIZE/10_FLUXES_and_METEO_2004-2026.09.html)
and [`20_CH-LAE_FP2026.1_2016-2026.09`](notebooks/80_FINALIZE/20_CH-LAE_FP2026.1_2016-2026.09.html).

## Not yet included

- The fluxes of the open-path LI-7500 (`IRGA75`) for 2004-2015. They are in progress for
  FP2026.2, which will extend the flux record back to 2004 and supersede FP2026.1.
  - The merged record of FP2026.2 takes the LI-7500 until 2015 and the LI-7200 from 1 January
    2016.
  - The LI-7500 data of the parallel period 2016-2017 are used to train and check the correction
    of [Level 1.1](L1.1.md). They are not in the merged record.
  - [Comparisons of the LI-7500 years](IRGA75_Comparisons.md) compares the LI-7500 years with
    earlier estimates.
- `PREC`, `SWC`, `TS`, `G`, `SW_OUT` and `LW_OUT` for January to September 2026. These columns
  end on 31 December 2025.
- The partitioning of `NEE` into `GPP` and `RECO`, which is run for FP2026.2.
- A correction of `LE` and `H` for the energy balance closure.

## Known limitations

- `H` is missing from 10 January to 20 March 2019. The gap-filled `H` in that period is model
  output only.
- `H` in 2024 is about a third lower than in the other years. The cause is the weather of 2024,
  with less radiation, more rain and a lower `VPD`. No instrument fault was found.
- `LE` and `ET` of the LI-7200 may be too low in humid and cold conditions.

All known issues, including those of the LI-7500 years of FP2026.2, are on [Issues](Issues.md).
For the LI-7500 years:

- The storage term drifts, because wet or blocked windows make the analyser read too high a CO~2~
  concentration. A screen of these readings is set for the next run and is not yet applied.
- The nighttime `NEE` of the LI-7500 years lies about 200 gC m^-2^ per year below the values
  expected from the LI-7200 years. The daytime `NEE` of 2004-2009 lies about 230 gC m^-2^ per year
  above them. Both biases are stated as uncertainties and are not corrected.
