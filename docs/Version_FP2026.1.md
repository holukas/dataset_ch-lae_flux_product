# FP2026.1 (2016-2026.09)

**Current version.** First release of this dataset. It holds the ecosystem fluxes measured with the
enclosed-path LI-7200 gas analyser (`IRGA72`) and the meteorological data of the site, from
January 2016 to September 2026. What changes with the next release is listed under
[Differences between versions](Version_Differences.md).

| | |
|---|---|
| release date | 27 October 2026 |
| availability | on request from the [Grassland Sciences group, ETH Zurich](https://gl.ethz.ch/) |
| dataset | `CH-LAE_FP2026.1_2016-2026.09`, as parquet and as CSV, with an `_INFO.md` file that gives the unit and a short description of every variable |
| period | 1 January 2016 00:15 to 30 September 2026 23:45 |
| time step | 30 minutes; the timestamp `TIMESTAMP_MIDDLE` marks the middle of each half-hour, in UTC+01:00 all year |
| size | 188,448 half-hours, 548 variables |

: FP2026.1 at a glance. {#tbl-fp2026-1}

## What it contains

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
[post-processing chain](FPC.qmd) for the levels behind the flux columns. The column names of the
dataset are those of the processing; a shorter set of names for publication is not defined yet.

## Not included

- the fluxes of the open-path LI-7500 (`IRGA75`) for 2004-2015, which come with FP2026.2;
- `PREC`, `SWC`, `TS`, `G`, `SW_OUT` and `LW_OUT` for January to September 2026;
- the partitioning of `NEE` into `GPP` and `RECO` ([Level 4.2](L4.2.md));
- a correction for the energy balance closure.

## Known problems of this release

- **Periods of low sample flow are still in the data.** In these periods the measuring cell of the
  LI-7200 was not flushed, and `FC` and `LE` stayed near zero; the values passed the automatic
  tests. They were found after the release and are removed by hand from FP2026.2. In FP2026.1,
  exclude `NEE`, `LE` and `ET` of these periods, gap-filled values included:
  - six periods from 30 January to 29 February 2016, and the night to 26 May 2016 07:45
    ([Yearly Notes, 2016](Yearly_Notes.md#start-up-of-the-li-7200-in-2016));
  - 28 April to 20 May and 21 to 27 May 2021
    ([Yearly Notes, 2021](Yearly_Notes.md#low-sample-flow-of-the-li-7200-in-may-2021));
  - 11 to 14 August 2023
    ([Yearly Notes, 2023](Yearly_Notes.md#zero-sample-flow-of-the-li-7200-in-august-2023)).
- **Settings of two outlier tests.** FP2026.1 was produced with the earlier, stricter test of
  negative nighttime `NEE` values, based on the spread of all nighttime values within ±15 days; in
  the released file it flags 180 values. Its absolute limits for `LE` were −50 to 800 W m-2. The
  tests used since 30 October 2026 are described under [Level 3.2](L3.2.md) and apply to FP2026.2.

The other known issues, which apply to both versions, are listed on [Issues](Issues.md).
