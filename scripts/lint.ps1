$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$files = Get-ChildItem -Path (Join-Path $PSScriptRoot "..") -Recurse -Include *.ps1 -File
$errors = @()
foreach ($f in $files) {
  try {
    [System.Management.Automation.Language.Parser]::ParseFile($f.FullName, [ref]$null, [ref]$null) | Out-Null
  } catch {
    $errors += "Parse error in $($f.FullName)"
  }
}
if ($errors.Count -gt 0) {
  $errors | ForEach-Object { Write-Error $_ }
  throw "Lint failed with $($errors.Count) parse errors."
}
Write-Host "[LINT] OK: all scripts parse cleanly" -ForegroundColor Green
