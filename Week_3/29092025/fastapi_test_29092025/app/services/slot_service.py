from datetime import datetime
from sqlalchemy.orm import Session # type: ignore
from app.db.models import Slot
from app.db.repository import Repository
from app.schemas.slot import SlotCreate, SlotUpdate

class SlotService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = Repository[Slot](db, Slot)

    def get(self, id: int):
        # TODO
        raise NotImplementedError("TODO: SlotService.get")

    def create(self, payload: SlotCreate):
        # TODO
        raise NotImplementedError("TODO: SlotService.create")

    def update(self, id: int, payload: SlotUpdate):
        # TODO
        raise NotImplementedError("TODO: SlotService.update")

    def delete(self, id: int) -> bool:
        # TODO
        raise NotImplementedError("TODO: SlotService.delete")

    def list_filtered(
        self,
        available: bool | None,
        practitioner_id: int | None,
        date_from: datetime | None,
        date_to: datetime | None,
        limit: int,
        offset: int,
        sort_by: str,
        order: str,
    ):
        # TODO
        raise NotImplementedError("TODO: SlotService.list_filtered")

    def book(self, id: int):
        # TODO
        raise NotImplementedError("TODO: SlotService.book")
