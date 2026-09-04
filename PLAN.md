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
| `FP2026.1` | 2016-2025 | `IRGA72` (LI-7200, enclosed path) | open |
| `FP2026.2` | 2004-2025 | `IRGA75` (LI-7500, open path) + `IRGA72` | open |

`FP2026.2` supersedes `FP2026.1` and re-includes it in full. The two releases
differ in the flux record only; the meteorological product is built once over
2004-2025 and serves both.


## 2. Record boundaries

These are the periods the dataset can cover, and the reason each one starts and
stops. They bound every table below.

| record | period | note |
|---|---|---|
| `IRGA75` fluxes | 2004 - 12 Dec 2017, plus 17 Jan - 20 Mar 2019 | analyser removed Dec 2017; the 2019 window is the stand-in run `2019_3` |
| `IRGA72` fluxes | 11 Jan 2016 - 2025 | two physical LI-7200 units, exchanged inside the 2019 gap |
| tower meteorology, 47 m | 2004 - 2025 | `PA` and `LW_IN` start Sep 2005 with the CNR1 and the pressure sensor |
| soil profile FF1 | 2004 - 2025 | sensors replaced as a set on 19 Mar 2020, no overlap across the change |
| radiometer | CNR1 Sep 2005 - Dec 2021, CNR4 from 14 Dec 2021 | logger constants updated 7 Jan 2022, 24 days later |

Setup periods, their notes and the unusable windows are in `docs/Yearly_Notes.md`
and are not repeated here.


## 3. Meteorological variables

### 3.1 In the dataset

One product notebook per variable in `workflow/10_METEO/30_PRODUCTS/`, joined by
`99_METEO_MERGED_2004-2025.ipynb` and documented on a page under
`docs/Meteo_Data.md`.

| variable | series | period | notebook | page | state |
|---|---|---|---|---|---|
| `SW_IN` | incoming shortwave, 47 m | 2004-2025 | `01` | yes | done |
| `TA` | air temperature, 47 m | 2004-2025 | `02` | yes | done |
| `PPFD_IN` | photosynthetic photon flux density, 47 m | 2004-2025 | `03` | yes | done |
| `RH` | relative humidity, 47 m | 2004-2025 | `04` | yes | done |
| `PA` | air pressure, 47 m | 2005-2025 | `05` | yes | done |
| `LW_IN` | incoming longwave, 47 m | 2005-2025 | `06` | yes | done |
| `VPD` | vapour pressure deficit, 47 m | 2004-2025 | `07` | yes | done |
| `PREC` | precipitation | 2004-2025 | `08` | yes | done |
| `SWC` | soil water content, 5 depths | 2004-2025 | `09` | yes | done |
| `TS` | soil temperature, 7 depths | 2004-2025 | `10` | yes | done |
| `G` | soil heat flux, forest floor, 3 plates | 2004-2025 | `11` | yes | done |
| `SW_OUT` | outgoing (reflected) shortwave, 47 m | 2005-2025 | `12` | yes | done |
| `LW_OUT` | outgoing (emitted) longwave, 47 m | 2005-2025 | `13` | yes | done |

Six of these are re-formatted for EddyPro by
`40_EXPORTS/EDDYPRO_BIOMET_CH-LAE_2004-2025.ipynb` (`TA`, `RH`, `PA`, `SW_IN`,
`LW_IN`, `PPFD_IN`) and are the biomet input to the final flux runs.

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
| `NEE` | CO~2~ flux plus storage, u*-filtered, gap-filled | open, chain exists |
| `LE` | latent heat flux plus storage, gap-filled | open, chain exists |
| `H` | sensible heat flux | **no chain notebook exists** |
| `GPP`, `RECO` | Level-4.2 partitioning of gap-filled `NEE` | **no notebook exists** |
| `ET` | derived from `LE` | not started; decide whether to publish |

`H` and the partitioned fluxes are the two real gaps in the flux side. `H` is
described in `docs/index.md` as part of the dataset and Level-4.2 is in the
processing-chain flowchart, but neither has a notebook.

### 4.2 Chain status

Levels as defined in `docs/FPC.qmd`.

