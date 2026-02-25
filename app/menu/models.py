from app.database import Base

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.menu.schemas import DishCategory


from typing import Optional

class Menu(Base):
    __tablename__="menu"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[Optional[str]]
    name: Mapped[str] = mapped_column(String(50))
    category: Mapped[DishCategory] = mapped_column(String(50), default=DishCategory.MAIN)
    
    price: Mapped[int]
    in_stock: Mapped[bool] = mapped_column(default=True)
    image_id: Mapped[Optional[int]]