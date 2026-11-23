from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.modules.auth.models import User  # noqa: F401
from app.modules.customer.models import Customer  # noqa: F401
from app.modules.customer_type.models import CustomerType  # noqa: F401

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)