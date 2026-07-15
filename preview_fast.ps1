#!/usr/bin/env pwsh
#
# Fast local preview: Quarto's live-reloading dev server for the docs pages.
# Auto-opens the browser and refreshes as you edit docs/*.md. Does NOT include
# the notebooks (the /notebooks/ links won't resolve) — for the full site as it
# deploys, use preview_full.ps1.
#
#   ./preview_fast.ps1
#
$ErrorActionPreference = 'Stop'
Set-Location -Path $PSScriptRoot
uv run quarto preview docs
