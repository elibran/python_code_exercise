from sqlalchemy import Column, Integer, String, Boolean # type: ignore
from .database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    done = Column(Boolean, nullable=False, default=False)
