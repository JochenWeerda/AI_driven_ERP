"""
Minimaler Server für das AI-gesteuerte ERP-System ohne FastAPI/Pydantic
Umgeht die Probleme mit Python 3.13.3
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from uuid import uuid4

# Füge Verzeichnisse zum Python-Pfad hinzu
backend_dir = Path(__file__).parent.absolute()
root_dir = backend_dir.parent
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(backend_dir))

# Starlette importieren statt FastAPI
from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route, Mount
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
import uvicorn

# --------------- Demo-Daten ---------------

# Inventur-Daten
inventuren = [
    {
        "id": 1,
        "bezeichnung": "Jahresinventur 2023",
        "inventurdatum": "2023-12-31",
        "status": "abgeschlossen",
        "lager_id": 1,
        "bemerkung": "Komplette Jahresinventur",
        "created_at": "2023-12-30T08:00:00",
        "updated_at": "2023-12-31T16:00:00"
    },
    {
        "id": 2,
        "bezeichnung": "Zwischeninventur Q1 2024",
        "inventurdatum": "2024-03-31",
        "status": "in_bearbeitung",
        "lager_id": 1,
        "bemerkung": "Quartalsinventur",
        "created_at": "2024-03-30T08:00:00",
        "updated_at": None
    }
]

# Artikel-Daten
artikel = [
    {
        "id": 1,
        "artikelnummer": "A-10001",
        "bezeichnung": "Bürostuhl Comfort Plus",
        "kategorie": "Büromöbel",
        "einheit": "Stück",
        "preis": 249.99,
        "lagerbestand": 15,
        "min_bestand": 5,
        "lieferant_id": 1
    },
    {
        "id": 2,
        "artikelnummer": "A-10002",
        "bezeichnung": "Schreibtisch ergonomisch",
        "kategorie": "Büromöbel",
        "einheit": "Stück",
        "preis": 349.99,
        "lagerbestand": 8,
        "min_bestand": 3,
        "lieferant_id": 1
    }
]

# Lager-Daten
lager = [
    {
        "id": 1,
        "bezeichnung": "Hauptlager",
        "standort": "Berlin",
        "verantwortlicher": "Max Mustermann"
    },
    {
        "id": 2,
        "bezeichnung": "Außenlager",
        "standort": "Hamburg",
        "verantwortlicher": "Erika Musterfrau"
    }
]

# Kunden-Daten
kunden = [
    {
        "id": 1,
        "kundennummer": "K-1001",
        "firma": "Muster GmbH",
        "ansprechpartner": "Thomas Müller",
        "strasse": "Hauptstraße 1",
        "plz": "10115",
        "ort": "Berlin",
        "telefon": "+49 30 12345678",
        "email": "kontakt@muster-gmbh.de",
        "kundenseit": "2022-01-15"
    },
    {
        "id": 2,
        "kundennummer": "K-1002",
        "firma": "Example AG",
        "ansprechpartner": "Lisa Schmidt",
        "strasse": "Industrieweg 42",
        "plz": "20095",
        "ort": "Hamburg",
        "telefon": "+49 40 87654321",
        "email": "info@example-ag.de",
        "kundenseit": "2023-03-10"
    }
]

# Adressen-Daten (im Format der L3-API)
adressen = [
    {
        "Nummer": 3,
        "Anrede": "",
        "Briefanr": "",
        "Name1": "Kunde 1",
        "Name2": "Name 2",
        "Name3": "Name 3",
        "Strasse": "Hauptstraße 100",
        "Nat": "D",
        "Plz": "48935",
        "Ort": "Wietmarschen-Lohne",
        "Telefon1": "05908 9009 222",
        "Telefon2": "05908 9009 200",
        "Email": "support@service-erp.de",
        "Art": "K",
        "Kundennr": 10000
    },
    {
        "Nummer": 4,
        "Anrede": "Firma",
        "Briefanr": "",
        "Name1": "Kunde 2",
        "Name2": "Zweigstelle",
        "Name3": "",
        "Strasse": "Industriestraße 42",
        "Nat": "D",
        "Plz": "48455",
        "Ort": "Bad Bentheim",
        "Telefon1": "05922 12345",
        "Telefon2": "",
        "Email": "kontakt@example.com",
        "Art": "K",
        "Kundennr": 10001
    }
]

# Aufträge-Daten
auftraege = [
    {
        "id": 1,
        "auftragsnummer": "A-2024-001",
        "kunde_id": 1,
        "auftragsdatum": "2024-01-10",
        "lieferdatum": "2024-01-20",
        "status": "abgeschlossen",
        "bemerkung": "Standardlieferung",
        "positionen": [
            {"artikel_id": 1, "menge": 5, "einzelpreis": 249.99},
            {"artikel_id": 2, "menge": 2, "einzelpreis": 349.99}
        ]
    },
    {
        "id": 2,
        "auftragsnummer": "A-2024-002",
        "kunde_id": 2,
        "auftragsdatum": "2024-02-15",
        "lieferdatum": "2024-03-01",
        "status": "in_bearbeitung",
        "bemerkung": "Expresslieferung",
        "positionen": [
            {"artikel_id": 1, "menge": 3, "einzelpreis": 249.99}
        ]
    }
]

# Bestellungen-Daten
bestellungen = [
    {
        "id": 1,
        "bestellnummer": "B-2024-001",
        "lieferant_id": 1,
        "bestelldatum": "2024-01-05",
        "lieferdatum": "2024-01-15",
        "status": "abgeschlossen",
        "bemerkung": "Standardbestellung",
        "positionen": [
            {"artikel_id": 1, "menge": 10, "einzelpreis": 149.99},
            {"artikel_id": 2, "menge": 5, "einzelpreis": 249.99}
        ]
    },
    {
        "id": 2,
        "bestellnummer": "B-2024-002",
        "lieferant_id": 2,
        "bestelldatum": "2024-02-10",
        "lieferdatum": "2024-02-25",
        "status": "in_bearbeitung",
        "bemerkung": "Dringend",
        "positionen": [
            {"artikel_id": 1, "menge": 5, "einzelpreis": 149.99}
        ]
    }
]

# Lieferanten-Daten
lieferanten = [
    {
        "id": 1,
        "lieferantennummer": "L-1001",
        "firma": "Büromöbel GmbH",
        "ansprechpartner": "Klaus Weber",
        "strasse": "Industriestraße 10",
        "plz": "50678",
        "ort": "Köln",
        "telefon": "+49 221 12345678",
        "email": "kontakt@bueromoebel-gmbh.de",
        "lieferant_seit": "2020-01-01"
    },
    {
        "id": 2,
        "lieferantennummer": "L-1002",
        "firma": "IT-Zubehör AG",
        "ansprechpartner": "Sandra Meier",
        "strasse": "Technikweg 5",
        "plz": "80331",
        "ort": "München",
        "telefon": "+49 89 87654321",
        "email": "info@it-zubehoer.de",
        "lieferant_seit": "2021-03-15"
    }
]

# Rechnungen-Daten
rechnungen = [
    {
        "id": 1,
        "rechnungsnummer": "R-2024-001",
        "auftrag_id": 1,
        "kunde_id": 1,
        "rechnungsdatum": "2024-01-21",
        "faelligkeitsdatum": "2024-02-20",
        "status": "bezahlt",
        "zahlungseingang": "2024-02-18",
        "betrag": 1748.93,
        "bemerkung": "Zahlung per Überweisung"
    },
    {
        "id": 2,
        "rechnungsnummer": "R-2024-002",
        "auftrag_id": 2,
        "kunde_id": 2,
        "rechnungsdatum": "2024-03-02",
        "faelligkeitsdatum": "2024-04-01",
        "status": "offen",
        "zahlungseingang": None,
        "betrag": 749.97,
        "bemerkung": "Standardrechnung"
    }
]

# Eingangslieferscheine-Daten
eingangslieferscheine = [
    {
        "id": 1,
        "nummer": "ELS-2024-001",
        "bestellung_id": 1,
        "lieferant_id": 1,
        "lieferdatum": "2024-01-15",
        "status": "abgeschlossen",
        "bemerkung": "Komplette Lieferung",
        "positionen": [
            {"artikel_id": 1, "menge": 10, "lager_id": 1},
            {"artikel_id": 2, "menge": 5, "lager_id": 1}
        ]
    },
    {
        "id": 2,
        "nummer": "ELS-2024-002",
        "bestellung_id": 2,
        "lieferant_id": 2,
        "lieferdatum": "2024-02-25",
        "status": "teillieferung",
        "bemerkung": "Teillieferung, Rest folgt",
        "positionen": [
            {"artikel_id": 1, "menge": 3, "lager_id": 1}
        ]
    }
]

# Verkaufslieferscheine-Daten
verkaufslieferscheine = [
    {
        "id": 1,
        "nummer": "VLS-2024-001",
        "auftrag_id": 1,
        "kunde_id": 1,
        "lieferdatum": "2024-01-20",
        "status": "abgeschlossen",
        "bemerkung": "Komplette Lieferung",
        "positionen": [
            {"artikel_id": 1, "menge": 5, "lager_id": 1},
            {"artikel_id": 2, "menge": 2, "lager_id": 1}
        ]
    },
    {
        "id": 2,
        "nummer": "VLS-2024-002",
        "auftrag_id": 2,
        "kunde_id": 2,
        "lieferdatum": "2024-03-01",
        "status": "in_vorbereitung",
        "bemerkung": "Express-Versand",
        "positionen": [
            {"artikel_id": 1, "menge": 3, "lager_id": 1}
        ]
    }
]

# Projekte-Daten
projekte = [
    {
        "id": 1,
        "projektnummer": "P-2024-001",
        "kunde_id": 1,
        "bezeichnung": "Büroausstattung Hauptsitz",
        "startdatum": "2024-01-10",
        "enddatum": "2024-02-28",
        "status": "abgeschlossen",
        "budget": 10000.00,
        "projektleiter": "Anna Schmidt",
        "bemerkung": "Komplettausstattung für neuen Hauptsitz"
    },
    {
        "id": 2,
        "projektnummer": "P-2024-002",
        "kunde_id": 2,
        "bezeichnung": "IT-Infrastruktur Upgrade",
        "startdatum": "2024-03-01",
        "enddatum": "2024-06-30",
        "status": "in_bearbeitung",
        "budget": 25000.00,
        "projektleiter": "Michael Weber",
        "bemerkung": "Modernisierung der IT-Infrastruktur"
    }
]

# Zeiterfassungen-Daten
zeiterfassungen = [
    {
        "id": 1,
        "mitarbeiter_id": 1,
        "projekt_id": 1,
        "datum": "2024-01-15",
        "stunden": 8.5,
        "taetigkeit": "Installation Büromöbel",
        "bemerkung": "Etage 1 komplett"
    },
    {
        "id": 2,
        "mitarbeiter_id": 2,
        "projekt_id": 1,
        "datum": "2024-01-15",
        "stunden": 7.75,
        "taetigkeit": "Installation Büromöbel",
        "bemerkung": "Etage 2 teilweise"
    }
]

# Dokumente-Daten
dokumente = [
    {
        "id": 1,
        "titel": "Angebot Büroausstattung",
        "typ": "Angebot",
        "pfad": "/dokumente/angebote/A-2024-001.pdf",
        "kunde_id": 1,
        "projekt_id": 1,
        "hochgeladen_am": "2024-01-05",
        "hochgeladen_von": "Michael Weber",
        "bemerkung": "Ursprüngliches Angebot"
    },
    {
        "id": 2,
        "titel": "Lieferschein Bürostühle",
        "typ": "Lieferschein",
        "pfad": "/dokumente/lieferscheine/L-2024-001.pdf",
        "kunde_id": 1,
        "projekt_id": 1,
        "hochgeladen_am": "2024-01-12",
        "hochgeladen_von": "Anna Schmidt",
        "bemerkung": "Lieferung Bürostühle"
    }
]

# --------------- API-Endpunkte ---------------

# Root-Endpunkt
async def root(request):
    return JSONResponse({
        "message": "Willkommen beim AI-Driven ERP System",
        "version": "1.0.0",
        "dokumentation": "/docs"
    })

# Gesundheitscheck
async def health_check(request):
    return JSONResponse({
        "status": "healthy", 
        "timestamp": datetime.utcnow().isoformat(),
        "api_version": "1.0",
        "services": {
            "database": "connected",
            "auth": "operational",
            "file_storage": "operational"
        }
    })

# --- Adresse-Endpunkte (im L3-Format) ---
async def get_adressen(request):
    filter_query = request.query_params.get("$filter")
    if filter_query:
        # Einfache Filterung für Demo-Zwecke
        if "Nummer eq " in filter_query:
            nummer = int(filter_query.split("Nummer eq ")[1])
            filtered = [a for a in adressen if a["Nummer"] == nummer]
            return JSONResponse({"Data": filtered})
    
    return JSONResponse({"Data": adressen})

# --- Artikel-Endpunkte (im L3-Format) ---
async def get_artikel_l3_format(request):
    filter_query = request.query_params.get("$filter")
    if filter_query:
        # Einfache Filterung für Demo-Zwecke
        if "Nummer eq '" in filter_query:
            nummer = filter_query.split("Nummer eq '")[1].split("'")[0]
            filtered = [
                {
                    "Nummer": a["artikelnummer"],
                    "Bezeichnung": a["bezeichnung"],
                    "Beschreibung": f"Kategorie: {a['kategorie']}",
                    "VerkPreis": a["preis"],
                    "EinkPreis": a["preis"] * 0.6,  # Demo-Zwecke
                    "Einheit": a["einheit"],
                    "Bestand": a["lagerbestand"]
                } 
                for a in artikel if a["artikelnummer"] == nummer
            ]
            return JSONResponse({"Data": filtered})
    
    # Konvertiere in L3-Format
    l3_artikel = [
        {
            "Nummer": a["artikelnummer"],
            "Bezeichnung": a["bezeichnung"],
            "Beschreibung": f"Kategorie: {a['kategorie']}",
            "VerkPreis": a["preis"],
            "EinkPreis": a["preis"] * 0.6,  # Demo-Zwecke
            "Einheit": a["einheit"],
            "Bestand": a["lagerbestand"]
        } 
        for a in artikel
    ]
    
    return JSONResponse({"Data": l3_artikel})

# --- Inventur-Endpunkte ---
async def get_inventuren(request):
    return JSONResponse({"inventuren": inventuren})

async def get_inventur(request):
    inventur_id = int(request.path_params["inventur_id"])
    for inv in inventuren:
        if inv["id"] == inventur_id:
            return JSONResponse(inv)
    return JSONResponse({"error": "Inventur nicht gefunden"}, status_code=404)

# --- Artikel-Endpunkte (Standard-Format) ---
async def get_artikel_standard(request):
    return JSONResponse({"artikel": artikel})

async def get_artikel_by_id(request):
    artikel_id = int(request.path_params["artikel_id"])
    for art in artikel:
        if art["id"] == artikel_id:
            return JSONResponse(art)
    return JSONResponse({"error": "Artikel nicht gefunden"}, status_code=404)

# --- Lager-Endpunkte ---
async def get_lager(request):
    filter_query = request.query_params.get("$filter")
    if filter_query:
        # Implementiere L3-ähnliche Filterung hier
        pass
    
    return JSONResponse({"lager": lager})

async def get_lager_by_id(request):
    lager_id = int(request.path_params["lager_id"])
    for l in lager:
        if l["id"] == lager_id:
            return JSONResponse(l)
    return JSONResponse({"error": "Lager nicht gefunden"}, status_code=404)

# --- Kunden-Endpunkte ---
async def get_kunden(request):
    filter_query = request.query_params.get("$filter")
    if filter_query:
        # Implementiere L3-ähnliche Filterung hier
        if "Nummer eq " in filter_query:
            nummer = int(filter_query.split("Nummer eq ")[1])
            filtered = [k for k in kunden if k["id"] == nummer]
            return JSONResponse({"Data": filtered})
    
    return JSONResponse({"kunden": kunden})

async def get_kunde_by_id(request):
    kunde_id = int(request.path_params["kunde_id"])
    for k in kunden:
        if k["id"] == kunde_id:
            return JSONResponse(k)
    return JSONResponse({"error": "Kunde nicht gefunden"}, status_code=404)

# --- Aufträge-Endpunkte ---
async def get_auftraege(request):
    filter_query = request.query_params.get("$filter")
    if filter_query:
        # Implementiere L3-ähnliche Filterung hier
        if "Nummer eq '" in filter_query:
            nummer = filter_query.split("Nummer eq '")[1].split("'")[0]
            filtered = [a for a in auftraege if a["auftragsnummer"] == nummer]
            return JSONResponse({"Data": filtered})
    
    return JSONResponse({"auftraege": auftraege})

async def get_auftrag_by_id(request):
    auftrag_id = int(request.path_params["auftrag_id"])
    for a in auftraege:
        if a["id"] == auftrag_id:
            return JSONResponse(a)
    return JSONResponse({"error": "Auftrag nicht gefunden"}, status_code=404)

# --- Bestellungen-Endpunkte ---
async def get_bestellungen(request):
    return JSONResponse({"bestellungen": bestellungen})

async def get_bestellung_by_id(request):
    bestellung_id = int(request.path_params["bestellung_id"])
    for b in bestellungen:
        if b["id"] == bestellung_id:
            return JSONResponse(b)
    return JSONResponse({"error": "Bestellung nicht gefunden"}, status_code=404)

# --- Lieferanten-Endpunkte ---
async def get_lieferanten(request):
    return JSONResponse({"lieferanten": lieferanten})

async def get_lieferant_by_id(request):
    lieferant_id = int(request.path_params["lieferant_id"])
    for l in lieferanten:
        if l["id"] == lieferant_id:
            return JSONResponse(l)
    return JSONResponse({"error": "Lieferant nicht gefunden"}, status_code=404)

# --- Rechnungen-Endpunkte ---
async def get_rechnungen(request):
    return JSONResponse({"rechnungen": rechnungen})

async def get_rechnung_by_id(request):
    rechnung_id = int(request.path_params["rechnung_id"])
    for r in rechnungen:
        if r["id"] == rechnung_id:
            return JSONResponse(r)
    return JSONResponse({"error": "Rechnung nicht gefunden"}, status_code=404)

# --- Eingangslieferscheine-Endpunkte ---
async def get_eingangslieferscheine(request):
    return JSONResponse({"eingangslieferscheine": eingangslieferscheine})

async def get_eingangslieferschein_by_id(request):
    els_id = int(request.path_params["els_id"])
    for els in eingangslieferscheine:
        if els["id"] == els_id:
            return JSONResponse(els)
    return JSONResponse({"error": "Eingangslieferschein nicht gefunden"}, status_code=404)

# --- Verkaufslieferscheine-Endpunkte ---
async def get_verkaufslieferscheine(request):
    return JSONResponse({"verkaufslieferscheine": verkaufslieferscheine})

async def get_verkaufslieferschein_by_id(request):
    vls_id = int(request.path_params["vls_id"])
    for vls in verkaufslieferscheine:
        if vls["id"] == vls_id:
            return JSONResponse(vls)
    return JSONResponse({"error": "Verkaufslieferschein nicht gefunden"}, status_code=404)

# --- Projekte-Endpunkte ---
async def get_projekte(request):
    return JSONResponse({"projekte": projekte})

async def get_projekt_by_id(request):
    projekt_id = int(request.path_params["projekt_id"])
    for p in projekte:
        if p["id"] == projekt_id:
            return JSONResponse(p)
    return JSONResponse({"error": "Projekt nicht gefunden"}, status_code=404)

# --- Zeiterfassung-Endpunkte ---
async def get_zeiterfassungen(request):
    projekt_id = request.query_params.get("projekt_id")
    mitarbeiter_id = request.query_params.get("mitarbeiter_id")
    
    if projekt_id:
        projekt_zeiten = [z for z in zeiterfassungen if z["projekt_id"] == int(projekt_id)]
        return JSONResponse({"zeiterfassungen": projekt_zeiten})
    elif mitarbeiter_id:
        mitarbeiter_zeiten = [z for z in zeiterfassungen if z["mitarbeiter_id"] == int(mitarbeiter_id)]
        return JSONResponse({"zeiterfassungen": mitarbeiter_zeiten})
    else:
        return JSONResponse({"zeiterfassungen": zeiterfassungen})

# --- Dokumente-Endpunkte ---
async def get_dokumente(request):
    return JSONResponse({"dokumente": dokumente})

async def get_dokument_by_id(request):
    dokument_id = int(request.path_params["dokument_id"])
    for d in dokumente:
        if d["id"] == dokument_id:
            return JSONResponse(d)
    return JSONResponse({"error": "Dokument nicht gefunden"}, status_code=404)

# Dashboard-Daten
async def get_dashboard_data(request):
    today = datetime.now().date()
    
    # Beispiel-Dashboard-Daten
    return JSONResponse({
        "umsatz_heute": 1245.67,
        "umsatz_monat": 38756.92,
        "offene_auftraege": 3,
        "offene_rechnungen": 5,
        "laufende_projekte": 2,
        "artikel_nachbestellen": [artikel[0]],
        "letzte_aktivitaeten": [
            {
                "typ": "Auftrag",
                "beschreibung": "Neuer Auftrag A-2024-003 erstellt",
                "zeitpunkt": (datetime.now() - timedelta(hours=2)).isoformat()
            },
            {
                "typ": "Rechnung",
                "beschreibung": "Rechnung R-2024-002 bezahlt",
                "zeitpunkt": (datetime.now() - timedelta(hours=4)).isoformat()
            }
        ]
    })

# Authentifizierung
async def login(request):
    try:
        body = await request.json()
        username = body.get("username")
        password = body.get("password")
        
        if username and password:
            # In einer echten Anwendung würde hier die Authentifizierung stattfinden
            token = str(uuid4())
            return JSONResponse({
                "token": token,
                "user": {
                    "id": 1,
                    "username": username,
                    "name": "Max Mustermann",
                    "role": "admin"
                }
            })
        else:
            return JSONResponse({"error": "Benutzername und Passwort erforderlich"}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)

# Swagger-UI
async def swagger_ui(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI-Driven ERP API Dokumentation</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui.css" />
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui-bundle.js" charset="UTF-8"></script>
        <script>
            window.onload = function() {
                const ui = SwaggerUIBundle({
                    url: "/api/v1/openapi.json",
                    dom_id: '#swagger-ui',
                    presets: [
                        SwaggerUIBundle.presets.apis
                    ],
                    layout: "BaseLayout"
                })
            }
        </script>
    </body>
    </html>
    """
    return PlainTextResponse(html, media_type="text/html")

