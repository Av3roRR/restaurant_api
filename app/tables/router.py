from fastapi import APIRouter, Depends, HTTPException, status

from app.tables.dao import TablesDAO
from app.bookings.dao import BookingsDAO

from app.users.dependencies import get_current_user
from app.tables.dependencies import check_date, check_table_availability


from datetime import datetime


router = APIRouter(
    prefix="/tables",
    tags=["Бронь столов"]
)

@router.get("/table/{id}")
async def get_table_info(id: int):
    table = await TablesDAO.get_by_id(id)
    return table



@router.post("/table/{id}/online_payment/") # онлайн оплата через ЮКассу
async def online_payment(id: int):
    pass


@router.post("/rent_table/{id}")
async def rent_table(id: int, date_from: datetime, date_to: datetime, user = Depends(get_current_user)):
    table = await TablesDAO.get_by_id(id)
    
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Столик не найден"
        )
    
    check_date(date_from, date_to)
    
    result = await check_table_availability(id, date_from, date_to)
    return result
    
    # Здесь также стоит добавить проверку, не занят ли стол на это время (конфликт бронирования)
    result = await BookingsDAO.add(table_id=id, user_id=user.id, date_from=date_from, date_to=date_to)
    return result

@router.post("/add_table")
async def add_table(seats: int):
    pass

@router.post("/delete_table/{id}")
async def delete_table(id: int):
    await TablesDAO.delete(id=id)
