from app.database import Base

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from typing import Optional

class Menu(Base):
    __tablename__="menu"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    image_id: Mapped[Optional[int]]