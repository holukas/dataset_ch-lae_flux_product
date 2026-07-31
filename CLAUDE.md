# CLAUDE.md

## What this repo is

Methods documentation for the **CH-LAE flux product** — an eddy-covariance
ecosystem-flux dataset for the mixed forest site CH-LAE. The actual flux
computation and meteo screening happen in a separate offline pipeline; this
repo's job is to **narrate the methods** used to produce the shared dataset and
publish them as a website.

## Layout

- `docs/` — the published Quarto website. Curated narrative pages (`*.md`, plus
  `FPC.qmd`), `images/`, the site mark (`logo.png`/`.svg` for the sidebar,
  `favicon.ico`/`.svg`/`.png` for the tab icon — the same artwork, so the two
  must be regenerated together), `references.bib`, `styles.css`, and
  `_quarto.yml` (single config). This is the reader-facing artifact and is kept
  clean. Only pages listed in `_quarto.yml`'s `website.sidebar.contents` are in
  the nav. Build output lands in `docs/_build/html/` (gitignored).
- `workflow/` — the real working notebooks and scripts, organized by stage:
  `00_L0_checks/`, `10_METEO/`, `20_MERGE_DATA/`, `30_FLUX_PROCESSING_CHAIN/`,
  `90_DATASET_OVERVIEW/`. This is research scratch space and is **not** built
  into the book. Two reserved folders: `_archive/` (dead/experimental, mirrors the
  stage layout) and `_templates/` (reusable notebook templates).

## Code/data layout and conventions

Code lives in this repo under `workflow/`. The **data files it produces live in a
separate, untracked folder** (not in git — too heavy):
`F:\Sync\luhk_work\dev-data\datasets-data\dataset_ch-lae_flux_product-data\workflow\`.

The two `workflow/` trees are **kept mirrored 1:1** — same stage folders, same
`IRGA72/`/`IRGA75/` instrument subfolders.

- **Numbering:** a data file carries the **same numeric prefix and relative path
  as the notebook/script that produces it**. Code vs data is told apart by which
  tree it is in, not by the number. (There is no odd/even offset.)
- **Instruments:** where a stage processes both sensors, split into `IRGA72/` and
  `IRGA75/` subfolders on both sides.
- **Filenames:** no spaces, no `+` (use `_and_`).
- **Figures stay in the repo** (`docs/images/` for published figures, a
  `figures/` subfolder under the relevant `workflow/` stage for working plots);
  only heavy data (`*.parquet`/`*.csv`/`*.pkl`) goes to the external data folder.
- Raw inputs (`0_data/`) and `tests/` outputs live only in the external data
  folder and are gitignored.
- **Stage 30 (`30_FLUX_PROCESSING_CHAIN/`) is intentionally left on its older
  internal numbering** on both sides; don't reorganize it without being asked.

## Stage 00 (`00_L0_checks`) and the EC setup

Level 0 is the preliminary flux calculation. EddyPro is run **per setup period**,
so this stage merges the per-run *FLUXNET* output files into one 30MIN record per
gas analyser (`01`/`11`) and then checks that record — fluxes, wind direction,
time lags — before anything downstream reads it. The merge notebook computes and
corrects nothing beyond dropping columns that do not belong; the check notebooks
export nothing.

`docs/Yearly_Notes.md` is the authority for the setup. Its `## Setup EC` table
lists every setup period with its raw-binary range, sonic, gas analysers, sensor
separations and the BICO/flux-run configuration. Read it there rather than
quoting from memory; the points below are the ones that keep costing time.

**The table's numbered notes are the important part and their legend is not in
this repo.** `(1)`-`(24)` are defined on the SwissFluxNet page linked at the top
of `Yearly_Notes.md`
(`swissfluxnet.ethz.ch/index.php/sites/site-info-ch-lae/ec-raw-binary-format-ch-lae/`).
They carry the corrections, the unusable periods and the time-lag settings — a
setup period read without its note looks clean when it is not. The BICO and `FR`
letters have no published legend on either page.

- **`IRGA72` and `IRGA75` name the analyser, not a period.** `IRGA75` is the
  open-path LI-7500, `IRGA72` the closed-path LI-7200. The LI-7500 runs from
  2004; the LI-7200 was added on **11 January 2016** (`2016_2`, first binary
  `2016011115.b05`, and the merged L0 record does start 2016-01-11 15:15). Both
  were calculated in parallel through `2017_1`. The LI-7500 was **removed from
  the site on 12 December 2017** (note 9) but kept logging empty values in the
  data stream until it was taken out of it on **31 January 2018** (notes 10, 11),
  which is why `2017_2` and `2018_1` list it in parentheses with no flux run.
  Each analyser has its own `0_data/` source folder, its own subfolder under
  every stage, and its own merged L0 file.
- **A gap in one analyser's run sequence is often a run in the other's — but not
  always, and the largest gaps have more than one cause.** The two longest holes
  in the merged IRGA72 record are both fully explained by the notes:
  - **69 days, 2019-01-10 15:15 → 2019-03-20 18:45.** Two causes end to end. The
    LI-7200 was replaced on 11 January 2019 and *both* units were defective, so
    `2019_2` yields mostly incomplete files and unusable fluxes (note 17); then
    the LI-7500 was brought back to stand in for it for `2019_3`, 17 January -
    20 March (note 16). `2019_3` is therefore in the IRGA75 source folder, which
    is what the `+2019` in `OPENLAG-IRGA75-Level-0_fluxnet_2005-2016+2019` means.
    A `2019_2` file exists here and yields **no** `FC` and **no** `LE` at all;
    its presence is not evidence that the period has data. It does yield 289
    half-hours of `H`, because `H` comes from the sonic and only the gas analyser
    was defective — so a coverage check run on `H` alone would miss this entirely.
    Judge a gas-analyser fault on a gas flux.
  - **56 days, 2021-12-13 19:15 → 2022-02-07 10:45.** `2021_2` and `2022_1` have
    no source file at all: the raw data was logged in an unknown format and the
    conversion fails on an unrecognised 44-byte IRGA record, so it may be
    corrupted (note 22). This gap cannot be filled from the other analyser.
- **`IRGA72` spans two physical analysers.** IRGA72-B (as `IRGA72-B-GN1` from
  `2017_2`) through `2019_2`, then IRGA72-A from `2019_4`, whose stream has 13
  columns — `diag_val` and `signal_strength` added, `status_byte` gone (note 14).
  The swap sits inside the 69-day gap above. Same trap as the meteo field names:
  one name, two instruments.
- **The analyser also moved on the boom.** Its separation from the sonic changes
  at `2023_2` from `N+6 E-1 V-15` to `N+11 E+1 V-1`, tube length and delay
  unchanged; the inlet was repositioned and `2023031319.L00` is the first
  complete file in the new position (note 23). A separation change moves time
  lags, which is exactly what `05_…check_timelags` looks at.
- **Time lags are not comparable across setup periods, and the notes say why.**
  An artificial lag of 12 s was introduced by buffer processing in `2019_2` and
  has to be allowed for in lag detection (note 13); `2022_2` carries no
  artificial lag and its detected lag falls in the expected range, ~1.25 s for
  CO2 (note 12); the lag then shifts again in `2022_3` (back to 8.5 s) and
  `2022_4` (lower still), and those two periods need to be calculated separately
  (note 7). A lag-detection notebook that pools setup periods is comparing
  different acquisition settings.
- **The sonic is HS50-B at 47 m, orientation `209°`, unchanged through the
  record — with one open question.** Note 5 records that the orientation may have
  changed to `206°` from `2005_2` onward and says recalculations should verify
  it; it is unresolved, and it is in the LI-7500 era. The `209°` itself was
  confirmed independently from wind-direction histograms across years; an old
  `locations.table` gives `183°` to `209°` and is not trusted.
- **The per-year sections below that table are partly unedited stubs.** The
  2021-2025 blocks say `Instruments: R350, IRGA75` and link to the **Chamau**
  setup page, contradicting the table's HS50-B and IRGA72-A. The table wins; do
  not take instrument names from those blocks.
- **The run label is the setup period, not a part of the year.** `2016_2+3` is
  one EddyPro run covering setup periods 2 and 3 of 2016, so a run boundary is a
  hardware or configuration change and runs do not map onto calendar years. Merge
  on the timestamps inside the files, never on the file names.
- **The EC output carries no meteo.** The 2025 IRGA72 run exported its biomet
  inputs (`TA_1_1_1`, `RH_1_1_1`, `PA_1_1_1`, `SW_IN_1_1_1`, `LW_IN_1_1_1`,
  `PPFD_IN_1_1_1`) into the FLUXNET file by mistake; no other run has them. The
  merge notebook drops them so the merged record keeps one column set over its
  whole length; meteo comes from the `10_METEO` products. The drop is guarded by
  reading the source **headers** and asserting that exactly one run carries the
  columns. A first version guarded on the year instead and failed: a run begins
  at the last binary of the previous December (`2025_1` starts
  `2024123119.L00`), so its records reach back into 31 December of the year
  before, and any per-year threshold is off by a day at every run boundary.
