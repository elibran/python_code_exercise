import os
import time
import pytest # type: ignore
from testcontainers.postgres import PostgresContainer # type: ignore
from sqlalchemy import create_engine, text # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore
from sqlalchemy.engine.url import make_url # type: ignore
from app.database import Base

@pytest.fixture(scope="session")
def pg_container():
    # No custom env; let Testcontainers choose defaults (often test:test@test)
    with PostgresContainer("postgres:16-alpine") as pg:
        raw_url = pg.get_connection_url()  # whatever the container actually exposes
        # Force SQLAlchemy to use psycopg2 driver, but keep creds/host/port/db EXACT
        url = str(make_url(raw_url).set(drivername="postgresql+psycopg2"))

        os.environ["DATABASE_URL"] = url
        print(f"[TEST DB URL] {url.replace(':', ':[redacted]', 1)}")

        # Wait for DB readiness
        engine = create_engine(url, pool_pre_ping=True)
        last_err = None
        for _ in range(120):
            try:
                with engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                    last_err = None
                    break
            except Exception as e:
                last_err = e
                time.sleep(0.5)
        if last_err:
            raise last_err

        yield url

@pytest.fixture(scope="session")
def db_engine(pg_container):
    engine = create_engine(pg_container, pool_pre_ping=True)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def db_session(db_engine):
    TestingSessionLocal = sessionmaker(bind=db_engine, autoflush=False, autocommit=False)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
