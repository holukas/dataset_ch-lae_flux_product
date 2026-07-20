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

- **`10_REFERENCE/`** — external reference data, one notebook per station. These
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
  - **Two stations, and they are not interchangeable.** `LAE` (Lägern, 2.5 km,
    845 m) is the full weather station and covers `TA`/`RH`/`PA`/`SW_IN` plus dew
    point, vapour pressure, sunshine and wind over 2004-2025 — but measures
    **no precipitation and no longwave**. `OED` (Ehrendingen, 3.8 km, 428 m) is
    precipitation-only. So `06` (`LW_IN`) has no MeteoSwiss reference at all.
  - **Year labels come from the last bin's start, not its label.** 10-min values
    are end-of-interval, so the final bin of 31 Dec is labelled 00:00 on 1 Jan,
    and the local-time shift pushes it again. Both traps silently misname the
    export `..._2004-2026`.
- **`20_SCREENING/`** — quality screening of the site's own measurements, one
  subfolder per variable (`SW_IN/`, `TA/`, `RH/`, `PA/`, `PPFD_IN/`, `LW_IN/`,
  `PREC/`, `NETRAD/`, `SWC/`). These write to **InfluxDB**, not to files, so the
  stage produces almost no data files. Some read a product from
  `10_REFERENCE/` — that is the edge that puts reference before screening.
- **`30_PRODUCTS/`** — one notebook **per meteo variable**, numbered in the order
  they may depend on each other: `01` `SW_IN`, `02` `TA`, `03` `PPFD_IN`,
  `04` `RH`, `05` `PA`, `06` `LW_IN`, `07` `VPD`. The order is real, not
  decorative — `02` and `03` read `01`, and `07` reads `01`/`02`/`04`. Each
  downloads the screened series from the database, corrects it, and writes a
  single product to the external data folder. The notebook name is a prefix of
  the file it writes (`02_METEO_TA_2004-2025.ipynb` →
  `02_METEO_TA_GAPFILLED_2004-2025.parquet`), so code and data line up by eye.
  No verb in the notebook name — the folder already says what these do.

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
  notebook works on `TIMESTAMP_MID` from that point on.
- **Data versions:** the same measurement exists under `meteoscreening_mst`
  (older) and `meteoscreening_diive` (newer). Merging them is a merge of two
  *screenings of one measurement*, not a gap-fill — use `combine_first` so a
  future overlap resolves deterministically instead of duplicating timestamps.
  The `mst`/`diive` boundary sits at 2021/2022 and is where unit and raw-source
  breaks hide; check the database's own unit tag (`show_field_overview`) against
  the magnitude of the data, and prove the exported series does not step there.
- **Guards:** a helper that can silently do nothing gets a **negative control**
  cell that feeds it bad input and asserts it raises. Sanity checks assert
  rather than assume (continuous index, no duplicates, physical range).
- **The 2012 faults are site history and recur in every variable:** the
  17 Aug 2012 logger clock error (+15.5 h shift of one block), the late-July/
  August power supply failure, and the Oct/Nov storm damage. Windows are always
  expressed on the **corrected** time axis. Copy the shared windows only when
  the variable has no better evidence — where an independent sensor exists,
  derive the variable's own windows from its residual and say so.
- **Completeness is per variable, not a house style.** `01`-`03` are gap-filled
  products and carry an `ISFILLED` flag naming the model that produced a value.
  `04` is reconstructed from a co-located sensor (a transfer between two
  measurements of the same quantity) and carries a `FLAG_<var>_MISSING`
  provenance flag: `0` measured, `1` never measured, `2` removed here,
  `3` reconstructed. `05`/`06` are exported as measured with no flag. A
  notebook that exports gaps says so in a closing note for downstream users.
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
