#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Startet das AI-driven ERP-System.
.DESCRIPTION
    Dieses Skript startet die notwendigen Komponenten des ERP-Systems.
    Es initialisiert die Python-Umgebung und startet den Backend-Server.
.PARAMETER BackendOnly
    Wenn gesetzt, wird nur der Backend-Server gestartet.
.PARAMETER Development
    Startet das System im Entwicklungsmodus mit zusätzlichen Debugging-Informationen.
.PARAMETER ResetDb
    Setzt die Datenbank zurück und erstellt sie neu.
#>
param(
    [switch]$BackendOnly = $false,
    [switch]$Development = $false,
    [switch]$ResetDb = $false
)

# Konfiguration
$PythonCmd = "python"
$BackendDir = Join-Path $PSScriptRoot "backend"
$FrontendDir = Join-Path $PSScriptRoot "frontend"
$RequirementsFile = Join-Path $BackendDir "requirements.txt"
$VenvDir = Join-Path $PSScriptRoot ".venv"
$BackendPort = 8000

# Farben für Konsole
function Write-ColorOutput {
    param (
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

# Funktion zum Überprüfen der Umgebung
function Check-Environment {
    Write-ColorOutput "[1/7] Überprüfe Python-Installation..." "Cyan"
    
    try {
        $pythonVersion = & $PythonCmd --version
        Write-ColorOutput "Python-Version: $pythonVersion" "Green"
    }
    catch {
        Write-ColorOutput "Python konnte nicht gefunden werden. Bitte installieren Sie Python 3.12 oder höher." "Red"
        exit 1
    }
    
    # Prüfe ob venv existiert, sonst erstelle es
    if (-not (Test-Path $VenvDir)) {
        Write-ColorOutput "[2/7] Erstelle virtuelle Python-Umgebung..." "Cyan"
        & $PythonCmd -m venv $VenvDir
        if (-not $?) {
            Write-ColorOutput "Fehler beim Erstellen der virtuellen Umgebung." "Red"
            exit 1
        }
    }
    else {
        Write-ColorOutput "[2/7] Virtuelle Python-Umgebung bereits vorhanden." "Green"
    }
    
    # Aktiviere venv
    Write-ColorOutput "[3/7] Aktiviere virtuelle Python-Umgebung..." "Cyan"
    $activateScript = Join-Path $VenvDir "Scripts\Activate.ps1"
    if (Test-Path $activateScript) {
        & $activateScript
        if (-not $?) {
            Write-ColorOutput "Fehler beim Aktivieren der virtuellen Umgebung." "Red"
            exit 1
        }
        Write-ColorOutput "Virtuelle Umgebung aktiviert." "Green"
    }
    else {
        Write-ColorOutput "Aktivierungsskript nicht gefunden: $activateScript" "Red"
        exit 1
    }
    
    # Installiere Abhängigkeiten
    Write-ColorOutput "[4/7] Installiere Abhängigkeiten..." "Cyan"
    if (Test-Path $RequirementsFile) {
        & python -m pip install -r $RequirementsFile
        if (-not $?) {
            Write-ColorOutput "Fehler beim Installieren der Abhängigkeiten." "Red"
            exit 1
        }
        Write-ColorOutput "Abhängigkeiten erfolgreich installiert." "Green"
    }
    else {
        Write-ColorOutput "Requirements-Datei nicht gefunden: $RequirementsFile" "Red"
        exit 1
    }
}

# Funktion zum Überprüfen des Backend-Codes
function Check-Backend {
    Write-ColorOutput "[5/7] Überprüfe Backend-Code..." "Cyan"
    
    # Prüfe ob main.py existiert
    $mainPyPath = Join-Path $BackendDir "main.py"
    if (Test-Path $mainPyPath) {
        Write-ColorOutput "main.py gefunden." "Green"
    }
    else {
        Write-ColorOutput "main.py nicht gefunden: $mainPyPath" "Red"
        exit 1
    }
    
    # Prüfe Python-Syntax
    & python -c "import os; path = os.path.normpath('$($mainPyPath.Replace('\', '\\'))'); import py_compile; py_compile.compile(path)"
    if ($?) {
        Write-ColorOutput "Syntaxprüfung erfolgreich" "Green"
    }
    else {
        Write-ColorOutput "Fehler in der Python-Syntax gefunden." "Red"
        exit 1
    }
    
    # Zeige Python-Pfad zur Fehlersuche
    if ($Development) {
        $pythonPath = & python -c "import sys; print(sys.path)"
        Write-ColorOutput "Python-Pfad: $pythonPath" "Gray"
    }
}

# Funktion zum Starten des Backend-Servers
function Start-Backend {
    Write-ColorOutput "[6/7] Starte Backend-Server..." "Cyan"
    
    # Setze Umgebungsvariablen
    $env:PYTHONPATH = $PSScriptRoot
    
    # Wechsle ins Backend-Verzeichnis
    Set-Location $BackendDir
    
    # Starte den Backend-Server
    Write-ColorOutput "Server wird unter http://localhost:$BackendPort verfügbar sein" "Yellow"
    Write-ColorOutput "API-Dokumentation: http://localhost:$BackendPort/docs" "Yellow"
    Write-ColorOutput "Health-Endpoint: http://localhost:$BackendPort/health" "Yellow"
    Write-ColorOutput "Drücken Sie STRG+C, um den Server zu beenden." "Yellow"
    Write-ColorOutput "=======================================" "Yellow"
    
    # Verwende einen modifizierten Import-Ansatz für den Server-Start
    $pythonScript = @"
import sys
import os

# Füge das Hauptverzeichnis zum Python-Pfad hinzu
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importiere die notwendigen Module
try:
    from backend.core.path_registry import get_registry
    registry = get_registry()
except ImportError:
    print("Pfadregister nicht gefunden, verwende Standardpfade.")

# Importiere FastAPI-Komponenten
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.api.v1.api import api_router

# Erstelle die FastAPI-Anwendung
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS-Middleware konfigurieren
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API-Router einbinden
app.include_router(api_router, prefix=settings.API_V1_STR)

# Root-Endpunkt
@app.get("/")
async def root():
    return {"message": "Willkommen beim AI-Driven ERP System"}

# Gesundheitscheck
@app.get("/health")
async def health_check():
    from datetime import datetime
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# Für direkte Ausführung
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=$BackendPort, reload=True)
"@
    
    # Speichere das Skript in einer temporären Datei
    $tempScriptPath = Join-Path $BackendDir "server_start.py"
    $pythonScript | Out-File -FilePath $tempScriptPath -Encoding utf8
    
    try {
        # Starte den Server
        & python $tempScriptPath
    }
    finally {
        # Lösche die temporäre Datei
        Remove-Item -Path $tempScriptPath -ErrorAction SilentlyContinue
    }
}

# Funktion zum Starten des Frontend-Servers (für zukünftige Implementierung)
function Start-Frontend {
    Write-ColorOutput "[7/7] Starte Frontend-Server..." "Cyan"
    # Hier könnte die Frontend-Implementierung starten
    Write-ColorOutput "Frontend-Server-Start noch nicht implementiert." "Yellow"
}

# Hauptfunktion
function Main {
    Write-ColorOutput "AI-Driven ERP-System wird gestartet..." "Green"
    
    # Überprüfe und initialisiere die Umgebung
    Check-Environment
    
    # Überprüfe den Backend-Code
    Check-Backend
    
    # Starte den Backend-Server
    Start-Backend
    
    # Starte den Frontend-Server, wenn nicht nur Backend angefordert wurde
    if (-not $BackendOnly) {
        Start-Frontend
    }
}

# Starte das Hauptprogramm
Main 