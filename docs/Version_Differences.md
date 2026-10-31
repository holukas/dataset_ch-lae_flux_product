# Differences between versions

The main differences between the releases, one row per aspect. The pages of
[FP2026.1](Version_FP2026.1.md) and [FP2026.2](Version_FP2026.2.md) give the details. FP2026.2 is
in progress, so its column describes the current processing.

| | FP2026.1 | FP2026.2 |
|---|---|---|
| Status | Current version, released 27 October 2026 | In progress; supersedes FP2026.1 |
| Period of the fluxes | 11 January 2016 to 30 September 2026 | 30 March 2004 to 30 September 2026 |
| Gas analyser | Enclosed-path LI-7200 (`IRGA72`) | Open-path LI-7500 (`IRGA75`) for 2004-2015, LI-7200 from 1 January 2016; `FLAG_FLUX_SOURCE` gives the analyser of each half-hour |
| Correction of the open-path CO~2~ flux ([L1.1](L1.1.md)) | Not needed | Applied to the LI-7500, fitted without `VPD` |
| Test of negative nighttime `NEE` ([L3.2](L3.2.md)) | One test, against the spread of all nighttime values within ±15 days; 180 values flagged | Two tests against the flux uncertainty: per record, and for the LI-7500 per night |
| Absolute limits of `LE` ([L3.2](L3.2.md)) | −50 to 800 W m-2 | −100 to 1000 W m-2 |
| Periods removed by hand ([L3.2](L3.2.md#instrument-problems-and-periods-removed-by-hand)) | LI-7200 faults of 2016, 2018-2019, 2020 and 2026 | Also the low sample flow of February 2016, May 2021 and August 2023, and the fog and rime periods of the LI-7500 in 2004, 2013 and 2014 |
| USTAR thresholds ([L3.3](L3.3.md)) | Three fixed thresholds (`CUT_16`, `CUT_50`, `CUT_84`) | The same thresholds, also for the LI-7500 years |
| Gap-filling ([L4.1](L4.1.md)) | XGBoost; MDS for comparison | The same; the models are trained anew in every run |
| Partitioning of `NEE` ([L4.2](L4.2.md)) | Not included | `GPP` and `RECO` from the nighttime and the daytime method; the daytime method from 14 September 2005, the first measured shortwave radiation |
| Meteorological data | Thirteen products; `PREC`, `SWC`, `TS`, `G`, `SW_OUT` and `LW_OUT` end on 31 December 2025 | The same; their extension to September 2026 is planned |

: Main differences between FP2026.1 and FP2026.2. {#tbl-version-differences}

## Effect on the LI-7200 fluxes

FP2026.2 contains the LI-7200 years of FP2026.1, processed again with the changes above. In the
current processing the annual `NEE` sums of 2016-2025 (`CUT_50`, XGBoost) differ from FP2026.1 by
−25 to +3 gC m^-2^, except 2021 (−111 gC m^-2^); annual `ET` differs by −7 to +9 mm, and by
+40 mm in 2021. The periods of low sample flow change `NEE`, `LE` and `ET` in the years concerned: in FP2026.1 their near-zero fluxes are kept as
measured values and enter the training of the gap-filling models; in FP2026.2 they are removed and
gap-filled.

## Moving from FP2026.1 to FP2026.2

- Use `FLAG_FLUX_SOURCE` to tell the two gas analysers apart; the step at 1 January 2016 is partly
  instrumental (see [Issues](Issues.md)).
- Recompute results that used annual sums of 2016 to 2026; do not combine sums from the two
  versions.
- The `GPP` and `RECO` columns are new.
