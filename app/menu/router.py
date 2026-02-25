from fastapi import APIRouter, HTTPException, status

from app.menu.dao import MenuDAO
from app.menu.dependencies import check_values


from typing import Literal

router = APIRouter(
    prefix="/menu",
    tags=["Меню"]
)

@router.post("/add_item")
async def add_item(
    name : str,
    category: str,
    price : float,
    description : str = None,
    in_stock : bool = True,
    image_id : int = None,
):
    result = await MenuDAO.add(name=name, category=category, price=price, description=description, in_stock=in_stock, image_id=image_id)
    return result

@router.post("/edit_item")
async def edit_item(change_category: Literal["name", "category", "price", "description", "in_stock"], value: str, id: int):
    try:
        check_values(change_category, value)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

    await MenuDAO.update(id=id, field=change_category, data=value)

# делается через celery задачку
@router.post("/update_photo/{id}")
async def update_photo(id: int):
    pass

@router.post("/delete_item/{id}")
async def delete_item(id: int):
    dish = await MenuDAO.find_one_or_none(id=id)
    if not dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Блюдо не найдено")
    
    await MenuDAO.delete(id=id)
    return "Блюдо успешно удалено"

@router.get("/get_item/{id}")
async def get_item(id: int):
    item = await MenuDAO.find_one_or_none(id=id)
    if not item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Такого блюда нет в меню")

@router.get("/get_items")
async def get_items(category: Literal["Закуски", "Салаты", "Гарниры",
                             "Супы", "Основные блюда", "Десерты",
                             "Напитки"]):
    dishes = await MenuDAO.find_all(category=category)
    
    if not dishes:
        return "Доступных блюд в данной категории нет"
    
    return dishes

@router.get("/get_all_dishes")
async def get_all_dishes():
    dishes = await MenuDAO.find_all()
    
    if not dishes:
        return "Доступных блюд нет"
    
    return dishes
