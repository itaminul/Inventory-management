from fastapi import FastAPI

from app.core.config import settings
from app.api.v1.router import api_router

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    debug=settings.DEBUG,
)

app.include_router(
    api_router,
    prefix="/api/v1",
)

@app.get("/")
def root():
    return {
        "message": "Inventory Management System API",
        "database": "inv_db",
        "status": "running",
    }

@app.get("/health")
def health_check():
    return {
        "status": "running",
    }
