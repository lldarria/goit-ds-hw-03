import json
from pymongo import MongoClient

# Підключення до MongoDB (локально або Atlas)
client = MongoClient("mongodb://localhost:27017/")
db = client["quotes_database"]
authors_collection = db["authors"]
quotes_collection = db["quotes"]

# Завантаження authors.json
with open("authors.json", "r", encoding="utf-8") as f:
    authors_data = json.load(f)

# Завантаження quotes.json
with open("quotes.json", "r", encoding="utf-8") as f:
    quotes_data = json.load(f)

# Додаємо дані в колекції MongoDB
authors_collection.insert_many(authors_data)
quotes_collection.insert_many(quotes_data)

print("Дані імпортовано в MongoDB!")