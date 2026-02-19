from app.database import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

class Tables(Base):
    __tablename__="tables"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    seats: Mapped[int] # количество мест за столом
    