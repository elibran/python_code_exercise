from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import make_url
from app.core.config import get_settings

_settings = get_settings()

# Ensure directory exists for file-based SQLite URLs
url = make_url(_settings.database_url)
if url.drivername.startswith("sqlite") and url.database not in (None, ":memory:"):
    db_path = Path(url.database)
    db_path.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    _settings.database_url,
    echo=False,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False} if url.drivername.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def db_ping() -> bool:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return True