- **Periods that are present in the record and should not be used as measured:**
  - **The wrong calibration gas (note 15)** affects **all IRGA72 CO2
    concentrations between 14 December 2017 and 15 March 2019** — not just the
    end of 2017, which is what `Yearly_Notes.md` alone suggests. The correction
    is a factor **0.974 applied to the CO2 concentration before the fluxes are
    calculated**, so it cannot be applied to a finished flux product. The
    LI-7500 fluxes of `2019_3` are unaffected (note 16), and the correct gas is
    in use from `2019_4` (note 18).
  - **May/June 2018 (note 19):** the LI-7200 flow module failed, which also
    prevented lag detection until the module was replaced on 7 June 2018. Do not
    use CO2 fluxes 19 May - 6 Jun 2018 or water fluxes 13 May - 6 Jun 2018.
  - **The 2016 commissioning (notes 20, 21):** `2016_2` splits into an
    installation phase and a low-flowrate phase, both to be avoided (water in the
    filter suppressed the CO2 and H2O fluxes), with an acceptable initialisation
    phase between them. Quality is good from `2016_3` on.
- **July 2013 (LI-7500 era):** the timestamp in the raw binary *file names* is
  wrong between `2013070615.b02` and `2013071214.b00` by about 6 hours (note 8;
  the MOXA clock was corrected on 12 July 2013). The raw files still carry the
  wrong names; the fix is to rename after the bico conversion. Uncorrected, it
  reached the FP2021 fluxes as a ~14.5 h shift between 2013-07-06 15:45 and
  2013-07-12 23:45.

## Stage 10 (`10_METEO`) conventions

The stage is split into three substages, numbered by decade in dependency order.
`x-`-prefixed notebooks are retired and no longer run (they still render, so keep
them valid); they stay at the stage root, outside the three substages, so they
are not mistaken for current work.

**Number only where order matters, and scope the number to its folder.** Notebook
numbers restart at `01` inside each substage — they are not unique stage-wide, and
a cross-folder reference must name the folder (`30_PRODUCTS/01`). This keeps file
numbering and substage numbering in separate spaces, so a growing substage can
never collide with the next decade. A substage whose notebooks have no dependency
order (`10_REFERENCE/`, `20_SCREENING/`) carries **no** numbers at all: numbering
independent notebooks asserts an order that does not exist and leaves no
principled answer to "what number is the new one?".

- **`10_REFERENCE/`** — external reference data, one notebook per station (or,
  for `REGIONAL`, per station *ensemble*). These
  download from a provider (currently MeteoSwiss, via the open-data STAC API) and
  write **files**; nothing here goes into the database. Outputs land flat in
  `10_REFERENCE/` on the data side, named
  `[<VAR>_]<provider>_<station>_<resolution>_<years>` — the leading `<VAR>_` only
  when the product holds a single variable (`PREC_MeteoSwiss_OED_30MIN_2014-2025`
  vs. the multi-variable `MeteoSwiss_LAE_30MIN_2004-2025`). Reference columns are
  suffixed `_<station>_MS` so they cannot be confused with tower columns.
  Because references are addressed by *path* rather than by database name, moving
  one breaks every reader — keep the filenames stable. A reference notebook may
  write more than one product when the source record itself is split (the OED
  precipitation record is daily to 2014 and 30MIN after), which is the one
  sanctioned exception to one-notebook-one-product in this stage.
  - **The stations are not interchangeable.** `LAE` (Lägern, 2.5 km, 845 m) is
    the full weather station and covers `TA`/`RH`/`PA`/`SW_IN` plus dew point,
    vapour pressure, sunshine and wind over 2004-2025 — but measures **no
    precipitation and no longwave**. `OED` (Ehrendingen, 3.8 km, 428 m) is
    precipitation-only. So `06` (`LW_IN`) has no MeteoSwiss reference at all.
  - **One reference finds a break; an ensemble says who moved.** A single nearby
    station can date a change at the tower, but when the two disagree it cannot
    say which of them stepped. `MeteoSwiss_REGIONAL_PREC` therefore fetches
    *every* MeteoSwiss precipitation station within 21 km that covers the whole
    period (daily; it raises below `MIN_STATIONS`), which is what makes the 2018
    acquisition break in `30_PRODUCTS/08` attributable to the tower — and, since
    the stations span elevations, gives an elevation-precipitation gradient as a
    by-product. Its station table is written alongside as a second csv: metadata
    for the product, not a second product.
  - **MeteoSwiss precipitation days run 06 UTC → 06 UTC.** Daily precipitation
    products are left on that native day and are **not** shifted to local time;
    anything compared against them must be re-aggregated onto the same 06-UTC day
    first (`30_PRODUCTS/08` has a `to_ms_precip_day()` helper). A local-midnight
    daily sum is wrong by six hours and smears every event across two days.
  - **Year labels come from the last bin's start, not its label.** 10-min values
    are end-of-interval, so the final bin of 31 Dec is labelled 00:00 on 1 Jan,
    and the local-time shift pushes it again. Both traps silently misname the
    export `..._2004-2026`.
- **`20_SCREENING/`** — quality screening of the site's own measurements, one
  subfolder per variable (`SW_IN/`, `TA/`, `RH/`, `PA/`, `PPFD_IN/`, `LW_IN/`,
  `PREC/`, `NETRAD/`, `SWC/`), one notebook per sensor and era. These read the
  **raw high-resolution** record from InfluxDB, screen and correct it there,
  resample to 30MIN, and write back to **InfluxDB** as `meteoscreening_diive` —
  not to files, so the substage produces almost no data files. Some read a
  product from `10_REFERENCE/` — that is the edge that puts reference before
  screening. `DatabaseInfluxStepwiseMeteoScreening.ipynb` at the substage root is
  the vendored diive template every variable notebook is derived from; the header
  of each notebook records which template version it came from.
  - **Screening is stepwise and committed by hand.** Run a test, look at its
    preview plot, then commit it with `mscr.addflag()`; re-run with other
    parameters as often as you like before committing. Run only the tests the
    variable actually needs and say in the notebook why the others are off.
    `finalize_outlier_detection()` aggregates the committed flags into `QCF`.
  - **The raw record can carry more than one time resolution** (SWC: 10MIN before
    the March 2021 logger rebuild, 1MIN after). diive drops resolution groups
    holding <0.2 % of records and **upsamples the coarser era onto the finest
    grid**, so the early era arrives as runs of identical values. Any test built
    on *differences* degenerates there — the rolling MAD of a mostly-constant
    series is `0` and the detection band collapses. Always check a test's
    flagged count **per era**, never on the total, and write windows as
    `60 * 24 * …` so they mean the same wall-clock span in both eras.
  - **A failed sensor read can be a number, not a gap.** The CR1000 firmware
    predates SDI-12 NaN support, so a failed SDI-12 read lands in the record as
    that sensor's calibration polynomial at zero response — a fixed negative
    value per sensor. `notna()` does not mean "measured": absolute limits, not
    the missing-values flag, is what catches these. Never *clip* to the physical
    minimum, which would turn a failed read into a fabricated 0.
  - **A variable with no external reference gets an internal one.** No weather
    service measures this plot's soil, so the SWC notebooks cross-check each
    depth against the other four depths of the same profile plus the screened
    precipitation product. That separates the loud failure (stops reporting) from
    the quiet one (stops being *coupled* — smooth, in-range, plausible values
    that no outlier test can see). The diagnostic is the response, not the value:
    rolling 30-day correlation of daily increments against the profile mean, and
    the rise after every >10 mm rain day. Depths are **not** replicates, so only
    the ordering is physically enforced (shallow wets first); the section
    produces *candidates*, never removals.
  - **The cross-check is repeated after screening** and must not get worse:
    if agreement with the reference drops, a test removed real signal, and the
    notebook says so loudly rather than leaving it to be noticed.
  - **Audit in proportion to what was removed.** On top of that re-check, two
    hard invariants are **asserted everywhere**: that every record counted as
    out-of-range really is outside the physical limits, and that none survived
    screening. The **full two-direction audit** — *is everything removed
    genuinely bad* (nothing left without a committed test asking; no isolated bad
    minute emptied the 30MIN mean that held it) and *is everything real still
    there* (every rain response preserved, agreement unchanged) — is reserved for
    a notebook whose `REMOVE_DATES` is **not empty**. A hand-drawn window is the
    only thing in these notebooks that deletes data on a person's say-so, so it
    is the thing that needs policing: at `SWC` 0.05 m the audit re-derives the
    window's own response ratio and rolling agreement against the record medians
    on every run, and fails it if they stop standing out — the justification is
    recomputed, not quoted from the prose beside it. Two cautions. A response is
    measured two days past its event, so an event on a window's trailing edge
    reports the *recovery* that ended the fault; judge on the median ratio, not
    the maximum rise. And where one field name spans two sensors (`SWC` 0.3 m),
    the audit must be **era-split** or it correlates increments from different
    probes across the dead period and reports nonsense.
  - **One sanctioned file output.** `SWC/SWC_FF1_PROFILE_2020-2025.ipynb`
    downloads the five raw profile depths **once** into a parquet the five
    per-depth notebooks read as their cross-check reference, instead of each of
    them pulling the same 2.5 M records. It is raw, values-only and carries **no
    database tags** — so it can never stand in for a screening notebook's own
    download, which needs the tags that travel through screening onto the upload.
    Each depth still downloads its own target live. Re-run it before the depth
    notebooks whenever the raw record grows or is re-ingested; the readers assert
    it covers their period so a stale file fails loudly.
  - **Copies of a notebook must re-derive their own evidence.** The per-depth SWC
    notebooks are copies of the 0.05 m one with `DEPTH` changed — but
    `REMOVE_DATES` belongs to a sensor, not to a variable, and carrying windows
    across depths would delete good data. Same rule as the shared 2012 windows
    below.
