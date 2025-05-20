from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-Driven ERP"
    API_V1_STR: str = "/api/v1"
    
    # CORS
    CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]  # Frontend-URL
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        return v
    
    # Datenbank
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "ai_erp"
    SQLALCHEMY_DATABASE_URI: str | None = None
    
    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict) -> str:
        if isinstance(v, str):
            return v
        return f"postgresql://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}@{values.get('POSTGRES_SERVER')}/{values.get('POSTGRES_DB')}"
    
    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB: str = "ai_erp_ml"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-here"  # In Produktion ändern!
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # MCP (Model Context Protocol)
    MCP_HOST: str = "localhost"
    MCP_PORT: int = 50051
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 