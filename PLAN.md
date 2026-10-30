# Dataset plan

Working document: what the CH-LAE flux product is to contain, what exists today,
and what is still missing. It is the place to look when picking up the work again.

It lives at the repository root rather than in `docs/` because Quarto renders
every `.md` under `docs/` onto the public website, and this file is internal.
When a section here settles it moves to the site — the variable inventory to
`docs/Variables.md`, the scope and coverage summary to `docs/Overview.md` — and
is deleted from this file so the two cannot drift apart.

Status vocabulary used throughout:

- **done** — exists, checked, and read by something downstream.
- **open** — planned, not started or not finished.
- **verify** — a fact this plan depends on that has not been established yet.
  Nothing marked `verify` may be quoted as settled in the published pages.


## 1. Releases

| release | period | gas analyser | state |
|---|---|---|---|
| `FP2026.1` | 2016 - Sep 2026 | `IRGA72` (LI-7200, enclosed path) | done, released 27 Oct 2026 |
| `FP2026.2` | 2004 - Sep 2026 | `IRGA75` (LI-7500, open path) 2004-2015 + `IRGA72` from 2016 | open: both chains run, merges to re-run (4.2) |

`FP2026.2` supersedes `FP2026.1` and re-includes it in full. The two releases
differ in the flux record only; the meteorological product is built once over
2004 - 30 Sep 2026 and serves both. The period was extended from 2025 in October
2026; section 3.1 lists which products have been carried along.


## 2. Record boundaries

These are the periods the dataset can cover, and the reason each one starts and
stops. They bound every table below.

| record | period | note |
|---|---|---|
| `IRGA75` fluxes | 2004 - 12 Dec 2017, plus 17 Jan - 20 Mar 2019 | analyser removed Dec 2017; the 2019 window is the stand-in run `2019_3` |
| `IRGA72` fluxes | 11 Jan 2016 - 30 Sep 2026 | two physical LI-7200 units, exchanged inside the 2019 gap; the Level-0 record ends 2026-10-01 00:45 at the run boundary |
| tower meteorology, 47 m | 2004 - 30 Sep 2026 | `PA` and `LW_IN` start Sep 2005 with the CNR1 and the pressure sensor; `PREC`, `SW_OUT` and `LW_OUT` products still end 2025 |
| soil profile FF1 | 2004 - 2025 | sensors replaced as a set on 19 Mar 2020, no overlap across the change; products not yet extended to 2026 |
| radiometer | CNR1 Sep 2005 - Dec 2021, CNR4 from 14 Dec 2021 | logger constants updated 7 Jan 2022, 24 days later |

Setup periods, their notes and the unusable windows are in `docs/Yearly_Notes.md`
and are not repeated here.


## 3. Meteorological variables

### 3.1 In the dataset

One product notebook per variable in `workflow/10_METEO/30_PRODUCTS/`, joined by
`99_METEO_MERGED_2004-2026.09.ipynb` (all thirteen; `08` to `13` still end 2025) and documented on a page under
`docs/Meteo_Data.md`.

| variable | series | period | notebook | page | state |
|---|---|---|---|---|---|
| `SW_IN` | incoming shortwave, 47 m | 2004 - Sep 2026 | `01` | yes | done |
| `TA` | air temperature, 47 m | 2004 - Sep 2026 | `02` | yes | done |
| `PPFD_IN` | photosynthetic photon flux density, 47 m | 2004 - Sep 2026 | `03` | yes | done |
| `RH` | relative humidity, 47 m | 2004 - Sep 2026 | `04` | yes | done |
| `PA` | air pressure, 47 m | 2005 - Sep 2026 | `05` | yes | done |
| `LW_IN` | incoming longwave, 47 m | 2005 - Sep 2026 | `06` | yes | done |
| `VPD` | vapour pressure deficit, 47 m | 2004 - Sep 2026 | `07` | yes | done |
| `PREC` | precipitation | 2004-2025 | `08` | yes | done |
| `SWC` | soil water content, 5 depths | 2004-2025 | `09` | yes | done |
| `TS` | soil temperature, 7 depths | 2004-2025 | `10` | yes | done |
| `G` | soil heat flux, forest floor, 3 plates | 2004-2025 | `11` | yes | done |
| `SW_OUT` | outgoing (reflected) shortwave, 47 m | 2005-2025 | `12` | yes | done |
| `LW_OUT` | outgoing (emitted) longwave, 47 m | 2005-2025 | `13` | yes | done |

Six of these are re-formatted for EddyPro by
`40_EXPORTS/EDDYPRO_BIOMET_CH-LAE_2004-2026.09.ipynb` (`TA`, `RH`, `PA`, `SW_IN`,
`LW_IN`, `PPFD_IN`) and are the biomet input to the final flux runs. The export
reads them from `99_METEO_MERGED_2004-2026.09.parquet`, not from the six product
files, and exports the measured `TA` and `RH`, not the homogenised columns. Over
2004-2025 it differs from the 2025 file only in model fills and reconstructions
of `TA`, `SW_IN`, `PPFD_IN` and `RH` and in the probe half-hour of 16 May 2025;
the notebook asserts this and attributes each difference.

**Extension to 30 September 2026.** The Lägern reference
(`10_REFERENCE/MeteoSwiss_LAE_2004-2026.09`) and products `01` to `06`, the six
biomet inputs, now end at `2026-09-30 23:45` and are named `*_2004-2026.09`
(`05`, `06`: `*_2005-2026.09`). Their 2026
screening notebooks (`20_SCREENING/*/<VAR>_T1_47_1_2026.09`) are committed. What
the extension brought:

