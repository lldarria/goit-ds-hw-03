from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson.objectid import ObjectId

#  Підключення до MongoDB (локальний сервер або Atlas)
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["cat_database"]
    collection = db["cats"]
    print(" Підключено до MongoDB!")
except ConnectionFailure:
    print(" Помилка підключення до MongoDB!")
    exit()

#  Функція створення нового запису
def create_cat(name, age, features):
    """Додає нового кота в базу даних."""
    try:
        cat = {"name": name, "age": age, "features": features}
        result = collection.insert_one(cat)
        print(f" Додано кота: {name}, ID: {result.inserted_id}")
    except Exception as e:
        print(f" Помилка створення кота: {e}")

#  Функція читання всіх записів
def read_all_cats():
    """Виводить всі записи з колекції."""
    try:
        cats = collection.find()
        for cat in cats:
            print(cat)
    except Exception as e:
        print(f" Помилка читання даних: {e}")

#  Функція пошуку кота за ім'ям
def read_cat_by_name(name):
    """Знаходить кота за ім’ям."""
    try:
        cat = collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print(" Кота з таким ім'ям не знайдено.")
    except Exception as e:
        print(f" Помилка пошуку: {e}")

#  Функція оновлення віку кота
def update_cat_age(name, new_age):
    """Оновлює вік кота за ім'ям."""
    try:
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.modified_count > 0:
            print(f" Оновлено вік кота {name} до {new_age} років.")
        else:
            print( "Кота з таким ім'ям не знайдено.")
    except Exception as e:
        print(f" Помилка оновлення віку: {e}")

#  Функція додавання нової характеристики
def add_cat_feature(name, new_feature):
    """Додає нову характеристику до списку features кота за ім'ям."""
    try:
        result = collection.update_one({"name": name}, {"$push": {"features": new_feature}})
        if result.modified_count > 0:
            print(f" Додано характеристику '{new_feature}' коту {name}.")
        else:
            print(" Кота з таким ім'ям не знайдено.")
    except Exception as e:
        print(f" Помилка додавання характеристики: {e}")

#  Функція видалення кота за ім’ям
def delete_cat_by_name(name):
    """Видаляє запис кота з колекції за ім'ям."""
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f" Кіт {name} видалений з бази.")
        else:
            print(" Кота з таким ім'ям не знайдено.")
    except Exception as e:
        print(f" Помилка видалення кота: {e}")

#  Функція видалення всіх котів
def delete_all_cats():
    """Видаляє всі записи з колекції."""
    try:
        result = collection.delete_many({})
        print(f" Видалено {result.deleted_count} записів.")
    except Exception as e:
        print(f" Помилка видалення всіх записів: {e}")

#  Тестування всіх функцій
if __name__ == "__main__":
    print("\n=== ТЕСТУВАННЯ ФУНКЦІЙ ===")

    # створюємо нового кота
    create_cat("Barsik", 3, ["ходить в капці", "дає себе гладити", "рудий"])

    # Читаємо всіх котів
    print("\n Всі коти у базі:")
    read_all_cats()

    # Знаходимо кота за ім’ям
    print("\n Пошук кота по імені:")
    read_cat_by_name("Barsik")

    # Оновлюємо вік кота
    print("\n Оновлення віку:")
    update_cat_age("Barsik", 4)

    # Додаємо нову характеристику
    print("\n Додавання характеристики:")
    add_cat_feature("Barsik", "любить рибу")

    # Видаляємо кота
    print("\n Видалення кота:")
    delete_cat_by_name("Barsik")

    # Видаляємо всіх котів
    print("\n Видалення всіх котів:")
    delete_all_cats()
