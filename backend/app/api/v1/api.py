from fastapi import APIRouter
from app.api.v1.endpoints import auth
from app.api.odata_router import router as odata_router
from app.api.v1.endpoints.wws import router as wws_router
from app.api.v1.endpoints.tse import router as tse_router
from app.api.v1.endpoints.waage import router as waage_router
from app.api.v1.endpoints.status import router as status_router

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(odata_router, prefix="/odata", tags=["odata"])
api_router.include_router(wws_router, prefix="/wws", tags=["wws"])
api_router.include_router(tse_router, prefix="/tse", tags=["tse"])
api_router.include_router(waage_router, prefix="/waage", tags=["waage"])
api_router.include_router(status_router, prefix="/system", tags=["system"]) 