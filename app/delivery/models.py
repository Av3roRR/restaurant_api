from app.database import Base

from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column

class Delivery(Base):
    __tablename__="delivery"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    list_of_dishes: Mapped[list[int]] = mapped_column(JSON)
    address: Mapped[str]
    price: Mapped[float]