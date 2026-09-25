import json
import os
from dis import name
from typing import List, Dict, Union, Any, Optional

# Визначення типів для анотацій (mypy)
# Структура запису: ключі - стрічки, значення - стрічки або цілі числа
Record = Dict[str, Union[str, int]]
Database = List[Record]

# Ім'я файлу для зберігання бази даних
DB_FILENAME = "library_db.json"

# Початкові дані (якщо файл не знайдено)
INITIAL_DATA: Database = [
    {"title": "Kobzar", "author": "Shevchenko", "year": 1840, "pages": 115},
    {"title": "The Forest Song", "author": "Ukrainka", "year": 1911, "pages": 96},
    {"title": "Tiger Trappers", "author": "Bagryany", "year": 1944, "pages": 280},
    {"title": "Shadows of Forgotten Ancestors", "author": "Kotsiubynsky", "year": 1911, "pages": 64},
    {"title": "Zahar Berkut", "author": "Franko", "year": 1883, "pages": 220}
]


def load_db(filename: str) -> Database:
    """
    Завантажує БД з файлу. Якщо файлу немає або він пошкоджений,
    повертає початковий список (INITIAL_DATA).
    """
    if not os.path.exists(filename):
        print(f"--- Файл {filename} не знайдено. Завантажено стартові дані. ---")
        return list(INITIAL_DATA)  # Повертаємо копію

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Елементарна перевірка, що це список
            if isinstance(data, list):
                print(f"--- Базу даних успішно завантажено з {filename} ---")
                return data
            else:
                print("--- Помилка формату файлу. Завантажено стартові дані. ---")
                return list(INITIAL_DATA)
    except (json.JSONDecodeError, IOError) as e:
        print(f"--- Помилка читання файлу ({e}). Завантажено стартові дані. ---")
        return list(INITIAL_DATA)


