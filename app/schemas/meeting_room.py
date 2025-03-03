from pydantic import BaseModel, Field, field_validator


class MeetingRoomBase(BaseModel):
    name: None | str = Field(None, min_length=1, max_length=100)
    description: None | str = None


class MeetingRoomCreate(MeetingRoomBase):
    name: str = Field(min_length=1, max_length=100)


class MeetingRoomDB(MeetingRoomBase):
    id: int

    # for using ORM-model in schema
    class Config:
        from_attributes = True


class MeetingRoomUpdate(MeetingRoomBase):

    @field_validator("name")
    @classmethod
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError("name cannot be empty (null or None)")
        return value

