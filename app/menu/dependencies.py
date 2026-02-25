

def check_values(category, value):
    if category == "name" or category == "description" or category == "category":
        if not isinstance(value, str):
            raise ValueError("Value должно быть строкой")
        
        if category == "category":
            if value not in ["Закуски", "Салаты", "Гарниры",
                             "Супы", "Основные блюда", "Десерты",
                             "Напитки"]:
                raise ValueError("Такой категории нет в меню")
    elif category == "price":
        if not isinstance(value, int):
            raise ValueError("Цена должна быть числом") 
    else:
        if not isinstance(value, bool):
            raise ValueError("Для наличия должно быть булевым значением(True/False)")
    
    return True