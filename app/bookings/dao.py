from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, cast, Date

from app.dao.base import BaseDAO
from app.bookings.models import Bookings
from app.database import async_session_maker


from datetime import datetime

class BookingsDAO(BaseDAO):
    model=Bookings