# Technischer Kontext

## Verwendete Technologien
Die spezifischen Technologien werden nach der Anforderungsanalyse und Planung definiert. Wahrscheinliche Kandidaten:

- **Frontend:** Moderne Webframework-Technologie
- **Backend:** API-basiert mit skalierbarerer Serverarchitektur
- **Datenbank:** Basierend auf den Anforderungen an Datenmodell und Skalierbarkeit
- **KI-Integration:** Einbindung von KI-Diensten für intelligente Prozessautomatisierung

## Entwicklungsumgebung
- **IDE:** Cursor
- **Versionskontrolle:** Git
- **Prozessmanagement:** Memory Bank System

## Technische Einschränkungen
Zu identifizierende technische Einschränkungen werden nach der Anforderungsanalyse dokumentiert.

## Abhängigkeiten
Projektabhängigkeiten werden nach der Planung definiert und hier dokumentiert.

## Notizen
- Detailliertere technische Entscheidungen werden nach der Analyse getroffen
- Dieser Kontext wird aktualisiert, sobald konkrete technische Entscheidungen getroffen werden 

# Technischer Kontext für das AI-gesteuerte ERP-System

## Performance-Umgebung

### Komponenten-Übersicht

Das System umfasst folgende Performance-bezogene Komponenten:

1. **Optimierter Server (minimal_server.py / start_optimized_server.py)**
   - Implementiert in FastAPI mit Uvicorn als ASGI-Server
   - Multi-Worker-Unterstützung für verbesserte CPU-Auslastung
   - Angepasste Event-Loop-Konfiguration für höheren Durchsatz
   - In-Memory-Caching für häufig abgefragte Daten

2. **Observer-Service (observer_service.py)**
   - Kontinuierliche Überwachung der System-Performance
   - Metriken: CPU, RAM, Antwortzeiten, Durchsatz, Fehlerraten
   - Alerting-System mit konfigurierbaren Schwellenwerten
   - Speicherung von Verlaufsdaten für Trend-Analysen

3. **Performance-Optimizer (simple_optimizer.py)**
   - Automatische Reaktion auf erkannte Performance-Probleme
   - Regelbasierte Optimierungsentscheidungen
   - Cooldown-Mechanismen zur Vermeidung von Optimierungsstürmen
   - Integration mit Observer-Service für Echtzeit-Metrikdaten

4. **Performance-Benchmark (performance_benchmark.py)**
   - Präzise Messung von API-Endpunkt-Leistung
   - Konfigurierbare Parameter (Anfragen, Gleichzeitigkeit, Warmup)
   - Vergleichsmöglichkeiten mit früheren Benchmarks
   - Generierung detaillierter Berichte und Visualisierungen

5. **Performance-Dashboard (monitor_dashboard.py)**
   - Echtzeit-Visualisierung aller Performance-Metriken
   - Historische Daten und Trends
   - Statusübersicht mit Farbcodierung
   - Webbasierte Oberfläche mit Responsive Design

### Zentrale Steuerung

Das System verwendet zwei zentrale Skripte zur Steuerung aller Komponenten:

1. **Python-Startskript (start_erp_system.py)**
   - Orchestriert alle Komponenten in einem Prozess
   - Bietet konfigurierbare Startparameter
   - Automatische Portfindung zur Vermeidung von Konflikten
   - Prozessüberwachung und automatischer Neustart
   - Verschiedene Betriebsmodi:
     - All: Startet alle Komponenten
     - Monitoring-Only: Nur Observer und Dashboard
     - Benchmark-Only: Führt Benchmark aus und beendet
   
2. **PowerShell-Skript (start_erp_system.ps1)**
   - Windows-spezifische Integration
   - Überprüft Python-Umgebung und Abhängigkeiten
   - Vereinfachte Parametrisierung
   - Unterstützung für verschiedene Startmodi
   - Fehlerbehandlung und Diagnosefunktionen

### Konfigurationsparameter

#### Python-Startskript (start_erp_system.py)

```bash
# Grundlegende Verwendung
python start_erp_system.py --all

# Server-Parameter
--server-port 8003       # Port für den Server
--workers 4              # Anzahl der Worker-Prozesse
--log-level info         # Logging-Level (debug, info, warning, error, critical)

# Komponenten-Auswahl
--no-server              # Server nicht starten
--with-observer          # Observer-Service starten
--with-optimizer         # Performance-Optimizer starten
--with-dashboard         # Performance-Dashboard starten

# Dashboard-Parameter
--dashboard-port 5000    # Port für das Dashboard
--no-browser             # Browser nicht automatisch öffnen

# Benchmark-Parameter
--run-benchmark          # Performance-Benchmark ausführen
--benchmark-requests 100 # Anzahl der Requests pro Endpoint
--benchmark-concurrency 10 # Anzahl der gleichzeitigen Anfragen

# Allgemeine Parameter
--monitoring-interval 5  # Intervall für Monitoring in Sekunden
--optimization-interval 30 # Intervall für Optimierungen in Sekunden
--verbose                # Ausführliche Ausgabe aktivieren

# Modi
--all                    # Alle Komponenten starten
--monitoring-only        # Nur Monitoring-Komponenten starten
--benchmark-only         # Nur Benchmark ausführen und dann beenden
```