def save_db(db: Database, filename: str) -> None:
    """Зберігає поточний стан БД у файл."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(db, f, indent=4, ensure_ascii=False)
        print(f"--- Базу даних успішно збережено у {filename} ---")
    except IOError as e:
        print(f"--- Помилка запису у файл: {e} ---")


def print_db(db: Database) -> None:
    """a. Вивести весь список."""
    if not db:
        print("--- База даних порожня ---")
        return

    print(f"{'№':<4} {'Title':<30} {'Author':<20} {'Year':<6} {'Pages':<6}")
    print("-" * 70)
    for idx, item in enumerate(db):
        print(f"{idx:<4} {str(item.get('title', '')):<30} "
              f"{str(item.get('author', '')):<20} "
              f"{str(item.get('year', 0)):<6} "
              f"{str(item.get('pages', 0)):<6}")
    print("-" * 70)


def add_record(db: Database) -> None:
    """b. Додавати елементи до списку з перевіркою типів."""
    print("Введіть дані нової книги:")
    try:
        title = input("Назва (title): ").strip()
        if not title:
            raise ValueError("Назва не може бути порожньою.")

        author = input("Автор (author): ").strip()
        if not author:
            raise ValueError("Ім'я автора не може бути порожнім.")

        year_str = input("Рік видання (year): ")
        if not year_str.isdigit():
            raise ValueError("Рік повинен бути числом.")
        year = int(year_str)

        pages_str = input("Кількість сторінок (pages): ")
        if not pages_str.isdigit():
            raise ValueError("Кількість сторінок повинна бути числом.")
        pages = int(pages_str)

        record: Record = {
            "title": title,
            "author": author,
            "year": year,
            "pages": pages
        }
        db.append(record)
        print("--- Запис додано успішно ---")

    except ValueError as e:
        print(f"--- Помилка введення: {e} ---")


def sort_db(db: Database) -> None:
    """c. Відсортувати список за заданим атрибутом."""
    field = input("Введіть назву поля для сортування (title, author, year, pages): ").strip()

    # Перевіряємо, чи є таке поле хоча б в одному записі або чи база не пуста
    if not db:
        print("База порожня, нічого сортувати.")
        return
    valid_keys = db[0].keys()
    if field not in valid_keys:
        print(f"--- Помилка: поля '{field}' не існує. Доступні: {list(valid_keys)} ---")
        return

    try:
        # sort in place
        db.sort(key=lambda x: str(x.get(field, "")))
        print(f"--- Відсортовано за полем '{field}' ---")
    except Exception as e:
        print(f"--- Помилка при сортуванні: {e} ---")


def delete_by_attribute(db: Database) -> None:
    """d. Видаляти елементи за заданим атрибутом."""
    field = input("Введіть назву поля (title, author...): ").strip()
    if not db:
        return

    if field not in db[0].keys():
        print("--- Такого поля не існує ---")
        return

    value = input(f"Введіть значення для поля '{field}', яке треба видалити: ").strip()

    # Спробуємо конвертувати у число, якщо поле числове
    search_val: Union[str, int] = value
    if value.isdigit():
        search_val = int(value)

    initial_len = len(db)
    # Залишаємо тільки ті, що НЕ дорівнюють значенню (фільтрація)
    # Використовуємо [:] для зміни списку "на місці"
    db[:] = [item for item in db if str(item.get(field)) != str(search_val)]

    deleted_count = initial_len - len(db)
    if deleted_count > 0:
        print(f"--- Видалено записів: {deleted_count} ---")
    else:
        print("--- Записів з таким значенням не знайдено ---")


def delete_by_index(db: Database) -> None:
    """e. Видаляти елемент за заданим індексом."""
    try:
        idx_str = input(f"Введіть індекс (0 - {len(db) - 1}): ")
        idx = int(idx_str)

        if 0 <= idx < len(db):
            removed = db.pop(idx)
            print(f"--- Видалено запис: {removed['title']} ---")
        else:
            print("--- Помилка: Індекс виходить за межі діапазону ---")
    except ValueError:
        print("--- Помилка: Введіть ціле число ---")
    except IndexError:
        print("--- Помилка: Невірний індекс ---")


def search_by_attribute(db: Database) -> None:
    """f. Виводити всі елементи за заданим атрибутом (пошук)."""
    field = input("Введіть поле для пошуку: ").strip()
    val = input("Введіть значення: ").strip()

    found = False
    print("-" * 20)
    for item in db:
        # Порівнюємо як рядки для простоти
        if str(item.get(field, "")) == val:
            print(item)
            found = True
    print("-" * 20)

    if not found:
        print("--- Нічого не знайдено ---")


def main() -> None:
    # Завантаження при старті
    db = load_db(DB_FILENAME)

    while True:
        print("\n========== MENU ==========")
        print("1. Показати всі записи")
        print("2. Додати запис")
        print("3. Сортувати записи")
        print("4. Видалити за атрибутом")
        print("5. Видалити за індексом")
        print("6. Знайти за атрибутом")
        print("7. Зберегти БД у файл")
        print("8. Завантажити БД з файлу (перезаписати поточні)")
        print("0. Вихід")

        choice = input("Ваш вибір: ").strip()

        if choice == '1':
            print_db(db)
        elif choice == '2':
            add_record(db)
        elif choice == '3':
            sort_db(db)
        elif choice == '4':
            delete_by_attribute(db)
        elif choice == '5':
            delete_by_index(db)
        elif choice == '6':
            search_by_attribute(db)
        elif choice == '7':
            save_db(db, DB_FILENAME)
        elif choice == '8':
            # Підтвердження дії, бо поточні дані в пам'яті зітруться
            confirm = input("Це перезапише незбережені дані. Продовжити? (y/n): ")
            if confirm.lower() == 'y':
                db = load_db(DB_FILENAME)
        elif choice == '0':
            # Пропонуємо зберегти перед виходом
            save_q = input("Зберегти зміни перед виходом? (y/n): ")
            if save_q.lower() == 'y':
                save_db(db, DB_FILENAME)
            print("До побачення!")
            break
        else:
            print("--- Невірний вибір. Спробуйте ще раз. ---")


if name == "main":
    main()