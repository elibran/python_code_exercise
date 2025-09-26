from fastapi import Depends, FastAPI, status # type: ignore
from sqlalchemy.orm import Session # type: ignore

from . import models, schemas, services
from .database import engine, get_db

# Create tables on startup (demo convenience; use migrations in prod)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Search API with SQL injection Safe with Pydantic Validation",
    version="1.2.0",
    docs_url="/v1/docs",
    redoc_url="/v1/redoc",
    openapi_url="/v1/openapi.json",
)

@app.get("/v1/health", tags=["meta"])
def health():
    return {"status": "ok", "service": "light-banking-api", "version": "v1"}

@app.post(
    "/v1/customers/",
    response_model=schemas.CustomerOut,
    status_code=status.HTTP_201_CREATED,
    tags=["customers"],
)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    entity = models.Customer(name=customer.name)
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity

@app.post(
    "/v1/accounts/",
    response_model=schemas.Account,
    status_code=status.HTTP_201_CREATED,
    tags=["accounts"],
)
def create_new_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    svc = services.AccountService(db=db)
    return svc.create_account(account)

@app.post(
    "/v1/search",
    response_model=list[schemas.SearchResult],
    status_code=status.HTTP_200_OK,
    tags=["search"],
    summary="Search by customer name (case-insensitive partial match, SQLi-safe)",
)
def search_by_name(payload: schemas.SearchByNameRequest, db: Session = Depends(get_db)):
    svc = services.SearchService(db=db)
    return svc.search_by_name(payload)
