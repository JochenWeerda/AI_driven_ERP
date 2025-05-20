from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, products, orders, customers, inventory, ai

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(customers.router, prefix="/customers", tags=["customers"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"]) 