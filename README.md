# dataset_ch-lae_flux_product

Methods documentation and processing notebooks for the **CH-LAE flux product**,
the PI dataset of the mixed forest station
[CH-LAE (Lägeren)](https://www.swissfluxnet.ethz.ch/index.php/sites/site-info-ch-lae/).
The site is part of [Swiss FluxNet](https://www.swissfluxnet.ethz.ch/), operated
by the [Grassland Sciences Group, ETH Zurich](https://gl.ethz.ch/).

**Published site: <https://holukas.github.io/dataset_ch-lae_flux_product/>**

**Author**: [Lukas Hörtnagl](https://gl.ethz.ch/people/person-detail.lukas.html)

> **The dataset is in preparation.** Both the data and this documentation are
> work in progress and subject to change. Please contact the author before using
> the data.

## Scope

The dataset comprises ecosystem fluxes measured by the eddy covariance method
(CO<sub>2</sub>, H<sub>2</sub>O, H), meteorological data and management
information for 2004–2025. Two releases are in preparation: `FP2026.1`
(2016–2025, the enclosed-path LI-7200 era) and `FP2026.2` (2004–2025, which
supersedes and re-includes the first).

The meteorological part currently comprises thirteen products: the four radiation
components (`SW_IN`, `SW_OUT`, `LW_IN`, `LW_OUT`), `PPFD_IN`, `TA`, `RH`, `VPD`,
`PA` and `PREC` at the 47 m tower level, and at the forest floor the soil heat
flux `G` (three plates), soil water content at five depths and soil temperature
at seven. Each product is one file per variable, carrying its values and a
provenance flag that states, half hour by half hour, whether a value was
measured, corrected, reconstructed or modelled. A final merge step joins them
into one wide table and writes a description of that table beside it, so a
recipient of the data folder can read what they have without finding this
website first.

This repository holds the **methods narrative and the notebooks that produce the
product**. The flux computation itself (EddyPro) and the meteo screening runs
happen in a separate offline pipeline; what is documented here is how their
output is checked, corrected, merged and exported.

## Layout

| Path | Contents |
| --- | --- |
| [`docs/`](docs/) | The reader-facing [Quarto website](https://holukas.github.io/dataset_ch-lae_flux_product/): narrative pages, per-variable meteo pages, the data-dashboards page, the flux-processing-chain levels, instrumentation and site info. Single config file [`docs/_quarto.yml`](docs/_quarto.yml). |
| [`workflow/`](workflow/) | The working notebooks and scripts, by numbered stage. Research scratch space, rendered onto the site as a notebook appendix but not part of the curated narrative. |
| `workflow/_archive/`, `workflow/_templates/` | Reserved: dead or experimental work (mirroring the stage layout), and reusable notebook templates. Both are excluded from the site build. |

### Workflow stages

| Stage | Purpose |
| --- | --- |
| `00_L0_checks/` | Level-0 preliminary flux calculation: merge the EddyPro per-setup-period runs, then check fluxes, wind direction and time lags per instrument. |
| `10_METEO/` | Meteo, in three substages — `10_REFERENCE/` (MeteoSwiss and NABEL reference series), `20_SCREENING/` (per-variable, per-sensor stepwise screening), `30_PRODUCTS/` (thirteen product notebooks `01`–`13`, one per variable, joined by `99` into the merged file and its information file) — plus `40_EXPORTS/` (the EddyPro biomet file). |
| `20_MERGE_DATA/` | Merge Level-1 fluxes with the meteo product, per instrument. |
| `30_FLUX_PROCESSING_CHAIN/` | Self-heating correction, u\* threshold detection, and the Level-3.3/4.1 chain runs. Kept on its own older internal numbering. |
| `90_DATASET_OVERVIEW/` | Dataset-wide overview notebooks, and the two generators for the standalone HTML products: 23 meteo dashboards, one per variable or soil depth, and the calendar explorer. |

Stages that process both analysers split into `IRGA72/` and `IRGA75/`
subfolders.

### Data files live outside this repository

Only code, prose and figures are tracked here. The data the notebooks read and
write is too heavy for git and lives in an untracked folder:

```
F:\Sync\luhk_work\dev-data\datasets-data\dataset_ch-lae_flux_product-data\workflow\
```

That tree is **mirrored 1:1** with `workflow/`: same stage folders, same
instrument subfolders, and a data file carries the same numeric prefix and
relative path as the notebook that produces it. Figures stay in the repo
(`docs/images/` for published figures, a `figures/` subfolder under the relevant
stage for working plots); only `*.parquet`, `*.csv` and `*.pkl` go to the
external folder, along with the raw inputs (`0_data/`) and the `tests/` outputs.

## Setup

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12–3.13. The environment
also vendors Quarto (as the `quarto-cli` dev dependency), so no separate Quarto
installation is needed.

```bash
uv sync
```

Note that [`diive`](https://github.com/holukas/diive) is declared as an editable
path dependency at `../../diive`, so a sibling checkout of that repository must
exist next to this one. Some notebooks additionally read the InfluxDB database
through `diive`'s `InfluxIO`.

## Building the site

Three PowerShell wrappers at the repo root drive the build; they exist so the
step order does not have to be remembered.

```bash
./preview_fast.ps1
```

Live-reload dev server for the narrative pages only — no notebooks, so
`/notebooks/` links will not resolve. This is the fast editing loop.

```bash
./preview_full.ps1
```

Full local build (website **and** notebooks) served over real HTTP, so search
and the notebook pages work. The check to run before deploying.

```bash
./deploy.ps1
```

The single deploy entry point: stages the notebooks, renders the site, clears
the staging, builds the dashboards, and publishes `docs/_build/html` to the
`gh-pages` branch with `ghp-import`. `-Preview` builds and serves,
`-NoPublish` builds only, `-NoDashboards` skips the dashboard and calendar
steps. It touches only `gh-pages`, never the source branch or working tree.

Under the wrappers the manual sequence is, in this order:

```bash
uv run python build_notebooks.py && uv run quarto render docs && uv run python build_notebooks.py --clean
```

`build_notebooks.py` is a **staging** step, not a converter: it copies the real
notebooks into `docs/notebooks/` (gitignored build inputs), disables execution
for that folder so Quarto shows the committed outputs and never runs a cell, and
generates the notebook index page: one table per workflow folder, giving each
notebook's number, title and file name. Rendering therefore gives the notebooks
the site theme, search, anchored headers and a table of contents, exactly like
the narrative pages.

## Helper scripts

| Script | Purpose |
| --- | --- |
| [`build_notebooks.py`](build_notebooks.py) | Stage `workflow/**/*.ipynb` into `docs/notebooks/` for the Quarto render; `--clean` removes the staging. |
| [`build_fieldbook_md.py`](build_fieldbook_md.py) | Render the GIN fieldbook export as one readable, redacted markdown file. Writes beside the export in the external data folder, never into this repository. |
| [`check_no_names.py`](check_no_names.py) | Fail if any name from the fieldbook redaction map appears anywhere in the repository. Run before publishing. |

## Conventions

The bulk of the conventions are scoped to one part of the tree and live in a
`CLAUDE.md` beside the work rather than in one long document:

- [`CLAUDE.md`](CLAUDE.md) — repository-wide rules, layout and writing register.
- [`workflow/00_L0_checks/CLAUDE.md`](workflow/00_L0_checks/CLAUDE.md) — the
  Level-0 checks, the EddyPro per-setup-period runs, and the EC setup table.
- [`workflow/10_METEO/CLAUDE.md`](workflow/10_METEO/CLAUDE.md) — the meteo stage,
  the GIN fieldbook and its redaction rules, the logger programs, and the
  structure of a product notebook.
- [`.claude/rules/docs.md`](.claude/rules/docs.md) — the Quarto website: build
  mechanics, notebook staging, markup conventions, and how the pages are
  organized. (It lives there rather than under `docs/` because Quarto would
  render it onto the public website.)

Two rules are worth stating up front, because both are enforced:

- **No real person's name goes into this repository.** The GIN fieldbook and the
  logger programs are personnel records and these notebooks render to a public
  website, so quoted strings are redacted through `redact_people()`, and names
  in prose and code comments count too. `check_no_names.py` scans the repository
  and exits non-zero. Published credit — acknowledgements, citations, photo
  credits, the author byline — is deliberate and exempt.
- **Filenames** carry no spaces and no `+` (use `_and_`).

## Licence

[GNU General Public License v3.0](LICENSE).
