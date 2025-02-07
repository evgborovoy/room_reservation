from typing import Optional
from pydantic import BaseModel, Field


class MeetingRoomBase(BaseModel):
    name: Optional[str] = Field(min_length=1, max_length=100)
    description: Optional[str] = None


class MeetingRoomCreate(MeetingRoomBase):
    name: str = Field(min_length=1, max_length=100)


class MeetingRoomDB(MeetingRoomBase):
    id: int

    class Config:
        from_attributes = True


class MeetingRoomUpdate(MeetingRoomBase):
    pass