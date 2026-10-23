# Stage 10 (`10_METEO`) conventions

> Stage-specific guidance. Repo-wide conventions and the hard rules live in the
> root `CLAUDE.md`.


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
  vs. the multi-variable `MeteoSwiss_LAE_30MIN_2004-2026.09`). `<years>` is
  `YYYY-YYYY` when the last year is complete and `YYYY-YYYY.MM` when it is not
  (LAE now ends 30 Sep 2026; OED and REGIONAL are still on 2025). Reference columns are
  suffixed `_<station>_MS` so they cannot be confused with tower columns.
  Because references are addressed by *path* rather than by database name, moving
  one breaks every reader — keep the filenames stable. A reference notebook may
  write more than one product when the source record itself is split (the OED
  precipitation record is daily to 2014 and 30MIN after), which is the one
  sanctioned exception to one-notebook-one-product in this stage.
  - **The stations are not interchangeable.** `LAE` (Lägern, 2.5 km, 845 m) is
    the full weather station and covers `TA`/`RH`/`PA`/`SW_IN` plus dew point,
    vapour pressure, sunshine and wind from February 2004 to September 2026 (the
    10-min record begins 2004-02-01, so January 2004 has no LAE value) — but measures **no
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
  - **Year labels come from the bins' starts, not their labels.** 10-min values
    are end-of-interval, so the final bin of a period is labelled 00:00 on the
    following day (1 Jan for a full year, 1 Oct for the September 2026 end), and
    the local-time shift pushes it again. Both traps silently misname the export
    (`..._2004-2026` for a record ending in 2025, `..._2004-2026.10` for one ending
    in September). The LAE notebook therefore declares `YEARS = '2004-2026.09'` in
    the settings, derives the label from the start of the first and last bin
    (`YYYY` if `END` is 1 January, `YYYY.MM` otherwise) and asserts that the two
    agree; it also asserts that the source data reach `END`, so a download that
    stops early fails instead of exporting a short file under the full label.
  - **The current year comes from the `_recent` files.** MeteoSwiss splits each
    record into `historical_<decade>` files, which end on 31 December of the
    previous year, and one `recent` file holding the current year up to the
    previous day (`_now` is not used). `source_files()` returns the historical
    files oldest first followed by the recent one, and the concatenation keeps the
    **first** duplicate, so the historical value wins wherever the two overlap.
    The recent file is updated daily, so the 2026 values are reproducible only as
    long as MeteoSwiss does not revise them (or republish them as historical);
    re-running the notebook later can change them, and with them every product that
    reads LAE.
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
  not decorative — `02` and `03` read `01`; `04` reads `02`'s product (measured
  and homogenised `TA` and its source flag, for the vapour pressure of its steps
  11 and 12); `06` reads `01` and `02` as diagnostics and `02`'s source flag for
  its night guard; `07` reads `01`/`02`/`04`. For `01`-`06` the run order is
  therefore: `10_REFERENCE/MeteoSwiss_LAE`, then `01`, then `02`, then `03`/`04`/`05`
  (independent of each other; `05` needs only the reference), then `06`. A
  notebook run against a stale upstream file does not fail, it silently uses the
  old values, so re-run the dependants whenever an upstream product changes. Each
  downloads the screened series from the database, corrects it, and writes a
  single product to the external data folder. The notebook name is a prefix of
  the file it writes (`02_METEO_TA_2004-2026.09.ipynb` →
  `02_METEO_TA_GAPFILLED_2004-2026.09.parquet`), so code and data line up by eye.
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
  `99_METEO_MERGED_2004-2026.09.ipynb` is the capstone: it runs last, joins the
  products onto one 30MIN `TIMESTAMP_MID` index with their
  provenance flags, and draws one overview figure per series. It **computes and
  corrects nothing** — a value in the merged table is exactly what its own
  notebook exported. Its `REGISTRY` is the one place a series is
  declared: the merge, the column check, the coverage table and the captions all
  read it, so adding a variable there is what makes it arrive everywhere.
  **It merges only the products already extended to `PERIOD_END`.** `PRODUCTS` is
  the subset of `REGISTRY` whose file stem ends in `PERIOD_LABEL` (`2026.09`), so at
  present `01`-`07`; `08`-`13` keep their entries, flag labels and descriptions,
  still name their `*_2025` files, and are left out. Extending one means changing
  its stem in `REGISTRY` and adding its figure cell (removed while it is out); a
  stem ending in neither period raises. Every merged product is asserted to end at
  `PERIOD_END`, and every code of a drawn flag to have a `FLAG_LABELS` entry. The
  2025 version of the notes on `07`-`13` is notebook version `5`. A
  multi-column product contributes **one entry per series a reader would
  analyse**, not one per column in its file — `09` five soil-moisture depths plus
  their homogenised twins, `10` the seven reconciled soil-temperature depths and
  **not** the eighteen individual channels, which are one sensor each and stay in
  their own notebook. Every entry needs its `MAY_HAVE_GAPS` reason if it can
  contain `NaN` and its `FLAG_LABELS` vocabulary for the flag drawn first.
  - **The record is being extended to 30 September 2026, notebook by notebook.**
    `01`-`07`, `99` and the LAE reference end there and carry the label `2026.09`;
    `08`-`13` and the unnumbered investigations still carry `2004-2025`
    names and read the **2025** files of their inputs, so they see neither the
    2026 data nor the changes made while extending (the HygroVUE10 era, the new
    `RH_T1_47_1_HOMOGENIZED`). Extending one means renaming it, pointing every
    path at the `2026.09` files and re-checking every statement and guard that
    assumed the record ends on 31 December.
  - **Two settings carry the end of the record.** `PERIOD_END = '2026-09-30
    23:45:00'` (`TIMESTAMP_MID` of the last record) is declared in the settings,
    used for the index and asserted at export (`export_df.index[-1] ==
    PERIOD_END`), because the file name claims it. `LAST_FULL_YEAR = 2025`
    (declared in `02`-`06`, not in `01`) keeps the partial 2026 out of every
    statistic that **compares calendar years** (annual means, Theil-Sen trends,
    era means, drift and year-on-year tables), because nine months without
    October-December are biased by season and read as a change. Counts, coverage
    and provenance tables keep 2026 and label it partial. A statistic over a fixed
    season can include the last year when that season is complete: `03`'s
    April-September ratios take 2026 and assert that `PERIOD_END` lies past
    30 September of its year, so moving the end earlier fails there rather than
    entering half a season.

