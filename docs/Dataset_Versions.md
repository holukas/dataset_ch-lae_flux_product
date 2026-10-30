# Dataset Versions

## Current dataset version

### **CH-LAE FP2026.1 (2016-2026.09) [current version]**

First release of this dataset. It holds the ecosystem fluxes measured with the enclosed-path LI-7200
gas analyser (`IRGA72`) and the meteorological data of the site, from January 2016 to September 2026.

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

FP2026.1 was produced with the earlier, stricter test of negative nighttime `NEE` values, based on
the spread of all nighttime values within ±15 days. In the released file it flags 180 values. The
tests used since 30 October 2026 are described under [Level 3.2](L3.2.md) and apply to FP2026.2
only.

See [Variables](Variables.md) for the main variables and the column suffixes, and the
[post-processing chain](FPC.qmd) for the levels behind the flux columns.

**Not yet included:**

- the fluxes of the open-path LI-7500 (`IRGA75`) for 2004-2015, which come with FP2026.2;
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

Extends the flux record back to 2004 with the fluxes of the open-path LI-7500 (`IRGA75`). Its CO~2~
flux is corrected for the errors of the open-path analyser ([Level 1.1](L1.1.md)). The merged
record takes the fluxes from the LI-7500 for 2004-2015 and from the LI-7200 from 1 January 2016;
`FLAG_FLUX_SOURCE` gives the analyser of each half-hour (`75` or `72`). The LI-7500 data of the
parallel period 2016-2017 train and check the correction and are not in the merged record. The
LI-7500 stand-in run of 2019 is not used either. FP2026.2 covers the full period of FP2026.1 and
supersedes it.

FP2026.2 also adds the partitioning of `NEE` into `GPP` and `RECO` ([Level 4.2](L4.2.md)).

The LI-7200 fluxes of FP2026.2 are not identical to those of FP2026.1. The chain now uses tests
of negative nighttime values based on the flux uncertainty ([Level 3.2](L3.2.md)), and the
gap-filling models are trained anew in every run. In the current processing the annual `NEE` sums
of 2016-2025 (`CUT_50`, XGBoost) differ from FP2026.1 by -40 to +3 gC m^-2^.

Both flux chains and the merged record have been run; the release is not final. The correction of
the LI-7500 flux is used as it is for FP2026.2, and improving it for the early years is planned for
a later version. The annual sums of 2004-2009 are kept as processed, without a flag or an added
uncertainty. They are the least certain of the record, and
[Comparisons of the LI-7500 years](IRGA75_Comparisons.md) compares them with FLUXNET and with
published estimates. The `NEE` of the LI-7500 years is also affected by the wet half-hours the
analyser did not measure and by cold, humid nights, and `LE` differs between the two analysers
(see [Issues](Issues.md)).

Also planned: the extension of `PREC`, `SWC`, `TS`, `G`, `SW_OUT` and `LW_OUT` to September 2026.
See the [Issues](https://github.com/holukas/dataset_ch-lae_flux_product/issues) of the
repository for other planned updates.
