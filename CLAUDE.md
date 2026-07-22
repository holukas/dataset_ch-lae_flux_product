# CLAUDE.md

## What this repo is

Methods documentation for the **CH-LAE flux product** — an eddy-covariance
ecosystem-flux dataset for the mixed forest site CH-LAE. The actual flux
computation and meteo screening happen in a separate offline pipeline; this
repo's job is to **narrate the methods** used to produce the shared dataset and
publish them as a website.

## Layout

- `docs/` — the published Quarto website. Curated narrative pages (`*.md`, plus
  `FPC.qmd`), `images/`, `logo.png`, `references.bib`, `styles.css`, and
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
  `99_METEO_MERGED_2004-2025.ipynb` is the capstone: it runs last, joins the
  products of `01`-`08` onto one 30MIN `TIMESTAMP_MID` index with their
  provenance flags, and draws one overview figure per series. It **computes and
  corrects nothing** — a value in the merged table is exactly what its own
  notebook exported.

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
    one deliberate exception: published credit, skipped by the checker.
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
  three times: `PREC_TOT_T1_47_1` spans two acquisition systems either side of
  2018; `SWC_FF1_0.3_1` spans two probes with a 327-day dead period between them,
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
  that its rescaling rests on climatology rather than on an overlap. Never let a
  name imply a continuity the hardware does not have: FLUXNET's `SWC_F_MDS_*`
  splices these two eras with a +9 to +12 % VWC step passed straight through,
  which is the outcome to avoid reproducing.
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
  `04` is reconstructed from a co-located sensor (a transfer between two
  measurements of the same quantity) and carries a `FLAG_<var>_MISSING`
  provenance flag: `0` measured, `1` never measured, `2` removed here,
  `3` reconstructed. `05`/`06` are exported as measured with no flag. `07` is
  computed by formula from finished products and its flag says what it was
  computed *from*. `08` and `09` export a **second, derived value column**
  alongside the measured one: `08` a `_HOMOGENIZED` rescaling of its pre-2018
  era, with its own `SOURCE` flag naming the acquisition era beside its
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
  and `logo.png` (favicon). The page set differs per site; only Stage-30 FPC
  pages that carry a mermaid cell need to be `.qmd` (see Docs).
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
