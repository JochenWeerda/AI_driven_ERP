"""
Einfache Server-Startdatei für das ERP-System
Umgeht die Probleme mit Python 3.13.3 und Pydantic/FastAPI
"""

import sys
import os
import importlib
from pathlib import Path

# Füge Verzeichnisse zum Python-Pfad hinzu
backend_dir = Path(__file__).parent.absolute()
root_dir = backend_dir.parent
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(backend_dir))

# Versuche, die notwendigen Module direkt zu importieren
try:
    # Versuche den Path-Registry-Import
    try:
        from backend.core.path_registry import get_registry
        registry = get_registry()
        print("Pfadregister erfolgreich initialisiert.")
    except ImportError:
        print("Pfadregister nicht gefunden, verwende Standardpfade.")
    
    # Versuche den Import-Handler zu importieren
    try:
        from backend.core.import_handler import import_from
        print("Import-Handler erfolgreich initialisiert.")
    except ImportError:
        print("Import-Handler nicht gefunden, verwende direkte Imports.")
        
        # Definiere eine Ersatzfunktion für import_from
        def import_from(module_path, obj_name):
            try:
                module = importlib.import_module(f"backend.{module_path}")
                return getattr(module, obj_name, None)
            except (ImportError, AttributeError):
                try:
                    module = importlib.import_module(module_path)
                    return getattr(module, obj_name, None)
                except (ImportError, AttributeError):
                    return None
    
    # Direkte App-Erstellung ohne main.py zu importieren
    print("Erstelle App direkt ohne main.py zu importieren.")
    
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    
    # Versuche settings zu importieren
    settings = import_from("app.core.config", "settings")
    if not settings:
        # Fallback-Settings
        class Settings:
            PROJECT_NAME = "AI-Driven ERP"
            VERSION = "0.1.0"
            API_V1_STR = "/api/v1"
            CORS_ORIGINS = ["*"]
        settings = Settings()
    
    # Erstelle die FastAPI-Anwendung
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
    
    # Versuche API-Router zu importieren
    try:
        from backend.app.api.v1.api import api_router
        app.include_router(api_router, prefix=settings.API_V1_STR)
        print("API-Router erfolgreich importiert und eingebunden.")
    except ImportError:
        try:
            from app.api.v1.api import api_router
            app.include_router(api_router, prefix=settings.API_V1_STR)
            print("API-Router erfolgreich importiert und eingebunden.")
        except ImportError:
            print("API-Router konnte nicht importiert werden.")
    
    # Root-Endpunkt
    @app.get("/")
    async def root():
        return {"message": "Willkommen beim AI-Driven ERP System"}
    
    # Gesundheitscheck
    @app.get("/health")
    async def health_check():
        from datetime import datetime
        return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
    
    # Starte den Server
    if __name__ == "__main__":
        import uvicorn
        print("Starte Server auf http://localhost:8000")
        print("API-Dokumentation: http://localhost:8000/docs")
        uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

except Exception as e:
    print(f"Fehler beim Starten des Servers: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc() 