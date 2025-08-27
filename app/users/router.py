from fastapi import APIRouter, HTTPException, status
from pydantic import EmailStr

from app.users.schemas import SRegistration
from app.users.dao import UsersDAO

from app.users.dependencies import check_user_info

from app.users.auth import get_password_hash, auth_user

router = APIRouter(
    prefix="/users",
    tags=["Пользователи"]
)

@router.post("/registration")
async def user_registration(
    user_info: SRegistration
):
    user = UsersDAO.find_one_or_none(email=user_info.email)
        
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователь с таким email уже существует")
    
    check_user_info(user_info)
    
    hashed_password = get_password_hash(user_info.password)
    
    UsersDAO.add(
        name=user_info.name,
        surname=user_info.surname,
        hashed_password=hashed_password,
        email=user_info.email,
        base_address=user_info.base_address
    )
    
    return "Учётная запись была создана!"

@router.post("/log_in")
async def user_login(email: EmailStr, password: str):
    existing_user = await auth_user(email=email, password=password)