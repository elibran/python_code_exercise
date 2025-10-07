from sqlalchemy import create_engine # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore
from sqlalchemy.pool import NullPool # type: ignore
from .config import settings
from sqlalchemy.orm import declarative_base # type: ignore
Base = declarative_base()

engine = create_engine(
    settings.database_url,  # e.g., "sqlite:///./dev.db" for dev, or test url in pytest
    pool_pre_ping=True,
    poolclass=NullPool,
    echo=False,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
