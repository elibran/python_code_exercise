from sqlalchemy import create_engine # type: ignore
from sqlalchemy.orm import sessionmaker, declarative_base, Session # type: ignore
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./app.db")

# For SQLite, check_same_thread=False is needed for multi-threaded access (TestClient/BackgroundTasks)
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)
Base = declarative_base()

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    from models import User, Order  # ensure models imported
    Base.metadata.create_all(bind=engine)
