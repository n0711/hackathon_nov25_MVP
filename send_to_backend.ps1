param(
    [Parameter(Mandatory = $false)]
    [string]$JsonPath = ".\sample_response.json"
)

# If the default path doesn't exist, try to auto-find a JSON file
if (!(Test-Path $JsonPath)) {
    Write-Host "JsonPath '$JsonPath' not found, searching for a JSON file..." -ForegroundColor Yellow
    $found = Get-ChildItem -Recurse -Filter *.json | Select-Object -First 1
    if ($found) {
        $JsonPath = $found.FullName
        Write-Host "Using JSON file: $JsonPath" -ForegroundColor Green
    } else {
        Write-Host "❌ No JSON file found in this repo." -ForegroundColor Red
        exit 1
    }
} else {
    $JsonPath = (Resolve-Path $JsonPath).Path
    Write-Host "Using JSON file: $JsonPath" -ForegroundColor Green
}

# Read JSON
$payload = Get-Content $JsonPath -Raw | ConvertFrom-Json

# Wrap for backend: { "data": <your-json> }
$body = @{ data = $payload } | ConvertTo-Json -Depth 10

# Call backend
$response = Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/recommend" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body

$response
