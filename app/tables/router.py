from fastapi import APIRouter

router = APIRouter(
    prefix="/tables",
    tags=["Бронь столов"]
)

@router.post("/online_payment") # онлайн оплата через ЮКассу
async def online_payment():
    pass

# Реализация только после разбора с bookings
@router.post("/rent_table/{id}")
async def rent_table(id: int):
    pass

@router.post("/return_table/{id}")
async def add_table(seats: int):
    pass