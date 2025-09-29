from sqlalchemy.orm import Session # type: ignore
from app.db.models import Practitioner
from app.db.repository import Repository
from app.schemas.practitioner import PractitionerCreate, PractitionerUpdate

class PractitionerService:
    def __init__(self, db: Session):
        self.repo = Repository[Practitioner](db, Practitioner)

    def get(self, id: int):
        return self.repo.get(id)

    def list(self, limit: int = 50, offset: int = 0):
        return self.repo.list(limit=limit, offset=offset)

    def create(self, payload: PractitionerCreate):
        obj = Practitioner(name=payload.name, specialty=payload.specialty)
        return self.repo.add(obj)

    def update(self, id: int, payload: PractitionerUpdate):
        obj = self.repo.get(id)
        if not obj:
            return None
        obj.name = payload.name
        obj.specialty = payload.specialty
        self.repo.update()
        return obj

    def delete(self, id: int) -> bool:
        obj = self.repo.get(id)
        if not obj:
            return False
        self.repo.delete(obj)
        return True
