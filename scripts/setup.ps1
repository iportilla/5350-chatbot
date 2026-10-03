# One-time setup for Windows (PowerShell).
# Easiest: double-click scripts\setup.cmd   (or run:  scripts\setup.cmd  in a terminal)
$ErrorActionPreference = "Continue"   # we check $LASTEXITCODE ourselves
Set-Location (Split-Path -Parent $PSScriptRoot)

Write-Host "== 5350 Chatbot Labs setup (Windows) =="

# 1. Find Python 3.10+  (the 'py' launcher first, then 'python')
$check = "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)"
$py = $null; $pyArgs = @()
if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 -c $check 2>$null
    if ($LASTEXITCODE -eq 0) { $py = "py"; $pyArgs = @("-3") }
}
if (-not $py -and (Get-Command python -ErrorAction SilentlyContinue)) {
    & python -c $check 2>$null
    if ($LASTEXITCODE -eq 0) { $py = "python" }
}
if (-not $py) {
    Write-Host "ERROR: Python 3.10 or newer was not found." -ForegroundColor Red
    Write-Host "  Install it from https://www.python.org/downloads/windows/"
    Write-Host "  IMPORTANT: tick 'Add python.exe to PATH' on the first installer screen."
    Write-Host "  Then close this window, open a new one, and run setup again."
    exit 1
}
& $py @pyArgs --version

# 2. Create the virtual environment
if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment in .venv ..."
    & $py @pyArgs -m venv .venv
    if ($LASTEXITCODE -ne 0) { Write-Host "ERROR: could not create .venv." -ForegroundColor Red; exit 1 }
}
$venvPy = ".venv\Scripts\python.exe"

# 3. Install packages
Write-Host "Installing packages (this can take a few minutes) ..."
& $venvPy -m pip install --quiet --upgrade pip
& $venvPy -m pip install --quiet -r requirements.txt
if ($LASTEXITCODE -ne 0) { Write-Host "ERROR: package install failed (see messages above)." -ForegroundColor Red; exit 1 }

# 4. Create .env and (optionally) store the API key
if (-not (Test-Path ".env")) {
    Copy-Item ".env.sample" ".env"
    Write-Host "Created .env from .env.sample"
}
if ((Get-Content ".env" -Raw) -match 'OPENAI_API_KEY="sk-\.\.\."') {
    Write-Host ""
    Write-Host "Paste your OpenAI API key and press Enter (typing is hidden)."
    Write-Host "Press Enter without typing to skip and edit .env later."
    $secure = Read-Host "OPENAI_API_KEY" -AsSecureString
    $key = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure))
    if ($key.Trim()) {
        $text = (Get-Content ".env" -Raw).Replace('OPENAI_API_KEY="sk-..."', "OPENAI_API_KEY=`"$($key.Trim())`"")
        [IO.File]::WriteAllText((Join-Path (Get-Location) ".env"), $text)
        Write-Host "Saved key to .env (this file is never committed to git)."
    }
}

# 5. Verify
Write-Host ""
& $venvPy run.py check
Write-Host ""
Write-Host "Next:  scripts\run.cmd lab1"