- **`30_PRODUCTS/`** — one notebook **per meteo variable**, numbered in the order
  they may depend on each other: `01` `SW_IN`, `02` `TA`, `03` `PPFD_IN`,
  `04` `RH`, `05` `PA`, `06` `LW_IN`, `07` `VPD`, `08` `PREC`, `09` `SWC`. The
  order is real,
  not decorative — `02` and `03` read `01`, and `07` reads `01`/`02`/`04`. Each
  downloads the screened series from the database, corrects it, and writes a
  single product to the external data folder. The notebook name is a prefix of
  the file it writes (`02_METEO_TA_2004-2025.ipynb` →
  `02_METEO_TA_GAPFILLED_2004-2025.parquet`), so code and data line up by eye.
  No verb in the notebook name — the folder already says what these do.
  An **unnumbered `<VAR>_<PURPOSE>.ipynb`** beside the numbered ones is an
  investigation that exports nothing and answers one question
  (`TA_HOMOGENIZATION_OPTIONS`, `TS_FF1_GAPFILL_ML_COMPARISON`). Use one when a
  product decision needs evidence: it reads the finished product rather than
  rebuilding it, scores the candidates on one table, and records what adopting
  the winner would require. **A rejection recorded in prose is a hypothesis, not
  a result** — three objections that had a two-sided `TA` correction rejected were
  written down as settled, and when finally measured none of them held.
  Where the question spans several variables the prefix is the **group**, not one
  `<VAR>`: `RADIATION_SENSOR_CONTINUITY.ipynb` attributes every level change in
  the site's radiation record and necessarily reads `SW_IN`, `PPFD_IN` and both
  references at once, because the attribution *is* the comparison between them.
  Same precedent as `09` covering five `SWC` depths — a depth, like a radiation
  sensor here, is only interpretable next to its neighbours. Such a notebook still
  exports nothing, and the product notebooks carry the conclusions plus their own
  guarding assertions rather than deferring to it.
  `99_METEO_MERGED_2004-2025.ipynb` is the capstone: it runs last, joins the
  products of `01`-`10` onto one 30MIN `TIMESTAMP_MID` index with their
  provenance flags, and draws one overview figure per series. It **computes and
  corrects nothing** — a value in the merged table is exactly what its own
  notebook exported. Its `PRODUCTS` registry is the one place a series is
  declared: the merge, the column check, the coverage table and the captions all
  read it, so adding a variable there is what makes it arrive everywhere. A
  multi-column product contributes **one entry per series a reader would
  analyse**, not one per column in its file — `09` five soil-moisture depths plus
  their homogenised twins, `10` the seven reconciled soil-temperature depths and
  **not** the eighteen individual channels, which are one sensor each and stay in
  their own notebook. Every entry needs its `MAY_HAVE_GAPS` reason if it can
  contain `NaN` and its `FLAG_LABELS` vocabulary for the flag drawn first.

### The GIN fieldbook

The site's maintenance record is exported from GIN and lives in the external data
folder **beside** `workflow/`, not inside it (it is an input to many stages, not
the output of one):
`...\dataset_ch-lae_flux_product-data\fieldbook_gin\CH-LAE-laegeren-export_<yyyymmdd>.csv`.
Columns: `Date` (`dd.mm.yyyy`), `Operation Tag`, `Event Tag`, `Location`,
`Device Model`, `Text`. The body is **HTML** — strip tags and unescape entities
before matching or printing.

- **It is also a personnel record — redact it before printing.** Its entries are
  signed with the names of the people who did the work, and these notebooks render
  to a public website. Every fieldbook string therefore passes through
  `redact_people()`, applied *inside* the notebook's own flattening helper
  (`plaintext()` / `bulk_plaintext()` / `strip_html()` / `_plaintext()`), so a
  print site added later is covered without anyone remembering it. The
  name → pseudonym map is `fieldbook_gin/redact_names.csv`, beside the export and
  **outside this repository**, so the repo never carries a real name; pseudonyms
  (`person 01`, `person 02`, …) are stable and append-only, so a re-run reproduces
  the same text. A missing map **raises** — carrying on with redaction quietly
  disabled prints real names and looks exactly like success.
  - **The map only knows the names it has already seen**, so
    `audit_unmapped_names()` catches the rest. After redaction, a token in one of
    the two shapes that actually carry names — the author parenthesis entries are
    signed with, and bylines like `with X` / `durch X` — that is neither an
    allowlisted technical term (`redact_allow.csv`) nor an all-caps device code
    raises. It never prints the candidates: an exception message is stored in a
    notebook like any other output, so the list goes to `redact_unmapped.txt`
    beside the map and only the count is shown. A third shape, any capitalised
    pair, was measured and **rejected** — 560 distinct tokens, nearly all sentence
    starters and device names, which would bury the signal.
  - **Names in prose and comments count too.** A worked example in a markdown cell
    or a code comment is exactly as published as a printed one, so use a pseudonym
    or an invented name (`Ada Lovelace`), never a real one. This was got wrong
    once already — in the comments explaining the redaction itself.
  - `python check_no_names.py` scans the repo for any mapped name and exits
    non-zero. Run it before publishing. `docs/index.md`'s acknowledgements are the
    one deliberate exception: published credit, skipped by the checker. A whole
    file is never skipped where a single **line** will do: an author byline
    (`**Author**`, `author:`, `page-footer:`) is exempt for the same reason a
    citation is, so a fieldbook quote pasted onto the same page is still checked.
- **`build_fieldbook_md.py` renders the whole export as one readable redacted
  markdown file** (`fieldbook_gin/CH-LAE_fieldbook_redacted_until_<year>.md`,
  beside the export, **never in this repo** — it is derived data, it stays a
  personnel record after redaction, and a markdown file under `docs/` is rendered
  onto the public website by Quarto whether or not the nav lists it. The script
  **refuses an `--out` path inside the repository** and `.gitignore` catches a
  hand copy; redaction makes the file shareable, not publishable).
  It flattens the HTML,
  drops the Word paste-in boilerplate, repairs the mojibake, splits the legacy
  block back out under its own dates, and removes what a notebook quoting three
  entries never had to: e-mail and IP addresses, account names, remote-access
  ports and paths through somebody's home directory. Rendering *everything*
  exposed shapes the quoting notebooks never touched, and each cost a bug:
  - **The `Namelist` column is a name list.** The map was built from entry bodies
    and knew a fraction of it; the whole-export scan added 53 surface forms and
    39 people. Surnames that only ever appear beside a mapped first name were the
    other half of the gap.
  - **Two nets, only one of which can raise.** The notebooks' two-shape net is
    kept as the raising check. The wide net — every capitalised token left
    standing, minus the export's own device vocabulary and minus anything seen
    lowercase — reports ~600 technical terms to a file and is what actually found
    the missing people. It cannot raise, for the reason the capitalised-pair shape
    was rejected above.
  - **Sanitise before redacting.** Redaction first turns an address into
    `person 07.person 07@x.ch`, which the e-mail rule then only half removes.
  - **A case-insensitive second pass is needed** (the record writes `eugenie` and
    `peter waldner` in lower case) and is dangerous: short mapped forms are
    ordinary words once lowercased. It runs on forms of five characters or more,
    minus `redact_ci_exclude.csv` beside the map — outside this repo, because
    naming the two German nouns concerned here would carry a real surname.
  - **A bare given name can be a physical constant.** `Stefan` was added and
    matched `Stefan-Boltzmann` — word boundaries do not see the hyphen. It was
    removed again; the full form covers the one occurrence in the record.
  - The extended map immediately found a real name in a stored notebook output,
    printed before the map knew it. Growing the map is how that is caught.
