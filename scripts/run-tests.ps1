$ErrorActionPreference = "Stop"; Set-StrictMode -Version Latest
& (Join-Path $PSScriptRoot "lint.ps1")
& (Join-Path $PSScriptRoot "smoke.ps1")
Write-Host "[TESTS] All checks passed." -ForegroundColor Green
