param()

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvPath = Join-Path $ProjectRoot ".venv"
$BundledPython = Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

function Find-Python312 {
    if ($env:DL_LAB_PYTHON -and (Test-Path -LiteralPath $env:DL_LAB_PYTHON)) {
        return $env:DL_LAB_PYTHON
    }

    if (Test-Path -LiteralPath $BundledPython) {
        $version = & $BundledPython -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
        if ($version -eq "3.12") {
            return $BundledPython
        }
    }

    try {
        $candidate = & py -3.12 -c "import sys; print(sys.executable)" 2>$null
        if ($LASTEXITCODE -eq 0 -and $candidate) {
            return $candidate.Trim()
        }
    }
    catch {}

    throw @"
Python 3.12 est requis pour cet environnement PyTorch sous Windows.
Installez-le depuis https://www.python.org/downloads/ puis relancez setup.ps1.
Vous pouvez aussi définir DL_LAB_PYTHON vers un python.exe 3.12.
"@
}

$Python312 = Find-Python312
Write-Host "Python sélectionné : $Python312"

if (-not (Test-Path -LiteralPath $VenvPath)) {
    Write-Host "Création de l'environnement virtuel..."
    & $Python312 -m venv $VenvPath
}

$VenvPython = Join-Path $VenvPath "Scripts\python.exe"

Write-Host "Mise à jour de pip..."
& $VenvPython -m pip install --upgrade pip setuptools wheel

Write-Host "Installation de PyTorch 2.5.1 avec CUDA 12.1..."
& $VenvPython -m pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cu121

Write-Host "Installation des dépendances du TP..."
& $VenvPython -m pip install -r (Join-Path $ProjectRoot "requirements.txt")

Write-Host "Création des notebooks..."
& $VenvPython (Join-Path $ProjectRoot "scripts\create_notebooks.py")

Write-Host "Enregistrement du kernel Jupyter..."
& $VenvPython -m ipykernel install --user --name dl-lab-1 --display-name "Python (DL-Lab-1)"

Write-Host "Vérification rapide de l'installation..."
& $VenvPython (Join-Path $ProjectRoot "scripts\verify_installation_quick.py")

Write-Host ""
Write-Host "Installation terminée. Lancez .\start_lab.ps1"
