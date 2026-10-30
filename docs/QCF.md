# QCF: overall quality control flag

The overall quality flag `QCF` combines the test flags of the post-processing chain into one flag
per record. It is calculated after each level, and each level includes the tests of the levels
before it, so the flag after Level 3.3 accounts for all tests.

Notebook: [`05_FPPC_IRGA72_NEE`](notebooks/30_FLUX_POST-PROCESSING_CHAIN/IRGA72/05_FPPC_IRGA72_NEE_2016-2026.09.html),
the tables "result of each Level-2 test" and "result of each Level-3.2 test" and Step 5.

## Flag values

| `QCF` | Meaning | Rule |
|---|---|---|
| 0 | Best quality | No test raised a flag |
| 1 | Good quality | One to three soft flags, no hard flag |
| 2 | Rejected | At least one hard flag, or more than three soft flags |

: Values of the overall quality flag. {#tbl-qcf-values}

Each test flags a record 0 (passed), 1 (soft flag, a warning) or 2 (hard flag, rejected). Most
tests set only hard flags. Soft flags come from the SSITC test (flag 1 as reported by EddyPro) and
from the spectral correction factor test (`SCF` from 2 to below 4). A missing flux is rejected by
the missing-value test, so it always has `QCF` 2.

The same rule applies by day and by night: records with `QCF` 0 and 1 are kept. FP2026.2 uses this
rule for both gas analysers. For the open-path LI-7500 (`IRGA75`) the notebook is
[`05_FPPC_IRGA75_NEE_OPCO`](notebooks/30_FLUX_POST-PROCESSING_CHAIN/IRGA75/05_FPPC_IRGA75_NEE_OPCO_2004-2017.html).

## Columns

For a flux `<flux>` after level `<level>`, for example `NEE_L3.1` after Level 3.3 in the scenario
`CUT_50`:

| Column | Content |
|---|---|
| `FLAG_L3.3_CUT_50_NEE_L3.1_QCF` | The overall flag: 0, 1 or 2 |
| `NEE_L3.1_L3.3_CUT_50_QCF` | The flux where `QCF` is 0 or 1 |
| `NEE_L3.1_L3.3_CUT_50_QCF0` | The flux where `QCF` is 0 |
| `SUM_L3.3_CUT_50_NEE_L3.1_SOFTFLAGS` | Sum of the soft flags, equal to their number |
| `SUM_L3.3_CUT_50_NEE_L3.1_HARDFLAGS` | Sum of the hard flags, twice their number |
| `SUM_L3.3_CUT_50_NEE_L3.1_FLAGS` | Sum of both |

: Columns of the overall quality flag, for `NEE` after Level 3.3 (`CUT_50`). {#tbl-qcf-columns}

The same columns exist after each level: `FLAG_L2_FC_QCF`, `FLAG_L3.1_NEE_QCF`,
`FLAG_L3.2_NEE_L3.1_QCF` and `FLAG_L3.3_<CUT>_NEE_L3.1_QCF` for `NEE`, and the same pattern for
`LE` and `H`, whose Level-3.3 columns carry `CUT_NONE`.

## Which columns to use

- **Gap-filled series:** `NEE_L3.1_L3.3_CUT_50_QCF_gfXG` and its scenarios, `LE_L3.1_L3.3_CUT_NONE_QCF_gfXG`,
  `H_L3.1_L3.3_CUT_NONE_QCF_gfXG` (see [Level 4.1](L4.1.md)). They are built from the records with
  `QCF` 0 and 1.
- **Measured values only:** the `_QCF` columns (`QCF` 0 and 1), or the `_QCF0` columns for the
  highest quality.

## Records per flag

| Flag column | `QCF` 0 | `QCF` 1 | `QCF` 2 |
|---|---|---|---|
| `FLAG_L2_FC_QCF` | 59,004 | 75,311 | 54,133 |
| `FLAG_L3.2_NEE_L3.1_QCF` | 56,975 | 67,024 | 64,449 |
| `FLAG_L3.3_CUT_16_NEE_L3.1_QCF` | 49,091 | 43,404 | 95,953 |
| `FLAG_L3.3_CUT_50_NEE_L3.1_QCF` | 46,828 | 39,996 | 101,624 |
| `FLAG_L3.3_CUT_84_NEE_L3.1_QCF` | 44,050 | 36,259 | 108,139 |
| `FLAG_L3.3_CUT_NONE_LE_L3.1_QCF` | 49,062 | 70,433 | 68,953 |
| `FLAG_L3.3_CUT_NONE_H_L3.1_QCF` | 84,975 | 56,071 | 47,402 |

: Records per value of the overall quality flag of the LI-7200 (`IRGA72`), out of the 188,448
half-hours of January 2016 to September 2026, in the current chain. `QCF` 2 includes the records
without a measured flux. In FP2026.1, produced with earlier settings of two Level-3.2 tests (see
[Level 3.2](L3.2.md)), `QCF` 2 has 140 more records of `NEE` after Level 3.2 and 418 more of
`LE`. {#tbl-qcf-records}
