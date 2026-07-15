#!/usr/bin/env pwsh
#
# Deploy the CH-LAE flux-product docs site to GitHub Pages.
#
# Builds the Quarto website and the notebook HTML, then publishes the output
# tree (docs/_build/html) to the gh-pages branch with ghp-import. ghp-import
# commits and (with -p) force-pushes gh-pages — it does NOT touch your source
# branch or working tree.
#
# Usage (from anywhere):
#   ./deploy.ps1                 # build + publish to gh-pages
#   ./deploy.ps1 -NoPublish      # build only, skip the push (local preview)
#   ./deploy.ps1 -Remote origin -Branch gh-pages
#
# Requires: uv (the env provides quarto-cli and ghp-import) and a configured
# git remote. Published site: https://holukas.github.io/dataset_ch-lae_flux_product/

[CmdletBinding()]
param(
    [switch]$NoPublish,
    [string]$Remote = 'origin',
    [string]$Branch = 'gh-pages'
)

$ErrorActionPreference = 'Stop'
# Always run from the repo root (this script's dir), regardless of caller cwd.
Set-Location -Path $PSScriptRoot

function Invoke-Step {
    param([string]$Desc, [scriptblock]$Cmd)
    Write-Host "==> $Desc" -ForegroundColor Cyan
    & $Cmd
    if ($LASTEXITCODE -ne 0) { throw "Step failed: $Desc (exit $LASTEXITCODE)" }
}

# 1. Render the Quarto website. This CLEANS docs/_build/html, so it must run
#    before the notebooks are layered in.
Invoke-Step 'Rendering Quarto website (docs/)' { uv run quarto render docs }

# 2. Convert all workflow notebooks to HTML under docs/_build/html/notebooks/.
#    Must come AFTER the render (step 1 wipes the output dir).
Invoke-Step 'Building notebook HTML (workflow/ -> notebooks/)' { uv run python build_notebooks.py }

if ($NoPublish) {
    Write-Host "Build complete. Output: docs/_build/html (publish skipped)." -ForegroundColor Green
    Write-Host "Preview: uv run python -m http.server 8000 --directory docs/_build/html" -ForegroundColor Green
    return
}

# 3. Publish to GitHub Pages.
#    -n  write .nojekyll (stop GitHub from running Jekyll over asset dirs)
#    -o  no history: replace gh-pages with a single fresh commit each deploy, so
#        the branch doesn't accumulate every past build's heavy notebook assets
#    -f  force (required by -o), -p  push
#    -r/-b  target remote/branch
$msg = "Deploy site {0}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm')
Invoke-Step "Publishing docs/_build/html to $Remote/$Branch" {
    uv run ghp-import docs/_build/html -n -o -f -p -r $Remote -b $Branch -m $msg
}

Write-Host "Deployed to $Remote/$Branch." -ForegroundColor Green
Write-Host "Live (after Pages rebuilds): https://holukas.github.io/dataset_ch-lae_flux_product/" -ForegroundColor Green
