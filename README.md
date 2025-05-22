# AI-driven ERP System

Ein modernes ERP-System mit KI-Funktionen für die automatisierte Geschäftsprozessverwaltung und intelligente Datenanalyse.

## Funktionen

- **Dokumentenmanagement**: Scannen, Speichern und Verwalten von Geschäftsdokumenten mit OCR-Funktionalität
- **E-Commerce-Integration**: Vollständige Produktverwaltung, Warenkorb und Bestellabwicklung
- **KI-gestützte Empfehlungen**: Intelligente Produktempfehlungen für Kunden
- **TSE-Integration**: Konformität mit den Anforderungen an elektronische Kassensysteme
- **Fuhrwerkswaagen-Integration**: Anschluss und Management von industriellen Wägesystemen

## Technologie-Stack

- **Backend**: Python mit FastAPI
- **Datenbank**: SQLAlchemy ORM
- **Authentifizierung**: JWT-basierte Authentifizierung
- **KI-Komponenten**: Integrierte KI-Modelle für Datenanalyse und Empfehlungen

## Installation

```bash
# Repository klonen
git clone https://github.com/AI-ERP-Developer/ai-driven-erp.git
cd ai-driven-erp

# Virtuelle Umgebung erstellen und aktivieren
python -m venv .venv
.\.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Abhängigkeiten installieren
pip install -r requirements.txt

# Server starten
cd backend
python minimal_server.py
```

## Dokumentation

Die API-Dokumentation ist verfügbar unter `http://localhost:8002/docs` nach dem Start des Servers.

## Entwicklung

Das Projekt verwendet das Memory Bank System zur Dokumentation und Verfolgung des Entwicklungsfortschritts. Alle relevanten Informationen finden sich im Verzeichnis `memory-bank/`.

## Lizenz

Copyright © 2024

## Roadmap

- Frontend-Implementierung
- KI-basierte Vorschläge für Bestellungen
- Automatisierte Dokumentenerkennung
- Integration mit externen Diensten
- Mobile App
