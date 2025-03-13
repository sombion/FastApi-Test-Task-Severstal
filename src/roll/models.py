from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy import Date
from src.database import Base


class Roll(Base):
    __tablename__ = "roll"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    length: Mapped[int]
    weight: Mapped[int]
    date_added: Mapped[datetime] = mapped_column(Date, nullable=True, default=func.now())
    date_removed: Mapped[datetime] = mapped_column(Date, nullable=True)