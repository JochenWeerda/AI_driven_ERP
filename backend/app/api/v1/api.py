from fastapi import APIRouter
from backend.app.api.v1.endpoints import auth
from backend.app.api.odata_router import router as odata_router

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(odata_router, prefix="/odata", tags=["odata"]) 