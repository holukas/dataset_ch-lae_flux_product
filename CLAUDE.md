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

- Jupyter Book 2.x (MyST engine, not the old Sphinx-based v1). Single config
  file `docs/myst.yml` (replaces v1's `_config.yml` + `_toc.yml`): project title,
  authors, `toc`, `bibliography`, and `site` template/logo all live there.
- Build with `jupyter book build --html docs` (or `jupyter book start docs` for
  the live dev server). Output goes to `docs/_build/`.
- Notebook execution is off by default for committed `.ipynb` outputs; the heavy
  pipeline runs offline, the book only narrates.
- Mermaid diagrams are native in MyST (` ```{mermaid} ` directive) — no
  sphinxcontrib-mermaid extension needed.
- Published to GitHub Pages via `ghp-import` (point it at `docs/_build/html`).
  For correct asset paths under the project subpath, set `BASE_URL` at build
  time, e.g. `BASE_URL=/dataset_ch-lae_flux_product jupyter book build --html docs`.
- Pages are plain `.md` and editable in Obsidian. Use standard Markdown links and
  MyST cross-references — **not** Obsidian `[[wikilinks]]`/`![[embeds]]`, which
  the book won't resolve.

## Hard rules

- **Never run `git commit` or `git push`.** The user does all committing.
- **Never build the book** (`jupyter book build`) unless explicitly asked.