- **`02` and `04` carry a new probe history at 47 m.** A Campbell HygroVUE10
  replaced the CS215 on 5 June 2026 (source code `4`). The CS215 itself has two
  states besides normal operation: it read too warm in sun from autumn 2024 until
  it was handled on 16 May 2025, and it carried no daytime shield excess after
  that. Both notebooks put the HygroVUE10 era onto the CS215 level in their
  homogenised columns.
- **`04` now exports `RH_T1_47_1_HOMOGENIZED`**, and reads `02`'s measured and
  homogenised `TA` to build it. This is a new value-changing read: `04` must be
  re-run whenever `02` changes.
- **Re-run done.** `02`, `04` and `06` were re-run on 22 Oct 2026, in that order,
  and the `TA`, `RH` and `LW_IN` pages carry the numbers of that run. `04` (saturation
  ceiling of the MP101A, step 13), `07` and `99` were re-run on 29 Oct 2026.

`07` is extended: it exports `VPD_T1_47_1` from the measured `TA` and `RH` and
`VPD_T1_47_1_HOMOGENIZED` from their homogenised columns, and `99` merges both.

Not yet extended, still reading or writing the `*_2025` files: `08` to
`13`, `RADIATION_SENSOR_CONTINUITY`, `TA_HOMOGENIZATION_OPTIONS` and
`build_meteo_dashboard.py` (whose paths `build_calendar_explorer.py` imports). The
`90_OVERVIEW` notebooks `METEO_TA`, `METEO_SW_IN` and `METEO_VPD` read the `*_2004-2026.09`
products and cover 2004-2025.

Open method items from the review of the extended notebooks:

- `05`: the seasonal-cycle check of the tower-Lägern difference is not cut at
  `LAST_FULL_YEAR`, unlike the other yearly statistics of the notebook.
- `05`: the post-2016 departure from the barometric formula against Lägern keeps
  growing, -0.061 kPa in 2025 and -0.074 kPa in January to September 2026. Section 6.
- `03`: the `PPFD_IN` decline has not continued since 2024; 2025 and 2026 stay
  within the ordinary one-year change of the 2024 level. The `PPFD_IN` page has to
  say so.
- `06`: the overcast ceiling of summer 2026 falls to 0.93-0.95, below every
  earlier year. The notebook attributes it to an exceptionally dry and clear
  summer, not to the instrument; no action beyond the `LW_IN` page.

### 3.2 Recently added

`G`, `SW_OUT` and `LW_OUT` were added in September 2026 and are listed in 3.1. Their
methods live in the notebooks and on their `docs/Meteo_Data_*.md` pages; only what is
still unresolved is kept here, in section 6.

Three things about them are worth knowing before the next variable is added, because
each cost a wrong result first.

- **A field rename is not an instrument change, and the two need not coincide.** The
  archive renamed the `G` fields on 2011-12-31 while the measurement carried on
  unchanged for another three months; the acquisition actually changed in March and
  April 2012. A first version of `11` put the era boundary on the rename and pushed a
  visible artefact into the exported product. Derive an era boundary from the data and
  report the rename separately.
- **A provenance flag must be built from where the values ended up, not from where they
  started.** `12` shifted the August 2012 block onto its corrected time axis without
  moving the masks that record which screening supplied each value, and exported 31
  records under the wrong screening. Anything that moves data in time has to move its
  provenance with it.
- **A threshold derived from an effect size degenerates when the effect is zero.**
  Several checks in `12` and `13` compared a scatter against a fraction of the very
  departure they were testing, so they could not pass when the answer was "no
  difference". Derive a threshold from what the record does when nothing happened, and
  check that such years exist before relying on them: in `13` they do not, and the
  notebook says so rather than pretending otherwise.

### 3.3 Candidates, not yet decided

Measured at the site, plausible for the dataset, no decision taken. Listed so the
scope question is asked once rather than rediscovered.

| candidate | raw database field | note |
|---|---|---|
| `PPFD_OUT` | `PPFD_OUT_T1_47_1`, `PPFD_OUT_T1_47_2` | two sensors; a reflected-PAR channel (`PPFD_refl`) already exists in the 2004 program, so the record may predate the 2016 PAR LITE |
| `PPFD_DIF` | `PPFD_DIF_T1_47_1` | Delta-T BF2 sunshine sensor, total and diffuse PAR, from Aug 2004 |
| second `PPFD_IN` | `PPFD_IN_T1_47_2` | a second incoming sensor at the same level; decide whether it is a replicate or a replacement era |
| `NETRAD` | `NETRAD_FF1_2_1`, `NETRAD_NABEL_T1_49_1` | no tower-level net radiometer field; a 47 m `NETRAD` would be derived from the four components. Only the NABEL sensor is screened (2004-2018), and no product exists |
| `ALB` | derived, `SW_OUT`/`SW_IN` | both components are now products (3.1), so this costs nothing extra. `12` already computes the albedo as a diagnostic and reports a median of 0.112 |
| `WS`, `WD` | — | A100LK cup anemometer from Jan 2016; the sonic series is already in the flux output |
| `SWP` | — | MPS-2 and TEROS 21 water potential, FF1 and FF2; same 19 Mar 2020 generation change as `SWC` |
| subcanopy (`M1_2`) | `SW_IN_BC_M1_2_1`, `SW_OUT_BC_M1_2_1`, `LW_IN_BC_M1_2_1`, `LW_OUT_BC_M1_2_1`, `PPFD_IN_BC_M1_2_1` | a full four-component radiation set below canopy, plus PAR — a second measurement level, not a single variable |
| forest floor | `PPFD_IN_AVG_FF1_2_1`, `NETRAD_FF1_2_1` | the FF1 profile's own radiation |

The database field names above are read from listings cached in the outputs of
the `SW_IN`, `LW_IN`, `PPFD_IN` and `NETRAD` screening notebooks. Field existence
is not coverage: the first and last date of each has still to be checked.

