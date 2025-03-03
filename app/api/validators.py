from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.meeting_room import meeting_room_crud
from app.crud.reservation import reservation_crud
from app.models import MeetingRoom, Reservation


async def check_meeting_room_exists(meeting_room_id: int, session: AsyncSession) -> MeetingRoom:
    meeting_room = await meeting_room_crud.get(meeting_room_id, session)
    if meeting_room is None:
        raise HTTPException(status_code=404, detail="Meeting room not found")
    return meeting_room


async def check_name_duplicate(room_name: str, session: AsyncSession) -> None:
    room_id = await meeting_room_crud.get_room_id_by_name(room_name, session)
    if room_id is not None:
        raise HTTPException(status_code=422, detail=f"meeting room with name '{room_name}' already exist")


async def check_reservation_intersections(**kwargs) -> None:
    reservations = await reservation_crud.get_reservations_at_the_same_time(**kwargs)
    if reservations:
       raise HTTPException(status_code=422, detail=f"intersections time with: {reservations}")


async def check_reservation_before_edit(reservation_id: int, session: AsyncSession) -> Reservation:
    reservation = await reservation_crud.get(reservation_id, session)
    if not reservation:
        raise HTTPException(404, "Reservation not found")
    return reservation

