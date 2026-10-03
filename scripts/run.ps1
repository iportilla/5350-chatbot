# Run a lab without activating anything.
# Usage:  scripts\run.cmd lab2      (scripts\run.cmd  -> list of labs)
Set-Location (Split-Path -Parent $PSScriptRoot)
$venvPy = ".venv\Scripts\python.exe"
if (-not (Test-Path $venvPy)) {
    Write-Host "The course environment isn't set up yet. Run:  scripts\setup.cmd" -ForegroundColor Yellow
    exit 1
}
& $venvPy run.py @args
exit $LASTEXITCODE
