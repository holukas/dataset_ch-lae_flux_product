# CLAUDE.md

## What this repo is

Methods documentation for the **CH-LAE flux product** — an eddy-covariance
ecosystem-flux dataset for the mixed forest site CH-LAE. The actual flux
computation and meteo screening happen in a separate offline pipeline; this
repo's job is to **narrate the methods** used to produce the shared dataset and
publish them as a website.

## Layout

- `docs/` — the published Jupyter Book. Curated MyST Markdown narrative pages
  (`*.md`), `images/`, `references.bib`, `_config.yml`, `_toc.yml`. This is the
  reader-facing artifact and is kept clean. Only files listed in `_toc.yml` are
  built.
- `workflow/` — the real working notebooks and scripts (organized by stage:
  `00_L0_checks/`, `10_METEO/`, `20_MERGE_DATA/`,
  `30_FLUX_PROCESSING_CHAIN/`, `90_DATASET_OVERVIEW/`). This is research scratch
  space and is **not** built into the book.

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