Excluded by an existing decision: the **profile masts** (`T1_17.5`, `T1_35`,
`M2`, `M3`, `M4`). The dataset takes its meteorology from the 47 m level and the
forest floor. See `docs/Instrumentation.md`.


## 4. Fluxes

### 4.1 What the dataset publishes

| flux | from | state |
|---|---|---|
| `NEE` | CO~2~ flux plus storage, u*-filtered, gap-filled | `05_FPPC` (was `01_FPPC`), run on `IRGA72` 2016 - Sep 2026 and `IRGA75` 2004-2017 |
| `LE` | turbulent latent heat flux, no storage, no u* filter, gap-filled | `25_FPPC` (was `11_FPPC`), both analysers |
| `H` | turbulent sensible heat flux from the sonic, no storage, no u* filter, gap-filled | `35_FPPC` (was `15_FPPC`), both analysers |
| `GPP`, `RECO` | Level-4.2 partitioning of gap-filled `NEE` | not in FP2026.1 (decided 26 Oct 2026); run in both `05_FPPC` for FP2026.2 |
| `ET` | derived from gap-filled `LE` in `25_FPPC` | both analysers |

`LE` and `H` follow Pastorello et al. (2020): they are turbulent fluxes without a
storage term and are not u*-filtered (decided 26 Oct 2026). The 2016-2024 chain
published storage-corrected `LE` and `H`; this version does not.

### 4.2 Chain status

