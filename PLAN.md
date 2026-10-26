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
| `FP2026.1` | 2016 - Sep 2026 | `IRGA72` (LI-7200, enclosed path) | open |
| `FP2026.2` | 2004 - Sep 2026 | `IRGA75` (LI-7500, open path) + `IRGA72` | open |

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
`99_METEO_MERGED_2004-2026.09.ipynb` (at present `01` to `06` only) and documented on a page under
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
  and the `TA`, `RH` and `LW_IN` pages carry the numbers of that run.

`07` is extended: it exports `VPD_T1_47_1` from the measured `TA` and `RH` and
`VPD_T1_47_1_HOMOGENIZED` from their homogenised columns, and `99` merges both.

Not yet extended, still reading or writing the `*_2025` files: `08` to
`13`, `RADIATION_SENSOR_CONTINUITY`, `TA_HOMOGENIZATION_OPTIONS`, the
`90_DATASET_OVERVIEW` notebooks, and `build_meteo_dashboard.py` (whose paths
`build_calendar_explorer.py` imports).

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
| `NEE` | CO~2~ flux plus storage, u*-filtered, gap-filled | `01_FPPC`, run on 2016 - Sep 2026 |
| `LE` | turbulent latent heat flux, no storage, no u* filter, gap-filled | `11_FPPC`, run on 2016 - Sep 2026 |
| `H` | turbulent sensible heat flux from the sonic, no storage, no u* filter, gap-filled | `15_FPPC`, run on 2016 - Sep 2026 |
| `GPP`, `RECO` | Level-4.2 partitioning of gap-filled `NEE` | not part of this version (decided 26 Oct 2026) |
| `ET` | derived from gap-filled `LE` in `11_FPPC` | run on 2016 - Sep 2026 |

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
| Raw | binary → ASCII (bico) | done | done | stub |
| L0 | preliminary run, per setup period | done, 2004-2019 | done, **through Sep 2026** | written |
| L1 | final run, per setup period | done, 2004-2019 | done, **2016 - Sep 2026** (re-run, 18 runs) | stub |
| L1.1 | self-heating correction (open path only) | notebooks exist | n/a | written |
| L2 | quality flags from L1 output | in `30_` chain | in `30_` chain | stub |
| L3.1 | storage term added (`NEE` only) | in `30_` chain | in `30_` chain | stub |
| L3.2 | outlier detection, u* threshold detection | done, 2005-2019 | done, 2016-2024 | stub |
| L3.3 | flags from three constant u* thresholds | `NEE` | `NEE` | written |
| L4.1 | gap-filling (long-term random forest) | open | `NEE`, `LE` | stub |
| L4.2 | partitioning into `GPP` / `RECO` | open | open | stub |
| QCF | overall quality flag | — | — | stub |

Every chain stage after Level 1 stops at **2024** for `IRGA72`. Section 5
describes the work that carries it to September 2026. Level 1 was re-run over the
whole 2016 - Sep 2026 record rather than extended, so every stage below it reads a
new input.

### 4.3 Auxiliary flux-derived series to decide on

Storage terms (`SC`, `SLE`, `SH`), friction velocity `USTAR`, the u* threshold
actually applied, the per-level quality flags and `QCF`, and the sonic wind
series. These exist in the processing output; the decision is which of them the
published file carries and under which names. `docs/Variables.md` is the page
that will state it.


## 5. Where to continue

In order. Each item is blocked by the one above it, except that the flux items
2 to 4 do not depend on the meteo item 1: their biomet input,
`EDDYPRO_BIOMET_CH-LAE_2004-2026.09.csv`, is written.

1. **Extend the rest of the meteo stage**: `08` to `13`,
   `RADIATION_SENSOR_CONTINUITY`, `TA_HOMOGENIZATION_OPTIONS`, the
   `90_DATASET_OVERVIEW` notebooks and `build_meteo_dashboard.py`; then the
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
   fills the rest of the gap; `15_FPPC` would then need that run in its input.
3. ~~**Carry `20_MERGE_DATA/IRGA72` to September 2026.**~~ Done 25 Oct 2026.
   `22.1_FLUXES_IRGA72_L1_2016-2026.09` merges the Level-1 runs; where two runs
   overlap at a year boundary it takes each record whole from one run, split at
   midnight, because the runs' values differ there.
   `22.3_FLUXES_L1_IRGA72_and_METEO_2016-2026.09` joins it with every column of
   `99` from 1 January 2016 00:15 (the flux columns are empty until 11 January)
   and must be re-run whenever `99` changes. The
   Level-0 merge (`00_L0_checks/IRGA72/01`) still joins its overlapping runs cell
   by cell with `combine_first`; Level 0 is preliminary, so this matters only
   where a Level-0 value is quoted.
4. **Review the `34_` flux chain and the fullset.** `01_FPPC` (`NEE`, with the
   Pastorello uncertainty), `11_FPPC` (`LE` and `ET`) and `15_FPPC` (`H`) ran on
   2016 - Sep 2026 (26 Oct 2026), all reading
   `22.3_FLUXES_L1_IRGA72_and_METEO_2016-2026.09` with the homogenised `TA` and
   `VPD` as drivers; `NEE` uses the fixed 2016-2024 u* thresholds, kept on purpose
   although the FLUXNET thresholds for CH-Lae are much higher (decided 26 Oct 2026).
   Each writes only the columns it adds, and `99_FPPC_IRGA72_MERGED_2016-2026.09` in
   the same folder merges these (158 columns). `80_FINALIZE/10_FLUXES_and_METEO_2004-2026.09`
   collects the meteo of `99`, the `IRGA72` Level-1 fluxes of `22.1` and that file
   into one file from 2004 (506 columns); release datasets are cut from it by
   period. The meteo reaches it only through `99`, so products `08` to `13` join once
   they are extended and merged there; the `IRGA75` fluxes are not in it yet. Still
   to check: `H` in 2024
   is about a third lower than in the other years.
   Level-4.2 partitioning is not part of this version of the dataset (decided
   26 Oct 2026); `01_FPPC` keeps `RUN_PARTITIONING = False`.
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
7. **Fill the stub pages**: `L1`, `L2`, `L3.1`, `L3.2`, `L4.1`, `L4.2`, `QCF`,
   `Raw_Data`, and `Overview`, `Variables`, `Versions`, `Software`,
   `Management_Data`, `Supplementary`, `Links`.


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
  `IRGA75` era. `workflow/00_L0_checks/CLAUDE.md`.
- **Shifted raw-file timestamps, July 2013.** The raw files still carry wrong
  names; the fix is applied by renaming after the bico conversion, and has to be
  applied again on any re-run. `docs/Yearly_Notes.md`.
- **Is `H` in the dataset?** `docs/index.md` says it is; nothing computes it.
  Section 4.1.
