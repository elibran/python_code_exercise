from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db import models as m
from app.services.practitioner_service import PractitionerService
from app.services.slot_service import SlotService

def make_session():
    engine = create_engine("sqlite+pysqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)()

def test_service_layer_crud_and_filters():
    db = make_session()

    psvc = PractitionerService(db)
    p1 = psvc.create(type("X", (), {"name":"Dr X","specialty":"Dentist"})())
    assert p1.id and p1.name == "Dr X"
    assert psvc.get(p1.id).id == p1.id
    psvc.update(p1.id, type("X", (), {"name":"Dr Y","specialty":"Ortho"})())
    assert psvc.get(p1.id).name == "Dr Y"

    ssvc = SlotService(db)
    now = datetime.utcnow().replace(microsecond=0)
    a = ssvc.create(type("S", (), {"practitioner_id": p1.id, "start_time": now, "end_time": now+timedelta(hours=1), "is_booked": False})())
    b = ssvc.create(type("S", (), {"practitioner_id": p1.id, "start_time": now+timedelta(hours=1), "end_time": now+timedelta(hours=2), "is_booked": True})())
    avail = ssvc.list_filtered(True, None, None, None, 50, 0, "start_time", "asc")
    assert all(not s.is_booked for s in avail)
    ssvc.book(a.id)
    assert ssvc.get(a.id).is_booked is True