Levels as defined in `docs/FPC.qmd`. The run-by-run progress of the flux
calculations (versions, settings, what has been run for which year) is logged in
the [flux progress sheet](https://docs.google.com/spreadsheets/d/1kltV0Vuh9L1IR_z9HWqLBzEKpT6-G7C3TUN7H6uvA4A/edit?gid=0#gid=0);
the table below summarizes it per level.

| level | what it does | `IRGA75` | `IRGA72` | site page |
|---|---|---|---|---|
| Raw | binary → ASCII (bico) | done | done | written |
| L0 | preliminary run, per setup period | done, 2004-2019 | done, **through Sep 2026** | written |
| L1 | final run, per setup period | re-run Oct 2026 (`FF-202610`, 19 runs); merged in `20_L1_FLUXES/IRGA75/99` (18 run files) | done, **2016 - Sep 2026** (re-run, 18 runs) | written, with `L1_EddyPro_Settings` |
| L1.1 | open-path correction (opco) | done: `30_.../IRGA75/00` (with the July 2013 clock shift) and `01` (opco without `VPD`), re-run 29 Oct 2026 | n/a | written |
| L2 | quality flags from L1 output | in `30_` chain | in `30_` chain | written |
| L3.1 | storage term added (`NEE` only) | in `30_` chain | in `30_` chain | written |
| L3.2 | outlier detection; u* threshold detection | in `30_` chain, with the manual fog removals; tests 5 and 6 (`NEGNIGHT`, `NEGNIGHTS`) relaxed to uncertainty-based limits in `05` (30 Oct 2026), not run yet; u* detection 2005-2019 | in `30_` chain; test 5 relaxed in `05`, not run yet; u* detection 2016-2024 | written |
| L3.3 | flags from three constant u* thresholds | `NEE` | `NEE` | written |
| L4.1 | gap-filling (XGBoost, MDS for comparison) | `NEE`, `LE`, `H` | `NEE`, `LE`, `H` | written |
| L4.2 | partitioning into `GPP` / `RECO` | run in `05` (FP2026.2) | run in `05` (FP2026.2 only) | written |
| QCF | overall quality flag | — | — | written |

Both chains run on their full records (`IRGA72` 2016 - Sep 2026, `IRGA75` 2004-2017).
The `IRGA72` chain was re-run on 29 Oct 2026 on the new meteo merge: `NEE`, `H` and `GPP`
unchanged, `LE` keeps more half-hours with the wider absolute limits. The `IRGA75` chain
(`00`, `01`, `05`, `25`, `35`) was re-run the same evening. **The merges downstream predate
both re-runs** and have to be re-run in this order: `IRGA75/99`, the stage merge
`30_.../99_FPPC_MERGED_2004-2026.09`, `80_FINALIZE/10`, then `90_OVERVIEW/FLUX_NEE`. The
relaxed negative-night tests (item 11) need one more run of both `05` first. The test variants `T2`
(2004-2006) and `T3` (2012-2014) of `IRGA75/05` have been re-run with the relaxed tests (results
in item 11).

### 4.3 Auxiliary flux-derived series to decide on

Storage terms (`SC`, `SLE`, `SH`), friction velocity `USTAR`, the u* threshold
actually applied, the per-level quality flags and `QCF`, and the sonic wind
series. These exist in the processing output; the decision is which of them the
published file carries and under which names. `docs/Variables.md` is the page
that will state it.


## 5. Where to continue

**Next runs (as of 30 Oct 2026).** Meteo `04`, `07`, `99` and the `IRGA72` chain are re-run;
`IRGA75/00` (clock shift of July 2013) and `IRGA75/01` (opco without `VPD`) are re-run. Next:

1. `IRGA75/05`, `25` and `35`, in parallel (they read `01`; `05` has test 6 `NEGNIGHTS` and
   the manual removals; restart the kernel so the editable diive with `NegativeNights` loads).
   `05` is re-run (30 Oct 2026); `25` and `35` are running. **Re-run `IRGA75/05` and
   `IRGA72/05` once more** for the relaxed tests 5 and 6 (item 11; restart the kernel, diive's
   `flag_outliers_negative_nights_test` has the new `systematic=` option), then `IRGA72/99`.
2. `IRGA75/99`.
3. `30_FLUX_POST-PROCESSING_CHAIN/99_FPPC_MERGED`.
4. `80_FINALIZE/10`.
5. `90_OVERVIEW/FLUX_NEE` and `90_OVERVIEW/METEO_VPD`.

Then, before the release: **find the cause of the positive early `IRGA75` years** (item 12).
opco without `VPD` is kept (evaluated 30 Oct 2026); the run with `VPD` is not needed. The
difference to FLUXNET is explained (item 12): FLUXNET's winter nights of 2004-2015 are too low,
so it is no check of the early years. What remains open is our own budget of the early years:
whether the winter nights (gap-filled 75-80 %, at about +2.7 umol m-2 s-1) and the early-year
sources are plausible, judged against the `IRGA72` years and any independent respiration data.

In order. Each item is blocked by the one above it, except that the flux items
2 to 4 do not depend on the meteo item 1: their biomet input,
`EDDYPRO_BIOMET_CH-LAE_2004-2026.09.csv`, is written.

1. **Extend the rest of the meteo stage**: `08` to `13` (`99` already merges
   them as they are, to December 2025, since 27 Oct 2026; extending one means
   changing its stem in the `99` registry), `RADIATION_SENSOR_CONTINUITY`, `TA_HOMOGENIZATION_OPTIONS`, the
   `90_OVERVIEW` notebooks and `build_meteo_dashboard.py`; then the
   `docs/Meteo_Data_*.md` pages and dashboards of those variables, including
   the `VPD` page for the two columns of `07`. The `05`
   seasonal-cycle cut (section 3.1) goes with this pass.
2. **Settle the open points of the `IRGA72` Level-1 re-run.** The re-run is
   complete: 18 runs over 2016 - Sep 2026, one per setup period, in
   `0_data/IRGA72-Level-1_fluxnet_2016-2026.09/`, with `2022_2`, `2022_3` and
   `2022_4` as separate runs (notes 7, 12). The runs through `2025_1` read
   `EDDYPRO_BIOMET_CH-LAE_2004-2025.csv` and the `2026_1` run reads
   `EDDYPRO_BIOMET_CH-LAE_2004-2026.09.csv`, which over 2004-2025 differs from the
   2025 file only in model fills, reconstructions and the probe half-hour of
   16 May 2025 (`40_EXPORTS`, comparison section). The wrong calibration gas of
   note 15 (factor 0.974 on the CO2 concentration, 14 Dec 2017 - 15 Mar 2019) was
   corrected during the conversion of the raw data to ASCII with bico, so the
   runs read corrected concentrations. Still open: the setup table in
   `docs/Yearly_Notes.md`, which has no `2026_1` row yet and still shows `2025_1`
   as `running`; and **`H` from 10 January to 20 March 2019 (revisit later)**. The
   Level-0 file of `2019_2` yields about 289 half-hours of `H`, but `2019_2` has no
   Level-1 run, so the Level-1 input of the flux chain has no `H` at all in this
   period. Decide whether `2019_2` gets a sonic-only run, as `2018_3` did, and
   whether the `H` of the LI-7500 run `2019_3` (17 Jan - 20 Mar 2019, same sonic)
   fills the rest of the gap; `35_FPPC` would then need that run in its input.
3. ~~**Carry `20_L1_FLUXES/IRGA72` to September 2026.**~~ Done 25 Oct 2026.
   `99_IRGA72_L1_MERGED_2016-2026.09` merges the Level-1 runs; where two runs
   overlap at a year boundary it takes each record whole from one run, split at
   midnight, because the runs' values differ there.
   `00_FPPC_IRGA72_INPUT_2016-2026.09` joins it with every column of
   `99` from 1 January 2016 00:15 (the flux columns are empty until 11 January)
   and must be re-run whenever `99` changes. The
   Level-0 merge (`00_L0_CHECKS/IRGA72/01`) still joins its overlapping runs cell
   by cell with `combine_first`; Level 0 is preliminary, so this matters only
   where a Level-0 value is quoted.
4. **Review the `IRGA72` flux chain and the finalize set.** `05_FPPC` (`NEE`, with the
   Pastorello uncertainty), `25_FPPC` (`LE` and `ET`) and `35_FPPC` (`H`) ran on
   2016 - Sep 2026 (26 Oct 2026), all reading
   `00_FPPC_IRGA72_INPUT_2016-2026.09` with the homogenised `TA` and
   `VPD` as drivers; `NEE` uses the fixed 2016-2024 u* thresholds, kept on purpose
   although the FLUXNET thresholds for CH-Lae are much higher (decided 26 Oct 2026).
   Each writes only the columns it adds, and `99_FPPC_IRGA72_MERGED_2016-2026.09` in
   the same folder merges these (158 columns). `80_FINALIZE/10_FLUXES_and_METEO_2004-2026.09`
   collects the meteo of `99`, the `IRGA72` Level-1 fluxes of `22.1` and that file
   into one file from 2004 (548 columns); release datasets are cut from it by
   period. `80_FINALIZE/20_CH-LAE_FP2026.1_2016-2026.09` cuts the FP2026.1 dataset
   `CH-LAE_FP2026.1_2016-2026.09` (parquet and CSV, with the `20_` prefix), keeping
   the variables with a value in 2016 - Sep 2026; its column names are not final yet.
   The `_INFO.md` files of both give each variable's unit and description, from
   `80_FINALIZE/variable_info.py`; `*_CORRDIFF` and `FILE_TIME_DURATION` are still
   to be checked against the EddyPro documentation. The meteo reaches it only
   through `99`, which merges all thirteen products; `08` to `13` end in December
   2025 until they are extended. It now also collects the `IRGA75` Level-1 fluxes, the opco
   columns and the stage merge of both analysers (to be re-run, section 4.2). Still
   to check: `H` in 2024
   is about a third lower than in the other years.
   Level-4.2 partitioning is not part of this version of the dataset (decided
   26 Oct 2026). On 29 Oct 2026 the `NEE` notebook was renumbered `01_FPPC` -> `05_FPPC`,
   the number of the `IRGA75` chain (`LE` and `H` became `25_FPPC` and `35_FPPC`), and partitioning was switched on for FP2026.2; it has not
   run yet. Before `99` and `80_FINALIZE` run on its output, `variable_info.py` needs
   descriptions of the partitioning columns (`describe_all` stops on undescribed columns), and
   the FP2026.1 cut (`80_FINALIZE/20`) must not be rerun, or must leave those columns out, so
   that the released FP2026.1 stays reproducible. The old output `01_FPPC_IRGA72_NEE_2016-2026.09`
   stays in the data folder until the rerun.
5. **Decide the candidate list in 3.3**, then freeze the variable inventory and
   write `docs/Variables.md`.
6. **Energy-balance-closure correction of `LE` and `H`** (future session, not part
   of FP2026.1 for now). Pastorello et al. (2020): `EBC_CF = (NETRAD - G)/(H + LE)`
   from half-hours with measured `NETRAD` and `G`, filtered at 1.5 times its IQR, then
   three hierarchical methods (±15-day window at 22:00-02:30 and 10:00-14:30; ±5 days
   and ±1 h; ±5 days in the neighbouring years), giving `LE_CORR`, `H_CORR` and their
   25th and 75th percentiles. The `LE` and `H` random and joint uncertainty of
   ONEFlux belong to the same step (the joint one is built from the `_CORR25` and
   `_CORR75` spread). Needs the `NETRAD` and `G` products at September 2026.
7. **Fill the stub pages**: `Supplementary` is still a stub. The other pages,
   including `L1`, `QCF`, `Raw_Data`, `Overview`, `Dataset_Versions`, `Software`
   and `Links`, were written on 27 Oct 2026; `Management_Data` was removed, as
   there are no management data.
8. **Sensitivity of the annual `NEE` sums to the number of XGBoost trees** (future
   session). The number of trees is now chosen by blocked cross-validation (the
   minimum of the error on held-out 14-day blocks; in the runs of 29 Oct 2026, 110, 100
   and 120 trees for `IRGA72` `NEE`, `LE` and `H`, and 90, 100 and 100 for `IRGA75`; the
   count is chosen anew in every run). Between 60 and 110 trees the blocked error changes by less than 1 %,
   but the difference XGBoost - MDS over 2016 - Sep 2026 (`CUT_50`) moves from
   +265 to +685 gC m-2, almost all of it from daytime gaps. Compute the annual sums at
   several numbers of trees (e.g. 60, 80, 110, 150, 250) to see how firm the 110-tree
   result is before publishing; if they spread widely, consider averaging models
   trained with several seeds or tree counts.
9. **Wet-weather gap of the `IRGA75` gap-filling.** Stated in `docs/Issues.md`
   (2016-2017: about 40 gC m-2 apart on shared half-hours, 180-190 gC m-2 per year
   apart gap-filled). Numbers of the first run of chain `05` (29 Oct 2026, before the
   opco fit without `VPD`): -38 gC m-2 shared, 179 (2016) and 194 (2017) gC m-2
   gap-filled; check them after the merges are re-run (section 4.2). Of the half-hours
   only the `IRGA72` measured, half have no `IRGA75` flux and 30 % an AGC above 90.
   Wetness drivers alone do not help (opco tests). To do: calibrate an adjustment of the filled `IRGA75` values on the
   2016-2017 half-hours where only the `IRGA72` measured (drivers: precipitation in
   the preceding hours, RH, reason for the gap, day or night, `TA`, season), test it
   across years (fit on 2016, check 2017, and the reverse), with and without the
   half-hours with rain, since the shared sonic may be wet then and the `IRGA72`
   fluxes may be affected too. Apply it to 2004-2015 only if it closes most of the
   gap in both directions; otherwise state the bias as an uncertainty of the
   `IRGA75` years (now the state of `docs/Issues.md`). The `RECO` and `GPP` bias of
   the night-time partitioning needs its own adjustment or stays a stated uncertainty.
   Related: the test R² of chain `05` (0.59
   against 0.73 for the `IRGA72`) is lowered by the records with AGC from 50 to 90,
   whose scatter against the `IRGA72` is four to seven times that at AGC 50.
   The QCF 0 and 1 decision (29 Oct 2026) is in `docs/L4.1.md`. Scratch prototypes (29 Oct 2026): gap-filling the `IRGA75` with one
   model over all years plus the `IRGA72` at the `IRGA75` gaps of the other overlap
   year closed 2017 to -13 and 2016 to -92 gC m-2 (cross-year); the rest of 2016 lies
   in cold days of October to December, where the opco correction falls short
   (freezing fog; no opco variant and no fog screen fixed it).
10. **H2O fluxes of the two analysers** (future session; for now both are accepted as
    they are, decided 29 Oct 2026). The difference and its likely cause (tube damping
    in the LI-7200 at high RH) are stated in `docs/Issues.md`. To do: compare the energy balance closure
    (`H + LE` against `NETRAD - G`) of both analysers in 2016-2017, by RH class; the one
    that closes better at high RH has the more realistic `LE`. Also note that the
    `IRGA75` loses more wet half-hours (63 % of half-hours with a valid `LE`, against
    70 %), which biases its gap-filled `LE` low.
11. **Cold-night `NEE` of the `IRGA75` years** (found 29 Oct 2026 in
    `90_OVERVIEW/FLUX_NEE`; the limitation is now stated in `docs/Issues.md`). Done
    on 29 Oct 2026: opco refitted without `VPD` (with `VPD` it corrected the cold nights
    of 2004-2015 by only about a third of the 2016-2017 value); four fog episodes removed
    by hand in `05`, `25` and `35` (`docs/L3.2.md`); the `NEGNIGHTS` test of whole nights
    added to `IRGA75/05`; it removed 75 nights in the run of 30 Oct 2026, mostly October
    to February. **Relaxed on 30 Oct 2026, not run yet** (both `05`): test 5 removes a record
    below -4 times max(`FC_RANDUNC_HF`, median `PAS20` of the nighttime records of its calendar
    month), for `IRGA75` combined in quadrature with `OPCO_SIGMA` = 1; test 6 removes a night
    whose median lies below -3 standard errors, with n reduced for a lag-1 autocorrelation of 0.2
    and `OPCO_SIGMA` added in quadrature as an error shared by the night (new diive option
    `systematic=`). Scratch estimate on the current inputs (checked by running both `05` to the
    end of Level 3.2): `IRGA72` 43 records (was 182); `IRGA75` 159 records (663) and 16 nights,
    250 records (75 nights, 1,150 records). Direct effect on the sums (removed records kept, at
    the current gap-filled values), before any change of the gap-filling models: about -3 gC m-2
    per year for `IRGA72`, -7 to -20 for `IRGA75` (-179 over 2004-2017). In 2016-2017 the new
    night test removes 2 `IRGA75` nights, both with positive `IRGA72` `NEE`, and applied to the
    `IRGA72` none; the old one removed 9, 2 of them on nights where the `IRGA72` was negative too,
    and 11 `IRGA72` nights. It lets through 7 nights (four in December 2016, three in October to
    December 2017) with medians of -0.6 to -5 (one at -7.6 with only 5 values, not tested) on
    which the `IRGA72` read +1 to +4; the uncertainty alone does not single them out. The training screen in `01` keeps the old
    test 5. **`T2` (2004-2006) re-run with the relaxed tests (30 Oct 2026):** test 5 removes 22
    records (was 160), test 6 5 nights, 71 records (15 nights, 221 records); the inputs to
    Level 3.2 are unchanged. `CUT_50`, XGB, gC m-2: 2004 +36 (was +78), 2005 +69 (+169), 2006
    +44 (+130); `CUT_16` 2006 is -9. The drop of 42 to 100 per year is five times the direct
    effect estimated above: most of it comes through the gap-filling model, which now learns
    from the kept negative night values (62-67 % of the records are filled). 2005 and 2006
    remain sources. **`T3` (2012-2014) re-run the same way:** test 5 removes 26 records (was
    125), test 6 no night (12 nights, 185 records); the lag-1 autocorrelation there is 0.10
    against the 0.2 assumed. `CUT_50`, XGB, gC m-2: 2012 -303 (was -223), 2013 -295 (-155),
    2014 -304 (-141), so -80 to -163 per year, again mostly through the gap-filling. Still open:
    calm cold nights (wind below 2 m s-1,
    below 0 degC) remain about 1 umol m-2 s-1 below the `IRGA72` after the refit; fix in
    opco (cold-night term or more cold training rows) rather than in the chain. The
    period medians in `FLUX_NEE` (+0.08 against +1.67 umol m-2 s-1 below 0 degC) and
    the upper bound of about 50 gC m-2 per year predate the refit; recompute them after
    the merges are re-run (section 4.2).
12. **opco without `VPD`** (kept; evaluated 30 Oct 2026, see the end of this item). Dropping `VPD` from opco (`IRGA75/01`, `FEATURES_XI`/`FEATURES_K`) raises the
    annual `NEE` of 2004-2010 by about +30 to +100 gC m-2 and lowers 2011-2017 by up to
    about 75, against the opco with `VPD` (from the mean correction per year). In test `T2`
    2004-2006 become a source (+78, +169, +130 gC m-2; the December 2004 removal and the
    `NEGNIGHTS` test add +30 to +125 of that). The three variants without the `VPD`
    artefact (no `VPD`, `VPD` in k only, `VPD` floored at 0.05 kPa) agree within about
    20 gC m-2, and all fit the overlap equally (-41 against -38 gC m-2 for the opco with
    `VPD`); trained on one overlap year and tested on the other, every variant leaves about
    +40 gC m-2 per year. There is no independent estimate of the annual sums to check them
    against.

    The full `05` run of 30 Oct 2026 (`CUT_50`, XGB, gC m-2): 2004 +161, 2005 +164,
    2006 +144, 2007 -101, 2008 +64, 2009 +59, 2010 -44; 2011-2017 within about 30 of the
    run before. Against that run, 2004-2010 rose by +53 to +396. Most of the rise is in the
    gap-filled records (60-70 % of each year): the model learns from winter values made
    more positive by the larger correction and by the removed negative nights. In 2004
    about 300 of the +396 lie in 1 January to 29 March (no measurements, gap-filled
    only) and in December. The `VPD` artefact remains after the RH ceiling fix, smaller: on
    calm nights below 5 degC `VPD` is exactly 0 in 14 % of 2004-2015 and 49 % of
    2016-2017 (before the fix about 0 against 70 %).

    **Evaluated 30 Oct 2026: keep opco without `VPD`.** Scratch analysis (no files
    changed; scripts in the session scratchpad `agent_opco/`):
    - Skill: out of fold all variants are equal (RMSE 2.46); cross-year (fit one overlap
      year, test the other) `VPD` is worse (RMSE 2.94 against 2.73, bootstrap difference
      +0.21 [+0.03, +0.40]); its in-sample gain is overfitting. Cross-year, corrected
      minus `IRGA72` per test year is within ±9 gC m-2 for every variant (the "+40" above
      came from another selection of half-hours).
    - `VPD` = 0 marks the RH probe at its ceiling, not the weather: the fog share from
      `LW_IN`/clear-sky `LW_IN` > 1.25 is the same in both periods (42 % and 43 % of
      nights below 5 degC), but `VPD` = 0 on those fog nights is 7 % in 2004-2015 against
      47 % in 2016-2017. With `VPD` the correction of foggy cold nights falls short in the
      early years. 7 % of 2004-2015 records lie outside the training support with `VPD`,
      2.5 % without. `VPD` carries no self-heating signal.
    - With `VPD`, 2004-2006 would stay sources (about +95, +66, +44 gC m-2): dropping
      `VPD` is not the main cause of the positive early years.
    - **Against FLUXNET** (ONEFlux v1.3, CH-Lae 2004-2024, `NEE_VUT_REF`; its input for
      2004-2015 is the FP2021 `IRGA75` flux with the Kittler et al. (2017) correction, for
      2016-2017 the `IRGA72`). Split half-hour by half-hour (30 Oct 2026, scratch, against
      the `05` run of 30 Oct with the strict night tests, `CUT_50`, XGB). Our annual sums are
      +250 to +460 gC m-2 higher in 2005-2014 (2004 +605, 2015 +168) and lower in 2016-2017
      (-245, -417). Per year, 2004-2015:
      - Nights that both fill: +150 to +275. FLUXNET fills them far lower than we do,
        +1.8 to +2.9 umol m-2 s-1 apart from November to March, +0.3 to +0.8 in June to
        September. FLUXNET's winter nights are near zero (December: measured +0.06, filled
        -0.12; our `IRGA72` 2016-2026: +3.2). With 75-80 % of the nights filled, this is
        most of the difference.
      - Nights FLUXNET keeps and we remove: +13 to +52. In October to May FLUXNET's values
        there average -2 to -8 umol m-2 s-1. These are the apparent winter uptake that our
        Level 3.2 removes. FLUXNET keeps them, and MDS fills the other winter nights from
        them.
      - Shared measured nights: +7 to +32. Our nights are 0.5 to 0.9 higher there; opco adds
        +0.5 to +0.9 at night, the FP2021 correction +0.2 to +0.4. By day both add about +3,
        and the day differences are small in all classes.
      - Our filled winter nights (+2.7) agree with our measured ones (+2.9 to +3.2) and with
        the `IRGA72` of 2016-2026 (+2.5 to +3.2). FLUXNET's 2004-2015 winter nights are the
        implausible ones, so the difference does not point to an error in this chain.
      - 2016-2017 (`IRGA72` in FLUXNET): FLUXNET's nights average +4.2 and +5.4, our
        `IRGA72` +3.7. Not explained yet.
    - **Against Etzold et al. (2011)** (2005-2009, LI-7500, mean NEE -415 gC m-2 per year,
      range -366 to -662; our `05` run of 30 Oct: +66). Their flux has WPL and the Burba et
      al. (2008) / Järvi et al. (2009) self-heating correction; winter fluxes of ±15
      umol m-2 s-1 kept in the data but excluded from the gap-filling fits; negative nights
      and as many positive ones trimmed; Lloyd-Taylor at night, a running mean below 0 degC;
      u* 0.3; night coverage 24 %. Mean monthly sums (theirs read from their Fig. 5, about
      ±10 gC m-2), gC m-2:

      | | Nov-Mar | Apr + Oct | May-Sep | year |
      |---|---|---|---|---|
      | Etzold et al. | about +170 | about 0 | about -570 | -415 |
      | ours, `IRGA75` with opco | +393 | +72 | -399 | +66 |
      | ours, without opco | +91 | -27 | -635 | -572 |
      | `IRGA72` 2016-2025 | +374 | +38 | -516 | -105 |
      | FLUXNET | +184 | +20 | -422 | -221 |

      "Without opco" adds the mean opco correction per month and day/night back to every
      half-hour (approximate); opco adds about +640 gC m-2 per year, +42 to +67 per month.
      **Their correction reproduced (30 Oct 2026):** the R script in
      `opco-data/references/` (Burba 2008 equation, Järvi 2009 fraction 0.085, surface
      temperature from the sonic temperature) applied to our `01` input adds about +210 gC
      m-2 per year (0.7-1.2 umol m-2 s-1 by day, 0.4-1.0 at night), against opco +640.
      Our flux with it in place of opco: -362 per year (theirs -415); Nov-Mar +192 (about
      +170), Apr + Oct +3 (about 0), May-Sep -558 (about -570). So about 430 of the 480
      difference is the size of the correction. The `IRGA72` years support opco in winter
      (+374 against +393 and +192) and lie between the two in summer (-516 against -399 and
      -558). **Still open:** our
      early-year summer has about 120 gC m-2 less uptake than the `IRGA72` years. Either opco's
      daytime correction (about +2.5 umol m-2 s-1 in summer, fitted on 2016-2017) is too large
      for 2005-2009, or the difference is real (climate, stand). Check whether the correction
      behaves the same against temperature, radiation and u* in both periods. Documented on
      `docs/IRGA75_Comparisons.md`.
      Scripts in the session scratchpad `flx/`.
    - Open: without `VPD`, foggy cold nights are corrected about 0.5 umol m-2 s-1 too
      little and clear ones as much too strongly (unbiased in the annual mean, but it
      reaches the partitioning). A longwave fog ratio as a driver removes most of it
      (annual change within ±20 gC m-2 in 2006-2015; not usable in 2004-2005 without
      `LW_IN`).
    - The opco run with `VPD` of section 5 is no longer needed. Still to decide: whether
      2004, which starts on 30 March, gets an annual sum.


