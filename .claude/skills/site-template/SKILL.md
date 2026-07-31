---
name: site-template
description: >-
  How to reuse this repository as the template for the flux-product documentation of
  another eddy-covariance site. Lists the site-specific bindings that must change
  (Quarto config, docs content and site mark, pyproject metadata, deploy strings,
  external data folder, workflow stages) and what is site-agnostic and copied as-is.
  Use when setting up a new site repo, porting this machinery elsewhere, or asking
  which parts of this repo are site-specific.
---

# Reusing this repo as a template for another site

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
  be `.qmd` (see `.claude/rules/docs.md`). The mark depicts **this** site's stand — spruce and beech
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
  too — every site needs the database download (the reason is in the `pyproject.toml` comment beside it).
- **`deploy.ps1`** — the hard-coded published URL and repo name appear only in
  comments and `Write-Host` messages; the actual push is generic
  (`origin`/`gh-pages`). Update the strings for tidiness.
- **`README.md`** — repo name/title.
- **External data folder** — the untracked
  `...\dataset_<site>_flux_product-data\workflow\` path (see "Code/data layout
  and conventions" in the root `CLAUDE.md`).
  One per site; the two `workflow/` trees still mirror 1:1.
- **`workflow/` stages** — the numbered stages (`00_/10_/20_/30_/90_`) are the
  shared pipeline shape and carry over. Instrument subfolders (`IRGA72/`,
  `IRGA75/`) and the Stage-30 internal numbering are site-specific — a site with
  different or single sensors won't have those exact subfolders.

