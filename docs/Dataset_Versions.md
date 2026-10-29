# Dataset Versions

## Current dataset version

### **CH-LAE FP2026.1 (2016-2026.09) [current version]**

First release of this dataset. It holds the ecosystem fluxes measured with the enclosed-path LI-7200 gas
analyser (`IRGA72`) and the meteorological data of the site, from January 2016 to September 2026.

| | |
|---|---|
| release date | 27 October 2026 |
| availability | on request from the [Grassland Sciences group, ETH Zurich](https://gl.ethz.ch/) |
| dataset | `CH-LAE_FP2026.1_2016-2026.09`, as parquet and as CSV, with an `_INFO.md` file that gives the unit and a short description of every variable |
| period | 1 January 2016 00:15 to 30 September 2026 23:45 |
| time step | 30 minutes; the timestamp `TIMESTAMP_MIDDLE` marks the middle of each half-hour, in UTC+01:00 all year |
| size | 188,448 half-hours, 548 variables |

**What it contains:**

- **CO~2~ flux (`NEE`)**, quality-controlled, filtered at three fixed USTAR thresholds
  (`CUT_16`, `CUT_50`, `CUT_84`) and gap-filled. `NEE` includes the CO~2~ storage term below
  the measurement height. Its random, USTAR and joint uncertainty follow Pastorello et al. (2020).
- **Latent heat flux (`LE`)** and **evapotranspiration (`ET`)**, quality-controlled and
  gap-filled, without USTAR filter and without storage term.
- **Sensible heat flux (`H`)** from the sonic anemometer, quality-controlled and gap-filled,
  without USTAR filter and without storage term.
- **Gap-filling:** XGBoost is the method of this dataset. MDS is included for comparison.
- **Level-1 fluxes:** the full EddyPro output, with the fluxes at each correction stage, the
  quality tests and the raw-data statistics.
- **Meteorological data:** all thirteen meteorological products with their provenance flags.
  `SW_IN`, `TA`, `PPFD_IN`, `RH`, `PA`, `LW_IN` and `VPD` run to September 2026. `PREC`,
  `SWC`, `TS`, `G`, `SW_OUT` and `LW_OUT` end on 31 December 2025 and are empty in 2026.

See [Variables](Variables.md) for the main variables and the column suffixes, and the
[post-processing chain](FPC.qmd) for the levels behind the flux columns.

**Not yet included:**

- the fluxes of the open-path LI-7500 (`IRGA75`, 2004 to 2017 and 2019), which come with
  FP2026.2;
- `PREC`, `SWC`, `TS`, `G`, `SW_OUT` and `LW_OUT` for January to September 2026;
- the partitioning of `NEE` into `GPP` and `RECO` ([Level 4.2](L4.2.md));
- a correction for the energy balance closure.

The column names of the dataset are those of the processing. A shorter set of names for
publication is not defined yet.

## Previous dataset versions

FP2026.1 is the first release of the dataset documented on this site. Earlier CH-LAE datasets,
published separately:

- [CH-LAE FP2022 (2004-2022)](https://doi.org/10.3929/ethz-b-000582198), ETH Zurich Research
  Collection
- [CH-LAE FP2021 (2004-2020)](https://www.swissfluxnet.ethz.ch/index.php/documentation/ch-lae-fp2021-2004-2020/)

## Upcoming updates

### **CH-LAE FP2026.2 (2004-2026.09) [in progress]**

Extends the flux record back to 2004 with the fluxes of the open-path LI-7500 (`IRGA75`),
with the CO2 flux corrected for the errors of the open-path analyser ([Level 1.1](L1.1.md)). Their annual `NEE` carries an extra uncertainty from the half-hours the analyser did not measure (see [Issues](Issues.md)). It re-includes FP2026.1
in full and supersedes it.

Also planned: the extension of `PREC`, `SWC`, `TS`, `G`, `SW_OUT` and `LW_OUT` to September 2026.
See the [Issues](https://github.com/holukas/dataset_ch-lae_flux_product/issues) of the
repository for other planned updates.
