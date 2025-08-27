from fastapi import HTTPException, status

from app.users.schemas import SRegistration

def get_current_user():
    pass


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

