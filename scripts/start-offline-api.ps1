# Start an offline REST stub for POST /analyze returning fixture JSON
param(
  [int]$Port = 5057
)
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Net.HttpListener
$listener = New-Object System.Net.HttpListener
$prefix = "http://localhost:{0}/" -f $Port
$listener.Prefixes.Add($prefix)
$listener.Start()
Write-Host "Offline API listening at $prefix (POST /analyze). Press Ctrl+C to stop." -ForegroundColor Green

try {
  while ($true) {
    $context = $listener.GetContext()
    $req  = $context.Request
    $res  = $context.Response
    if ($req.HttpMethod -eq "POST" -and $req.Url.AbsolutePath -eq "/analyze") {
      $json = Get-Content -Raw -Path (Join-Path $PSScriptRoot "..\\fixtures\\offline_demo.json")
      $buffer = [System.Text.Encoding]::UTF8.GetBytes($json)
      $res.ContentType = "application/json"
      $res.StatusCode = 200
      $res.OutputStream.Write($buffer,0,$buffer.Length)
      $res.OutputStream.Close()
    } else {
      $res.StatusCode = 404
      $msg = '{"error":"Not Found"}'
      $buf = [System.Text.Encoding]::UTF8.GetBytes($msg)
      $res.OutputStream.Write($buf,0,$buf.Length)
      $res.OutputStream.Close()
    }
  }
} finally {
  $listener.Stop()
  $listener.Close()
}
