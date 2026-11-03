# FP2026.2 (2004-2026.09)

**In progress.** FP2026.2 extends the flux record back to 2004 with the fluxes of the open-path
LI-7500 (`IRGA75`). It contains the full period of FP2026.1 and supersedes it. What changes against
FP2026.1 is listed under [Differences between versions](Version_Differences.md).

## What it adds

- **Fluxes of 2004-2015 from the LI-7500.** Its CO~2~ flux is corrected for the errors of the
  open-path analyser ([Level 1.1](L1.1.md)). The merged record takes the fluxes from the LI-7500
  for 2004-2015 and from the LI-7200 from 1 January 2016; `FLAG_FLUX_SOURCE` gives the analyser of
  each half-hour (`75` or `72`). It leaves out two sets of LI-7500 data: those of the parallel
  period 2016-2017, which train and check the correction, and the stand-in run of 2019.
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
- The USTAR thresholds are higher. They are detected with the ONEFlux moving point method, one set
  per analyser ([Level 3.3](L3.3.md)), remove more nights of low turbulence and raise the
  night-time respiration.

With these changes, the annual `NEE` sums of 2016-2025 (`CUT_50`, XGBoost) are 3 to
206 gC m^-2^ higher than in FP2026.1, except in 2021 (−69 gC m^-2^). The main cause is the higher
USTAR threshold: fewer nights stay measured, and the night-time respiration is higher. In 2021 the
removal of the low sample flow of May 2021 lowers the sum, and the higher threshold raises it. At
`CUT_50`, 2016, 2017 and 2022 to 2024 are now net sources of CO~2~. Annual `ET` differs by −10 to
+10 mm, and by +38 mm in 2021. Part of the spread comes from the gap-filling models, which are
trained anew in every run.

## State of the release

Both flux chains and the merged record have been run with the USTAR thresholds of FP2026.2 and the
31-day Hampel filter. The release is not final. The correction of the LI-7500 flux is used as it is
for FP2026.2; improving it for the early years is planned for a later version. The annual sums of
2004-2009 are kept as processed, without a flag or an added uncertainty. They are the least certain
of the record. [Comparisons of the LI-7500 years](IRGA75_Comparisons.md) compares them with FLUXNET
and with published estimates.

Known limitations of the LI-7500 years, described on [Issues](Issues.md):

- **Storage term.** Wet or blocked windows make the LI-7500 read too high a CO~2~ concentration,
  and its storage term does not sum to about zero over a year
  ([Issues](Issues.md#the-storage-term-of-the-li-7500-drifts)). A screen of the concentration
  readings is set for the next run and is not yet applied in the data ([Level 3.1](L3.1.md)).
- **Night-time and daytime `NEE`.** Against the values expected from the LI-7200 years, night-time
  `NEE` of all LI-7500 years is too low, and daytime `NEE` of 2004-2009 too high. Both biases are
  stated as uncertainties and are not corrected
  ([Issues](Issues.md#biases-of-the-li-7500-nee-against-a-climate-baseline)).
- **Cold nights.** On overcast, foggy and calm cold nights the LI-7500 reads too little
  respiration, about 53 gC m^-2^ per year in 2004-2015, part of the night bias above
  ([Issues](Issues.md#nighttime-nee-of-the-li-7500-is-too-low-on-cold-and-humid-nights)).
- **Calibration of 2004-2010.** CO~2~ read too low in 2004-2007 and H~2~O too high from May 2008
  to December 2010; not corrected
  ([Issues](Issues.md#calibration-of-the-li-7500-in-2004-2010)).
- **`LE`** differs between the two analysers
  ([Issues](Issues.md#le-of-the-two-gas-analysers-differs-in-humid-and-cold-conditions)).

## Prepared for the next run

Two changes are prepared but not applied in the current data:

- **Screen of the LI-7500 CO~2~ concentration for the storage term.** diive `run_level31` takes the
  options `concentration_valid` and `restart_screening={'skip_after_gaps': 3}`. A reading enters
  the storage term only:
  - at an AGC of 55 or less;
  - without rain in the previous 3 hours;
  - at a relative humidity below 99.5 %;
  - not among the first 3 records after a gap.

  The settings are in
  [`05_FPPC_IRGA75_NEE_OPCO`](notebooks/30_FLUX_POST-PROCESSING_CHAIN/IRGA75/05_FPPC_IRGA75_NEE_OPCO_2004-2017.html),
  Step 3; the chain has not been run with them yet ([Level 3.1](L3.1.md)).
- **USTAR thresholds detected on the complete years of each analyser.** `CUT_16`, `CUT_50` and
  `CUT_84` are 0.317, 0.429 and 0.549 m s^-1^ for the LI-7500 (2004-2017) and 0.416, 0.526 and
  0.647 m s^-1^ for the LI-7200 (2016-2025), one set per analyser as in the current data. One set
  for both analysers, from one record of the site, is not adopted: the two records differ in which
  nights they keep, not in the turbulence they measure
  ([Threshold constraints](L3.3_Constraints.md)).

Also planned: the extension of `PREC`, `SWC`, `TS`, `G`, `SW_OUT` and `LW_OUT` to September 2026.
