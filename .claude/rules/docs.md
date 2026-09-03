---
paths:
  - "docs/**"
---
# Docs (Quarto website)

> Guidance for the published site under `docs/`. The writing-register rule applies
> to notebook markdown as well and therefore stays in the root `CLAUDE.md`, together
> with the rule never to build the docs unless asked.

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
- Three `include-after-body` partials (all listed in `_quarto.yml`) apply
  client-side tweaks Quarto has no option for. `_mermaid-zoom.html` makes every
  Mermaid diagram pannable and zoomable: the flowcharts on `Meteo_Product_Chain.qmd`
  and `FPC.qmd` are wider than the article column, so Quarto scales them down until
  the labels are hard to read, and `lightbox: auto` cannot help because it works on
  `<img>` elements while a mermaid cell renders to an inline `<svg>`. It wraps each
  diagram in a drag-to-pan viewport with zoom buttons, deliberately requiring
  **ctrl/cmd + wheel** to zoom so a reader scrolling past a diagram is never trapped
  inside it, and carries no external library. Mermaid renders after the partial runs
  and Quarto exposes no hook for it, hence the MutationObserver. The other two move
  things into the **right ("On this page") sidebar**: `_theme-toggle.html` relocates the **light/dark
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


