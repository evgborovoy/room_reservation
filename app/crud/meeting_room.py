from typing import Optional
from fastapi.encoders import jsonable_encoder

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomUpdate


async def create_meeting_room(new_room: MeetingRoomCreate, session: AsyncSession) -> MeetingRoom:
    # конвертируем MeetingRoomCreate в словарь
    new_room_data = new_room.model_dump()

    # Создаём объект модели MeetingRoom.
    # В параметры передаём пары "ключ=значение"
    db_room = MeetingRoom(**new_room_data)

    # Добавляем созданный объект в сессию.
    # Никакие действия с базой пока ещё не выполняются.
    session.add(db_room)

    # Записываем изменения непосредственно в БД.
    await session.commit()

    # Обновляем объект db_room: считываем данные из БД, чтобы получить его id.
    await session.refresh(db_room)
    # Возвращаем созданный объект класса MeetingRoom.
    return db_room


async def get_room_id_by_name(room_name: str, session: AsyncSession) -> Optional[int]:
    db_room_id = await session.execute(
        select(MeetingRoom.id).where(MeetingRoom.name == room_name)
    )
    db_room_id = db_room_id.scalars().first()
    return db_room_id


async def read_all_rooms_from_db(session: AsyncSession) -> list[MeetingRoom]:
    all_rooms = await session.execute(select(MeetingRoom))
    return all_rooms.scalars().all()


async def find_one_or_none(room_id: int, session: AsyncSession) -> Optional[MeetingRoom]:
    room = await session.execute(select(MeetingRoom).where(MeetingRoom.id == room_id))
    return room.scalars().first()


async def update_room(
        db_room: MeetingRoom,
        room_in: MeetingRoomUpdate,
        session: AsyncSession
) -> MeetingRoom:
    obj_data = jsonable_encoder(db_room)
    update_data = room_in.model_dump(exclude_unset=True)

    for field in obj_data:
        if field in update_data:
            setattr(db_room, field, update_data[field])

    session.add(db_room)
    await session.commit()
    await session.refresh(db_room)

    return db_room


async def delete_meeting_room(
        db_room: MeetingRoom,
        session: AsyncSession,
) -> MeetingRoom:
    # Удаляем объект
    await session.delete(db_room)
    # Фиксируем изменения в БД.
    await session.commit()
    # Не обновляем объект через метод refresh(),
    # следовательно он всё ещё содержит информацию об удаляемом объекте.
    return db_room