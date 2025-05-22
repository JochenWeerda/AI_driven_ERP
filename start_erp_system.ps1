# Hauptskript zum Starten des ERP-Systems mit Überwachung
# Startet sowohl Backend (mit Watchdog) als auch Frontend

param (
    [switch]$BackendOnly,  # Nur Backend starten
    [switch]$FrontendOnly, # Nur Frontend starten
    [int]$MaxRestarts = 5,  # Maximale Anzahl von Neustarts für den Watchdog
    [int]$CheckInterval = 15,  # Überprüfungsintervall in Sekunden
    [int]$TimeoutThreshold = 45,  # Timeout in Sekunden
    [switch]$Debug  # Debug-Modus aktivieren
)

# Debug-Ausgaben aktivieren
$DebugMode = $Debug -or $true  # Während des Testens immer aktivieren

# Funktion zum Anzeigen von Nachrichten
function Show-Message {
    param (
        [string]$Message,
        [ConsoleColor]$Color = [ConsoleColor]::White
    )
    
    $originalColor = [Console]::ForegroundColor
    [Console]::ForegroundColor = $Color
    Write-Host "[$((Get-Date).ToString('HH:mm:ss'))] $Message"
    [Console]::ForegroundColor = $originalColor
}

# Debug-Funktion
function Debug-Message {
    param (
        [string]$Message
    )
    
    if ($DebugMode) {
        $originalColor = [Console]::ForegroundColor
        [Console]::ForegroundColor = [ConsoleColor]::Magenta
        Write-Host "[DEBUG] $Message"
        [Console]::ForegroundColor = $originalColor
    }
}

# Funktion zum Erstellen der Logverzeichnisse
function Create-LogDirectories {
    $logPath = Join-Path (Get-Location).Path "watchdog_logs"
    
    if (-not (Test-Path $logPath)) {
        try {
            New-Item -Path $logPath -ItemType Directory -Force | Out-Null
            Debug-Message "Log-Verzeichnis erstellt: $logPath"
        } catch {
            Show-Message "Fehler beim Erstellen des Log-Verzeichnisses: $($_.Exception.Message)" ([ConsoleColor]::Red)
        }
    }
}

# Funktion zum Starten des Backends mit Watchdog
function Start-BackendWithWatchdog {
    Show-Message "Starte Backend mit Watchdog..." ([ConsoleColor]::Cyan)
    
    # Erstelle Logverzeichnisse
    Create-LogDirectories
    
    # Absoluter Pfad zum Watchdog-Skript
    $watchdogPath = Join-Path (Get-Location).Path "backend\watchdog.ps1"
    
    Debug-Message "Prüfe Watchdog-Pfad: $watchdogPath"
    Debug-Message "Watchdog-Datei existiert: $(Test-Path $watchdogPath)"
    
    # Überprüfe, ob das Watchdog-Skript existiert
    if (-not (Test-Path $watchdogPath)) {
        Show-Message "FEHLER: Watchdog-Skript nicht gefunden unter: $watchdogPath" ([ConsoleColor]::Red)
        return $null
    }
    
    # Erstelle das Arbeitsverzeichnis für den Watchdog (Backend-Verzeichnis)
    $workingDirectory = Join-Path (Get-Location).Path "backend"
    Debug-Message "Arbeitsverzeichnis für Watchdog: $workingDirectory"
    Debug-Message "Arbeitsverzeichnis existiert: $(Test-Path $workingDirectory)"
    
    # Überprüfe, ob alle erforderlichen Skripte vorhanden sind
    $startBackendPath = Join-Path $workingDirectory "start_backend.ps1"
    $watchdogLoggerPath = Join-Path $workingDirectory "watchdog_logger.ps1"
    
    Debug-Message "start_backend.ps1 existiert: $(Test-Path $startBackendPath)"
    Debug-Message "watchdog_logger.ps1 existiert: $(Test-Path $watchdogLoggerPath)"
    
    if (-not (Test-Path $startBackendPath)) {
        Show-Message "FEHLER: start_backend.ps1 nicht gefunden!" ([ConsoleColor]::Red)
        return $null
    }
    
    if (-not (Test-Path $watchdogLoggerPath)) {
        Show-Message "WARNUNG: watchdog_logger.ps1 nicht gefunden - Watchdog wird ohne Logging ausgeführt" ([ConsoleColor]::Yellow)
    }
    
    # Starte den Watchdog in einem neuen Fenster
    try {
        Debug-Message "Starte Watchdog-Prozess mit Argumenten: -NoExit -File $watchdogPath -MaxRestarts $MaxRestarts -CheckInterval $CheckInterval -TimeoutThreshold $TimeoutThreshold"
        
        # Erstelle Argument-Array für Start-Process
        $arguments = @(
            "-NoExit"
            "-File"
            ".\watchdog.ps1"
            "-MaxRestarts"
            "$MaxRestarts"
            "-CheckInterval"
            "$CheckInterval"
            "-TimeoutThreshold"
            "$TimeoutThreshold"
        )
        
        $process = Start-Process powershell -ArgumentList $arguments -PassThru -WorkingDirectory $workingDirectory
        
        if ($process -eq $null) {
            Show-Message "FEHLER: Watchdog-Prozess konnte nicht gestartet werden!" ([ConsoleColor]::Red)
            return $null
        }
        
        Debug-Message "Watchdog-Prozess gestartet mit PID: $($process.Id)"
        Show-Message "Watchdog gestartet (PID: $($process.Id))" ([ConsoleColor]::Green)
        return $process
    }
    catch {
        Show-Message "FEHLER: Konnte Watchdog nicht starten: $($_.Exception.Message)" ([ConsoleColor]::Red)
        return $null
    }
}