- **Read it in the notebook, don't quote it from memory.** Both `20_SCREENING/SWC`
  and `30_PRODUCTS/08` open the csv and filter it in a cell, so the adjudication
  written up next to a removal window can be re-run and challenged instead of
  taken on trust.
- **Never filter on the device tag alone.** The entries that explain a fault are
  routinely filed under something else: the two 2018 entries that document the
  precipitation acquisition change sit under the datalogger and the CNR1, and the
  entries behind the SWC gaps are power-supply and logger entries carrying no
  soil device at all. Filter on operation tag **or** location **or** free text
  (`soil|SWC|Teros|SDI|power|logger`, `rain gauge|rainbucket|…`).
- **The free-text net has to be cut for the era you are asking about, and some
  identities are not in the text at all.** A regex naming today's hardware finds
  nothing before it was installed — `Teros` and `SWC` return no pre-2020 hit; the
  older soil profile is `SoilM|MPS|decagon|multiplier`. And the sensor *type* of
  that profile (`EC-20`) appears **zero** times in the body: it lives only in the
  `Device Model`/`Device Name` columns, so a text-only filter misses the whole
  pre-2020 sensor identity. Search the device columns too.
- **The pre-2011 record exists, but inside a single row — a date filter cannot
  see it.** One row dated **`03.06.2011`** (`Event Tag = FBA`, operation and
  location both `na`) carries a **28,802-character** body beginning *"Additional
  old fieldbook entries 2006-2011"*. It is the legacy fieldbook pasted in when
  GIN was introduced, and it holds **94 dated sub-entries covering 2006-08-31 →
  2011-06-03**. Their dates live *in the text*; the row's own `Date` is 2011, so
  the `fb['date'].between(START, STOP)` filter every notebook uses **misses all
  of them** and reports silence where there is a record. Any notebook reaching
  before 2011 must parse this row specially and say so.
  - **Parsing it:** convert `<br>` and closing block tags to newlines *before*
    stripping tags, or the whole body collapses into one unreadable line.
    Sub-entries begin with a `dd.mm.yyyy` at line start, sometimes in wiki
    emphasis (`==01.03.2011 (person 01)==`). The text is mixed German and
    English — a soil filter needs `Waldboden|Bodenfeuchte|Boden` as well as
    `soil|moisture` — and carries mojibake (`Ã` for `Ü`/`Ö`).
  - **It pays for itself.** Two gaps that the data show at every depth of the old
    soil profile, and that were otherwise unexplained, are named here to the day:
    *"No forest floor logger data recorded from doy 69 to 162"* (2009) = the
    93-day gap 2009-03-10 → 06-11; and *"zwischen 6. Maerz und 28. Mai 2010 eine
    Sicherung herausgerutscht … der Logger ohne Strom"* = the 83-day gap
    2010-03-06 → 05-28. Both are **retro-added remarks** written a year later by
    someone other than the original author — weaker than a contemporaneous entry,
    and worth flagging as such where a removal rests on them.
  - **What is genuinely absent is 2004-2005.** The bulk row starts 2006-08-31
    while the soil record starts 2004-09-07, so those first two years have no
    site record at all. The rows dated 2003, 2006 and 2016-01-01 are backdated
    GIN inventory imports, not events.
- **Other holes are informative too.** August 2020 is empty — the month the 5 cm
  SWC probe decouples — and June 2024 is empty, covering the unexplained 44-hour
  station gap. Silence is not evidence of nothing happening; it is evidence the
  record stops there.
- **Assert the filter matched.** An export whose format changed silently returns
  zero rows, which reads exactly like "nothing happened at the site". Both
  notebooks `assert len(...) > 0`.
- **Evidence first, fieldbook second.** The data locate the candidate period —
  `30_PRODUCTS/08` scans blind for the month where the catch ratio steps hardest,
  the SWC notebooks scan for lost rain response — and only then is the fieldbook
  asked what happened there. Letting the fieldbook drive the search finds only
  faults somebody already noticed.
- **A missing entry is not a veto.** The Aug-Oct 2020 decoupling of the 5 cm SWC
  probe has no fieldbook entry at all and is still removed, on physical evidence
  alone; conversely the fieldbook records dates but no times, so every boundary
  taken from it carries a day of slack. Where the fieldbook cannot separate two
  candidate dates (the 71-day 2018 transition), the interval gets **its own flag
  code** rather than being assigned to one side.
- **The `Device Model` column outranks the literature on what a sensor was.**
  Published descriptions of this site name sensors that the fieldbook contradicts,
  and three were checked against the export rather than adopted: Shekhar et al.
  (2024) give `TA`/`RH` as a Rotronic HygroClip HC2-S3 (the fieldbook has HC2-S3
  units only on the profile masts `M3`/`M4`/`T1_35`, never at `T1_47`), soil
  moisture as a Decagon EC-5 (the string `EC-5` occurs **zero** times in the
  export; CH-LAE is EC-20 then TEROS 12, and the paper assigns EC-20 to CH-Dav —
  the two sites appear transposed), and the Delta-T `BF2116` to CH-Dav (that
  serial is registered at CH-LAE `T1_47`). The findings live in
  `docs/Instrumentation.md`, which is where sensor-level identity belongs; a
  variable page states only what its own series needs. Grouping devices by
  `Location` and `Device Model` answers this in one pass and is the first thing to
  run when a paper and this repo disagree.
- **A backdated import row gives the model; the install date is in an event entry
  days away.** The `01.01.2016` rows say only "Added device to site", so the date
  a device went up is not on the row that names it — but it is in the export.
  Reading the days *around* the import found one visit, **8 January 2016**, that
  installed the LI-7200, the replacement `A100LK` cup anemometer and both PAR LITE
  sensors together, and a `2008-10-07` relay entry that puts the CNR1 on the tower
  logger years before GIN existed. Never report a backdated date as a deployment
  date and never give up at the import row: search the *model and serial* across
  the whole export, keep the nearest `### date` heading above each hit, and read
  the legacy 2011 block too. A serial found in an event entry dates the device
  exactly.
- **A sensor swap and its calibration constants can be separated by weeks, and the
  gap is a data-quality window.** The CNR4 was installed on **14 December 2021**
  with the installing entry noting the logger script still needed the new
  constants; the program was updated on **7 January 2022** (`SW_IN` 13.89,
  `SW_OUT` 14.38, `LW_IN` 10.85, `LW_OUT` 11.33 µV W⁻¹ m²). Those 24 days are
  flagged unverified in `docs/Instrumentation.md` and are **not** resolved by
  `01`'s continuity checks, which compare seasonal and annual ratios and would
  average a 24-day error away. When a fieldbook entry says a constant still has to
  be changed, find the entry that changed it and treat the interval between them
  as suspect until measured.
- **GIN has no `TA`/`RH` device at `T1_47` for the whole dataset period** — the
  first is a HygroVUE10 in June 2026, after the record ends. So the MP101A →
  CS215 identification and its January 2016 date rest on the **logger programs**
  and on the step in the data, with no fieldbook corroboration at all. A fieldbook
  silence about a level is not evidence that nothing was mounted there. Where the
  fieldbook *does* speak it corroborates: the CNR4's first entry is 14 December
  2021, the date `01` derives independently for the radiometer swap.

### The logger programs

