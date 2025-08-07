from app.database import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime

class Bookings(Base):
    __tablename__="bookings"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[datetime]
    date_to: Mapped[datetime]