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
        # TODO: Implement
        raise NotImplementedError("TODO: Repository.get")

    def list(self, limit: int = 50, offset: int = 0):
        # TODO: Implement
        raise NotImplementedError("TODO: Repository.list")

    def add(self, obj: ModelT) -> ModelT:
        # TODO: Implement
        raise NotImplementedError("TODO: Repository.add")

    def delete(self, obj: ModelT) -> None:
        # TODO: Implement
        raise NotImplementedError("TODO: Repository.delete")

    def update(self) -> None:
        # TODO: Implement
        raise NotImplementedError("TODO: Repository.update")
