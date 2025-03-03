from datetime import datetime

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.reservation import Reservation


class CRUDReservation(CRUDBase):

    async def get_reservations_at_the_same_time(self, *, meeting_room_id: int, from_reserve: datetime,
                                                to_reserve: datetime, reservation_id: None | int = None,
                                                session: AsyncSession) -> list[Reservation]:
        statement = select(Reservation).where(
            Reservation.meeting_room_id == meeting_room_id,
            and_(
                from_reserve <= Reservation.to_reserve,
                to_reserve >= Reservation.from_reserve
            )
        )
        if reservation_id is not None:
            statement = statement.where(
                Reservation.id != reservation_id
            )
        reservations = await session.execute(statement)
        reservations = reservations.scalars().all()
        return reservations

    async def get_future_reservations_for_room(self, meeting_room_id: int, session: AsyncSession):
        reservations = await session.execute(
            select(Reservation).where(
                Reservation.meeting_room_id == meeting_room_id,
                Reservation.to_reserve > datetime.now()
            )
        )
        reservations = reservations.scalars().all()
        return reservations


reservation_crud = CRUDReservation(Reservation)
