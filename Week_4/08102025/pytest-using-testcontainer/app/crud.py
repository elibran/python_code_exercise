from sqlalchemy.orm import Session # type: ignore
from . import models, schemas

def create_task(db: Session, task_in: schemas.TaskCreate) -> models.Task:
    task = models.Task(title=task_in.title, done=False)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def list_tasks(db: Session) -> list[models.Task]:
    return db.query(models.Task).order_by(models.Task.id.asc()).all()
