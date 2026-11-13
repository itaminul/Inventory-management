from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.core.config import settings
engine = create_engine(
    settings.DATABASE_URL,
    poll_pre_ping=True,
    poll_size=10,
    max_overflow=20,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)