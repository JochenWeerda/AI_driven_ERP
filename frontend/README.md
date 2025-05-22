# AI-gesteuertes ERP-System - Frontend

Dieses Verzeichnis enthält den Frontend-Code für das AI-gesteuerte ERP-System.

## Technologien

- **Framework:** React mit Vite
- **UI-Bibliothek:** Material-UI (MUI)
- **HTTP-Client:** Axios
- **Zustandsmanagement:** React Context API und Hooks

## Einrichtung

1. Abhängigkeiten installieren:

```bash
npm install
```

2. Entwicklungsserver starten:

```bash
npm run dev
```

## Hauptfunktionen

### Dashboard

Das Dashboard bietet eine Übersicht über die wichtigsten Systemfunktionen und KPIs:

- Status der Technischen Sicherungseinrichtung (TSE)
- Status der Fuhrwerkswaagen
- Systemübersicht

### Artikel-Katalog

Der Artikel-Katalog ermöglicht die Verwaltung und Suche von Artikeln:

- Artikel durchsuchen
- Details anzeigen
- KI-basierte Empfehlungen für ausgewählte Kunden

### Waagen-Verwaltung

Die Waagen-Verwaltung bietet Funktionen zur Integration mit Fuhrwerkswaagen:

- Status der Waagen überwachen
- Messungen verwalten
- Messungen verarbeiten oder stornieren

## Verzeichnisstruktur

- **/src** - Hauptquelldateien
  - **/assets** - Statische Assets (Bilder, Fonts, etc.)
  - **/components** - Wiederverwendbare UI-Komponenten
  - **/hooks** - Custom React Hooks
  - **/pages** - Seitenkomponenten
  - **/services** - API-Services und andere Dienste
  - **/store** - Zustandsmanagement
  - **/utils** - Hilfsfunktionen

## Entwicklung

### Neue Komponenten hinzufügen

1. Erstellen Sie die Komponente im Verzeichnis `/src/components`
2. Importieren und verwenden Sie die Komponente in einer Seite

### Neue API-Endpunkte verwenden

1. Fügen Sie den Endpunkt im API-Service (`/src/services/api.js`) hinzu
2. Verwenden Sie die API in einer Komponente oder Seite

## Codebeispiel

```jsx
import React from 'react';
import { useEffect, useState } from 'react';
import api from '../services/api';

const MeineKomponente = () => {
  const [daten, setDaten] = useState([]);
  
  useEffect(() => {
    const fetchDaten = async () => {
      try {
        const response = await api.get('/api/v1/meine-daten');
        setDaten(response.data);
      } catch (error) {
        console.error('Fehler beim Abrufen der Daten:', error);
      }
    };
    
    fetchDaten();
  }, []);
  
  return (
    <div>
      {/* Komponenten-Inhalt */}
    </div>
  );
};

export default MeineKomponente;
```