## The GIN fieldbook

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
- **GIN registers no `TA`/`RH` device at `T1_47` before June 2026.** Neither the
  MP101A nor the CS215 was ever registered at that location. The first device
  entry there is the `ADD` of the HygroVUE10 (SN E6730) on 5 June 2026, followed on
  11 June by a change of its SDI-12 configuration ID together with the logger
  program; `04` asserts these are the only entries filed there. No entry removes
  the CS215 (it was never added), so the swap is dated by the raw 1-min `TA` gap
  11:10-11:31 that day and by the level change against Lägern, and `02`/`04` carry
  the HygroVUE10 era as source code `4`. The free text names both earlier probe
  families, but at other heights on the mast where they were also used, and names
  the CS215 at this logger only in a wiring repair years after 2016. So the
  MP101A → CS215 identification and its January 2016 date rest on the **logger
  programs** and on the step in the data, with no fieldbook corroboration at all.
  A fieldbook silence about a level is not evidence that nothing was mounted
  there. Where the fieldbook *does* speak it corroborates: the CNR4's first entry
  is 14 December 2021, the date `01` derives independently for the radiometer
  swap, and the two entries that bracket the CS215's excess heating (19 Sep 2024,
  intake tubing attached at the 47 m sonic; 16 May 2025, the inlet heating found
  melted and disconnected) are filed under the sonic and under no device at all,
  and neither names the temperature probe, which is the device-tag rule above once
  more. `02` asserts both entries and asserts that no CS215 is registered at
  `T1_47`, so a later export that adds one fails and gets read.

## The logger programs

