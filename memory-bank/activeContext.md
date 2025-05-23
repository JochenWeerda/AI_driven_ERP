# Aktiver Kontext

## Architektur-Übersicht

Das ERP-System ist in der Umstellung von einer monolithischen zu einer Microservice-Architektur. Dies erfordert eine schrittweise Dekomposition des Codes und die Einführung von Überwachungs- und Optimierungsmechanismen.

### Aktuelle Komponenten

1. **Frontend**: React-Anwendung mit modularem Aufbau
   - Theme-System wurde implementiert mit Hell/Dunkel/Kontrast-Modi
   - Redux wurde für zustandsbasierte Komponenten entfernt
   - Router wurde für Navigation implementiert

2. **Backend**: Python-basierter Kern mit modularen Diensten
   - Minimal-Server läuft auf Port 8003
   - Kompatibilität mit Python 3.13.3 sichergestellt
   - Vorbereitung auf Microservices durch Service-Extraktion

3. **Observer-Service**: Microservice-Überwachungssystem
   - Überwacht CPU, RAM und Latenzzeiten aller Services
   - Erstellt automatisierte Optimierungsberichte
   - Web-Dashboard zur Echtzeit-Visualisierung der Metriken

### In Entwicklung

1. **Theme Microservice**: 
   - Extraktion aus dem Monolithen
   - REST-API für Theme-Verwaltung
   - Eigenständiger Node.js-Service auf Port 5001
   - Integration mit Observer-Service erforderlich

## Projektübergreifende Performance-Richtlinien

Die folgenden Anforderungen gelten für alle Komponenten des ERP-Systems:

### Verbindliche Anforderungen

1. **Health-Endpunkte für alle Services**
   - Jeder Microservice muss einen `/health`-Endpunkt implementieren
   - Standard-JSON-Format gemäß `observer-microservice.md`
   - Mindestdaten: Status, Version, CPU, RAM, Antwortzeiten

2. **Performance-Schwellwerte**
   - API-Antwortzeiten: 300ms Warnung, 500ms kritisch
   - CPU-Auslastung: 70% Warnung, 85% kritisch
   - RAM-Auslastung: 75% Warnung, 90% kritisch
   - Schwellwerte in `observer_config.json` konfigurierbar

3. **Leistungskritische Komponenten überwachen**
   - ERP-Kern (Backend-Minimal-Server)
   - Theme-Service (Erste Microservice-Extraktion)
   - Frontend-Client (Browser-Performance)
   - Datenbank-Performance

4. **CI/CD-Integration**
   - Performance-Tests vor jedem Merge verpflichtend
   - Schwellwert-Überschreitungen blockieren Pull-Requests
   - Automatisierte Optimierungsberichte bei jedem Build

### Entwicklungspraxis

1. **Optimierungsprozess**
   - Observer identifiziert Performance-Probleme
   - Team bewertet Berichte und priorisiert Optimierungen
   - Implementierung der Verbesserungen
   - Verifizierung durch Observer-Metriken

2. **Dokumentation**
   - Performance-Entscheidungen in Commit-Messages dokumentieren
   - Service-spezifische Schwellwerte begründen
   - Optimierungsansätze in Optimierungsberichten reflektieren

3. **Verantwortlichkeiten**
   - Jedes Team ist für die Performance seiner Services verantwortlich
   - DevOps überwacht Observer-Infrastruktur
   - Architektur-Team überprüft Schwellwerte
   - Produktmanagement priorisiert Performance-Issues

Diese Richtlinien sichern eine kontinuierliche Performance-Optimierung und bilden die Grundlage für eine skalierbare, reaktionsschnelle Microservice-Architektur.

## Aktueller Fokus
- Implementierung der Kernfunktionen des ERP-Systems
- Integration von TSE und Fuhrwerkswaagen
- Entwicklung der Frontend-Komponenten

## Letzte Änderungen
- Backend-API-Endpunkte für die Hauptfunktionen implementiert
- Datenbankmodelle für die wichtigsten Tabellen erstellt
- Frontend-UI-Komponenten für Dashboard, Artikel-Katalog und Waagen-Management entwickelt
- Integration mit TSE und Fuhrwerkswaagen umgesetzt

## Nächste Schritte
1. Erweiterte Geschäftslogik implementieren
2. Berichtssystem entwickeln
3. Authentifizierung und Berechtigungen verfeinern
4. Umfassende Tests durchführen

## Aktive Entscheidungen
- Memory Bank wird als primäres System für die Dokumentation und Aufgabenverfolgung verwendet
- Der Entwicklungsprozess folgt dem strukturierten Ansatz: VAN → PLAN → CREATIVE → IMPLEMENT → REFLECT → ARCHIVE
- Backend nutzt FastAPI mit SQLAlchemy für optimale Leistung und Entwicklungsgeschwindigkeit
- Frontend basiert auf React mit Material-UI für modernes, responsives Design
- Die Projektarchitektur ist modular aufgebaut, um zukünftige Erweiterungen zu erleichtern
- Die KI-Funktionen werden zunächst mit einfachen Algorithmen implementiert und später durch komplexere Modelle ersetzt 