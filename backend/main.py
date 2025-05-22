"""
Hauptmodul des AI-Driven ERP-Systems
"""

# Initialisiere das Pfadregister als erstes
try:
    from core.path_registry import get_registry
    registry = get_registry()
except ImportError:
    try:
        from backend.core.path_registry import get_registry
        registry = get_registry()
    except ImportError:
        # Fallback ohne Pfadregister
        import os
        import sys
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        sys.path.insert(0, current_dir)
        sys.path.insert(0, parent_dir)
        sys.path.insert(0, os.path.join(current_dir, 'app'))

# Importiere den Import-Handler
try:
    from core.import_handler import import_module, import_from, import_all_from
except ImportError:
    try:
        from backend.core.import_handler import import_module, import_from, import_all_from
    except ImportError:
        # Fallback ohne Import-Handler
        import importlib
        def import_module(name):
            try:
                return importlib.import_module(name)
            except ImportError:
                try:
                    return importlib.import_module(f"app.{name}")
                except ImportError:
                    return None
        
        def import_from(module_name, attr):
            module = import_module(module_name)
            if module:
                return getattr(module, attr, None)
            return None
        
        def import_all_from(module_name, *attrs):
            result = {}
            module = import_module(module_name)
            if module:
                for attr in attrs:
                    val = getattr(module, attr, None)
                    if val is not None:
                        result[attr] = val
            return result

# Standard-Imports
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime

# Dynamische Importe über den Handler
settings = import_from('core.config', 'settings')
if not settings:
    settings = import_from('app.core.config', 'settings')

get_db = import_from('db.database', 'get_db')
if not get_db:
    get_db = import_from('app.db.database', 'get_db')

engine = import_from('db.database', 'engine')
if not engine:
    engine = import_from('app.db.database', 'engine')

Base = import_from('db.base', 'Base')
if not Base:
    Base = import_from('app.db.base', 'Base')

api_router = import_from('api.v1.api', 'api_router')
if not api_router:
    api_router = import_from('app.api.v1.api', 'api_router')

# Import der Modelle
Tour = import_from('models.odata_models', 'Tour')
Pickliste = import_from('models.odata_models', 'Pickliste')
Auftrag = import_from('models.odata_models', 'Auftrag')
Auftragsposition = import_from('models.odata_models', 'Auftragsposition')

if not Tour:
    Tour = import_from('app.models.odata_models', 'Tour')
    Pickliste = import_from('app.models.odata_models', 'Pickliste')
    Auftrag = import_from('app.models.odata_models', 'Auftrag')
    Auftragsposition = import_from('app.models.odata_models', 'Auftragsposition')

# Erstelle die Datenbanktabellen
Base.metadata.create_all(bind=engine)

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

@app.on_event("startup")
async def startup_event():
    """Initialisiere die Datenbank mit Testdaten beim Start"""
    try:
        insert_test_data()
        print("Testdaten erfolgreich initialisiert")
    except Exception as e:
        print(f"Fehler beim Initialisieren der Testdaten: {e}")

def insert_test_data():
    """Fügt Testdaten in die Datenbank ein, wenn sie leer ist"""
    db: Session = next(get_db())
    try:
        if db.query(Tour).count() == 0:
            # Erstelle eine Tour
            tour = Tour(
                tournr=1,
                datum=datetime.utcnow(),
                status="planung"
            )
            db.add(tour)
            db.commit()
            db.refresh(tour)
            
            # Erstelle eine Pickliste
            pickliste = Pickliste(
                picklistnr=100,
                erstelltam=datetime.utcnow(),
                status="neu",
                tour_id=tour.id
            )
            db.add(pickliste)
            db.commit()
            db.refresh(pickliste)
            
            # Erstelle einen Auftrag
            auftrag = Auftrag(
                belegnr=200,
                datum=datetime.utcnow(),
                art="lieferung",
                status="neu",
                pickliste_id=pickliste.id
            )
            db.add(auftrag)
            db.commit()
            db.refresh(auftrag)
            
            # Erstelle eine Auftragsposition
            pos = Auftragsposition(
                artikelnr="A-123",
                menge=5,
                auftrag_id=auftrag.id
            )
            db.add(pos)
            db.commit()
    except Exception as e:
        db.rollback()
        print(f"Fehler beim Einfügen der Testdaten: {e}")
        raise
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Willkommen beim AI-Driven ERP System"}

@app.get("/health")
async def health_check():
    """Grundlegender Gesundheitscheck für Watchdog-Prozesse
    
    Dieser Endpunkt wird vom Watchdog regelmäßig abgefragt,
    um zu überprüfen, ob der Server noch reagiert.
    """
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()} 