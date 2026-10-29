# Software

The software used to produce FP2026.1 and FP2026.2 (in progress), by processing step. Versions are given where the
notebooks or the project's lock file record them.

| Step | Software | Version | Use |
|---|---|---|---|
| Raw data | [bico](https://github.com/holukas/bico) | to be checked | Conversion of the raw binary eddy covariance files to ASCII. The wrong-calibration-gas factor (0.974 on the CO~2~ concentration, 14 December 2017 to 15 March 2019) is applied in this step. |
| Level 0 and Level 1 | [EddyPro](https://www.licor.com/env/products/eddy_covariance/eddypro) (LI-COR), run with [fluxrun](https://github.com/holukas/fluxrun) | to be checked | Flux calculation, one run per setup period. Level 0 is a preliminary run; Level 1 is the final run whose FLUXNET output enters the dataset. |
| Level 1.1 (FP2026.2 only) | [opco](https://github.com/holukas/opco) | v0.1.0 | Correction of the CO~2~ flux of the open-path LI-7500, trained on the 2016-2017 overlap with the LI-7200. |
| Merging, post-processing, meteo products, finalize | [diive](https://github.com/holukas/diive) ([documentation](https://diive.readthedocs.io/)) | v0.93.0 | Merging of the Level-1 runs, quality flags, storage term, outlier removal, USTAR filtering, gap-filling (XGBoost and MDS), uncertainty, the meteorological products and the final dataset. |
| USTAR threshold detection | [REddyProc](https://cran.r-project.org/web/packages/REddyProc/index.html) (R) | to be checked | Detection of the USTAR thresholds with `sEstimateUstarScenarios`, on the `NEE` of the LI-7200 (2016-2024) and of the LI-7500 (2005-2019); see [Level 3.3](L3.3.md) for how the three constant thresholds were chosen from both. The input was prepared with diive v0.90.0. |

: Software by processing step {#tbl-software}

The version of diive is the one printed by every notebook of the flux chains of both analysers
(`20_L1_FLUXES`, `30_FLUX_POST-PROCESSING_CHAIN`), of the meteo products `01` to `07` and `99`, and
of `80_FINALIZE`. The meteo products `08` to `13` were last run with diive
v0.91.0 and v0.91.1.

## Python environment

The notebooks run in Python 3.12 in an environment managed with
[uv](https://docs.astral.sh/uv/). The project declares three direct dependencies in
`pyproject.toml`: diive (with its database extra), SciPy and opco; everything else arrives through
diive. Versions from `uv.lock`, for Windows:

| Package | Version | Use in this repository |
|---|---|---|
| diive | 0.93.0 | all processing steps above |
| pandas | 3.0.3 | data handling in every notebook |
| opco | 0.1.0 | correction of the LI-7500 CO~2~ flux (FP2026.2) |
| NumPy | 2.4.6 | numerical work |
| SciPy | 1.17.1 | trend statistics (Theil-Sen slopes, Kendall's tau) |
| XGBoost | 3.2.0 | gap-filling models, called through diive |
| scikit-learn | 1.8.0 | used in the meteo stage |
| Matplotlib | 3.10.9 | figures |
| PyArrow | 19.0.1 | parquet files |
| influxdb-client | 1.50.0 | access to the site database in the meteo screening |

: Python packages {#tbl-python-packages}

The documentation website is built with [Quarto](https://quarto.org/) (quarto-cli 1.9.38).

## Repository

All notebooks are in the [repository](https://github.com/holukas/dataset_ch-lae_flux_product)
under `workflow/`, and rendered on this site under [Notebooks](notebooks/index.html).
