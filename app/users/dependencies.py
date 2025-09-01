from fastapi import HTTPException, status, Depends, Request

from jose import jwt, JWTError
from datetime import datetime, timezone

from app.users.schemas import SRegistration
from app.config import settings
from app.users.dao import UsersDAO

def get_token(request: Request):
    cookie = request.cookies.get("access_token", None)
    if cookie is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Невозможно определить пользователя")
    
    return cookie


async def get_current_user(token = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректные данные в cookie")
    
    expire: str = payload.get("exp")
    if not expire or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Токен был просрочен")
    
    user_id: id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось получить необходимые данные из cookie")
    
    user = await UsersDAO.find_by_id(model_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Такого пользователя не существует")
    
    return user
    


def check_user_info(user_info: SRegistration):
    name = user_info.name
    
    if len(name) > 20 or not name.isalpha():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Введено некорректное имя")
    
    surname = user_info.surname
    
    if not surname.isalpha():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректная фамилия была введена")
    
    password = user_info.password
    
    if len(password) < 8:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Длина пароля меньше 8 символов")
    
    if len(password) > 32:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Длина пароля больше 32 символов")
    
    has_num = 0
    has_lowercase = 0
    has_uppercase = 0
    
    for el in password:
        if has_num == 0 and ord(f"{el}") in range(ord("0"), ord("9") + 1):
            has_num = 1
        elif has_lowercase == 0 and ord(f"{el}") in range(ord("a"), ord("z") + 1):
            has_lowercase = 1
        elif has_uppercase == 0 and ord(f"{el}") in range(ord("A"), ord("Z") + 1):
            has_uppercase = 1
    
    detail_ex = []
    if has_num == 0:
        detail_ex.append("Необходимо, чтобы в пароле была использована как минимум 1 цифра!")
    if has_lowercase == 0:
        detail_ex.append("Необходимо, чтобы в пароле были использованы строчные английские символы a-z")
    if has_uppercase == 0:
        detail_ex.append("Необходимо, чтобы в пароле были использованы заглавные английские символы A-Z")
    
    if has_num + has_lowercase + has_uppercase < 3:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail_ex)
    
    return True

