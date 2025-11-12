param([int]$Port = 5057)
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Assert($cond, $msg) { if (-not $cond) { throw $msg } }
function HasKey($obj, $k) { return ($obj.PSObject.Properties.Name -contains $k) }

# 1) CLI offline path produces valid JSON with required keys
$cliOut = & (Join-Path $PSScriptRoot "analyze.ps1") -Offline
Assert ($cliOut) "CLI offline returned empty output"
try { $cliJson = $cliOut | ConvertFrom-Json -ErrorAction Stop } catch { throw "CLI output not valid JSON" }
Assert (HasKey $cliJson 'summary' -and HasKey $cliJson 'insights' -and HasKey $cliJson 'actions' -and HasKey $cliJson 'meta') "CLI JSON missing required top-level keys"

# 2) REST stub: start → probe POST /analyze → teardown
$stub = Join-Path $PSScriptRoot "start-offline-api.ps1"
$ps = Start-Process -PassThru -FilePath "powershell" -ArgumentList "-NoProfile","-ExecutionPolicy","Bypass","-File","`"$stub`"","-Port",$Port

# probe readiness with retries
$ok = $false
for ($i=0; $i -lt 20; $i++) {
  Start-Sleep -Milliseconds 250
  try {
    $resp = Invoke-WebRequest -UseBasicParsing -Method POST -Uri ("http://localhost:{0}/analyze" -f $Port) -ContentType "application/json" -Body "{}" -TimeoutSec 2
    if ($resp.StatusCode -eq 200) { $ok = $true; break }
  } catch { }
}
# teardown
try { $proc = Get-Process -Id $ps.Id -ErrorAction SilentlyContinue; if ($proc) { Stop-Process -Id $ps.Id -Force } } catch { }

Assert $ok "REST stub did not return 200 within timeout"

# 3) REST JSON shape sanity
try { $restJson = ($resp.Content | ConvertFrom-Json -ErrorAction Stop) } catch { throw "REST response not valid JSON" }
Assert (HasKey $restJson 'summary' -and HasKey $restJson 'insights' -and HasKey $restJson 'actions' -and HasKey $restJson 'meta') "REST JSON missing required top-level keys"

Write-Host "[SMOKE] OK: CLI + REST offline verified" -ForegroundColor Green
