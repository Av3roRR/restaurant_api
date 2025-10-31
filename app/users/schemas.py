from pydantic import BaseModel, Field, EmailStr

from typing import Optional

class SRegistration(BaseModel):
    name: str = Field(min_length=2, description="Имя пользователя", examples=["John"])
    surname: str = Field(min_length=1, description="Фамилия пользователя", examples=["Doe"])
    password: str = Field(min_length=8, description="Пароль пользователя", examples=["12345678"])
    email: EmailStr = Field(None, description="Почта пользователя", examples=["example@gmail.com"])
    base_address: Optional[str] = Field(None, description="Адрес пользователя")