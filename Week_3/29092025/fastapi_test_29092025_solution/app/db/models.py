from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship # type: ignore
from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey # type: ignore
from .base import Base

class Practitioner(Base):
    __tablename__ = "practitioners"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    specialty: Mapped[str] = mapped_column(String(100), nullable=False)
    slots = relationship("Slot", back_populates="practitioner", cascade="all, delete-orphan")

class Slot(Base):
    __tablename__ = "slots"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    practitioner_id: Mapped[int] = mapped_column(ForeignKey("practitioners.id", ondelete="CASCADE"), nullable=False, index=True)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    is_booked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    practitioner = relationship("Practitioner", back_populates="slots")