## 6. Open questions

Carried here because each blocks a scope decision or a published statement.

- ~~**How far back do `SW_OUT_T1_47_1` and `LW_OUT_T1_47_1` reach?**~~ Answered, and
  the first answer was wrong. Only the **raw** fields begin in 2020; the
  MeteoScreeningTool wrote both channels into `ch-lae_processed` back to
  **2005-09-14**, because it read CSVs rather than the raw bucket. `SW_OUT` and
  `LW_OUT` are therefore 2005-2025 products. The same is likely to hold for any
  other field whose raw record looks short, so check `meteoscreening_mst` before
  concluding a record is recent.
- ~~**Are the raw `G_M1..M3_0.05_1` fields the same plates as the processed
  `G_FF1_0.025_1..3`?**~~ Answered by `11`: they are, and over the timestamps they
  share the screened series is bit-identical to the raw one, so "screened by the
  MeteoScreeningTool" means "passed through unchanged" there. That overlap is only
  about 14 % of the pre-rebuild record.
- ~~**Does `G` carry a storage term above the plate?**~~ Decided: no. `11` estimates
  the term and reports its size instead, because adding it would need a measured bulk
  density and a soil temperature above the plate, and this site has neither. An
  energy-balance closure computed from `G` is therefore a closure at plate depth.
