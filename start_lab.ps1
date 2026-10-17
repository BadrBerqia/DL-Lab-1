param()

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path -LiteralPath $VenvPython)) {
    throw "Environnement absent. Exécutez d'abord .\setup.ps1"
}

Set-Location -LiteralPath $ProjectRoot
& $VenvPython -m jupyter lab
