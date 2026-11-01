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
- A third Hampel filter, over 31 days, removes extreme values of `NEE`, `LE` and `H` that the
  13-day filter does not test or does not single out ([Level 3.2](L3.2.md)).
- Periods of low sample flow of the LI-7200 found after the release of FP2026.1 are removed by
  hand: February 2016, May 2018, May 2021 and August 2023
  ([Level 3.2](L3.2.md#instrument-problems-and-periods-removed-by-hand)).
- The gap-filling models are trained anew in every run.
- Higher USTAR thresholds, detected with the ONEFlux moving point method, one set per analyser
  ([Level 3.3](L3.3.md)). They remove more nights of low turbulence and raise the night-time
  respiration.

With these changes, the annual `NEE` sums of 2016-2025 (`CUT_50`, XGBoost) are 3 to
206 gC m^-2^ higher than in FP2026.1, except 2021: −69 gC m^-2^. The main cause is the higher USTAR
threshold: fewer nights stay measured, and the night-time respiration is higher. In 2021 the removal
of the low sample flow of May 2021 lowers the sum, and the higher threshold raises it. At `CUT_50`,
2016, 2017 and 2022 to 2024 are now net sources of CO~2~. Annual `ET` differs by −10 to +10 mm,
and by +38 mm in 2021. Part of the spread comes from the gap-filling models, which are trained anew
in every run.

## State of the release

Both flux chains and the merged record have been run with the USTAR thresholds of FP2026.2 and the
31-day Hampel filter. The release is not final. The correction of
the LI-7500 flux is used as it is for FP2026.2, and improving it for the early years is planned for
a later version. The annual sums of 2004-2009 are kept as processed, without a flag or an added
uncertainty. They are the least certain of the record, and
[Comparisons of the LI-7500 years](IRGA75_Comparisons.md) compares them with FLUXNET and with
published estimates. The `NEE` of the LI-7500 years is also affected by the wet half-hours the
analyser did not measure and by cold, humid nights, and `LE` differs between the two analysers
(see [Issues](Issues.md)).

Also planned: the extension of `PREC`, `SWC`, `TS`, `G`, `SW_OUT` and `LW_OUT` to September 2026.
