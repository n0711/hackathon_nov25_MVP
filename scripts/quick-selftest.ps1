param([int]$Port = 5057)
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

# 1) CLI offline sanity
$cli = & (Join-Path $PSScriptRoot "analyze.ps1") -Offline
if (-not $cli) { throw "CLI offline output empty" }

# 2) Start REST stub in child PowerShell
$stub = Join-Path $PSScriptRoot "start-offline-api.ps1"
$ps = Start-Process -PassThru -FilePath "powershell" -ArgumentList "-NoProfile","-ExecutionPolicy","Bypass","-File","`"$stub`"","-Port",$Port

# 3) Probe readiness with retries
$ready = $false
for ($i=0; $i -lt 15; $i++) {
  Start-Sleep -Milliseconds 300
  try {
    $r = Invoke-WebRequest -UseBasicParsing -Method POST -Uri ("http://localhost:{0}/analyze" -f $Port) -ContentType "application/json" -Body "{}" -TimeoutSec 2
    if ($r.StatusCode -eq 200) { $ready = $true; break }
  } catch { Start-Sleep -Milliseconds 200 }
}

# 4) Teardown if still running
try {
  $proc = Get-Process -Id $ps.Id -ErrorAction SilentlyContinue
  if ($proc) { Stop-Process -Id $ps.Id -Force -ErrorAction SilentlyContinue }
} catch { }

if (-not $ready) { throw "REST stub did not return 200 within timeout" }
Write-Host "Self-test OK (CLI + REST offline)" -ForegroundColor Green