- **`G` around 2011/2012: the correction does not make the record homogeneous, and
  the daily-record panel of the dashboard shows it.** Three facts, all from the
  exported file. At the 2012 acquisition change the median daily amplitude of
  plates 1 and 2 falls by three to four times, from 8.4 and 10.3 W m-2 in 2011 to
  2.6 and 3.3 in 2012 and 1.2 and 1.8 in 2013, while **plate 3 does not follow**:
  it runs 15.7, 12.1, 10.8 across the same years. And the reconciled column swings
  between adjacent years, 4.8 in 2011, 5.7 in 2012, 3.4 in 2013, 5.5 in 2014, which
  no soil does. Part of what this entry originally described in 2011 was a separate
  fault, since found and flagged: plate 2 read backwards from June to December 2011,
  and the reconciled column averaged it with plate 1 and nearly cancelled. Those
  records now carry flag `5` and the 2011 swing reads 4.8 rather than 2.0. The 2012
  change itself is unaffected and still unexplained.
  So whatever happened in 2012 did not happen to all three plates equally, and the
  per-calendar-month gains do not repair it. Notebook `11` already reports the
  symptom from the other side: its gain hold-out, fitted on odd years and scored on
  even ones, misses by up to 69 % inside a single setup, which is what a gain
  contaminated by climatology rather than describing an instrument looks like.
  Until this is understood, treat the amplitude of `G` as not comparable across
  2011/2012 in either the measured or the reconciled columns, and do not read a
  trend through it. Three things to try: whether plate 3 escaping the change
  identifies what changed, since it is the plate discarded in 2021 and the only one
  excluded from the reconciled column; whether the fieldbook's 2012-04-25 program
  "with corrected multipliers and offset" names channels anywhere; and whether the
  amplitude loss is a gain change or a loss of coupling, which the plates' response
  to a rain event or to a clear-sky day would separate. Section 3.2.
