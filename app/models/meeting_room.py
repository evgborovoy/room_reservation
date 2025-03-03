from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import relationship

from app.core.db import Base


class MeetingRoom(Base):
    __tablename__ = "meeting_room"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    reservations = relationship("Reservation", cascade="delete")