# OpenAPI Spec
async def openapi_spec(request):
    return JSONResponse({
        "openapi": "3.0.0",
        "info": {
            "title": "AI-Driven ERP API",
            "version": "1.0.0",
            "description": "API für das AI-gesteuerte ERP-System"
        },
        "paths": {
            "/api/v1/adresse": {
                "get": {
                    "summary": "Liste aller Adressen (L3-Format)",
                    "responses": {"200": {"description": "Erfolgreiche Anfrage"}}
                }
            },
            "/api/v1/artikel/l3format": {
                "get": {
                    "summary": "Liste aller Artikel (L3-Format)",
                    "responses": {"200": {"description": "Erfolgreiche Anfrage"}}
                }
            },
            "/api/v1/inventur": {
                "get": {
                    "summary": "Liste aller Inventuren",
                    "responses": {"200": {"description": "Erfolgreiche Anfrage"}}
                }
            },
            "/api/v1/artikel": {
                "get": {
                    "summary": "Liste aller Artikel",
                    "responses": {"200": {"description": "Erfolgreiche Anfrage"}}
                }
            }
        }
    })

# Routen definieren
routes = [
    # Grundlegende Endpunkte
    Route("/", endpoint=root),
    Route("/health", endpoint=health_check),
    Route("/docs", endpoint=swagger_ui),
    Route("/api/v1/openapi.json", endpoint=openapi_spec),
    
    # Auth
    Route("/api/v1/auth/login", endpoint=login, methods=["POST"]),
    
    # Dashboard
    Route("/api/v1/dashboard", endpoint=get_dashboard_data),
    
    # L3-Kompatible Endpunkte
    Route("/api/v1/adresse", endpoint=get_adressen),
    Route("/api/v1/artikel/l3format", endpoint=get_artikel_l3_format),
    
    # Inventur-Endpunkte
    Route("/api/v1/inventur", endpoint=get_inventuren),
    Route("/api/v1/inventuren", endpoint=get_inventuren),
    Route("/api/v1/inventur/{inventur_id:int}", endpoint=get_inventur),
    
    # Artikel-Endpunkte
    Route("/api/v1/artikel", endpoint=get_artikel_standard),
    Route("/api/v1/artikel/{artikel_id:int}", endpoint=get_artikel_by_id),
    
    # Lager-Endpunkte
    Route("/api/v1/lager", endpoint=get_lager),
    Route("/api/v1/lager/{lager_id:int}", endpoint=get_lager_by_id),
    
    # Kunden-Endpunkte
    Route("/api/v1/kunden", endpoint=get_kunden),
    Route("/api/v1/kunde", endpoint=get_kunden),  # L3-Kompatibilität
    Route("/api/v1/kunden/{kunde_id:int}", endpoint=get_kunde_by_id),
    
    # Auftrags-Endpunkte
    Route("/api/v1/auftraege", endpoint=get_auftraege),
    Route("/api/v1/auftrag", endpoint=get_auftraege),  # L3-Kompatibilität
    Route("/api/v1/auftraege/{auftrag_id:int}", endpoint=get_auftrag_by_id),
    
    # Bestellungs-Endpunkte
    Route("/api/v1/bestellungen", endpoint=get_bestellungen),
    Route("/api/v1/bestellung", endpoint=get_bestellungen),  # L3-Kompatibilität
    Route("/api/v1/bestellungen/{bestellung_id:int}", endpoint=get_bestellung_by_id),
    
    # Lieferanten-Endpunkte
    Route("/api/v1/lieferanten", endpoint=get_lieferanten),
    Route("/api/v1/lieferanten/{lieferant_id:int}", endpoint=get_lieferant_by_id),
    
    # Rechnungs-Endpunkte
    Route("/api/v1/rechnungen", endpoint=get_rechnungen),
    Route("/api/v1/rechnungsausgang", endpoint=get_rechnungen),  # L3-Kompatibilität
    Route("/api/v1/rechnungen/{rechnung_id:int}", endpoint=get_rechnung_by_id),
    
    # Lieferschein-Endpunkte
    Route("/api/v1/eingangslieferscheine", endpoint=get_eingangslieferscheine),
    Route("/api/v1/eingangslieferschein", endpoint=get_eingangslieferscheine),  # L3-Kompatibilität
    Route("/api/v1/eingangslieferscheine/{els_id:int}", endpoint=get_eingangslieferschein_by_id),
    
    Route("/api/v1/verkaufslieferscheine", endpoint=get_verkaufslieferscheine),
    Route("/api/v1/verkaufslieferschein", endpoint=get_verkaufslieferscheine),  # L3-Kompatibilität
    Route("/api/v1/verkaufslieferscheine/{vls_id:int}", endpoint=get_verkaufslieferschein_by_id),
    
    # Projekt-Endpunkte
    Route("/api/v1/projekte", endpoint=get_projekte),
    Route("/api/v1/projekte/{projekt_id:int}", endpoint=get_projekt_by_id),
    
    # Zeiterfassungs-Endpunkte
    Route("/api/v1/zeiterfassung", endpoint=get_zeiterfassungen),
    
    # Dokument-Endpunkte
    Route("/api/v1/dokumente", endpoint=get_dokumente),
    Route("/api/v1/dms", endpoint=get_dokumente),  # L3-Kompatibilität
    Route("/api/v1/dokumente/{dokument_id:int}", endpoint=get_dokument_by_id),
]

# Middleware definieren
middleware = [
    Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
]

# Starlette-App erstellen
app = Starlette(
    debug=True,
    routes=routes,
    middleware=middleware
)

# Server starten
if __name__ == "__main__":
    print("Minimaler Server wird gestartet...")
    print("Server läuft auf http://localhost:8000")
    print("API-Dokumentation verfügbar unter: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000) 