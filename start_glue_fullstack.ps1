param(
    [switch]$NoBrowser
)

$root       = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendDir = Join-Path $root "glue_fullstack\backend"

if (-not (Test-Path $backendDir)) {
    Write-Host "glue_fullstack\backend not found under $root"
    exit 1
}

$node = Get-Command node -ErrorAction SilentlyContinue
$npm  = Get-Command npm  -ErrorAction SilentlyContinue

if (-not $node -or -not $npm) {
    Write-Host "Node.js / npm not found. Install Node.js LTS first."
    exit 1
}

Set-Location $backendDir
Write-Host "Working in: $(Get-Location)"

if (-not (Test-Path "node_modules")) {
    Write-Host "node_modules missing → running npm install..."
    npm install
}

Write-Host "Starting glue backend + UI at http://localhost:3000"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location `"$backendDir`"; npm start"

if (-not $NoBrowser) {
    Start-Process "http://localhost:3000"
}
