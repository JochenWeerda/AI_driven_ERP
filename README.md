# AI-Driven ERP-System

Ein modernes, KI-gesteuertes Enterprise Resource Planning System, das die Funktionalitäten klassischer ERP-Systeme (wie ServiceERP L3) bietet und durch KI-Funktionen erweitert.

## Funktionen

- **Adressverwaltung**: Kunden-, Lieferanten- und Partneradressen
- **Artikelverwaltung**: Artikelstammdaten, Lagerbestände, Preise
- **Auftragsverwaltung**: Auftragserfassung, -bearbeitung und -verfolgung
- **Bestellwesen**: Lieferantenbestellungen und Bestellverfolgung
- **Lagerverwaltung**: Lagerbestände, Inventuren und Lagerbewegungen
- **Rechnungswesen**: Rechnungserstellung, Eingangsrechnungen
- **Lieferscheine**: Verkaufs- und Eingangslieferscheine
- **Dokumentenmanagement**: Zentrales Dokumentenarchiv
- **Projektmanagement**: Projektverwaltung und -controlling
- **Zeiterfassung**: Arbeitszeiterfassung und -auswertung

## Technologiestack

- **Backend**: Python 3.13.3 mit Starlette-Framework
- **API**: RESTful-API mit JSON-Datenaustausch
- **Datenbank**: SQLite/PostgreSQL mit SQLAlchemy ORM
- **Frontend**: In Planung (Vue.js oder React)
- **KI-Integration**: In Planung

## Besonderheiten

- **L3-Kompatibilität**: Unterstützt Datenformate und Schnittstellen wie ServiceERP L3
- **Moderne Architektur**: Modulare und skalierbare Architektur
- **Python 3.13.3-Unterstützung**: Optimiert für die neueste Python-Version
- **Erweiterte Filterung**: Unterstützt komplexe Abfragen mit L3-ähnlicher Filtersyntax

## Installation

### Voraussetzungen

- Python 3.13.3 oder höher
- pip (Python-Paketmanager)

### Setup

1. Repository klonen:
   ```bash
   git clone https://github.com/benutzername/AI_driven_ERP.git
   cd AI_driven_ERP
   ```

2. Virtuelle Umgebung erstellen und aktivieren:
   ```bash
   python -m venv .venv
   # Unter Windows:
   .\.venv\Scripts\activate
   # Unter Linux/Mac:
   source .venv/bin/activate
   ```

3. Abhängigkeiten installieren:
   ```bash
   pip install -r backend/requirements.txt
   ```

4. Server starten:
   ```bash
   cd backend
   python minimal_server.py
   ```

Der Server ist dann unter http://localhost:8000 erreichbar. Die API-Dokumentation ist unter http://localhost:8000/docs verfügbar.

## Entwicklung

Das Projekt befindet sich in aktiver Entwicklung. Beiträge sind willkommen!

### Entwicklungsrichtlinien

- Alle neuen Features sollten mit Tests abgedeckt sein
- Code muss PEP 8 entsprechen
- Änderungen müssen dokumentiert werden

## Lizenz

[MIT](LICENSE)

## Roadmap

- Frontend-Implementierung
- KI-basierte Vorschläge für Bestellungen
- Automatisierte Dokumentenerkennung
- Integration mit externen Diensten
- Mobile App