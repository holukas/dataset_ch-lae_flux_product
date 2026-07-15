# CLAUDE.md

## What this repo is

Methods documentation for the **CH-LAE flux product** — an eddy-covariance
ecosystem-flux dataset for the mixed forest site CH-LAE. The actual flux
computation and meteo screening happen in a separate offline pipeline; this
repo's job is to **narrate the methods** used to produce the shared dataset and
publish them as a website.

## Layout

- `docs/` — the published Jupyter Book. Curated MyST Markdown narrative pages
  (`*.md`), `images/`, `references.bib`, and `myst.yml` (single config). This is
  the reader-facing artifact and is kept clean. Only files listed in `myst.yml`'s
  `toc` are built.
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

## Environment

- Managed with **uv** (not poetry). Python **3.12**.
- `uv sync` to set up; `uv run <cmd>` to run inside the env.
- Local editable path deps via `[tool.uv.sources]`: `diive` (`../../diive`),
  `dbc-influxdb` (`../../poet/dbc-influxdb`).

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
- Quarto is **not** a pip/uv library — it's a standalone binary. It's vendored
  into the env via the `quarto-cli` dev dependency, so run it as
  `uv run quarto ...`.
- Build with `uv run quarto render docs` (or `uv run quarto preview docs` for the
  live dev server). Output goes to `docs/_build/html/`.
- **Notebooks** (`workflow/**/*.ipynb`) are published as standalone HTML under
  `docs/_build/html/notebooks/`, mirroring the `workflow/` tree, by
  `build_notebooks.py` (repo root; `uv run python build_notebooks.py`). It uses
  **nbconvert**, never executes the notebooks (committed cell outputs only), and
  skips anything with a `_`-prefixed path component (`_archive/`, `_templates/`,
  `_create_readme.ipynb`, `_TEMPLATE*`). It writes into the site's output tree, so
  run it **after** `quarto render docs` (which cleans `docs/_build/html/`). The
  narrative pages link to these at `.../notebooks/<stage>/<name>.html`.
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
- Pages are editable in Obsidian. Use standard Markdown links and Quarto
  cross-references — **not** Obsidian `[[wikilinks]]`/`![[embeds]]`, which the
  site won't resolve.

## Hard rules

- **Never run `git commit` or `git push`.** The user does all committing.
- **Never build the docs** (`quarto render`/`quarto preview`, or
  `build_notebooks.py`) unless explicitly asked. A full site build is
  `quarto render docs` **then** `build_notebooks.py`, in that order.
