# Observer-Microservice Starter für PowerShell

Write-Host "Observer-Microservice wird gestartet..." -ForegroundColor Cyan
Write-Host ""

# Prüfen, ob Python installiert ist
try {
    $pythonVersion = (python --version 2>&1)
    Write-Host "Python Version: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "Fehler: Python ist nicht installiert oder nicht im PATH." -ForegroundColor Red
    Write-Host "Bitte installieren Sie Python und versuchen Sie es erneut."
    exit 1
}

# Prüfen, ob die Abhängigkeiten installiert sind
Write-Host "Installiere/Aktualisiere Abhängigkeiten..." -ForegroundColor Yellow
python -m pip install -r observer_requirements.txt

# Parameter für den Observer
$port = 8010
$reportInterval = 15

# Starten des Observer-Services
Write-Host ""
Write-Host "Observer-Service wird gestartet auf Port $port" -ForegroundColor Green
Write-Host "Dashboard wird verfügbar sein unter: http://localhost:$port" -ForegroundColor Cyan
Write-Host ""
Write-Host "Drücken Sie STRG+C, um den Service zu beenden." -ForegroundColor Yellow
Write-Host ""

try {
    python start_observer_simple.py --port $port --report-interval $reportInterval
}
catch {
    Write-Host "Fehler beim Starten des Observer-Services: $_" -ForegroundColor Red
}
finally {
    Write-Host "Observer-Service wurde beendet." -ForegroundColor Cyan
} 