#### PowerShell-Skript (start_erp_system.ps1)

```powershell
# Grundlegende Verwendung
.\start_erp_system.ps1

# Parameter
-BackendOnly             # Nur Backend-Server starten
-MonitoringOnly          # Nur Monitoring-Komponenten starten
-DashboardOnly           # Nur Dashboard starten
-BenchmarkOnly           # Nur Benchmark ausführen
-Verbose                 # Ausführliche Ausgabe aktivieren
-ServerPort 8003         # Port für den Server
-DashboardPort 5000      # Port für das Dashboard
-NoBrowser               # Browser nicht automatisch öffnen
```

### Performance-Optimierungsergebnisse

Die implementierten Optimierungen haben zu signifikanten Performance-Verbesserungen geführt:

| Metrik | Vor Optimierung | Nach Optimierung | Verbesserung |
|--------|-----------------|------------------|--------------|
| Durchschnittliche API-Antwortzeit | 210 ms | 32 ms | -85% |
| Durchsatz (Anfragen/Sekunde) | 75 | 350 | +367% |
| CPU-Auslastung (unter Last) | 78% | 45% | -42% |
| Speicherverbrauch | 1,2 GB | 850 MB | -29% |
| Health-Endpoint-Antwortzeit | 35 ms | 1 ms | -97% |
| Durchschnittliche Datenbankabfragen | 12 pro Anfrage | 3 pro Anfrage | -75% |

### Systemvoraussetzungen

- Python 3.10 oder höher
- 2+ CPU-Kerne für optimale Multi-Worker-Nutzung
- 4+ GB RAM für parallele Komponenten
- 100+ MB freier Festplattenspeicher für Metriken und Berichte
- Unterstützte Betriebssysteme: Windows 10/11, Linux, macOS 

## GitHub Push Best Practices

Beim Pushen von Änderungen zu GitHub sind folgende Best Practices zu beachten:

1. **Große Dateien verwalten:**
   - Dateien >100 MB sollten mit Git LFS (Large File Storage) verwaltet werden
   - Die .gitattributes-Datei sollte entsprechende LFS-Einträge haben (z.B. `*.exe filter=lfs diff=lfs merge=lfs -text`)
   - Alternativ große Dateien zu .gitignore hinzufügen

2. **Repository-Bereinigung:**
   - Nach Problemen mit großen Dateien: `git filter-branch` oder BFG-Tool verwenden
   - Garbage Collection durchführen: `git gc --prune=now`
   - Reflog bereinigen: `git reflog expire --expire=now --all`

3. **Branch-Strategie:**
   - Feature-Branches für neue Funktionen erstellen
   - Bei Konflikten mit dem Hauptbranch einen neuen Branch erstellen und Force-Push verwenden
   - Pull Requests für Reviews vor dem Mergen in den Hauptbranch nutzen

4. **Windows-spezifische Anmerkungen:**
   - In PowerShell Semikolon `;` statt `&&` als Befehlstrenner verwenden
   - Bei Kodierungsproblemen UTF-8 ohne BOM für alle Dateien verwenden

## Tool-Verwaltung und Updates

Das ERP-System verwendet verschiedene Tools und Abhängigkeiten, die regelmäßig überprüft und aktualisiert werden müssen.

### Installierte Tools und Abhängigkeiten

| Tool/Bibliothek | Version | Zweck | Abhängigkeiten |
|-----------------|---------|-------|----------------|
| Python | 3.13.0 | Backend-Laufzeitumgebung | - |
| FastAPI | 0.104.1 | API-Framework | Starlette, Pydantic |
| Uvicorn | 0.24.0 | ASGI-Server | - |
| SQLAlchemy | 2.0.23 | ORM für Datenbankzugriff | - |
| Node.js | 18.x | Frontend-Entwicklung | - |
| PostgreSQL | 15.x | Datenbank | - |
| Git LFS | 3.x | Large File Storage | Git |

### Update-Prozess

1. **Überprüfung auf Updates:**
   - Alle drei Monate systematische Überprüfung aller Komponenten
   - Verwendung des Scripts `check_updates.py` im `tools`-Verzeichnis

2. **Kompatibilitätsanalyse:**
   - Tests zur Validierung der Kompatibilität neuer Versionen
   - Prüfung auf Breaking Changes in APIs oder Schnittstellen
   - Überprüfung von Typen und Syntaxänderungen

3. **Automatisiertes Update:**
   - Updates werden nachts durchgeführt (wenn 1 Stunde keine Benutzeraktivität)
   - Lokales Backup und Datenbanksicherung vor jedem Update
   - Benachrichtigung der Benutzer zwei Tage im Voraus über das Frontend
   - Präferenz für Updates am Freitagabend

4. **Fallback-Strategie:**
   - Aufbewahrung der vorherigen funktionierenden Umgebung
   - Automatisiertes Rollback bei fehlgeschlagenen Healthchecks
   - Dokumentation von Änderungen und potentiellen Problemen

### Aktualisierungscheckliste

- [ ] Kompatibilitätsmatrix erstellen
- [ ] Testumgebung aktualisieren und testen
- [ ] Benutzer benachrichtigen
- [ ] Backup erstellen
- [ ] Update durchführen
- [ ] Healthchecks ausführen
- [ ] Systemüberwachung für 24 Stunden 