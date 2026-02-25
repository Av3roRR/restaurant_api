import enum


class DishCategory(str, enum.Enum):
    APPETIZERS = "Закуски"
    SALADS = "Салаты"
    SOUPS = "Супы"
    MAIN = "Основные блюда"
    SIDES = "Гарниры"
    DESSERTS = "Десерты"
    DRINKS = "Напитки"