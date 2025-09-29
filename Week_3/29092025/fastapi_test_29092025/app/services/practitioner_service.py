from sqlalchemy.orm import Session # type: ignore
from app.db.models import Practitioner
from app.db.repository import Repository
from app.schemas.practitioner import PractitionerCreate, PractitionerUpdate

class PractitionerService:
    def __init__(self, db: Session):
        # TODO: Initialize repository
        self.repo = Repository[Practitioner](db, Practitioner)

    def get(self, id: int):
        # TODO
        raise NotImplementedError("TODO: PractitionerService.get")

    def list(self, limit: int = 50, offset: int = 0):
        # TODO
        raise NotImplementedError("TODO: PractitionerService.list")

    def create(self, payload: PractitionerCreate):
        # TODO
        raise NotImplementedError("TODO: PractitionerService.create")

    def update(self, id: int, payload: PractitionerUpdate):
        # TODO
        raise NotImplementedError("TODO: PractitionerService.update")

    def delete(self, id: int) -> bool:
        # TODO
        raise NotImplementedError("TODO: PractitionerService.delete")
