from fastapi import APIRouter, HTTPException, status, Response, Depends
from pydantic import EmailStr

from app.users.schemas import SRegistration
from app.users.dao import UsersDAO

from app.users.dependencies import check_user_info, get_current_user, check_address


from app.users.auth import get_password_hash, auth_user, create_access_token

router = APIRouter(
    prefix="/users",
    tags=["Пользователи"]
)

@router.post("/registration")
async def user_registration(
    user_info: SRegistration
):
    user = await UsersDAO.find_one_or_none(email=user_info.email)
        
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователь с таким email уже существует")
    
    check_user_info(user_info)
    
    hashed_password = get_password_hash(user_info.password)
    
    await UsersDAO.add(
        name=user_info.name,
        surname=user_info.surname,
        hashed_password=hashed_password,
        email=user_info.email,
        base_address=user_info.base_address
    )
    
    return "Учётная запись была создана!"

@router.post("/log_in")
async def user_login(response: Response, email: EmailStr, password: str):
    existing_user = await auth_user(email=email, password=password)
    
    cookie_jwt = create_access_token({"sub": str(existing_user.id)})
    
    response.set_cookie("access_token", cookie_jwt, httponly=True)
    
    return {"access_token": cookie_jwt}

@router.post("/set_user_address")
async def get_user_address(new_address: str, user = Depends(get_current_user)):
    check_address(new_address)
    
    response = await UsersDAO.update(id=user.id, field="base_address", data=new_address)
    if user.base_address == "string":
        return f"Был установлен новый адрес доставки: {new_address}"
    else:
        return f"Старый адрес доставки был обновлён на новый: {new_address}"


@router.post("/log_out")
def user_logout(response: Response):
    response.delete_cookie("access_token")


@router.get("/me")
async def current_user(user = Depends(get_current_user)):
    return user

