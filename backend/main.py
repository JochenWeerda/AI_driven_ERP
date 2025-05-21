from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.database import get_db, engine
from app.db.base import Base
from app.api.v1.api import api_router
from app.models.odata_models import Tour, Pickliste, Auftrag, Auftragsposition
from datetime import datetime

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
    insert_test_data()

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
    return {"status": "healthy"} 