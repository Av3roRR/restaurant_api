from fastapi import HTTPException, status
from sqlalchemy import select, and_, or_

from app.tables.dao import TablesDAO
from app.bookings.dao import BookingsDAO

from app.bookings.models import Bookings

from app.database import async_session_maker

async def check_table_availability(table_id, date_from, date_to):
    # рассмотреть три случая и все проверить есть ли такие записи в таблице
    # рассматриваются все случаи, которые возможны с условием, что бронь стола максимум 2 часа
    bookings = select(Bookings).where(
        Bookings.table_id == table_id, or_(
            and_(
            Bookings.date_from <= date_from,
            Bookings.date_to <= date_to
            ),
            and_(
            Bookings.date_from >= date_from,
            Bookings.date_to >= date_to
            )
        )
    )
    
    with async_session_maker() as session:
        result = await session.execute(bookings)
    
    return result.mappings().all()
    
    
def check_date(date_from, date_to):
    if date_from >= date_to:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректные даты")
    
    hours_from = date_from.hour
    hours_to = date_to.hour

    minutes_from = date_from.minute
    minutes_to = date_to.minute

    if (hours_from >= 2 and hours_from <= 10) or (hours_to >= 2 and hours_to <= 10):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Нерабочие часы")
    
    if hours_to - hours_from < 0:
        hours_to += 24
    
    if hours_to - hours_from > 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Нельзя арендовать столик больше, чем на 2 часа")
    
    if (minutes_from != 0) or (minutes_to != 0):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректное время")

    
    return True