- **What is `LW_*_COR_T1_47_1` in `ch-lae_processed`?** A longwave correction from
  earlier work that neither `06` nor `13` uses. `13` established only that the raw
  field is already fed from the logger's temperature-corrected channel; what the
  separately stored series adds is still unknown.
- **The 24-day CNR4 window, 14 Dec 2021 - 7 Jan 2022.** The radiometer was exchanged
  on 14 December and its constants reached the logger program on 7 January, so the
  conversion in force between those dates is not established. It now touches four
  products (`01`, `06`, `12`, `13`), all of which flag the interval rather than
  correcting it. `12` tests it against MeteoSwiss and finds the levels **not**
  consistent with the old constant still being applied, which bounds the error but
  does not identify the constant. A correction has to be applied to all four channels
  together. `docs/Instrumentation.md`.
- **What moved `LW_OUT` at the December 2021 exchange?** `13` measures a step in the
  annual means at the CNR1 to CNR4 change and flags it rather than correcting it,
  because nothing measured through the change. Whether it is the instrument or the
  conversion cannot be separated with what is on site.
- **Does the tower barometer or Lägern drift?** After the January 2016 step, the
  departure of tower `PA` from the barometric formula against Lägern grows from
  +0.017 kPa in 2016 to -0.061 kPa in 2025 and -0.074 kPa in January to September
  2026. The formula is computed from Lägern's own pressure, so `05` cannot say
  which side moves, and after 2018 there is no NABEL barometer to separate them.
  The product is exported as measured. Section 3.1.
- **Which CNR1 was on the tower?** `docs/Instrumentation.md` and `06` give SN 020484,
  which is also what the logger program comments say, but the fieldbook row recording
  the 14 December 2021 exchange names CNR1_020522 at a different location. Probably a
  GIN bookkeeping artefact, unreconciled.
- **Sonic orientation from `2005_2`**: note 5 records a possible change from
  209° to 206° and asks for verification. Unresolved, and it falls in the
  `IRGA75` era. `workflow/00_L0_CHECKS/CLAUDE.md`.
- ~~**Shifted raw-file timestamps, July 2013.**~~ Handled for FP2026.2 in
  `30_.../IRGA75/00`, which moves the flux records back by 7 h (`docs/Yearly_Notes.md`).
  The raw files still carry the wrong names: a new Level-1 run from renamed files
  would need that shift removed from `00`.
- ~~**Is `H` in the dataset?**~~ Yes: `35_FPPC` in both chains. Section 4.1.
