# DLLS5-Service — Windows one-line installer
# Usage: Win+R -> paste:  powershell -c "irm https://raw.githubusercontent.com/groundboxerrespect/dlls5-service/main/install.ps1 | iex"
$ErrorActionPreference = "Stop"
Write-Host "🎮 Installing DLLS5-Service..." -ForegroundColor Green

# Check Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python not found. Install Python 3.10+ from https://python.org (tick 'Add to PATH')" -ForegroundColor Red
    exit 1
}

# Clone or update
if (Test-Path "dlls5-service") {
    Set-Location dlls5-service
    git pull 2>$null
} else {
    git clone https://github.com/groundboxerrespect/dlls5-service.git
    Set-Location dlls5-service
}

# Venv + deps
python -m venv .venv
& .\.venv\Scripts\python.exe -m pip install --upgrade pip -q
& .\.venv\Scripts\pip.exe install -r requirements.txt -q

Write-Host ""
Write-Host "✅ Done! Starting server at http://localhost:8000" -ForegroundColor Green
Start-Process "http://localhost:8000"
& .\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000