The dataloggers' own programs say what a sensor was and how its raw signal was
converted, which the fieldbook usually does not. They live in the external data
folder beside `workflow/`, like the fieldbook:
`...\dataset_ch-lae_flux_product-data\csi_loggerscripts\` (the CR10X `.CSI`
programs, 2004-2006) and
`...\logger_scripts\ch-lae_idl_t1_47_1-Version_20160118\` (the CR1000 `.CR1`
program). They are what dates and identifies the 2016 `TA` change and give both
eras' calibration constants. **Read them in the notebook, don't quote them** —
same rule as the fieldbook.

- **They are signed, so they are a personnel record too.** Anything printed from
  a logger program passes through the same `redact_people()` and
  `audit_unmapped_names()` nets as the fieldbook.
- **A program names the channel, not the column.** The raw pre-2016 meteo stream
  is headerless CR10X *array* files (`logger<date>.aNN`), so a column name such
  as `AirT_C` comes from the acquisition-side configuration and will not be found
  in the program; match on the channel and its multiplier instead.
- **There is more than one CR10X program, and reading all of them is the point.**
  Six `LAEGEREN.*.CSI` files span 2004-2006. The three from 2004 measure **no**
  incoming shortwave — their comments record that the radiometer's channels then
  carried a PAR sensor — and the CNR1 instruction first appears in the program
  dated **14 September 2005**, which is the day the tower `SW_IN` record begins.
  A date derived from a program and confirmed by the data is worth an assertion.
- **Parse the constants out of the program text; do not read them off once.**
  `01` extracts the multiplier and offset from every program that measures the
  sensor and asserts they are all identical (`99.7009` and `0`, i.e. 1000/10.03
  for a Kipp & Zonen CNR1, SN 020484 — the same instrument before and after 2016).
  The two program languages write the same two numbers differently, so the parser
  matches each shape separately and **raises** rather than returning an empty dict
  that would agree with anything.
- **Say what the programs cover and what they do not.** No tower program between
  May 2006 and January 2016 survives on disk, so the constants could in principle
  have changed and changed back inside that gap. The programs establish two
  endpoints; the data have to cover the interval between them.
- **The redaction net fires on logger-program syntax too.** `Diff` (from
  `Volt (Diff) (P2)`) and `Kin` (from `Messung von Kin`) are name-shaped and were
  added to `redact_allow.csv` — the sanctioned fix, since that file lives beside
  the map outside this repository. Adding a row: the reason field is free text, so
  **quote it or keep commas out of it**, or the csv gains a third column and every
  later read raises a tokenizing error.

The shape below is deliberate — follow it when adding a variable.

- **Structure of a notebook:** about-this-notebook → data sources → timestamp
  convention → settings (`DIRCONF`, `TIMEZONE_OFFSET_TO_UTC_HOURS`,
  `REQUIRED_TIME_RESOLUTION`, `TARGET`/`REFERENCE`, `OUTNAME`/`OUTPATH`) →
  helpers → download per `data_version` → merge → corrections → export →
  read the written file back → runtime footer. Sections carry emoji headers.
- **Timestamps:** the database stores UTC `TIMESTAMP_END`. `InfluxIO.download`
  shifts by `TIMEZONE_OFFSET_TO_UTC_HOURS` to local time, then
  `TimestampSanitizer(output_middle_timestamp=True, nominal_freq='30min')`
  converts to `TIMESTAMP_MID` and **raises** if the data are not 30MIN. Every
  `30_PRODUCTS/` notebook works on `TIMESTAMP_MID` from that point on.
  **`20_SCREENING/` is the exception** and it is easy to get wrong: those
  notebooks stay on `TIMESTAMP_END` throughout, because
  `StepwiseMeteoScreeningDb` converts to `TIMESTAMP_MID` *internally* for
  screening and hands back `TIMESTAMP_END` after `resample()`, ready for upload.
  So anything a screening notebook reads from a `30_PRODUCTS/` file (the
  precipitation product, stored on `TIMESTAMP_MID`) must be shifted by +15 min
  before use. `TIMEZONE_OFFSET_TO_UTC_HOURS` is applied identically on download
  and upload and must match the timezone the raw data was logged in.
- **Data versions:** the same measurement exists under `meteoscreening_mst`
  (older) and `meteoscreening_diive` (newer). Merging them is a merge of two
  *screenings of one measurement*, not a gap-fill — use `combine_first` so a
  future overlap resolves deterministically instead of duplicating timestamps.
  The `mst`/`diive` boundary sits at 2021/2022 and is where unit and raw-source
  breaks hide; check the database's own unit tag (`show_field_overview`) against
  the magnitude of the data, and prove the exported series does not step there.
- **A field name is a statement about the variable, not about the instrument.**
  This site reuses one name across sensor generations, and it has caught us
  four times: `TA_T1_47_1` spans a Rotronic MP101A read as a single-ended analog
  voltage (CR10X program, multiplier 0.1, offset 0 — 10 mV per °C) and a Campbell
  CS215 on SDI-12 (CR1000 program, multiplier 1), sensor and acquisition replaced
  together on 2016-01-21; the analog chain carried a constant ≈ -11 mV zero-point
  error, so the pre-2016 record reads ≈ 1.3 °C too cold; `PREC_TOT_T1_47_1`
  spans two acquisition systems either side of 2018; `SWC_FF1_0.3_1` spans two
  probes with a 327-day dead period between them,
  the second installed 40 cm downslope; and every `SWC_FF1_*` name carries the
  **old EC-20 profile** under `meteoscreening_mst` back to 2004 — the
  MeteoScreeningTool screened the earlier sensors and stored them under the later
  names, so the pre-2020 half of that column is a different instrument. Before
  merging data versions, ask what hardware each era was, not just what it is
  called: compare season-matched levels across the boundary, and check whether
  the eras overlap at all. Where they do (`08`), prove they are the same series
  before splicing. Where they do not (`SWC`), the step cannot be calibrated away
  and the honest product is a **`SOURCE` flag naming the sensor generation** —
  optionally with a `_HOMOGENIZED` second column, which must then say out loud
  what its rescaling rests on: climatology where nothing spans the break (`SWC`),
  but an independent co-located sensor where one does (`02`, see below). Never let a name imply a continuity the hardware does
  not have: FLUXNET's `SWC_F_MDS_*`
  splices these two eras with a +9 to +12 % VWC step passed straight through,
  which is the outcome to avoid reproducing.
- **A step at a hardware change need not be one number, and a constant can only
  remove the part that is one.** `02` is the worked case. The 2016 sensor swap
  moved two things at once: a **zero-point error** in the old analog chain,
  constant day and night, and a **radiation-shield difference**, present only in
  sunlight because both 47 m sensors sit in passive shields and the newer one
  heats more. The constant (+1.3197 °C on the earlier era) removes the first
  completely — the night step against MeteoSwiss falls to −0.01 °C — and leaves
  +0.37 °C in daylight, which no constant can reach. The second term is fitted
  per era against **NABEL**, which is aspirated and so has no shield error of its
  own, and only the *difference* between the two eras' responses is removed, from
  the later era. It is zero wherever there is no radiation, which is what stops it
  correcting the night a second time, and it brings the daytime step to +0.06 °C.
  The lesson generalises: **split the residual by night and day before deciding
  a correction is finished.** A statistic over all hours averages the two and
  reports neither.
- **Fit against one reference, score against another.** The `TA` terms are fitted
  against NABEL (same tower, aspirated, but ends 2018) and scored against
  MeteoSwiss Lägern (2.5 km away, independent institution, covers the record).
  Neither correction has ever seen the series that judges it, which is what makes
  the scores a test rather than a restatement of a fit. Where a correction must be
  extrapolated beyond its fitting reference, say so and test it there: `02`'s
  shield term is fitted on three NABEL years and applied over ten, and the
  extrapolated years land within 0.03 °C of the earlier era's own level.
- **A hardware change is a hypothesis about the data, not a finding.** The 2016
  acquisition change moved `TA` by 1.3 °C, so it was assumed to have moved `SW_IN`
  as well. It did not, and `01` now carries the negative result with the
  assertions that keep it true. **A negative result is a result** and is worth a
  section: without one the question gets re-opened every time someone notices the
  date. The rule generalises — ask what each hardware change actually replaced.
  For `TA` the sensor *and* its conversion changed; for `SW_IN` the 2016 change
  swapped only the logger, and the real sensor change is **December 2021**
  (CNR1 → CNR4, sensitivity 10.03 → 13.89 µV/W/m²), which no one had looked at.
  Neither moved the series.
- **Radiation errors are multiplicative, so compare radiation in ratios.** A
  sensitivity 3 % wrong reads 3 % low at every irradiance, so a difference mixes
  the error with the weather and a ratio does not. Three controls belong in the
  helper rather than at each call site, because each of them manufactured a change
  that was not one while this was being written:
  - **season** — monthly medians averaged over calendar months, restricted to
    April-September, because snow and rime on an upward-facing sensor and the
    horizon differences between two sites at low sun both read as calibration;
  - **illumination** — select on *potential* radiation, which is astronomical and
    cannot drift; selecting on a measured series biases the ratio towards it;
  - **how sunny the year was** — a ratio between two sensors is immune, a ratio
    against potential radiation is **not**. A clear-sky index rises in a sunny
    year because more half-hours sit near the envelope. An earlier pass read that
    as a drift of the tower and attributed the 2011 event to the wrong station.
- **With *n* sensors there are *n(n−1)/2* ratios, and the pattern of which ones
  move names the sensor.** Each sensor appears in *n−1* of them, so a change at
  one moves exactly its own ratios. This is `02`'s step 3️⃣ generalised, and
  `RADIATION_SENSOR_CONTINUITY.ipynb` implements it as a `moved()` rule that
  **returns no sensor when the pattern does not identify one** — two sensors
  moving at once looks exactly like a table with several large entries. Three
  sensors suffice only while all three overlap: NABEL ends in 2018, which is why
  the co-located `PPFD_IN` sensor is the fourth witness and why the post-2018
  period is decidable at all. The rule caught a real trap — across the Dec 2021
  radiometer swap the pair `SW_IN`/`PPFD_IN` moves, but because the **PAR sensor**
  is drifting, not the pyranometer. **A ratio says two sensors separated, never
  which of them left.**
- **A reference can be the thing that moved.** MeteoSwiss Lägern steps by about
  5 % on **6 October 2010** — three tower-side sensors from two institutions step
  against it together and not against each other. The cause is in the reference
  file itself: `SW_IN_DIFF_LAE_MS` begins on exactly that timestamp, so the
  station's radiation instrumentation was rebuilt. It remains a sound gap-filling
  driver, because a driver supplies the *state of the sky* and a scale change does
  not alter which half-hours were cloudy — but **a tower-minus-Lägern difference
  is not evidence about the tower across that date**. `01` and `03` use it as a
  driver; `02` and `TA_HOMOGENIZATION_OPTIONS` only as a binning covariate.
- **Not everything found has to be corrected, and saying so is the deliverable.**
  Two real changes in this record are left in place and documented instead: the
  tower pyranometer rising ~3 % from 2013, and `PPFD_IN` falling ~7 % since 2021
  and still falling. Both develop over years rather than stepping at a date, so
  there is no boundary at which a correction could be applied, and neither has a
  fieldbook entry naming a cause. Correcting an unattributed drift towards a
  reference replaces a measurement with a guess.
- **A threshold below the measurement's own noise is mis-set, not strict.** `01`'s
  first 2016 guard was `< 1.0 %` and the data came in at −0.99 % — one hundredth
  of a percent from firing on *nothing having happened*, because the wall sat
  below the median ordinary-year change of the same statistic. Derive the
  threshold from what the record does in a quiet year, assert that it stays above
  that, and pair it with a relative test (the change here is smaller than the
  worst change elsewhere). This is not the same as relaxing a guard: a guard that
  cannot distinguish signal from its own scatter never had a chance of being
  informative.
- **Assert on the pairs the change could physically have touched.** `01`'s first
  version asserted on all three pairwise ratios at 2016 and failed — on the pair
  between the two *references*, which a change to this tower's logger cannot have
  moved. Say which subset the assertion covers and why.
- **Choosing a model order needs a shape criterion as well as an error.** A
  record-weighted RMSE is dominated by the bulk of the data — for a radiation
  term, the many half-hours at low sun — so a curve can be wrong by several tenths
  of a degree in the brightest conditions and barely move it. Those are exactly
  the conditions daily maxima come from. `02` therefore picks the smallest order
  that is both within a tolerance of the best held-out error **and** within
  0.15 °C of its own binned means, and re-checks the second on every run. Never
  draw a fitted curve beyond the range it was fitted on; clip the driver and hold
  the response flat above it, or the polynomial invents a tail.
- **A `data_version` filter is not a tag filter.** Within one field and data
  version there can be several series carrying different `gain`, `raw_varname` or
  `freq` tags, so anything reading tags must handle a list, not a scalar. A
  differing `gain` tag does **not** by itself mean the stored values differ in
  scale — it records what was applied to that era's own raw source (SWC is `1`
  for `mst`, which read a CSV already in `%`, and `100` for `diive`, which reads
  `m^3/m^3` and multiplies), and both eras are stored in `%`. Check the tag
  *against the magnitude* before rescaling anything, because the tag alone looks
  exactly like a factor-100 bug.
- **Guards:** a helper that can silently do nothing gets a **negative control**
  cell that feeds it bad input and asserts it raises. Sanity checks assert
  rather than assume (continuous index, no duplicates, physical range).
- **Every table carries a caption above it and every figure one below it.**
  `tabcap()` and `figcap()` are the two helpers; they live in `02`, `99` and the
  overview and should be copied as-is. Two things they got wrong once each.
  **Define them above their first use** — in `99` they sat beside the figure
  helper, several cells below the table that called one, and the notebook only
  failed at run time. And where one call site draws many figures (`99` draws one
  per series from a single `plot_product()`), **build the caption from the
  series' own metadata row** rather than writing it out per series: a series
  added to `PRODUCTS` later then cannot arrive without a caption, and one whose
  aggregation or flag column changes cannot keep a caption describing what it
  used to be.
  - **A plotting helper called from more than one place owns its caption.** `01`'s
    four gap-filling helpers each build theirs from the arguments and the data
    they were handed, so the second call site cannot arrive without one. Only
    raw dataframe echoes, `%%time` output, diive's own `report()` and the save
    confirmation go uncaptioned — that is the line `02` draws and the one to
    follow.
  - **Look at the figure before believing the caption.** Two captions in `01`
    were wrong about their own panels — one described a spike at exactly zero as
    "a few W m-2 wide", another said two fitted lines were "almost on top of each
    other" when the panel, once its clipped y-range was fixed, showed them
    converging from a visible separation. Extract the rendered PNGs and read
    them; a caption is a claim about a picture, and it is checkable.
- **A visual is worth adding wherever a table states a number that has a shape.**
  `01` gained seven figures on this principle: the nighttime offset had a summary
  table and no plot, and the plot is what shows the offset *drifts* — which is
  the whole reason it is removed per day rather than as a constant. Likewise a
  `describe()` of the two gap-filling drivers said they cover a similar range; the
  hexbin says NABEL tracks the tower at RMSE 41 W m⁻² and MeteoSwiss at 69, which
  is the actual reason the record is filled in two periods.
- **Pair a level check with a spread check on the fills themselves.** `01` plots
  the clearness-index distribution of measured against model-filled records: they
  should have the same *shape*, including the overcast tail. A filled
  distribution that is narrower, or that has lost the tail, is climatology
  wearing the right mean. Same idea as `02`'s spread test against a reference.
- **The 2012 faults are site history and recur in every variable:** the
  17 Aug 2012 logger clock error (+15.5 h shift of one block), the late-July/
  August power supply failure, and the Oct/Nov storm damage. Windows are always
  expressed on the **corrected** time axis. Copy the shared windows only when
  the variable has no better evidence — where an independent sensor exists,
  derive the variable's own windows from its residual and say so.
  - **They are tower history, and do not transfer to the forest floor unread.**
    Checked against the fieldbook for the soil profile: the 17 Aug 2012 clock
    entry describes the **meteo** logger and a lag of **28 h 25 min**, not the FF
    logger and not +15.5 h; the late-July/August power entries are explicitly
    about the **tower** battery and fuses; and the Oct/Nov storm check found
    damage to **sap-flow** sensors only, naming no soil sensor. What *is* at the
    forest floor in that window is three consecutive interventions on the soil
    sensors' own wiring and power between 18 Jul and 15 Aug 2012, plus a
    2012-04-25 logger program "with corrected multipliers and offset" that names
    no channels. So for a forest-floor variable these windows are a hypothesis to
    test, not a window to copy — and the MOXA clock faults of Aug/Sep/Oct 2012
    are a *fourth* thing again, belonging to the eddy acquisition computer.
- **Completeness is per variable, not a house style.** `01`-`03` are gap-filled
  products and carry an `ISFILLED` flag naming the model that produced a value.
  `01` and `03` export **two columns only** — measured-and-filled plus `ISFILLED`
  — and deliberately no `_HOMOGENIZED` column, because both series were tested at
  their hardware changes and neither steps. That absence is a claim, so it is the
  claim the notebook asserts; `09` makes the same point in the other direction by
  refusing a duplicate column at the one `SWC` depth with a single era.
  `02` gained a code `5` for records reconstructed from the co-located NABEL
  sensor at 49 m, because the timestamp-only fallback that had been filling them
  (code `2`) produces climatology, not weather. `02` is also the one product that
  is *both* gap-filled and inhomogeneous, so it exports four columns on the
  `08`/`09` pattern — measured, `ISFILLED`, `_HOMOGENIZED`, and a `SOURCE` flag
  naming the acquisition era (`0` CS215, `1` MP101A, `2` changeover, era
  undetermined, `3` before the tower record begins).
  `04` is reconstructed from a co-located sensor (a transfer between two
  measurements of the same quantity) and carries a `FLAG_<var>_MISSING`
  provenance flag: `0` measured, `1` never measured, `2` removed here,
  `3` reconstructed. `05`/`06` are exported as measured with no flag. `07` is
  computed by formula from finished products and its flag says what it was
  computed *from*. `08` and `09` likewise export a **second, derived value
  column** alongside the measured one: `08` a `_HOMOGENIZED` rescaling of its
  pre-2018 era, with its own `SOURCE` flag naming the acquisition era beside its
  `ISFILLED` flag; `09` a `_HOMOGENIZED` column per depth (four of five — 0.5 m
  has a single era and deliberately gets none, because a duplicate column invites
  someone to difference it, get zero and conclude the record is homogeneous) plus
  one `SOURCE` flag per depth naming the **sensor set**. `09` is also the only
  notebook covering five columns of one variable, because a soil-moisture depth
  is only interpretable next to the depths above and below it. A notebook that
  exports gaps says so in a closing note for downstream users.
- **Order of operations matters** and is stated in the notebook: timestamp shift
  → removal of damaged periods → value corrections. Masks such as
  "never measured" must be captured *before* any correction that can write a
  value into a missing record (notebook `03`'s nighttime zero-offset did
  exactly that and made 7,543 modelled values look measured).
- **Never train a gap-filling model across an instrument change.** One model
  spanning the 2016 `TA` sensor change put its filled records on neither era's
  level, which silently invalidated the homogenisation offset for exactly those
  records. `02` therefore fits three periods, and its two boundaries exist for
  different reasons — the sensor change, and the loss of a driver where the NABEL
  reference ends. Say which boundary is which; a reader assumes both are hardware.
- **An assertion states what a correction does, so changing the correction
  breaks it — and that is the system working, not an obstacle.** Adding the
  shield term to `02` fired three separate guards that all asserted the later era
  is never modified: `02`'s break-year check, `02`'s export check and the
  overview's integrity check. Each was **re-derived** to describe two terms (the
  later era now carries exactly the radiative excess; the correction after the
  break is never positive, is exactly zero in the dark, and takes many distinct
  values rather than behaving like a second constant). None was relaxed. A guard
  that fires on a deliberate change has just proved it can fire.
- **An audit that averages over a group can hide two opposite errors that
  cancel.** In `02` a per-year check passed on a year holding 11,150 records
  1.1 °C too cold and 1,495 records 5.5 °C too warm. Assert per year **and per
  fill method**: populations produced by different models have no reason to
  agree, so a statistic over their union is a statistic about neither.
- **A check whose reference is fitted on the very records it tests cannot fail.**
  A correction derived as `mean(reference) - mean(window)` and then "verified"
  against that same reference reports a departure of exactly zero by
  construction. The non-circular form is a hold-out: refit excluding the period,
  predict it, and judge the departure against the irreducible scatter between the
  two sensors.
- **A level test cannot catch a fill with the right mean and no weather in it**,
  so pair it with a **spread** test against a reference — a timestamp-only
  climatology scatters several degrees more widely than a measurement does. The
  gate only works in one direction, though: records built from a fitted line
  scatter *less* than a measurement, so for those neither level nor spread is
  evidence and the hold-out is what supports them.
- **Compute the figure in the notebook rather than quoting it in prose.**
  Several numbers written into `02`'s markdown went stale within a day of being
  written; an f-string off the live object cannot. Same rule as the SWC audit
  recomputing its own justification.
- **Statistics over measured records only and over the complete gap-filled
  column disagree** — by 0.085 °C on a period difference in `02` — because a
  measured-only mean is seasonally biased wherever a year's gaps cluster. Report
  both and label which is which, rather than letting a reader discover the
  discrepancy and distrust the product.
- Site-specific bits (variable names, sensor heights, fieldbook entries, the
  co-located NABEL reference) do **not** carry over to another site; the
  notebook structure and the checks do.

## Environment

- Managed with **uv** (not poetry). Python **3.12**.
- `uv sync` to set up; `uv run <cmd>` to run inside the env.
- Local editable path dep via `[tool.uv.sources]`: `diive` (`../../diive`).
- The dep is declared as **`diive[db]`**, not plain `diive`. The `db` extra pulls in
  `influxdb-client`, which diive's `InfluxIO` needs to reach the database (the
  `10_METEO` download notebooks). diive also ships `db` as a dependency group, but
  groups are local to the project that declares them and are not part of published
  metadata — `uv sync --group db` only works *inside* diive, so from here the extra
  is the only way to get it.
- **`scipy` is declared directly**, not relied on through `diive`:
  `30_PRODUCTS/02` imports it itself for Theil-Sen and Kendall's tau, and an
  import that only works transitively breaks the day the dependency it travels
  through drops it.

## Docs

- Quarto **website** project (Pandoc-based, not Jupyter Book/MyST). Single config
  file `docs/_quarto.yml`: title, `website.sidebar.contents` (the nav, with a
  `section:` for the nested Flux-Processing-Chain pages), `bibliography`, theme,
  and favicon all live there. `output-dir: _build/html` keeps the old publish
  path. It's a **website**, not a book, specifically so the left sidebar is
  collapsible/hideable.
- Author is footer-only: **do not** set `author` metadata anywhere (that renders
  it in each page's top title block) — the name lives in `website.page-footer`.
  `date-modified: last-modified` (project level) shows a "Modified" last-updated
  date on every page (filesystem mtime, not the git commit date).
- Two `include-after-body` partials (both listed in `_quarto.yml`) move things
  into the **right ("On this page") sidebar** with client-side JS, since Quarto
  has no option for either: `_theme-toggle.html` relocates the **light/dark
  toggle** to the top of the right sidebar (and `styles.css` restyles it into a
  labelled "Dark mode"/"Light mode" pill — CSS only, keying off Quarto's
  `.alternate` class), and `_last-modified-sidebar.html` moves the **"Modified"
  date** to the end of the right sidebar. Both fall back to the left sidebar on
  TOC-less pages. (Note: Quarto caps the article body at a fixed readable width
  and centers it, so there is deliberately **no** "hide sidebar to widen content"
  control — that would require overriding Quarto's layout grid.)
- Quarto is **not** a pip/uv library — it's a standalone binary. It's vendored
  into the env via the `quarto-cli` dev dependency, so run it as
  `uv run quarto ...`.
- Build with `uv run quarto render docs` (or `uv run quarto preview docs` for the
  live dev server). Output goes to `docs/_build/html/`.
- **Notebooks** (`workflow/**/*.ipynb`) are rendered by **Quarto itself**, as
  full site pages — they get the site theme, light/dark toggle, search, lightbox,
  a right-hand TOC, and anchored/linkable headers, just like the narrative pages.
  `build_notebooks.py` (repo root) is now a **staging** step, not a converter: it
  copies the real notebooks into `docs/notebooks/` (gitignored build inputs,
  mirroring the `workflow/` tree), writes a `_metadata.yml` there that sets
  `execute: enabled: false` (Quarto shows the committed outputs and **never runs**
  a cell), and generates `docs/notebooks/index.qmd` — a themed landing page with
  one Quarto *listing* per stage. This generated index is the **only** notebook
  index — a hand-generated `workflow/README.md` used to duplicate it for the old
  Jupyter Book build and was deleted once it had rotted to 3 live links out of
  48. It skips any `_`-prefixed path component
  (`_archive/`, `_templates/`, `_TEMPLATE*`). While
  staging it also **sanitizes each copy** for two diive-notebook quirks that
  otherwise break/uglify the render (the copies are throwaway, so the real
  notebooks are untouched): a bare `---` thematic-break line in a markdown cell
  (Pandoc parses it as a YAML front-matter block and the build aborts — same
  gotcha as the narrative pages) is rewritten to `***`; and a notebook that
  doesn't lead with a `# ` H1 (e.g. the meteoscreening notebooks open with a logo
  image + a styled `<span>`) gets a `title:` injected from its filename, so its
  page and listing row aren't blank/garbage. Because the
  notebooks are now part of the render, the order **flipped**: stage
  **before** `quarto render docs`, not after. Run order:
  `uv run python build_notebooks.py` → `uv run quarto render docs` →
  `uv run python build_notebooks.py --clean` (drop the staged copies). `deploy.ps1`
  does all three. The sidebar's "Notebooks" entry points at `notebooks/index.html`.
  (History: this replaced a standalone-**nbconvert** build whose HTML carried
  JupyterLab styling and had no header anchors or shared nav.)
