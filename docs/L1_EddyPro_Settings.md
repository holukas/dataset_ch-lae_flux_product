# Level-1: EddyPro settings

The Level-1 fluxes are calculated with EddyPro, one run per setup period and gas analyser. All runs
belong to Level-1 version `FF-202610`:

- **`IRGA72`**, the enclosed-path LI-7200: 18 runs, 2016 to September 2026. These are the fluxes of
  FP2026.1.
- **`IRGA75`**, the open-path LI-7500: 19 runs, 2004 to 2017 and 2019. These fluxes are in progress
  for FP2026.2 and are not part of FP2026.1.

This page lists the settings of these runs. They are taken from the EddyPro project (`.eddypro`)
and metadata (`.metadata`) file of each run and checked against the EddyPro output. Both files of
every run are shared with the dataset, in the folder `EDDYPRO_SETTINGS/IRGA72` or
`EDDYPRO_SETTINGS/IRGA75`. The runs and the merged record are described on [Level-1](L1.md), the
setup periods on [Yearly Notes](Yearly_Notes.md).

## Settings common to all runs

: EddyPro settings shared by all runs of both gas analysers. {#tbl-ep-common}

| Setting | Value |
|---|---|
| Software | EddyPro 7.0.9, run through fluxrun |
| Raw data | 20 Hz, files of 6 hours, file name gives the start time |
| Averaging period | 30 minutes; a period with more than 10 % missing raw records is not calculated |
| Coordinate rotation | double rotation |
| Detrending | block averaging |
| Time lag | covariance maximisation within a window per gas; the nominal lag is used when the maximum lies at the edge of the window |
| Angle-of-attack correction | not applied |
| Self-heating correction | not applied in EddyPro; for the LI-7500 it follows as [Level 1.1](L1.1.md) |
| Low-frequency spectral correction | Moncrieff et al. (2004) |
| Quality flags | steady-state and integral turbulence tests, 0/1/2 scheme of Mauder and Foken (2004) |
| Random uncertainty | Finkelstein and Sims (2001) |
| Footprint | Kljun et al. (2004) |
| Raw-data tests | the nine tests of Vickers and Mahrt (1997), all enabled; spikes and values outside the absolute limits are removed before the fluxes are calculated |
| Spike detection | 5 standard deviations for `W`, 3.5 for `U`, CO~2~ and H~2~O; at most 3 consecutive values count as a spike; hard flag above 1 % spikes |
| Absolute limits | horizontal wind 30 m s^-1^, vertical wind 5 m s^-1^, sonic temperature -40 to 50 °C, CO~2~ 200 to 900 µmol mol^-1^, H~2~O 0 to 40 mmol mol^-1^ |
| Site | 47.478333 N, 8.364389 E, 689 m a.s.l.; canopy height 37 m, displacement height 24.79 m, roughness length 5.55 m |
| Sonic anemometer | Gill, at 47 m, north offset 209°; path lengths 11 cm (horizontal) and 12.5 cm (vertical) |
| Output | FLUXNET format, full output, biomet and metadata files |

## Settings that differ between the gas analysers

: EddyPro settings that depend on the gas analyser. {#tbl-ep-analysers}

| Setting | LI-7200 (`IRGA72`) | LI-7500 (`IRGA75`) |
|---|---|---|
| CO~2~ and H~2~O | dry mole fractions (mixing ratios), µmol mol^-1^ and mmol mol^-1^ | molar densities, mmol m^-3^ |
| Density (WPL) correction | not needed, because the analyser reports mole fractions | applied, Webb et al. (1980) |
| High-frequency spectral correction | Fratini et al. (2012) | Horst (1997) |
| Spectral assessment | in situ, from the run's own data or a neighbouring run | in situ, from the run's own data or a neighbouring run |
| Analyser | intake tube 100 cm long, 5.3 mm inner diameter, flow 12 L min^-1^; path lengths 1.27 cm (horizontal) and 12.7 cm (vertical) | open path; path lengths 0.95 cm (horizontal) and 12.7 cm (vertical) |
| Separation from the sonic | N +6, E -1, V -15 cm; N +11, E +1, V -1 cm from `2023_2` | N +33, E 0, V -5 cm |
| Air temperature | from the LI-7500 in the same raw files up to `2018_1`, then from the biomet file | from the LI-7500 |

## LI-7200 runs (`IRGA72`, FP2026.1)

: Settings that change between the `IRGA72` runs. Time-lag windows and nominal lags in seconds. {#tbl-ep-runs}

| Setup periods | Gas analyser | CO~2~ lag window, nominal | H~2~O lag window, nominal |
|---|---|---|---|
| `2016_2` to `2018_1` | IRGA72-B; the LI-7500 is in the same raw files | 0.05 to 1.00, 0.30 to 0.35 | 0.05 to 4.00, 0.40 to 0.55 |
| `2018_2`, `2018_4+2019_1` | IRGA72-B-GN1 | 0.05 to 1.00, 0.30 to 0.35 | 0.05 to 4.00, 0.40 to 0.45 |
| `2018_3` | none: sonic only, `H`, `TAU` and `USTAR` | | |
| `2019_4` to `2021_1` | IRGA72-A | 7.90 to 8.80, 8.40 | about 7.75 to 13.05, 8.45 to 8.55 |
| `2022_2` | IRGA72-A | 0.95 to 1.40, 1.25 | 1.00 to 4.00, 1.40 |
| `2022_3` | IRGA72-A | 8.45 to 9.55, 8.95 | 8.20 to 13.05, 9.00 |
| `2022_4` | IRGA72-A | 8.00 to 9.30, 8.45 | 8.00 to 13.00, 8.55 |
| `2023_1` to `2026_1` | IRGA72-A | 7.90 to 8.80, 8.45 | 7.75 to 13.05, 8.50 to 8.55 |

- **Time lags.** The lags of about 8.4 s from `2019_4` on are not the travel time through the
  intake tube. According to the setup notes 12 and 13 (see [Yearly Notes](Yearly_Notes.md)), they
  include an artificial delay added by the data acquisition. `2022_2` has no such delay, and its
  CO~2~ lag of 1.25 s lies in the expected range. The lag shifts again in `2022_3` and `2022_4`,
  which are therefore separate runs (note 7). Lags are not comparable across setup periods.
- **Analyser position.** The inlet was moved in March 2023 (note 23), which changes the
  separation from `2023_2` on. Tube length and flow are unchanged.
- **Spectral assessment.** Four short setup periods use the assessment of a neighbouring run:
  `2016_2` that of `2016_3`, `2018_1` that of `2017_1+2`, `2022_2` and `2022_4` that of `2022_3`.
- **Biomet file.** The runs up to `2025_1` read `EDDYPRO_BIOMET_CH-LAE_2004-2025.csv`, the `2026_1`
  run reads `EDDYPRO_BIOMET_CH-LAE_2004-2026.09.csv`. The file holds `TA`, `RH`, `SW_IN`, `LW_IN`,
  `PA` and `PPFD_IN` at the 47 m tower level, with the timestamp at the end of the half-hour. Over
  2004 to 2025 the two files differ only in model fills, reconstructions and one half-hour on
  16 May 2025.

: The `IRGA72` runs of Level-1 version `HS50_IRGA72_FF-202610`. {#tbl-ep-ids}

| Run | Level-1 ID | Run | Level-1 ID |
|---|---|---|---|
| `2016_2` | `Level-1_FR-20261021-175449` | `2021_1` | `Level-1_FR-20260902-174442` |
| `2016_3` | `Level-1_FR-20261019-195550` | `2022_2` | `Level-1_FR-20261021-180457` |
| `2017_1+2` | `Level-1_FR-20261019-195156` | `2022_3` | `Level-1_FR-20260902-173931` |
| `2018_1` | `Level-1_FR-20261021-175903` | `2022_4` | `Level-1_FR-20261021-180903` |
| `2018_2` | `Level-1_FR-20261019-194911` | `2023_1` | `Level-1_FR-20260902-173731` |
| `2018_3` | `Level-1_FR-20261021-180146` | `2023_2` | `Level-1_FR-20260902-173626` |
| `2018_4+2019_1` | `Level-1_FR-20261019-193809` | `2024` | `Level-1_FR-20260902-173438` |
| `2019_4` | `Level-1_FR-20261019-193534` | `2025` | `Level-1_FR-20260902-173353` |
| `2020` | `Level-1_FR-20261019-193404` | `2026_1` | `Level-1_1_FR-20261023-141128` |

## LI-7500 runs (`IRGA75`, in progress for FP2026.2)

: Time-lag settings of the `IRGA75` runs, in seconds. {#tbl-ep-runs-75}

| Setup periods | Lag window | Nominal lag, CO~2~ / H~2~O |
|---|---|---|
| `2004` to `2017_1+2` | 0.05 to 0.75 | 0.20 to 0.30 / 0.20 to 0.30 |
| `2019_3` | 11.90 to 12.70 | 12.20 / 12.15 |

- **Time lags.** An open-path analyser needs only a short lag window, for the separation from the
  sonic. The lag of about 12 s in `2019_3`, when the LI-7500 stood in for the LI-7200, includes an
  artificial delay from the data acquisition, as in the preceding period `2019_2` (note 13).
- **Other instruments in the raw files.** In `2005_2`, `2005_3` and `2008_2+3` the raw files also
  hold a quantum cascade laser (QCL-L2, QCL-L and QCL-ISO), and in `2016_2+3` and `2017_1+2` the
  LI-7200. These are declared in the metadata but not used: the `IRGA75` fluxes come from the
  LI-7500 only.
- **Spectral assessment.** `2005_2` and `2005_3` use the assessment of `2005_1+4`, `2016_1` that of
  `2015`. All other runs compute their own.
- **Biomet file.** All runs read `EDDYPRO_BIOMET_CH-LAE_2004-2025.csv`.
- **File names.** The project and metadata files of `2005_3` end in `_OPENLAG`, a name left over
  from the Level-0 run. Their settings are those of a Level-1 run, with the same lag window as the
  other `IRGA75` runs.

: The `IRGA75` runs of Level-1 version `HS50_IRGA75_FF-202610`. {#tbl-ep-ids-75}

| Run | Level-1 ID | Run | Level-1 ID |
|---|---|---|---|
| `2004` | `Level-1_FR-20261025-015217` | `2011` | `Level-1_FR-20261023-175826` |
| `2005_1+4` | `Level-1_FR-20261025-014900` | `2012` | `Level-1_FR-20261023-155153` |
| `2005_2` | `Level-1_FR-20261026-082007` | `2013` | `Level-1_FR-20261023-154110` |
| `2005_3` | `Level-1_FR-20261026-081729` | `2014` | `Level-1_FR-20261023-153808` |
| `2006` | `Level-1_FR-20261025-014531` | `2015` | `Level-1_FR-20261023-153526` |
| `2007` | `Level-1_FR-20261025-014245` | `2016_1` | `CH-LAE_2016_1_FR-20261025-000304` |
| `2008_1+4` | `Level-1_FR-20261025-013712` | `2016_2+3` | `Level-1_FR-20261023-153227` |
| `2008_2+3` | `Level-1_FR-20261025-013950` | `2017_1+2` | `Level-1_FR-20261023-150135` |
| `2009` | `Level-1_FR-20261025-013458` | `2019_3` | `Leve-1_FR-20261023-145907` |
| `2010` | `Level-1_FR-20261025-000606` | | |

## Known limitations

- **Sonic model.** All runs declare a Gill HS-50. From 2016 to 19 December 2019 the sonic was a
  Gill HS-100 (fieldbook); for the years before 2016 the fieldbook has no sonic record. EddyPro
  uses the model for the path lengths of the sonic, so the HS-50 entry is nominal where the sonic
  was an HS-100.
- **Gaps between runs.** The setup periods `2019_2`, `2021_2` and `2022_1` have no run of either
  analyser; `2019_3` has an `IRGA75` run only. See [Level-1](L1.md).
