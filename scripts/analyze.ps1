param(
  [string]$CsvPath = "",
  [switch]$Offline
)
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Write-Json($obj) { $obj | ConvertTo-Json -Depth 8 }

if ($Offline) {
  $fixture = Get-Content -Raw -Path (Join-Path $PSScriptRoot "..\\fixtures\\offline_demo.json")
  Write-Output $fixture
  exit 0
}

if (-not $CsvPath -or -not (Test-Path $CsvPath)) {
  Write-Error "CsvPath not provided or not found. Use -Offline for the demo fixture."
}

# Placeholder compute path (Phase B+). For now, just echo a minimal response shape.
$response = [ordered]@{
  summary  = @{ n_students = 0; n_events = 0; mean_score = 0.0 }
  insights = @()
  actions  = @()
  meta     = @{ run_id = [guid]::NewGuid().ToString(); created_at = (Get-Date).ToString("s") + "Z"; version = "0.1.0" }
}
Write-Json $response