- Pages are plain `.md` **except** `FPC.qmd`: Quarto only allows executable cells
  (the ` ```{mermaid} ` flowchart) in `.qmd` files. Any page that gains an
  executable cell must be renamed to `.qmd`; the output `.html` name is unchanged.
- Quarto markup conventions (not MyST): callouts `::: {.callout-note title="…"}`
  … `:::` (need a blank line before the opening fence); figures
  `![caption](path){#fig-x}` referenced with `@fig-x`; table caption line
  `: caption {#tbl-x}` referenced with `@tbl-x`; math is native `$…$`/`$$…$$`.
- Two Pandoc gotchas in narrative text: use `***` for horizontal rules (a bare
  `---` line is parsed as a YAML block and breaks the build), and escape a stray
  `@word` as `\@word` so it isn't treated as a citation key.
- **Register: this is scientific documentation. Headings and prose stay neutral
  and professional.** No colloquialisms, no jokes, no second-person warnings
  dressed up as banter. Write `## Known limitations`, not
  `## What will bite you`; `reads approximately 25 % low`, not `reads a quarter
  low`; `their gaps are retained`, not `their gaps stay gaps`. The register is
  that of a data-product manual a stranger will cite, not that of a commit
  message. This applies to the published `docs/` pages **and** to notebook
  markdown, since the notebooks render as site pages too. Direct imperatives
  addressed to the reader (`Filter on the flag before …`) are fine and are not
  what this rules out.
- **A page under `docs/` is written for the person using the data**: which
  columns exist, units, period, coverage, which provenance flag to filter on,
  and the known limitations. Keep it concise and leave the method narrative to
  the notebooks the page links to — they already carry the full evidence trail,
  and repeating it on the page buries the few facts a data user needs. Verify
  column names, units and coverage against the exported files, not against the
  notebook prose.
- **Every meteo parameter gets its own page**, named `Meteo_Data_<VAR>.md`
  (`Meteo_Data_TA.md`, then `Meteo_Data_SW_IN.md`). `Meteo_Data.md` stays general — the
  conventions shared by all products, the variables table, and how the products
  are built — and carries a **table of the per-
  variable pages at the top**, listing all ten parameters whether or not their
  page exists yet, so an entry without a link reads as a page not yet written
  rather than a variable not in the dataset. Adding a page means editing that one
  cell **and** adding the file to the nav in `docs/_quarto.yml`; a page absent
  from the nav is unreachable. The per-variable pages are **nested under
  `Meteo_Data.md`** with the `section:` construction (the same one `FPC.qmd`
  uses), not listed beside it: with `collapse-level: 1` the sidebar then ships
  them collapsed, so ten of them cannot crowd out every other page. Writing
  `- section: Meteo_Data.md` keeps that page a link in its own right rather than
  turning it into a bare heading.
- **A limitation belongs to a variable, so it lives on that variable's page**, in
  its `## Known limitations` section, and nowhere else. `Meteo_Data.md` names the
  section and points at the pages instead of restating them: a duplicated bullet
  is the one that goes stale, and a reader picking a variable arrives at its page
  anyway. The two exceptions are properties of a *reference* rather than of a
  product (the October 2010 MeteoSwiss Lägern rebuild, the NABEL series ceasing
  to be independent in mid-2018); the general page says they exist and recur, and
  each variable page that is touched by one states what it means there.
  A limitation of the *processing chain* rather than of a variable — the 2022
  time-shift investigation — belongs on `Issues.md`.
- **Sensor identity lives on `Instrumentation.md`, site description on
  `Site_Info.md`.** The same split as limitations, one level up: a variable page
  says which instrument produced *its* series and what a change did to *its*
  values, and `Instrumentation.md` holds the full model/serial/period tables for
  every level of the tower and the soil profile, including the sensors that feed
  no product (the profile masts) and the published attributions that are wrong.
  `Site_Info.md` holds what a stranger needs before reading any of it — position,
  slope, climate, stand, soil, management and footprint — sourced to the Swiss
  FluxNet site page and the published site descriptions, with **every value naming
  its source** and disagreements between sources shown rather than resolved
  silently. Both pages carry a `## References` section holding a `::: {#refs} :::`
  div, which is how a Quarto page renders the bibliography it cites; entries go in
  `docs/references.bib`. Where a published number will later be replaced by one
  computed from this dataset, say so in a `callout-warning` naming the products it
  will come from — a stale figure that looks authoritative is worse than a marked
  placeholder.
- **Explain what was done in plain terms, and link every notebook that carries
  the evidence.** A per-variable page opens with a short list of the notebooks
  behind it — the one that builds the product, any investigation that settled a
  decision, and the overview — so a reader who wants the derivation is one click
  away and the page itself can stay short. Describe a correction by what changed
  physically and what was done about it, not by its algebra: "both sensors sit
  in passive shields, which heat up in sun, and the newer one heats more" is the
  register, not the fitted polynomial. Give the size of the effect and the size
  of what is left, and leave the fit to the notebook.
- **A page says what a variable does *not* need, when a reader would expect it
  to.** `Meteo_Data_TA.md` opens by telling the reader which of two columns to
  use; `Meteo_Data_SW_IN.md` opens by explaining why there is only one, since the
  same 2016 date that split `TA` did not split this variable. A limitation that is
  a property of an *input* rather than of the product belongs there too — the
  October 2010 step in the MeteoSwiss driver changes nothing in the file, but it
  changes what a comparison against that station means.
- **Verify every number on the page against the exported file, not the notebook
  prose.** Coverage claims are the easiest to get wrong: "every year from 2006 is
  at least 93 % measured" was written from memory and 2012 is 92.7 %.
- Published to GitHub Pages via `ghp-import` (point it at `docs/_build/html`).
  Quarto uses relative asset paths, so the project subpath works with no extra
  env vars.
- Three PowerShell wrappers at the repo root save you from remembering the
  step order (all respect the "never build unless asked" rule):
  - `preview_fast.ps1` — Quarto live-reload dev server for `docs/*.md` only
    (no notebooks; `/notebooks/` links won't resolve). Fast edit loop.
  - `preview_full.ps1` — full local build (website **+** notebooks) served over
    real HTTP, so search and `/notebooks/` work. Final check before deploy.
  - `deploy.ps1` — the one deploy entry point: stages notebooks, renders the
    site (notebooks included), clears the staging, then `ghp-import`s
    `docs/_build/html` to `gh-pages`
    (`-o`/single-commit so the branch doesn't accumulate old notebook assets).
    `-Preview` = build + serve (same as `preview_full.ps1`), `-NoPublish` =
    build only, `-Remote`/`-Branch` override the target. It touches only
    `gh-pages`, never your source branch/working tree.
- Pages are editable in Obsidian. Use standard Markdown links and Quarto
  cross-references — **not** Obsidian `[[wikilinks]]`/`![[embeds]]`, which the
  site won't resolve.

## Reusing this repo as a template for another site

This repo is the **template** for the flux-product docs of other EC sites. The
machinery (Quarto website, `build_notebooks.py`, the `deploy.ps1`/preview
wrappers, the mirrored `workflow/` + external-data layout, the uv env) is
site-agnostic and should be copied as-is. Only the **site-specific bindings**
below change per site — grep for the old site code (`ch-lae`, `CH-LAE`) to find
stragglers.

- **`docs/_quarto.yml`** — `website.title`, `favicon`, `repo-url`,
  `page-footer` (author/© year), and the whole `website.sidebar.contents` page
  list. Keep `output-dir`, the theme pair, `lightbox`, `search`, and
  `date-modified` as-is unless a site asks otherwise.
- **`docs/` content** — replace the narrative pages, `references.bib`, `images/`,
  and the site mark (`logo.*` + `favicon.*`, plus `website.logo-alt`). The page
  set differs per site; only Stage-30 FPC pages that carry a mermaid cell need to
  be `.qmd` (see Docs). The mark depicts **this** site's stand — spruce and beech
  for the mixed forest at Lägern — in colours sampled from the site banner
  (`images/logo1.jpg`), so another site needs its own artwork, not a recolour.
  Three things the drawing has to respect: the `.svg` is the editable source and
  the raster files are generated from it; the `.ico` must carry a hand-drawn
  16 px frame rather than a downscale of the 256 px one; and foliage must differ
  in **value** from the tile, not just in hue — a first draft used a dark spruce
  that vanished into the petrol background below 24 px.
- **`pyproject.toml`** — `project.name`, `description`, `authors`. Keep the dep
  groups and `[tool.uv.sources]` (the `../../diive` editable path) unless the
  sibling-repo layout differs on that machine. Keep the `[db]` extra on `diive`
  too — every site needs the database download (see Environment).
- **`deploy.ps1`** — the hard-coded published URL and repo name appear only in
  comments and `Write-Host` messages; the actual push is generic
  (`origin`/`gh-pages`). Update the strings for tidiness.
- **`README.md`** — repo name/title.
- **External data folder** — the untracked
  `...\dataset_<site>_flux_product-data\workflow\` path (see Code/data layout).
  One per site; the two `workflow/` trees still mirror 1:1.
- **`workflow/` stages** — the numbered stages (`00_/10_/20_/30_/90_`) are the
  shared pipeline shape and carry over. Instrument subfolders (`IRGA72/`,
  `IRGA75/`) and the Stage-30 internal numbering are site-specific — a site with
  different or single sensors won't have those exact subfolders.

## Hard rules

- **Never run `git commit` or `git push`.** The user does all committing.
- **Never build the docs** (`quarto render`/`quarto preview`, or
  `build_notebooks.py`) unless explicitly asked. A full site build is
  `build_notebooks.py` (stage) **then** `quarto render docs` **then**
  `build_notebooks.py --clean`, in that order (or just run `deploy.ps1`).
