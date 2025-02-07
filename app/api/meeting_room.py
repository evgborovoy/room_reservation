from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import True_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.meeting_room import (
    create_meeting_room, get_room_id_by_name, read_all_rooms_from_db,
    update_room, find_one_or_none, delete_meeting_room
)
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomDB, MeetingRoomUpdate
from app.models.meeting_room import MeetingRoom

router = APIRouter(prefix="/meeting_rooms", tags=["Meeting Rooms"])


@router.post(
    "/",
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
)
async def create_new_meeting_room(meeting_room: MeetingRoomCreate, session: AsyncSession = Depends(get_async_session)):
    await check_name_duplicate(meeting_room.name, session)

    new_room = await create_meeting_room(meeting_room, session)
    return new_room


@router.get(
    "/",
    response_model=list[MeetingRoomDB],
    response_model_exclude_none=True
)
async def get_all_meeting_rooms(session: AsyncSession = Depends(get_async_session)):
    return await read_all_rooms_from_db(session)


@router.patch(
    "/{meeting_room_id}",
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
)
async def partially_update_room(room_id: int,
                                room_in: MeetingRoomUpdate,
                                session: AsyncSession = Depends(get_async_session)
                                ):
    meeting_room = await check_meeting_room_exists()
    meeting_room = await update_room(meeting_room, room_in, session)
    return meeting_room


@router.delete(
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
)
async def remove_meeting_room(
        meeting_room_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    # Выносим повторяющийся код в отдельную корутину.
    meeting_room = await check_meeting_room_exists(
        meeting_room_id, session
    )
    meeting_room = await delete_meeting_room(
        meeting_room, session
    )
    return meeting_room


async def check_meeting_room_exists(meeting_room_id: int, session: AsyncSession) -> MeetingRoom:
    meeting_room = await find_one_or_none(
        meeting_room_id, session
    )
    if meeting_room is None:
        raise HTTPException(status_code=404, detail="Meeting room not found")
    return meeting_room


async def check_name_duplicate(room_name: str, session: AsyncSession) -> None:
    room_id = await get_room_id_by_name(room_name, session)
    if room_id is not None:
        raise HTTPException(status_code=422, detail=f"meeting room with name '{room_name}' already exist")
