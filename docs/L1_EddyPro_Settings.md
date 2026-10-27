# Level-1: EddyPro settings

The Level-1 fluxes of FP2026.1 come from 18 EddyPro runs, one per setup period of the enclosed-path
LI-7200 (`IRGA72`). All belong to the Level-1 version `HS50_IRGA72_FF-202610`. This page lists the
settings of these runs, taken from their EddyPro project (`.eddypro`) and metadata (`.metadata`)
files and checked against the EddyPro output. The runs and the merged record are described on
[Level-1](L1.md); the setup periods on [Yearly Notes](Yearly_Notes.md).

The processing settings are the same in all 18 runs. What differs between runs are the gas
analyser, its position, the time-lag windows, the source of the air temperature and whether a
run computes its own spectral assessment.

## Settings common to all runs

: EddyPro settings of all `IRGA72` runs of FP2026.1. {#tbl-ep-common}

| Setting | Value |
|---|---|
| Software | EddyPro 7.0.9, run through fluxrun |
| Raw data | 20 Hz, files of 6 hours, file name gives the start time |
| Averaging period | 30 minutes; a period with more than 10 % missing raw records is not calculated |
| Coordinate rotation | double rotation |
| Detrending | block averaging |
| Time lag | covariance maximisation within a window per gas; the nominal lag is used when the maximum lies at the edge of the window |
| CO~2~ and H~2~O | dry mole fractions (mixing ratios) from the LI-7200, in µmol mol^-1^ and mmol mol^-1^; therefore no density (WPL) correction |
| Angle-of-attack correction | not applied |
| Self-heating correction | not applied (it concerns the open-path LI-7500 only) |
| High-frequency spectral correction | Fratini et al. (2012), with an in-situ spectral assessment |
| Low-frequency spectral correction | Moncrieff et al. (2004) |
| Quality flags | steady-state and integral turbulence tests, 0/1/2 scheme of Mauder and Foken (2004) |
| Random uncertainty | Finkelstein and Sims (2001) |
| Footprint | Kljun et al. (2004) |
| Raw-data tests | the nine tests of Vickers and Mahrt (1997), all enabled; spikes and values outside the absolute limits are removed before the fluxes are calculated |
| Spike detection | 5 standard deviations for `W`, 3.5 for `U`, CO~2~ and H~2~O; at most 3 consecutive values count as a spike; hard flag above 1 % spikes |
| Absolute limits | horizontal wind 30 m s^-1^, vertical wind 5 m s^-1^, sonic temperature -40 to 50 °C, CO~2~ 200 to 900 µmol mol^-1^, H~2~O 0 to 40 mmol mol^-1^ |
| Site | 47.478333 N, 8.364389 E, 689 m a.s.l.; canopy height 37 m, displacement height 24.79 m, roughness length 5.55 m |
| Sonic anemometer | Gill, at 47 m, north offset 209°; path lengths 11 cm (horizontal) and 12.5 cm (vertical) |
| LI-7200 | intake tube 100 cm long, 5.3 mm inner diameter, flow 12 L min^-1^; path lengths 1.27 cm (horizontal) and 12.7 cm (vertical) |
| Output | FLUXNET format, full output, biomet and metadata files |

## Settings that differ between runs

: Settings that change between the `IRGA72` runs. Separations are from the sonic anemometer, in cm (N northward, E eastward, V vertical). Time-lag windows and nominal lags are in seconds. {#tbl-ep-runs}

| Setup periods | Gas analyser | Separation | CO~2~ lag window, nominal | H~2~O lag window, nominal | Air temperature from |
|---|---|---|---|---|---|
| `2016_2` to `2018_1` | IRGA72-B; the LI-7500 is in the same raw files | N +6, E -1, V -15 | 0.05 to 1.00, 0.30 to 0.35 | 0.05 to 4.00, 0.40 to 0.55 | LI-7500 temperature in the raw files |
| `2018_2`, `2018_4+2019_1` | IRGA72-B-GN1 | N +6, E -1, V -15 | 0.05 to 1.00, 0.30 to 0.35 | 0.05 to 4.00, 0.40 to 0.45 | biomet file |
| `2018_3` | none: sonic only, `H`, `TAU` and `USTAR` | | | | biomet file |
| `2019_4` to `2021_1` | IRGA72-A | N +6, E -1, V -15 | 7.90 to 8.80, 8.40 | about 7.75 to 13.05, 8.45 to 8.55 | biomet file |
| `2022_2` | IRGA72-A | N +6, E -1, V -15 | 0.95 to 1.40, 1.25 | 1.00 to 4.00, 1.40 | biomet file |
| `2022_3` | IRGA72-A | N +6, E -1, V -15 | 8.45 to 9.55, 8.95 | 8.20 to 13.05, 9.00 | biomet file |
| `2022_4` | IRGA72-A | N +6, E -1, V -15 | 8.00 to 9.30, 8.45 | 8.00 to 13.00, 8.55 | biomet file |
| `2023_1` | IRGA72-A | N +6, E -1, V -15 | 7.90 to 8.80, 8.45 | 7.75 to 13.05, 8.50 | biomet file |
| `2023_2` to `2026_1` | IRGA72-A | N +11, E +1, V -1 | 7.90 to 8.80, 8.45 | 7.75 to 13.05, 8.50 to 8.55 | biomet file |

- **Time lags.** The lags of about 8.4 s from `2019_4` on are not the travel time through the
  intake tube. According to the setup notes 12 and 13 (see [Yearly Notes](Yearly_Notes.md)), they
  include an artificial delay added by the data acquisition. `2022_2` has no such delay, and its CO~2~ lag of
  1.25 s lies in the expected range. The lag shifts again in `2022_3` and `2022_4`, which are
  therefore separate runs (note 7). Lags are not comparable across setup periods.
- **Analyser position.** The inlet was moved in March 2023 (note 23), which changes the
  separation from `2023_2` on. Tube length and flow are unchanged.
- **Air temperature.** Up to `2018_1` the air temperature comes from the LI-7500, which is in the
  same raw files. From `2018_2` on the LI-7500 is no longer in the raw files, and the air
  temperature comes from the biomet file.
- **Biomet file.** The runs up to `2025_1` read `EDDYPRO_BIOMET_CH-LAE_2004-2025.csv`, the `2026_1`
  run reads `EDDYPRO_BIOMET_CH-LAE_2004-2026.09.csv`. The file holds `TA`, `RH`, `SW_IN`, `LW_IN`,
  `PA` and `PPFD_IN` at the 47 m tower level, with the timestamp at the end of the half-hour. Over
  2004 to 2025 the two files differ only in model fills, reconstructions and one half-hour on
  16 May 2025.

## Spectral assessment

Each run computes the in-situ spectral assessment for the high-frequency correction from its own
data, except four short setup periods, which use the assessment of a neighbouring period:

: Runs that use the spectral assessment of another run. {#tbl-ep-sa}

| Run | Assessment taken from |
|---|---|
| `2016_2` | `2016_3` |
| `2018_1` | `2017_1+2` |
| `2022_2` | `2022_3` |
| `2022_4` | `2022_3` |

## Runs

: The `IRGA72` runs of Level-1 version `HS50_IRGA72_FF-202610`. {#tbl-ep-ids}

| Run | Level-1 ID |
|---|---|
| `2016_2` | `Level-1_FR-20261021-175449` |
| `2016_3` | `Level-1_FR-20261019-195550` |
| `2017_1+2` | `Level-1_FR-20261019-195156` |
| `2018_1` | `Level-1_FR-20261021-175903` |
| `2018_2` | `Level-1_FR-20261019-194911` |
| `2018_3` | `Level-1_FR-20261021-180146` |
| `2018_4+2019_1` | `Level-1_FR-20261019-193809` |
| `2019_4` | `Level-1_FR-20261019-193534` |
| `2020` | `Level-1_FR-20261019-193404` |
| `2021_1` | `Level-1_FR-20260902-174442` |
| `2022_2` | `Level-1_FR-20261021-180457` |
| `2022_3` | `Level-1_FR-20260902-173931` |
| `2022_4` | `Level-1_FR-20261021-180903` |
| `2023_1` | `Level-1_FR-20260902-173731` |
| `2023_2` | `Level-1_FR-20260902-173626` |
| `2024` | `Level-1_FR-20260902-173438` |
| `2025` | `Level-1_FR-20260902-173353` |
| `2026_1` | `Level-1_1_FR-20261023-141128` |

Each run folder holds its project and metadata file, named after the setup period and the
instruments, for example `CH-LAE_2025_1_[IRGA72]_HS50-B_IRGA72-A.eddypro`.

## Known limitations

- **Sonic model.** All runs declare a Gill HS-50. From 2016 to 19 December 2019 the sonic was a
  Gill HS-100 (fieldbook). EddyPro uses the model for the path lengths of the sonic, so the
  HS-50 entry is nominal for that period.
- **Gaps between runs.** The setup periods `2019_2`, `2019_3`, `2021_2` and `2022_1` have no
  `IRGA72` run; see [Level-1](L1.md).
