# FP2026.2 (2004-2026.09)

**In progress.** FP2026.2 extends the flux record back to 2004 with the fluxes of the open-path
LI-7500 (`IRGA75`). It contains the full period of FP2026.1 and supersedes it. What changes against
FP2026.1 is listed under [Differences between versions](Version_Differences.md).

## What it adds

- **Fluxes of 2004-2015 from the LI-7500.** Its CO~2~ flux is corrected for the errors of the
  open-path analyser ([Level 1.1](L1.1.md)). The merged record takes the fluxes from the LI-7500
  for 2004-2015 and from the LI-7200 from 1 January 2016; `FLAG_FLUX_SOURCE` gives the analyser of
  each half-hour (`75` or `72`). The LI-7500 data of the parallel period 2016-2017 train and check
  the correction and are not in the merged record. The LI-7500 stand-in run of 2019 is not used
  either.
- **Partitioning of `NEE`** into `GPP` and `RECO` ([Level 4.2](L4.2.md)).

## Changes to the LI-7200 fluxes

The LI-7200 fluxes of FP2026.2 are not identical to those of FP2026.1:

- The chain uses tests of negative nighttime values based on the flux uncertainty
  ([Level 3.2](L3.2.md)).
- Periods of low sample flow of the LI-7200 found after the release of FP2026.1 are removed by
  hand: February 2016, May 2021 and August 2023
  ([Level 3.2](L3.2.md#instrument-problems-and-periods-removed-by-hand)).
- The gap-filling models are trained anew in every run.

In the current processing the annual `NEE` sums of 2016-2025 (`CUT_50`, XGBoost) differ from
FP2026.1 by −25 to +3 gC m^-2^, except 2021: −111 gC m^-2^, from the removal of the low sample flow
of May 2021. Annual `ET` differs by −7 to +9 mm, and by +40 mm in 2021.

## State of the release

Both flux chains and the merged record have been run; the release is not final. The correction of
the LI-7500 flux is used as it is for FP2026.2, and improving it for the early years is planned for
a later version. The annual sums of 2004-2009 are kept as processed, without a flag or an added
uncertainty. They are the least certain of the record, and
[Comparisons of the LI-7500 years](IRGA75_Comparisons.md) compares them with FLUXNET and with
published estimates. The `NEE` of the LI-7500 years is also affected by the wet half-hours the
analyser did not measure and by cold, humid nights, and `LE` differs between the two analysers
(see [Issues](Issues.md)).

Also planned: the extension of `PREC`, `SWC`, `TS`, `G`, `SW_OUT` and `LW_OUT` to September 2026.
