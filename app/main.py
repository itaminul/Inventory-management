import json
from fastapi import FastAPI, status, Request, HTTPException
from app.core.config import settings
from app.api.v1.router import api_router as api_router_link
from app.core.exceptions import register_exception_handlers
from app.core.logging import setup_logging
from app.core.middleware import request_logging_middleware
from app.modules.customer.models import Customer  # noqa:
from app.modules.customer_type.models import CustomerType  # noqa: F401
from app.modules.product.models import Product
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)
# Register all global validation, JSON, and database exception handlers
register_exception_handlers(app)

# Register middleware
app.middleware("http")(request_logging_middleware)

# Register API routes
app.include_router(
    api_router_link,
    prefix=settings.API_V1_STR,  # e.g., "/api/v1"
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print("\n--- 422 VALIDATION ERROR ---")
    print(json.dumps(exc.errors(), indent=2))
    print("----------------------------\n")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )



@app.get("/")
async def root():
    return {"message": "Welcome to the API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
