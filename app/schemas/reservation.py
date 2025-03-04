from datetime import datetime, timedelta

from pydantic import BaseModel, model_validator, field_validator, Field

FROM_TIME = (datetime.now() + timedelta(minutes=10)).isoformat(timespec='minutes')
TO_TIME = (datetime.now() + timedelta(hours=1)).isoformat(timespec='minutes')

class ReservationBase(BaseModel):
    from_reserve: datetime = Field(examples=[FROM_TIME])
    to_reserve: datetime = Field(examples=[TO_TIME])

    class Config:
        extra = "forbid"


class ReservationDB(ReservationBase):
    id: int
    meeting_room_id: int
    user_id: int | None = None

    # for using ORM-model in schema
    class Config:
        from_attributes = True


class ReservationUpdate(ReservationBase):

    @field_validator("from_reserve")
    @classmethod
    def check_from_reserve_later_than_now(cls, value):
        if value <= datetime.now():
            raise ValueError(
                "The booking start time cannot be less than the current time")
        return value

    @model_validator(mode="after")
    @classmethod
    def check_from_reserve_before_to_reserve(cls, values):
        if values.from_reserve >= values.to_reserve:
            raise ValueError(
                "The start time of the booking cannot be later than the end time")
        return values


class ReservationCreate(ReservationUpdate):
    meeting_room_id: int
