from fastapi import FastAPI # type: ignore
from .routers import auth, accounts
app = FastAPI(title="Banking API (FastAPI + JWT)")
app.include_router(auth.router)
app.include_router(accounts.router)
@app.get("/health")
def health(): return {"status":"ok"}
