# CLAUDE.md

## What this repo is

Methods documentation for the **CH-LAE flux product** — an eddy-covariance
ecosystem-flux dataset for the mixed forest site CH-LAE. The actual flux
computation and meteo screening happen in a separate offline pipeline; this
repo's job is to **narrate the methods** used to produce the shared dataset and
publish them as a website.

## Layout

- `docs/` — the published Quarto website, with a single config file
  `docs/_quarto.yml`. This is the reader-facing artifact and is kept clean. Only
  pages listed in `_quarto.yml`'s `website.sidebar.contents` are in the nav.
  Build output lands in `docs/_build/html/` (gitignored). The site mark
  (`logo.*` for the sidebar, `favicon.*` for the tab icon) is the same artwork,
  so the two must be regenerated together.
- `workflow/` — the real working notebooks and scripts, organized by numbered
  stage. This is research scratch space and is **not** built into the book. Two
  reserved folders: `_archive/` (dead/experimental, mirrors the stage layout)
  and `_templates/` (reusable notebook templates).
- `PLAN.md` — what the dataset is to contain, what exists, and what is missing:
  the variable inventory, the flux chain's state per level, the ordered list of
  what to do next, and the open questions blocking scope decisions. Read it
  before starting new work and update it when a stage's state changes. It sits at
  the root rather than in `docs/` because Quarto would publish it; settled
  sections move to `docs/Overview.md` and `docs/Variables.md` and are deleted
  from `PLAN.md`, so the two never state the same thing twice.

## Where the detailed guidance lives

The bulk of this project's conventions are scoped to one part of the tree and
live in a `CLAUDE.md` beside the work, so they load when that area is opened
rather than in every session. Read the relevant one before working there.

- `workflow/00_L0_checks/CLAUDE.md` — Level-0 preliminary flux calculation, the
  EddyPro per-setup-period runs, and the EC setup table in `docs/Yearly_Notes.md`
  (the analysers, the gaps and their causes, time lags, unusable periods).
- `workflow/10_METEO/CLAUDE.md` — the meteo stage: its three substages, the GIN
  fieldbook and its redaction rules, the logger programs, and the full structure
  and checking conventions of a product notebook.
- `.claude/rules/docs.md` — the Quarto website: build mechanics, notebook
  staging, markup conventions, and how the narrative and per-variable pages are
  organized. (It lives here rather than as `docs/CLAUDE.md` because Quarto
  renders every `.md` under `docs/` onto the public website.)
- `.claude/skills/site-template/SKILL.md` — reusing this repo as the template for
  another site.

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

## Writing register

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

## Hard rules

- **Never commit or push without being asked.** `git commit` and `git push` run
  only on an explicit request; never as the closing step of a task, and never to
  tidy up a working tree. Staging, diffing and reading the log need no request.
- **Never build the docs** (`quarto render`/`quarto preview`, or
  `build_notebooks.py`) unless explicitly asked. A full site build is
  `build_notebooks.py` (stage) **then** `quarto render docs` **then**
  `build_notebooks.py --clean`, in that order (or just run `deploy.ps1`).
- **Never write a real person's name into this repo.** The GIN fieldbook and the
  logger programs are personnel records and these notebooks render to a public
  website, so every quoted string is redacted through `redact_people()`, and
  names in prose and code comments count too — use a pseudonym or an invented
  name. `python check_no_names.py` scans the repo and exits non-zero; run it
  before publishing. The full redaction machinery is documented in
  `workflow/10_METEO/CLAUDE.md`.
