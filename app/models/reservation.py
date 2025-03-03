from sqlalchemy import Integer, Column, ForeignKey, DateTime
from app.core.db import Base


class Reservation(Base):
    __tablename__ = "reservation"

    id = Column(Integer, primary_key=True)
    from_reserve = Column(DateTime)
    to_reserve = Column(DateTime)
    meeting_room_id = Column(Integer, ForeignKey("meeting_room.id"))

    def __repr__(self):
        return f"Room #{self.meeting_room_id} reserved from {self.from_reserve} to {self.to_reserve}"