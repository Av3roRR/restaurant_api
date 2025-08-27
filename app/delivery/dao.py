from app.dao.base import BaseDAO

from app.delivery.models import Delivery

class DeliveryDAO(BaseDAO):
    model=Delivery