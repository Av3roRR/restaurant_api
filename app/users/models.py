from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from app.database import Base

class Users(Base):
    __tablename__="users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String(30))
    hashed_password: Mapped[str]
    email: Mapped[Optional[str]]    
    base_address: Mapped[Optional[str]]