from fastapi import APIRouter

router = APIRouter(
    prefix="/tables",
    tags=["Бронь столов"]
)

@router.post("/online_payment") # онлайн оплата через ЮКассу
async def online_payment():
    pass