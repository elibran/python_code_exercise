from datetime import datetime
from sqlalchemy.orm import Session # type: ignore
from sqlalchemy import select, asc, desc, and_ # type: ignore
from app.db.models import Slot
from app.db.repository import Repository
from app.schemas.slot import SlotCreate, SlotUpdate

class SlotService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = Repository[Slot](db, Slot)

    def get(self, id: int):
        return self.repo.get(id)

    def create(self, payload: SlotCreate):
        obj = Slot(
            practitioner_id=payload.practitioner_id,
            start_time=payload.start_time,
            end_time=payload.end_time,
            is_booked=payload.is_booked,
        )
        return self.repo.add(obj)

    def update(self, id: int, payload: SlotUpdate):
        obj = self.repo.get(id)
        if not obj:
            return None
        if payload.practitioner_id is not None:
            obj.practitioner_id = payload.practitioner_id
        if payload.start_time is not None:
            obj.start_time = payload.start_time
        if payload.end_time is not None:
            obj.end_time = payload.end_time
        if payload.is_booked is not None:
            obj.is_booked = payload.is_booked
        self.repo.update()
        return obj

    def delete(self, id: int) -> bool:
        obj = self.repo.get(id)
        if not obj:
            return False
        self.repo.delete(obj)
        return True

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
        sort_col = getattr(Slot, sort_by)
        ordering = asc(sort_col) if order == "asc" else desc(sort_col)
        conditions = []
        if available is not None:
            conditions.append(Slot.is_booked.is_(False) if available else Slot.is_booked.is_(True))
        if practitioner_id is not None:
            conditions.append(Slot.practitioner_id == practitioner_id)
        if date_from is not None:
            conditions.append(Slot.end_time >= date_from)
        if date_to is not None:
            conditions.append(Slot.start_time <= date_to)

        stmt = select(Slot)
        if conditions:
            stmt = stmt.where(and_(*conditions))
        stmt = stmt.order_by(ordering).limit(limit).offset(offset)
        return self.db.execute(stmt).scalars().all()

    def book(self, id: int):
        obj = self.repo.get(id)
        if not obj:
            raise KeyError("Not found")
        if obj.is_booked:
            raise ValueError("Slot already booked")
        obj.is_booked = True
        self.repo.update()
        return obj
