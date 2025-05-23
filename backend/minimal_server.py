"""
Minimaler Server für das AI-gesteuerte ERP-System ohne FastAPI/Pydantic
Umgeht die Probleme mit Python 3.13.3
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime, timedelta, UTC
from uuid import uuid4
import psutil
import time

# Füge Verzeichnisse zum Python-Pfad hinzu
backend_dir = Path(__file__).parent.absolute()
root_dir = backend_dir.parent
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(backend_dir))

# Import des Cache-Managers
from cache_manager import cache

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

# E-Commerce-Daten
produkte = [
    {
        "id": 1,
        "sku": "P-10001",
        "name": "Business Laptop Pro",
        "description": "Leistungsstarker Laptop für professionelle Anwendungen",
        "price": 1299.99,
        "cost_price": 899.99,
        "inventory_level": 25,
        "category_id": 1,
        "tax_rate": 19.0,
        "weight": 1.8,
        "dimensions": "35 x 25 x 2 cm",
        "active": True,
        "created_at": "2024-01-01T10:00:00",
        "updated_at": None,
        "image_urls": ["https://example.com/images/laptop1.jpg"],
        "tags": ["business", "laptop", "premium"]
    },
    {
        "id": 2,
        "sku": "P-10002",
        "name": "Wireless Office Headset",
        "description": "Komfortables Headset für Bürokommunikation",
        "price": 129.99,
        "cost_price": 69.99,
        "inventory_level": 42,
        "category_id": 2,
        "tax_rate": 19.0,
        "weight": 0.3,
        "dimensions": "20 x 18 x 8 cm",
        "active": True,
        "created_at": "2024-01-05T11:30:00",
        "updated_at": None,
        "image_urls": ["https://example.com/images/headset1.jpg"],
        "tags": ["audio", "büro", "kommunikation"]
    }
]

produkt_kategorien = [
    {
        "id": 1,
        "name": "Computer & Laptops",
        "description": "Computer, Laptops und Zubehör",
        "parent_id": None,
        "active": True,
        "created_at": "2024-01-01T08:00:00",
        "updated_at": None
    },
    {
        "id": 2,
        "name": "Audio & Headsets",
        "description": "Kopfhörer, Mikrofone und Audiozubehör",
        "parent_id": None,
        "active": True,
        "created_at": "2024-01-01T08:15:00",
        "updated_at": None
    }
]

warenkörbe = [
    {
        "id": 1,
        "customer_id": 1,
        "session_id": "sess_abc123",
        "created_at": "2024-03-15T14:30:00",
        "updated_at": "2024-03-15T14:45:00",
        "items": [
            {
                "id": 1,
                "cart_id": 1,
                "product_id": 1,
                "quantity": 1,
                "price": 1299.99,
                "created_at": "2024-03-15T14:30:00",
                "updated_at": None
            }
        ]
    }
]

bestellungen_ecommerce = [
    {
        "id": 1,
        "order_number": "ORD-20240310-abc123",
        "customer_id": 1,
        "order_date": "2024-03-10T15:30:00",
        "status": "versandt",
        "shipping_address_id": 1,
        "billing_address_id": 1,
        "payment_method": "kreditkarte",
        "shipping_method": "standard",
        "subtotal": 1299.99,
        "tax_amount": 246.99,
        "shipping_cost": 4.99,
        "discount_amount": 0.0,
        "total_amount": 1551.97,
        "notes": "Bitte vor der Haustür abstellen",
        "created_at": "2024-03-10T15:30:00",
        "updated_at": "2024-03-11T09:15:00"
    }
]

bestellpositionen = [
    {
        "id": 1,
        "order_id": 1,
        "product_id": 1,
        "product_name": "Business Laptop Pro",
        "quantity": 1,
        "unit_price": 1299.99,
        "tax_rate": 19.0,
        "discount_amount": 0.0,
        "total_price": 1546.98,
        "created_at": "2024-03-10T15:30:00"
    }
]

adressen_ecommerce = [
    {
        "id": 1,
        "customer_id": 1,
        "address_type": "shipping",
        "first_name": "Thomas",
        "last_name": "Müller",
        "company": "Muster GmbH",
        "street": "Hauptstraße 1",
        "additional": "Etage 3",
        "postal_code": "10115",
        "city": "Berlin",
        "country": "Deutschland",
        "phone": "+49 30 12345678",
        "is_default": True,
        "created_at": "2024-01-15T10:00:00",
        "updated_at": None
    },
    {
        "id": 2,
        "customer_id": 1,
        "address_type": "billing",
        "first_name": "Thomas",
        "last_name": "Müller",
        "company": "Muster GmbH",
        "street": "Hauptstraße 1",
        "additional": "Etage 3",
        "postal_code": "10115",
        "city": "Berlin",
        "country": "Deutschland",
        "phone": "+49 30 12345678",
        "is_default": True,
        "created_at": "2024-01-15T10:00:00",
        "updated_at": None
    }
]

rabatte = [
    {
        "id": 1,
        "code": "SOMMER2024",
        "description": "Sommerrabatt 2024",
        "discount_type": "prozentual",
        "discount_value": 10.0,
        "minimum_order_value": 50.0,
        "valid_from": "2024-06-01T00:00:00",
        "valid_to": "2024-08-31T23:59:59",
        "usage_limit": 1000,
        "used_count": 45,
        "active": True,
        "created_at": "2024-05-15T09:00:00",
        "updated_at": None
    }
]

bewertungen = [
    {
        "id": 1,
        "product_id": 1,
        "customer_id": 1,
        "rating": 5,
        "title": "Hervorragendes Produkt",
        "comment": "Bin sehr zufrieden mit dem Laptop. Schnell, leise und tolles Display.",
        "verified_purchase": True,
        "created_at": "2024-03-20T18:30:00",
        "updated_at": None,
        "is_approved": True
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

# Gesundheitscheck mit Performance-Optimierung
@cache.cached(ttl=10)  # 10 Sekunden cachen
async def health_check(request):
    # CPU-Nutzung des aktuellen Prozesses ermitteln - reduziertes Intervall
    current_process = psutil.Process(os.getpid())
    
    # Keine CPU-Messung bei jeder Anfrage, da teuer
    # Stattdessen alle 10 Sekunden per Cache-TTL
    cpu_usage = current_process.cpu_percent(interval=0.05)
    
    # Speichernutzung ermitteln
    memory_info = current_process.memory_info()
    memory_usage_percent = current_process.memory_percent()
    
    # Laufzeit berechnen
    start_time = current_process.create_time()
    uptime_seconds = time.time() - start_time
    
    # Aktuelle Zeit im ISO-Format mit UTC
    current_time = datetime.now(UTC).isoformat()
    
    # API-Anfragen zählen (einfache statische Variable für Demonstration)
    if not hasattr(health_check, "request_count"):
        health_check.request_count = 0
    health_check.request_count += 1
    
    # Durchschnittliche Antwortzeit (Mock-Wert für Demonstration)
    avg_response_time = 42.5  # ms
    
    return JSONResponse({
        "status": "online",
        "version": "1.0.0",
        "timestamp": current_time,
        "uptime_seconds": int(uptime_seconds),
        "metrics": {
            "cpu_usage_percent": round(cpu_usage, 2),
            "memory_usage_percent": round(memory_usage_percent, 2),
            "request_count": health_check.request_count,
            "average_response_time_ms": avg_response_time,
            "database_connections": 3,
            "queue_size": 0
        },
        "services": {
            "database": "connected",
            "auth": "operational",
            "file_storage": "operational"
        }
    })

# --- Adresse-Endpunkte (im L3-Format) ---
@cache.cached(ttl=60)
async def get_adressen(request):
    filter_query = request.query_params.get("$filter")
    if filter_query:
        # Einfache Filterung für Demo-Zwecke
        if "Nummer eq " in filter_query:
            nummer = int(filter_query.split("Nummer eq ")[1])
            # Direkter Lookup statt Liste filtern
            addr = lookup_maps['adressen_by_nummer'].get(nummer)
            if addr:
                return JSONResponse({"Data": [addr]})
            return JSONResponse({"Data": []})
    
    return JSONResponse({"Data": adressen})

# --- Artikel-Endpunkte (im L3-Format) ---
@cache.cached(ttl=120)
async def get_artikel_l3_format(request):
    filter_query = request.query_params.get("$filter")
    if filter_query:
        # Einfache Filterung für Demo-Zwecke
        if "Nummer eq '" in filter_query:
            nummer = filter_query.split("Nummer eq '")[1].split("'")[0]
            # Verwende Lookup-Map statt Liste filtern
            artikel_item = lookup_maps['artikel_by_nummer'].get(nummer)
            if artikel_item:
                l3_artikel = {
                    "Nummer": artikel_item["artikelnummer"],
                    "Bezeichnung": artikel_item["bezeichnung"],
                    "Beschreibung": f"Kategorie: {artikel_item['kategorie']}",
                    "VerkPreis": artikel_item["preis"],
                    "EinkPreis": artikel_item["preis"] * 0.6,  # Demo-Zwecke
                    "Einheit": artikel_item["einheit"],
                    "Bestand": artikel_item["lagerbestand"]
                }
                return JSONResponse({"Data": [l3_artikel]})
            return JSONResponse({"Data": []})
    
    # Konvertiere in L3-Format - einmal berechnen und cachen
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
@cache.cached(ttl=300)
async def get_inventuren(request):
    return JSONResponse({"inventuren": inventuren})

@cache.cached(ttl=300)
async def get_inventur(request):
    inventur_id = int(request.path_params["inventur_id"])
    inv = lookup_maps['inventuren_by_id'].get(inventur_id)
    if inv:
        return JSONResponse(inv)
    return JSONResponse({"error": "Inventur nicht gefunden"}, status_code=404)

# --- Artikel-Endpunkte (Standard-Format) ---
@cache.cached(ttl=120)
async def get_artikel_standard(request):
    return JSONResponse({"artikel": artikel})

@cache.cached(ttl=120)
async def get_artikel_by_id(request):
    artikel_id = int(request.path_params["artikel_id"])
    art = lookup_maps['artikel_by_id'].get(artikel_id)
    if art:
        return JSONResponse(art)
    return JSONResponse({"error": "Artikel nicht gefunden"}, status_code=404)

# --- Lager-Endpunkte ---
@cache.cached(ttl=300)
async def get_lager(request):
    filter_query = request.query_params.get("$filter")
    if filter_query:
        # Implementiere L3-ähnliche Filterung hier
        pass
    
    return JSONResponse({"lager": lager})

@cache.cached(ttl=300)
async def get_lager_by_id(request):
    lager_id = int(request.path_params["lager_id"])
    l = lookup_maps['lager_by_id'].get(lager_id)
    if l:
        return JSONResponse(l)
    return JSONResponse({"error": "Lager nicht gefunden"}, status_code=404)

# --- Kunden-Endpunkte ---
@cache.cached(ttl=180)
async def get_kunden(request):
    filter_query = request.query_params.get("$filter")
    if filter_query:
        # Implementiere L3-ähnliche Filterung hier
        if "Nummer eq " in filter_query:
            nummer = int(filter_query.split("Nummer eq ")[1])
            # Verwende Lookup statt Liste filtern
            kunde = lookup_maps['kunden_by_id'].get(nummer)
            if kunde:
                return JSONResponse({"Data": [kunde]})
            return JSONResponse({"Data": []})
    
    return JSONResponse({"kunden": kunden})

@cache.cached(ttl=180)
async def get_kunde_by_id(request):
    kunde_id = int(request.path_params["kunde_id"])
    k = lookup_maps['kunden_by_id'].get(kunde_id)
    if k:
        return JSONResponse(k)
    return JSONResponse({"error": "Kunde nicht gefunden"}, status_code=404)

# --- Aufträge-Endpunkte ---
@cache.cached(ttl=120)
async def get_auftraege(request):
    filter_query = request.query_params.get("$filter")
    if filter_query:
        # Implementiere L3-ähnliche Filterung hier
        if "Nummer eq '" in filter_query:
            nummer = filter_query.split("Nummer eq '")[1].split("'")[0]
            # Verwende Lookup statt Liste filtern
            auftrag = lookup_maps['auftraege_by_nummer'].get(nummer)
            if auftrag:
                return JSONResponse({"Data": [auftrag]})
            return JSONResponse({"Data": []})
    
    return JSONResponse({"auftraege": auftraege})

@cache.cached(ttl=120)
async def get_auftrag_by_id(request):
    auftrag_id = int(request.path_params["auftrag_id"])
    a = lookup_maps['auftraege_by_id'].get(auftrag_id)
    if a:
        return JSONResponse(a)
    return JSONResponse({"error": "Auftrag nicht gefunden"}, status_code=404)

# --- Bestellungen-Endpunkte ---
@cache.cached(ttl=120)
async def get_bestellungen(request):
    return JSONResponse({"bestellungen": bestellungen})

@cache.cached(ttl=120)
async def get_bestellung_by_id(request):
    bestellung_id = int(request.path_params["bestellung_id"])
    b = lookup_maps['bestellungen_by_id'].get(bestellung_id)
    if b:
        return JSONResponse(b)
    return JSONResponse({"error": "Bestellung nicht gefunden"}, status_code=404)

# --- Lieferanten-Endpunkte ---
@cache.cached(ttl=300)
async def get_lieferanten(request):
    return JSONResponse({"lieferanten": lieferanten})

@cache.cached(ttl=300)
async def get_lieferant_by_id(request):
    lieferant_id = int(request.path_params["lieferant_id"])
    l = lookup_maps['lieferanten_by_id'].get(lieferant_id)
    if l:
        return JSONResponse(l)
    return JSONResponse({"error": "Lieferant nicht gefunden"}, status_code=404)

# --- Rechnungen-Endpunkte ---
@cache.cached(ttl=180)
async def get_rechnungen(request):
    return JSONResponse({"rechnungen": rechnungen})

@cache.cached(ttl=180)
async def get_rechnung_by_id(request):
    rechnung_id = int(request.path_params["rechnung_id"])
    r = lookup_maps['rechnungen_by_id'].get(rechnung_id)
    if r:
        return JSONResponse(r)
    return JSONResponse({"error": "Rechnung nicht gefunden"}, status_code=404)

# --- Eingangslieferscheine-Endpunkte ---
@cache.cached(ttl=180)
async def get_eingangslieferscheine(request):
    return JSONResponse({"eingangslieferscheine": eingangslieferscheine})

@cache.cached(ttl=180)
async def get_eingangslieferschein_by_id(request):
    els_id = int(request.path_params["els_id"])
    els = lookup_maps['els_by_id'].get(els_id)
    if els:
        return JSONResponse(els)
    return JSONResponse({"error": "Eingangslieferschein nicht gefunden"}, status_code=404)

# --- Verkaufslieferscheine-Endpunkte ---
@cache.cached(ttl=180)
async def get_verkaufslieferscheine(request):
    return JSONResponse({"verkaufslieferscheine": verkaufslieferscheine})

@cache.cached(ttl=180)
async def get_verkaufslieferschein_by_id(request):
    vls_id = int(request.path_params["vls_id"])
    vls = lookup_maps['vls_by_id'].get(vls_id)
    if vls:
        return JSONResponse(vls)
    return JSONResponse({"error": "Verkaufslieferschein nicht gefunden"}, status_code=404)

# --- Projekt-Endpunkte ---
@cache.cached(ttl=240)
async def get_projekte(request):
    return JSONResponse({"projekte": projekte})

@cache.cached(ttl=240)
async def get_projekt_by_id(request):
    projekt_id = int(request.path_params["projekt_id"])
    p = lookup_maps['projekte_by_id'].get(projekt_id)
    if p:
        return JSONResponse(p)
    return JSONResponse({"error": "Projekt nicht gefunden"}, status_code=404)

# --- Zeiterfassungs-Endpunkte ---
@cache.cached(ttl=120)
async def get_zeiterfassungen(request):
    projekt_id = request.query_params.get("projekt_id")
    mitarbeiter_id = request.query_params.get("mitarbeiter_id")
    
    # Optimierung: Erstelle Indizes nur wenn nötig (Lazy-Loading)
    if not hasattr(get_zeiterfassungen, "indices_created"):
        get_zeiterfassungen.indices_created = True
        get_zeiterfassungen.by_projekt = {}
        get_zeiterfassungen.by_mitarbeiter = {}
        
        for z in zeiterfassungen:
            pid = z["projekt_id"]
            mid = z["mitarbeiter_id"]
            
            if pid not in get_zeiterfassungen.by_projekt:
                get_zeiterfassungen.by_projekt[pid] = []
            get_zeiterfassungen.by_projekt[pid].append(z)
            
            if mid not in get_zeiterfassungen.by_mitarbeiter:
                get_zeiterfassungen.by_mitarbeiter[mid] = []
            get_zeiterfassungen.by_mitarbeiter[mid].append(z)
    
    if projekt_id:
        pid = int(projekt_id)
        projekt_zeiten = get_zeiterfassungen.by_projekt.get(pid, [])
        return JSONResponse({"zeiterfassungen": projekt_zeiten})
    elif mitarbeiter_id:
        mid = int(mitarbeiter_id)
        mitarbeiter_zeiten = get_zeiterfassungen.by_mitarbeiter.get(mid, [])
        return JSONResponse({"zeiterfassungen": mitarbeiter_zeiten})
    else:
        return JSONResponse({"zeiterfassungen": zeiterfassungen})

# --- Dokumente-Endpunkte ---
@cache.cached(ttl=300)
async def get_dokumente(request):
    return JSONResponse({"dokumente": dokumente})

@cache.cached(ttl=300)
async def get_dokument_by_id(request):
    dokument_id = int(request.path_params["dokument_id"])
    d = lookup_maps['dokumente_by_id'].get(dokument_id)
    if d:
        return JSONResponse(d)
    return JSONResponse({"error": "Dokument nicht gefunden"}, status_code=404)

# Dashboard-Daten
@cache.cached(ttl=60)  # Dashboard-Daten für 60 Sekunden cachen
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

# E-Commerce-Routen mit Cache
@cache.cached(ttl=240)  # 4 Minuten Cache
async def get_produkte(request):
    return JSONResponse({"produkte": produkte})

@cache.cached(ttl=240)
async def get_produkt_by_id(request):
    produkt_id = int(request.path_params["id"])
    p = lookup_maps['produkte_by_id'].get(produkt_id)
    if p:
        return JSONResponse(p)
    return JSONResponse({"error": "Produkt nicht gefunden"}, status_code=404)

@cache.cached(ttl=300)  # 5 Minuten Cache für relativ statische Daten
async def get_produkt_kategorien(request):
    return JSONResponse({"kategorien": produkt_kategorien})

@cache.cached(ttl=300)
async def get_produkt_kategorie_by_id(request):
    kategorie_id = int(request.path_params["id"])
    k = lookup_maps['produkt_kategorien_by_id'].get(kategorie_id)
    if k:
        return JSONResponse(k)
    return JSONResponse({"error": "Kategorie nicht gefunden"}, status_code=404)

# Nicht Cachen - dynamische Daten
async def get_warenkorb(request):
    # In einer echten Anwendung würde hier die Session-ID überprüft werden
    return JSONResponse(warenkörbe[0])

@cache.cached(ttl=120)
async def get_bestellungen_ecommerce(request):
    return JSONResponse({"bestellungen": bestellungen_ecommerce})

@cache.cached(ttl=120)
async def get_bestellung_ecommerce_by_id(request):
    bestellung_id = int(request.path_params["id"])
    b = lookup_maps['bestellungen_ecommerce_by_id'].get(bestellung_id)
    if b:
        return JSONResponse(b)
    return JSONResponse({"error": "Bestellung nicht gefunden"}, status_code=404)

@cache.cached(ttl=180)
async def get_adressen_ecommerce(request):
    return JSONResponse({"adressen": adressen_ecommerce})

@cache.cached(ttl=300)
async def get_rabatte(request):
    return JSONResponse({"rabatte": rabatte})

@cache.cached(ttl=180)
async def get_bewertungen(request):
    return JSONResponse({"bewertungen": bewertungen})

# Lookup-Maps für schnellere ID-basierte Abfragen
def create_lookup_maps():
    # Für alle Datenstrukturen Lookup-Maps erstellen
    lookup_maps = {
        'artikel_by_id': {a['id']: a for a in artikel},
        'artikel_by_nummer': {a['artikelnummer']: a for a in artikel},
        'inventuren_by_id': {i['id']: i for i in inventuren},
        'lager_by_id': {l['id']: l for l in lager},
        'kunden_by_id': {k['id']: k for k in kunden},
        'kunden_by_nummer': {k.get('kundennummer', str(k['id'])): k for k in kunden},
        'auftraege_by_id': {a['id']: a for a in auftraege},
        'auftraege_by_nummer': {a['auftragsnummer']: a for a in auftraege},
        'bestellungen_by_id': {b['id']: b for b in bestellungen},
        'lieferanten_by_id': {l['id']: l for l in lieferanten},
        'rechnungen_by_id': {r['id']: r for r in rechnungen},
        'els_by_id': {e['id']: e for e in eingangslieferscheine},
        'vls_by_id': {v['id']: v for v in verkaufslieferscheine},
        'projekte_by_id': {p['id']: p for p in projekte},
        'dokumente_by_id': {d['id']: d for d in dokumente},
        'produkte_by_id': {p['id']: p for p in produkte},
        'produkt_kategorien_by_id': {k['id']: k for k in produkt_kategorien},
        'bestellungen_ecommerce_by_id': {b['id']: b for b in bestellungen_ecommerce},
        'adressen_by_nummer': {a['Nummer']: a for a in adressen}
    }
    return lookup_maps

# Lookup-Maps erstellen
lookup_maps = create_lookup_maps()

# Optimierte ID-basierte Abfragefunktion
def get_by_id(collection, id_field, id_value):
    map_name = f"{collection}_by_{id_field}"
    if map_name in lookup_maps:
        return lookup_maps[map_name].get(id_value)
    return None

# Routen definieren mit optimierten API-Endpunkten
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
    
    # Neue E-Commerce-Routen
    Route("/api/v1/produkte", endpoint=get_produkte),
    Route("/api/v1/produkte/{id:int}", endpoint=get_produkt_by_id),
    Route("/api/v1/kategorien", endpoint=get_produkt_kategorien),
    Route("/api/v1/kategorien/{id:int}", endpoint=get_produkt_kategorie_by_id),
    Route("/api/v1/warenkorb", endpoint=get_warenkorb),
    Route("/api/v1/ecommerce/bestellungen", endpoint=get_bestellungen_ecommerce),
    Route("/api/v1/ecommerce/bestellungen/{id:int}", endpoint=get_bestellung_ecommerce_by_id),
    Route("/api/v1/ecommerce/adressen", endpoint=get_adressen_ecommerce),
    Route("/api/v1/rabatte", endpoint=get_rabatte),
    Route("/api/v1/bewertungen", endpoint=get_bewertungen),
]

# Middleware konfigurieren mit aktivierten HTTP-Optimierungen
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In Produktionsumgebung einschränken
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

# App mit optimierter Konfiguration erstellen
app = Starlette(
    debug=False,  # Debug-Modus ausschalten für bessere Performance
    routes=routes,
    middleware=middleware,
    on_startup=[create_lookup_maps],  # Lookup-Maps beim Start erstellen
)

# Statische Files für Dokumentation
app.mount("/docs/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")

# Nur wenn direkt ausgeführt
if __name__ == "__main__":
    import argparse
    
    # Kommandozeilenargumente parsen
    parser = argparse.ArgumentParser(description="Minimaler Server für AI-Driven ERP System")
    parser.add_argument("--port", type=int, default=8003, help="Port für den Server (Standard: 8003)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host-Adresse (Standard: 0.0.0.0)")
    parser.add_argument("--workers", type=int, default=4, help="Anzahl der Worker-Prozesse (Standard: 4)")
    args = parser.parse_args()
    
    print(f"Minimaler Server wird gestartet...")
    print(f"Server läuft auf http://localhost:{args.port}")
    print(f"API-Dokumentation verfügbar unter: http://localhost:{args.port}/docs")
    
    # Uvicorn mit optimierten Einstellungen starten
    uvicorn.run(
        "minimal_server:app",
        host=args.host,
        port=args.port,
        workers=args.workers,
        loop="uvloop",  # Schnellere Event-Loop
        http="httptools",  # Schnellerer HTTP-Parser
        log_level="warning",  # Reduziere Log-Ausgabe
        access_log=False,  # Access-Logs für bessere Performance deaktivieren
        limit_concurrency=1000,  # Max. gleichzeitige Verbindungen
        limit_max_requests=10000,  # Max. Anfragen pro Worker
        timeout_keep_alive=5,  # Timeout für Keep-Alive reduzieren
        reload=False,  # Auto-Reload deaktivieren
    ) 