The dataloggers' own programs say what a sensor was and how its raw signal was
converted, which the fieldbook usually does not. They live in the external data
folder beside `workflow/`, like the fieldbook:
`...\dataset_ch-lae_flux_product-data\csi_loggerscripts\` (the CR10X `.CSI`
programs, 2004-2006) and
`...\logger_scripts\ch-lae_idl_t1_47_1-Version_20160118\` (the CR1000 `.CR1`
program). They are what dates and identifies the 2016 `TA` change and give both
eras' calibration constants.

- **Declare the constant in the notebook, then verify it against the program when
  the program is there.** The external data folder cannot be assumed present: a
  notebook that only parses cannot run without it, and a reader of the published
  page sees no number, only the claim that one was read. So write each constant
  into the settings with a comment naming its source file, use *that* value
  everywhere downstream, and let the parser assert the declaration rather than
  supply it. Where the folder is missing, print that the constants are declared
  but unverified for this run and skip the parsing cells behind a
  `LOGGER_SCRIPTS_AVAILABLE` guard. Downstream results must never depend on
  whether the files happened to be present, or two runs of one notebook disagree.
  This is the same "a setting is a claim" pattern the date settings already use.
- **The fieldbook is the exception and stays a hard dependency.** Its content is
  quoted text rather than a handful of numbers, and it needs the redaction map,
  which must never live in this repo. A missing map still **raises**: carrying on
  with redaction disabled prints real names onto a public page.

- **They are signed, so they are a personnel record too.** Anything printed from
  a logger program passes through the same `redact_people()` and
  `audit_unmapped_names()` nets as the fieldbook.
- **A program names the channel, not the column.** The raw pre-2016 meteo stream
  is headerless CR10X *array* files (`logger<date>.aNN`), so a column name such
  as `AirT_C` comes from the acquisition-side configuration and will not be found
  in the program; match on the channel and its multiplier instead.
- **There is more than one CR10X program, and reading all of them is the point.**
  Six `LAEGEREN.*.CSI` files span 2004-2006. The three from 2004 measure **no**
  radiometer channel at all — their comments record that those channels then
  carried a PAR sensor. The CNR1 instruction first appears in the program dated
  **18 August 2005**, which measures all four channels (`Kin`, `Kout`, `Lin`,
  `Lout`). The programs of 14 September 2005 and 24 May 2006 carry a conversion
  for only three, because `Kout` lost its own instruction to the two-repetition
  `Ex-Del-Diff` described above.
  - This corrects an earlier version of this file, which put the first CNR1
    instruction in the **14 September 2005** program. What that program changed is
    the relay, moving `Lout` and `Kout` onto DIFF3 and DIFF4; a comment in the file
    says so. 14 September remains the day the tower `SW_IN` *record* begins, which
    is a fact about the data and not about the program. Anything asserting the
    program date — `01` does — needs re-reading against this.
  - A date derived from a program and confirmed by the data is worth an assertion,
    but assert the claim the programs actually support.
- **Parse the constants out of the program text; do not read them off once.**
  `01` extracts the multiplier and offset from every program that measures the
  sensor and asserts they are all identical (`99.7009` and `0`, i.e. 1000/10.03
  for a Kipp & Zonen CNR1, SN 020484 — the same instrument before and after 2016).
  The two program languages write the same two numbers differently, so the parser
  matches each shape separately and **raises** rather than returning an empty dict
  that would agree with anything. Parsing now checks the declared constant above
  rather than replacing it, which makes it a stronger test: it verifies the number
  a reader can actually see.
- **A storage location is named twice, and only one of the two carries the
  conversion.** A CR10X program names a location in the instruction that measures
  into it, and again in the `Average` instruction that writes it to the data
  table. Only the first is followed by `Mult` and `Offset`. A pattern that selects
  the location alone therefore matches twice and a strict count check fires on a
  perfectly normal program — which is how `12` and `13` both failed. Require
  `Mult` inside the block, keep the count check strict, and add a control that the
  filter can reject everything, so a layout change fails loudly instead of
  silently selecting nothing.
- **One instruction can fill several locations.** From 14 September 2005 the
  outgoing pair is a single `Ex-Del-Diff` with two repetitions, so the outgoing
  shortwave location follows the outgoing longwave one and has **no instruction of
  its own**. Assert the constants across all locations of all programs rather than
  looking one channel up, and report the per-program channel layout so a missing
  channel reads as a layout fact rather than as a missing measurement.
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
  read the written file back → runtime footer. Sections carry emoji headers; the
  `📊 Plot:` / `📋 Table:` subheading rule is in the root `CLAUDE.md`.
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
  error, so the pre-2016 record reads ≈ 1.3 °C too cold. The same name (and
  `RH_T1_47_1`, from the same probe) then carries two further states of the CS215
  and, from 5 June 2026, a Campbell HygroVUE10 with unchanged database tags (see
  the five probe states below); `PREC_TOT_T1_47_1`
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
  but an independent co-located sensor where one does (`02` and `04` at 2016, both
  against NABEL, see below), and a nearby station where only that spans it (`02`
  and `04` at June 2026, against Lägern). Never let a name imply a continuity the hardware does
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
  extrapolated years land within 0.03 °C of the earlier era's own level. `04`'s
  2016 `RH` transfer follows the same arrangement (NABEL fit, Lägern score) and
  also prints the transfer fitted against Lägern beside it, because the two
  disagree (about 0.5 %RH on average, more near saturation) and that difference
  is the uncertainty of the correction. Where **only one reference spans a
  change** (NABEL ends in 2018, so the 2026 probe change has only Lägern), a
  **month hold-out** takes the second reference's place: each month is left out,
  the transfer refitted on the rest, and the month predicted. Say in the
  limitations that this tests transfer to unseen data, not agreement with an
  independent instrument.
- **The 47 m T/RH probe has five states, and `02` and `04` share them** (one probe
  call delivers `TA_T1_47_1` and `RH_T1_47_1`; `04` declares the same timestamps
  and asserts its `FLAG_RH_T1_47_1_SOURCE` equals `02`'s `FLAG_TA_T1_47_1_SOURCE`):
  - code `1` Rotronic MP101A, analog, to 31 Dec 2015, then the changeover outage
    to 21 Jan 2016 (code `2`, neither era);
  - code `0` Campbell CS215, SDI-12, the reference level of both homogenisations;
  - code `7` CS215 with excess daytime heating from 22 Oct 2024 (`EXCESS_START`),
    which follows the 19 Sep 2024 installation of intake tubing at 47 m. The
    excess grows over weeks, so its onset is dated by a rule on the daytime
    excess over the 35 m sensor, not by the fieldbook date. In `02` it gets the
    normal CS215's shield term, which under-corrects it in sun; it is flagged,
    not corrected further;
  - code `6` CS215 after the probe was handled on 16 May 2025 (`RESET_START`):
    the daytime shield excess is gone, so it gets no shield term, only a constant
    night term fitted over the months in which every radiation class is populated
    (March-September);
  - code `4` Campbell HygroVUE10 from 5 Jun 2026 11:45 `TIMESTAMP_MID`
    (`HV_START`).
  Code `5` is the handling half-hour (16 May 2025 09:30-10:00) and the swap
  half-hour (5 Jun 2026 11:00-11:30): neither is a stable probe state, so both are
  removed in *Corrections*, modelled or reconstructed with the period **before**
  them, and homogenised with it. Codes `2`, `3` (before the tower record) and `5`
  are what no instrument stands behind. Do not confuse source code `5` with `02`'s
  `ISFILLED` code `5` (reconstructed from NABEL); the two flags have separate
  vocabularies.
  - **The evidence pattern that dated and attributed these states is reusable.**
    A second sensor on the **same tower** (`TA_T1_35_1`, raw 1-min, no screened
    version) is the witness: the pair 47 m - 35 m dates a change at the 47 m probe,
    and the pair 35 m - Lägern, which holds no 47 m measurement, cannot step at
    it, so a step in the first pair and not the second puts the change on the
    probe and not on the reference. The **raw 1-min record** dates handling to the
    minute (a jump of about 5 °C between 09:32 and 09:42 that the 35 m sensor does
    not show; a gap 11:10-11:31 at the swap), which the 30MIN product cannot. The
    fieldbook then confirms rather than drives, as above.
  - **Check a reference period for state changes inside it.** The HygroVUE10 was
    first compared with the CS215 over the summers 2022-2025, which mixed the
    post-May-2025 state (code `6`) into "the normal CS215". It is now
    `HV_CS215_YEARS = [2022, 2023, 2024]`, code `0` only, diive screening
    throughout. Before a period serves as the reference level of a transfer, list
    every state change known to fall inside it and assert the sample holds one
    state; `04`'s `CS215_LAST_NORMAL_YEAR` (the year before `EXCESS_START`)
    applies the same rule to the era-mean transfer and the drift.
  - **An established instrument change is corrected at night too**, even when its
    night difference is within the year-to-year scatter of the reference level.
    The change is established by independent evidence (fieldbook, raw-data gap or
    jump, a radiation-dependent step), so leaving the night alone asserts that
    the instrument did not change at night, which nothing supports. The scatter
    is reported beside the term as its uncertainty, and the limitations say the
    term is small against it. This applies to `02`'s night terms of code `6` and
    of the HygroVUE10.
- **`02` brings the HygroVUE10 onto the normal CS215 level, then treats it as the
  CS215.** The transfer is fitted against Lägern on two season-matched samples:
  the HygroVUE10 from `HV_FIT_START` (12 Jun 2026, the day after the SDI-12
  configuration change; 5-11 June are transitional and enter no fit) to
  `PERIOD_END`, and code `0` on the same calendar dates of `HV_CS215_YEARS`. It has
  two terms: a radiation term, the difference of the two samples' residual curves
  against tower `SW_IN` on the shield term's own `shield_basis`, with its
  zero-radiation part removed and the driver clipped to the range both samples
  cover; and a constant night term. It is scored by the month hold-out. The
  homogenised HygroVUE10 value is then corrected as a CS215 value, i.e. the shield
  term of step 10 is applied on top, so every era ends on the same reference (the
  MP101A's shield behaviour at the CS215 night level). The measured column keeps
  the HygroVUE10 as measured. The fit rests on one summer; its winter behaviour
  is untested and it is to be refitted once the record holds a winter.
- **`04` now exports `RH_T1_47_1_HOMOGENIZED`, on the CS215 level.**
  - **MP101A era (codes `1`, `2`, `3`, by timestamp before `BREAK`):** raised by a
    humidity-dependent transfer fitted against NABEL **locally at the break**, the
    MP101A over 2013-2015 against the CS215 from February 2016 to the end of
    NABEL's independent period (July 2018; from August 2018 the NABEL `RH` column
    copies the tower), binned on the **reference** humidity (binning on the
    tower's own reading manufactures a slope by regression to the mean), and
    scored against Lägern. The transfer fitted on the **era means** was tried
    first and is unstable: halves of each era disagree by up to the size of the
    correction, because the MP101A drifts down and the CS215 up against Lägern,
    each by more over its own era than the step between them. Close to the break
    the drift has had little time to act, and the local transfer is stable under
    shorter windows. The drift inside each era is documented and **not corrected**
    (unattributed after 2018; fitting it away would replace the measurement with
    the reference), so neither column is fit for multi-decade trends.
  - **CS215, codes `0`, `6`, `7`, and the probe half-hours (code `5`):** copied
    unchanged. In `04`'s step 11, vapour pressure shows that the May 2025 change in
    `RH` is one of the probe's temperature, not of its humidity element, so
    correcting it would be correcting `TA`, which is `02`'s job.
  - **HygroVUE10 era (code `4`):** transferred in **vapour pressure**, because a
    probe-temperature error moves `RH` and leaves `e` in place, and the two probes
    differ in their radiation behaviour; a transfer in %RH would mix the humidity
    elements with the temperature sensors. `e` comes from each sensor's own `RH`
    and `TA` (tower `RH` with `02`'s measured `TA`, Lägern `RH_LAE_MS` with
    `TA_LAE_MS`), `Delta_e` is fitted linear in `e_LAE` (the code decides linear
    against constant from the bin spread and found linear) against the same
    CS215 summers 2022-2024, and the result is converted back with **`02`'s
    homogenised `TA`**: `RH_HOM = 100 * (e_47 - Delta_e) / es(TA_HOM)`, capped to
    `[0, 100]`. So from June 2026 the homogenised `RH` refers to a temperature
    without the shield's radiative excess and lies above what a CS215 would read
    in sun; at night they agree. This is why `04` reads `02`'s product and `02`
    must run first.
  - `04`'s reconstruction offsets (NABEL, then Lägern) are fitted **within each
    of the five era/state labels**, so a reconstructed record sits on its own
    probe's level, and each probe half-hour takes the label of the era before it.
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
  tower pyranometer rising ~3 % from 2013, and `PPFD_IN` falling from 2022 to 2024 to
  ~7 % below its 2006-2010 level, flat since (2025 and 2026 within 0.4 % of 2024). Both develop over years rather than stepping at a date, so
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
  **A guard placed before the variable it uses is defined passes only when the
  cells were run out of order**: in an interactive session the name already
  exists from a later cell, so the assertion runs and passes, and a fresh
  top-to-bottom run raises `NameError`. A static check of definition order found
  `BREAK` (defined in step 4) used by a guard in step 2 of `02`. When adding a
  guard to an early cell, check where every name it reads is first assigned, and
  move the guard or the definition; dates a guard needs early belong in the
  settings, which is why `04` declares the 2024-2026 probe dates there.
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
  `02` gained an `ISFILLED` code `5` for records reconstructed from the co-located
  NABEL sensor at 49 m, because the timestamp-only fallback that had been filling
  them (code `2`) produces climatology, not weather. `02` is also gap-filled *and*
  inhomogeneous, so it exports four columns on the `08`/`09` pattern — measured,
  `ISFILLED`, `_HOMOGENIZED`, and a `SOURCE` flag naming the probe and its state
  (the eight codes of the five probe states above).
  `04` is complete but not modelled: gaps are reconstructed from another
  measurement of the same quantity (a per-month offset within the era/state), and
  it exports four columns too: `RH_T1_47_1` (every era as measured),
  `FLAG_RH_T1_47_1_MISSING` (`0` measured, `1` never measured, `2` removed here,
  `3` from NABEL, `4` from Lägern; `1` and `2` stay in the vocabulary but do not
  occur, because the two references cover every gap), `RH_T1_47_1_HOMOGENIZED`
  and `FLAG_RH_T1_47_1_SOURCE` with `02`'s codes. Its file keeps the name
  `04_METEO_RH_CORRECTED_...`. `05` is exported as measured with no flag and no
  homogenised column, although it steps by about 0.09 kPa at January 2016: one
  part in a thousand, documented with the correction a user can apply. `06` is
  exported as measured with no `ISFILLED` column but a `SOURCE` flag naming the
  radiometer and calibration factor (the 7 June 2016 factor correction, the
  CNR1 → CNR4 changeover); its step is flagged, not removed. `07` is
  computed by formula from finished products and its flag says what it was
  computed *from*. It exports `VPD_T1_47_1` from the measured `TA`/`RH` pair and
  `VPD_T1_47_1_HOMOGENIZED` from the homogenised pair, never a mixed pair: the
  homogenised `TA` with the measured `RH` (its version `3`) corrects one of two
  opposing MP101A errors and stepped most at 2016 of the bases `07` scores. `08` and `09` likewise export a **second, derived value
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
  records. `02` therefore fits five periods, `P1` (MP101A, with NABEL), `P2`
  (CS215 to the end of NABEL), `P3` (CS215 without NABEL, to the handling record of
  16 May 2025, codes `0` and `7`), `P3b` (code `6`, to the swap record) and `P4`
  (HygroVUE10), and its four boundaries exist for different reasons: three are
  instrument changes (`BREAK`, `RESET_START`, `HV_START`) and one is the loss of a
  driver where the NABEL reference ends. Say which boundary is which; a reader
  assumes they are all hardware. A gradual change is **not** a boundary: the onset
  of code `7` grows over weeks, so there is no record at which to split, and its
  gaps are filled by `P3`. Each probe half-hour belongs to the period before it.
  The period cell asserts the periods tile the record exactly once, that none
  spans any of the three changes, and that the short `P3b`/`P4` still hold enough
  measured records for a model of their own (fewer must be said, not merged away).
- **An assertion states what a correction does, so changing the correction
  breaks it — and that is the system working, not an obstacle.** Adding the
  shield term to `02` fired three separate guards that all asserted the later era
  is never modified: `02`'s break-year check, `02`'s export check and the
  overview's integrity check. Each was **re-derived** to describe two terms (the
  later era now carries exactly the radiative excess; the correction after the
  break is never positive, is exactly zero in the dark, and takes many distinct
  values rather than behaving like a second constant). None was relaxed. A guard
  that fires on a deliberate change has just proved it can fire. The same applies
  downstream: `06` relies on the two `TA` columns differing at night by one
  constant per era, and its guard now checks that per source code, read from
  `02`'s `FLAG_TA_T1_47_1_SOURCE`: exactly zero on codes `0`/`7`, one constant
  each on `1`, `6` and `4`. A new night term in `02` must arrive with its code in
  that guard.
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

