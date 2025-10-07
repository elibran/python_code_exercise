from fastapi import FastAPI, Depends # type: ignore
from sqlalchemy.orm import Session # type: ignore
from .database import Base, engine, get_db
from . import crud, schemas
from .logging_conf import logger

# Create tables on startup for the dev SQLite case
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/tasks", response_model=schemas.TaskOut, status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating task: {task.title}")
    created = crud.create_task(db, task)
    return created

@app.get("/tasks", response_model=list[schemas.TaskOut])
def get_tasks(db: Session = Depends(get_db)):
    tasks = crud.list_tasks(db)
    logger.info(f"Listing {len(tasks)} tasks")
    return tasks
