from typing import Generator
from sqlalchemy import create_engine # type: ignore
from sqlalchemy.orm import declarative_base, sessionmaker, Session # type: ignore

SQLALCHEMY_DATABASE_URL = "sqlite:///./db/banking.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
