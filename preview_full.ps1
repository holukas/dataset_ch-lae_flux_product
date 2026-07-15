#!/usr/bin/env pwsh
#
# Full local preview: build the entire site (Quarto website + notebooks) exactly
# as it will deploy, then serve it locally and open the browser. Use this as the
# final check before ./deploy.ps1. Extra args pass through to deploy.ps1
# (e.g. -Port 8080).
#
#   ./preview_full.ps1
#   ./preview_full.ps1 -Port 8080
#
$ErrorActionPreference = 'Stop'
Set-Location -Path $PSScriptRoot
& "$PSScriptRoot/deploy.ps1" -Preview @args
