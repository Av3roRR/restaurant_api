from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime

from app.users.dependencies import get_current_user

from app.bookings.dao import BookingsDAO

from typing import Literal


router = APIRouter(
    prefix="/booking",
    tags=["Бронирования"]
)

# добавить проверку по роли пользователя + добавить роли для пользователей админ/user
@router.post("/delete_booking")
async def delete_booking(id: int, user = Depends(get_current_user)):
    booking = await BookingsDAO.find_one_or_none(id=id)
    
    if booking is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Бронирование не найдено")
    
    if booking.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    
    await BookingsDAO.delete(id=id)
    return "Удаление прошло успешно"

#добавить проверку, что делает это пользователь с правом админа
@router.post("/update_booking_field")
async def update_booking(id: int, field: Literal["date_from", "date_to", "table_id"], value: str):
    booking = await BookingsDAO.find_one_or_none(id=id)
    
    if booking is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Бронирование не найдено")
    
    
    try:
        if field == "table_id":
            value = int(value)
        elif field == "date_from" or field == "date_to":
            value = datetime.strptime(value, "%Y-%m-%d %H:%M")
            
            if value.minute != 0:
                raise ValueError
            
            if field == "date_from":
                if value < datetime.now():
                    raise ValueError
                if value > booking.date_to:
                    raise ValueError
                diff = booking.date_to - value
            else:
                if value > datetime.now():
                    raise ValueError
                if value < booking.date_from:
                    raise ValueError
                diff = value - booking.date_from
        
            hours = diff.seconds // 3600 
            minutes = (diff.seconds % 3600) // 60
            if diff.days > 1 or hours > 2 or minutes > 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректное время для бронирования")
            
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Это поле нельзя обновить")
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректные данные для этого поля")
    await BookingsDAO.update(id=id, field="", data=value)
    return "Обновление прошло успешно"

@router.post("/update_booking_fields")
async def get_booking(id: int, user = Depends(get_current_user)):
    booking = await BookingsDAO.find_one_or_none(id=id)
    
    if booking is None or booking.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Бронирование не найдено")

    return booking

@router.post("/add_booking")
async def add_booking():
    pass

@router.post("/get_bookings")
async def get_booking(user = Depends(get_current_user)):
    bookings = await BookingsDAO.find_all(user_id=user.id)
    
    if not bookings:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Бронирований нет")
    
    return bookings