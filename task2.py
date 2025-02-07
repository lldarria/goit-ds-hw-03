import requests
import json
from bs4 import BeautifulSoup

#  URL головної сторінки
BASE_URL = "http://quotes.toscrape.com"

#  Дані для збереження
quotes_data = []
authors_data = {}

#  Обхід усіх сторінок із цитатами
page = 1
while True:
    response = requests.get(f"{BASE_URL}/page/{page}")
    soup = BeautifulSoup(response.text, "html.parser")

    # Знаходимо всі цитати на сторінці
    quotes = soup.find_all("div", class_="quote")
    if not quotes:
        break  # Виходимо з циклу, якщо більше немає сторінок

    for quote in quotes:
        text = quote.find("span", class_="text").get_text(strip=True)
        author = quote.find("small", class_="author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote.find_all("a", class_="tag")]

        # Додаємо цитату у список
        quotes_data.append({"author": author, "quote": text, "tags": tags})

        # Якщо автора ще немає в authors_data, отримуємо деталі
        if author not in authors_data:
            author_page_link = quote.find("a")["href"]
            author_page = requests.get(BASE_URL + author_page_link)
            author_soup = BeautifulSoup(author_page.text, "html.parser")

            born_date = author_soup.find("span", class_="author-born-date").get_text(strip=True)
            born_location = author_soup.find("span", class_="author-born-location").get_text(strip=True)
            description = author_soup.find("div", class_="author-description").get_text(strip=True)

            # Додаємо інформацію про автора
            authors_data[author] = {
                "fullname": author,
                "born_date": born_date,
                "born_location": born_location,
                "description": description,
            }

    print(f" Оброблено сторінку {page}")
    page += 1  # Переходимо до наступної сторінки

# Збереження у JSON-файли
with open("quotes.json", "w", encoding="utf-8") as f:
    json.dump(quotes_data, f, ensure_ascii=False, indent=4)

with open("authors.json", "w", encoding="utf-8") as f:
    json.dump(list(authors_data.values()), f, ensure_ascii=False, indent=4)

print("\n Дані збережено в quotes.json та authors.json")
