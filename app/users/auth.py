from fastapi import HTTPException, status
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from pydantic import EmailStr
from jose import jwt
from datetime import datetime, timezone, timedelta

from app.users.dao import UsersDAO
from app.users.schemas import SRegistration
from app.config import settings


pwd_hasher = PasswordHasher()

def verify_password(hashed_password: str, inserted_password: str):
    return pwd_hasher.verify(hashed_password, inserted_password)

def get_password_hash(password: str):
    return pwd_hasher.hash(password)

async def auth_user(email: EmailStr, password: str):
    existing_user = await UsersDAO.find_one_or_none(email=email)
    
    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь с такой почтой не найден")

    try:    
        pwd_verify = verify_password(existing_user.hashed_password, password)
    except VerifyMismatchError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Введён неправильный пароль")
    
    return existing_user
        
    
def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = (datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES)).timestamp()
    
    to_encode.update({"exp": int(expire)})
    encoded_jwt = jwt.encode(to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt