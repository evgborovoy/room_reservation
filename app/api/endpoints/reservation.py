from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_meeting_room_exists, check_reservation_intersections, check_reservation_before_edit
from app.core.user import current_user, current_superuser
from app.models import User
from app.schemas.reservation import ReservationDB, ReservationCreate, ReservationUpdate
from app.crud.reservation import reservation_crud
from app.core.db import get_async_session

router = APIRouter()


@router.post("/", response_model=ReservationDB)
async def create_reservation(reservation: ReservationCreate, session: AsyncSession = Depends(get_async_session),
                             user: User = Depends(current_user)):
    await check_meeting_room_exists(reservation.meeting_room_id, session)
    await check_reservation_intersections(**reservation.model_dump(), session=session)
    new_reservation = await reservation_crud.create(reservation, session=session, user=user)
    return new_reservation


@router.get("/", response_model=list[ReservationDB], dependencies=[Depends(current_superuser)])
async def get_all_reservations(session: AsyncSession = Depends(get_async_session)):
    """Only for superuser"""
    reservations = await reservation_crud.get_multi(session)
    return reservations


@router.get("/my_reservations", response_model=list[ReservationDB], response_model_exclude={"user_id"})
async def get_my_reservations(user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    """Get all reservations for current user"""
    reservations = await reservation_crud.get_by_user(user, session)
    return reservations


@router.patch("/{reservation_id}", response_model=ReservationDB)
async def update_reservation(reservation_id: int, obj_in: ReservationUpdate,
                             session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    """For superuser or user who create reservation"""
    reservation = await check_reservation_before_edit(reservation_id, session, user)
    await check_reservation_intersections(**obj_in.model_dump(), reservation_id=reservation_id,
                                          meeting_room_id=reservation.meeting_room_id, session=session)
    reservation = await reservation_crud.update(db_obj=reservation, obj_in=obj_in, session=session)
    return reservation


@router.delete("/{reservation_id}", response_model=ReservationDB)
async def delete_reservation(reservation_id: int, session: AsyncSession = Depends(get_async_session),
                             user: User = Depends(current_user)):
    """For superuser or user who create reservation"""
    reservation = await check_reservation_before_edit(reservation_id, session, user)
    reservation = await reservation_crud.remove(reservation, session)
    return reservation