# Funktion zum Starten des Frontends
function Start-Frontend {
    Show-Message "Starte Frontend..." ([ConsoleColor]::Cyan)
    
    # Überprüfe, ob das Frontend-Verzeichnis existiert
    $frontendPath = Join-Path (Get-Location).Path "frontend"
    Debug-Message "Frontend-Pfad: $frontendPath"
    Debug-Message "Frontend-Verzeichnis existiert: $(Test-Path $frontendPath)"
    
    if (-not (Test-Path $frontendPath)) {
        Show-Message "FEHLER: Frontend-Verzeichnis nicht gefunden unter: $frontendPath" ([ConsoleColor]::Red)
        return $null
    }
    
    # Starte das Frontend in einem neuen Fenster
    try {
        Debug-Message "Starte Frontend-Prozess mit Befehl: cd $frontendPath; npm run dev"
        
        $process = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; npm run dev" -PassThru
        
        if ($process -eq $null) {
            Show-Message "FEHLER: Frontend-Prozess konnte nicht gestartet werden!" ([ConsoleColor]::Red)
            return $null
        }
        
        Debug-Message "Frontend-Prozess gestartet mit PID: $($process.Id)"
        Show-Message "Frontend gestartet (PID: $($process.Id))" ([ConsoleColor]::Green)
        return $process
    }
    catch {
        Show-Message "FEHLER: Konnte Frontend nicht starten: $($_.Exception.Message)" ([ConsoleColor]::Red)
        return $null
    }
}

# Hauptlogik
Debug-Message "Aktuelles Verzeichnis: $(Get-Location)"
Show-Message "=== AI-DRIVEN ERP SYSTEM STARTER ===" ([ConsoleColor]::Magenta)
Show-Message "Starte Komponenten mit folgenden Einstellungen:" ([ConsoleColor]::White)
Show-Message "- MaxRestarts: $MaxRestarts" ([ConsoleColor]::White)
Show-Message "- CheckInterval: $CheckInterval Sekunden" ([ConsoleColor]::White)
Show-Message "- TimeoutThreshold: $TimeoutThreshold Sekunden" ([ConsoleColor]::White)

$backendProcess = $null
$frontendProcess = $null

# Starte die gewünschten Komponenten
if (-not $FrontendOnly) {
    $backendProcess = Start-BackendWithWatchdog
    
    if ($backendProcess -eq $null) {
        Show-Message "KRITISCHER FEHLER: Backend konnte nicht gestartet werden. Beende Starter." ([ConsoleColor]::Red)
        exit 1
    }
}

if (-not $BackendOnly) {
    $frontendProcess = Start-Frontend
    
    if ($frontendProcess -eq $null -and -not $BackendOnly) {
        Show-Message "FEHLER: Frontend konnte nicht gestartet werden." ([ConsoleColor]::Red)
    }
}

# Warte auf Benutzerinteraktion
Show-Message "Drücken Sie STRG+C, um alle Prozesse zu beenden..." ([ConsoleColor]::Yellow)

try {
    # Überwache die Prozesse
    while ($true) {
        $allStopped = $true
        
        if ($backendProcess -ne $null) {
            $backendRunning = -not $backendProcess.HasExited
            $allStopped = $allStopped -and -not $backendRunning
            Debug-Message "Backend-Prozess läuft: $backendRunning"
        }
        
        if ($frontendProcess -ne $null) {
            $frontendRunning = -not $frontendProcess.HasExited
            $allStopped = $allStopped -and -not $frontendRunning
            Debug-Message "Frontend-Prozess läuft: $frontendRunning"
        }
        
        if ($allStopped) {
            Show-Message "Alle Prozesse wurden beendet." ([ConsoleColor]::Yellow)
            break
        }
        
        Start-Sleep -Seconds 5
    }
}
catch {
    Debug-Message "Fehler in der Hauptschleife: $($_.Exception.Message)"
}
finally {
    # Bereinigen, wenn der Benutzer STRG+C drückt
    if ($backendProcess -ne $null -and -not $backendProcess.HasExited) {
        Show-Message "Beende Backend-Prozess..." ([ConsoleColor]::Yellow)
        Stop-Process -Id $backendProcess.Id -Force -ErrorAction SilentlyContinue
    }
    
    if ($frontendProcess -ne $null -and -not $frontendProcess.HasExited) {
        Show-Message "Beende Frontend-Prozess..." ([ConsoleColor]::Yellow)
        Stop-Process -Id $frontendProcess.Id -Force -ErrorAction SilentlyContinue
    }
    
    Show-Message "Alle Prozesse wurden beendet." ([ConsoleColor]::Green)
} 