| level | what it does | `IRGA75` | `IRGA72` | site page |
|---|---|---|---|---|
| Raw | binary → ASCII (bico) | done | done | stub |
| L0 | preliminary run, per setup period | done, 2004-2019 | done, **through 2025** | written |
| L1 | final run, per setup period | done, 2004-2019 | done through 2024, **being re-run 2016-2025** | stub |
| L1.1 | self-heating correction (open path only) | notebooks exist | n/a | written |
| L2 | quality flags from L1 output | in `30_` chain | in `30_` chain | stub |
| L3.1 | storage term added | in `30_` chain | in `30_` chain | stub |
| L3.2 | outlier detection, u* threshold detection | done, 2005-2019 | done, 2016-2024 | stub |
| L3.3 | flags from three constant u* thresholds | `NEE` | `NEE`, `LE` | written |
| L4.1 | gap-filling (long-term random forest) | open | `NEE`, `LE` | stub |
| L4.2 | partitioning into `GPP` / `RECO` | open | open | stub |
| QCF | overall quality flag | — | — | stub |

Every chain stage stops at **2024** for `IRGA72`. Section 5 describes the work
that carries it to 2025; Level 1 is being re-run over the whole 2016-2025 record
rather than extended, so every stage below it reads a new input.

### 4.3 Auxiliary flux-derived series to decide on

Storage terms (`SC`, `SLE`, `SH`), friction velocity `USTAR`, the u* threshold
actually applied, the per-level quality flags and `QCF`, and the sonic wind
series. These exist in the processing output; the decision is which of them the
published file carries and under which names. `docs/Variables.md` is the page
that will state it.


## 5. Where to continue

In order. Each item is blocked by the one above it.

1. **Final fluxes for `IRGA72`, 2016-2025.** A complete re-run of Level 1 over
   the whole `IRGA72` record rather than an extension of the 2016-2024 set, so
   the released fluxes come from one EddyPro configuration end to end. One run
   per setup period, using each period's own time-lag window from
   `00_L0_checks/IRGA72/05_IRGA72-L0_check_timelags_2016-2025.ipynb` and the
   biomet file `EDDYPRO_BIOMET_CH-LAE_2004-2025.csv`. Output into
   `0_data/IRGA72-Level-1_fluxnet_2016-2025/`. The biomet file is ready and has
   been checked against the 2016-2024 runs: same timestamp convention, no
   discontinuity. Three points to settle before starting: whether the wrong
   calibration gas of note 15 is corrected inside the run (factor 0.974 on the
   CO2 concentration, 14 Dec 2017 - 15 Mar 2019 — it cannot be applied to a
   finished flux); whether `2019_2` gets a sonic-only run for `H`, as `2018_3`
   did; and that `2022_2`, `2022_3` and `2022_4` stay separate runs, their lag
   windows being far apart (notes 7, 12).
2. **Carry `20_MERGE_DATA/IRGA72` to 2025** — notebooks `22.1` and `22.3`, both
   currently named `2016-2024`.
3. **Carry the `30_FLUX_PROCESSING_CHAIN` stages to 2025** — `32_` u* detection,
   `34_` L3.3 and L4.1 for `NEE` and `LE`. Note that stage `34_IRGA72_2016-2024`
   holds notebooks whose filenames say `IRGA75`; check which instrument they
   actually process before extending them.
4. ~~**Add `SW_OUT`, `LW_OUT` and `G`.**~~ Done, September 2026: notebooks `11`,
   `12` and `13`, registered in `99` and documented under `docs/Meteo_Data.md`.
   Two follow-ups they leave behind. The **24-day CNR4 window** now affects four
   radiation products rather than two, and a correction there has to be applied to
   all four at once (section 6). And `docs/Instrumentation.md` needs its heat flux
   plate row corrected: it describes one plate where the site had three.
5. **Decide the candidate list in 3.3**, then freeze the variable inventory and
   write `docs/Variables.md`.
6. **Close the flux gaps** — `H` through the chain, and Level-4.2 partitioning.
7. **Fill the stub pages** — `L1`, `L2`, `L3.1`, `L3.2`, `L4.1`, `L4.2`, `QCF`,
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
  between adjacent years, 4.7 in 2011, 5.7 in 2012, 3.4 in 2013, 5.5 in 2014, which
  no soil does. Part of what this entry originally described in 2011 was a separate
  fault, since found and flagged: plate 2 read with its sign reversed from June to
  December 2011, and the reconciled column averaged it with plate 1 and nearly
  cancelled. Those records now carry flag `5` and the 2011 swing reads 4.7 rather
  than 2.0. The 2012 change itself is unaffected and still unexplained.
  So whatever happened in 2012 did not happen to all three plates equally, and the
  per-calendar-month gains do not repair it. Notebook `11` already reports the
  symptom from the other side: its gain hold-out, fitted on odd years and scored on
  even ones, misses by up to 109 % inside a single setup, which is what a gain
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
