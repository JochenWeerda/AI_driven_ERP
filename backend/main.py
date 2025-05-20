from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router
from app.core.mcp import setup_mcp_client

app = FastAPI(
    title="AI-Driven ERP",
    description="Modernes Warenwirtschaftssystem mit KI-Integration",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS-Konfiguration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API-Router einbinden
app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """Initialisierung beim Start der Anwendung"""
    await setup_mcp_client()

@app.get("/health")
async def health_check():
    """Health-Check-Endpunkt"""
    return {"status": "healthy", "version": "0.1.0"} 