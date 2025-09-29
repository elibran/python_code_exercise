from typing import TypeVar, Generic, Type
from sqlalchemy.orm import Session # type: ignore
from sqlalchemy import select # type: ignore
from app.db.base import Base

ModelT = TypeVar("ModelT", bound=Base)

class Repository(Generic[ModelT]):
    def __init__(self, db: Session, model: Type[ModelT]):
        self.db = db
        self.model = model

    def get(self, id: int):
        return self.db.get(self.model, id)

    def list(self, limit: int = 50, offset: int = 0):
        stmt = select(self.model).limit(limit).offset(offset)
        return self.db.execute(stmt).scalars().all()

    def add(self, obj: ModelT) -> ModelT:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: ModelT) -> None:
        self.db.delete(obj)
        self.db.commit()

    def update(self) -> None:
        self.db.commit()
