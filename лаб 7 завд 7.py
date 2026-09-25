from os import name
from typing import List, Dict, Union

from rich.console import Console
from rich.table import Table

# Тип для холодильника
Fridge = Dict[str, Union[str, int, float]]
Database = List[Fridge]

console = Console()

# Початкова база даних (5 елементів)
db: Database = [
    {"maker": "Samsung", "volume": 300, "energy": 250, "price": 15000},
    {"maker": "LG", "volume": 320, "energy": 240, "price": 16000},
    {"maker": "Bosch", "volume": 280, "energy": 220, "price": 18000},
    {"maker": "Indesit", "volume": 250, "energy": 300, "price": 10000},
    {"maker": "Whirlpool", "volume": 350, "energy": 280, "price": 20000},
]


def print_db(data: Database) -> None:
    table = Table(title="База даних: Холодильники")
    table.add_column("№", style="cyan", no_wrap=True)
    table.add_column("Виробник", style="magenta")
    table.add_column("Об'єм (л)", justify="right", style="green")
    table.add_column("Енергоспож. (кВт/рік)", justify="right", style="yellow")
    table.add_column("Ціна (грн)", justify="right", style="red")

    for idx, item in enumerate(data, 1):
        table.add_row(
            str(idx),
            str(item["maker"]),
            str(item["volume"]),
            str(item["energy"]),
            str(item["price"])
        )
    console.print(table)


def add_item(data: Database) -> None:
    print("Додавання нового холодильника:")
    try:
        maker = input("Виробник: ")
        volume = float(input("Об'єм (л): "))
        energy = float(input("Енергоспоживання: "))
        price = float(input("Ціна: "))
        data.append({
            "maker": maker, "volume": volume,
            "energy": energy, "price": price
        })
        print("Додано успішно!")
    except ValueError:
        print("Помилка вводу даних!")


def sort_db(data: Database) -> None:
    key = select_attribute()
    if key:
        data.sort(key=lambda x: x[key])  # type: ignore
        print(f"Відсортовано за {key}")


def delete_by_attribute(data: Database) -> None:
    key = select_attribute()
    if not key: return
    val = input("Введіть значення для видалення: ")
    # Конвертуємо тип для порівняння, якщо це число
    try:
        if key == "maker":
            val_comp = val  # type: ignore
        else:
            float(val)

        initial_len = len(data)
        # Видаляємо (фільтруємо in-place або створюємо новий список)
        # Для простоти змінимо посиланням, але в функції краще повертати новий
        data[:] = [x for x in data if str(x[key]) != str(val)]
        print(f"Видалено {initial_len - len(data)} записів.")
    except ValueError:
        print("Невірний формат значення.")


def delete_by_index(data: Database) -> None:
    try:
        idx = int(input("Введіть номер рядка (N): ")) - 1
        if 0 <= idx < len(data):
            removed = data.pop(idx)
            print(f"Видалено: {removed['maker']}")
        else:
            print("Невірний індекс")
    except ValueError:
        print("Потрібно ввести число")


def filter_by_attribute(data: Database) -> None:
    key = select_attribute()
    if not key: return
    val = input("Значення для пошуку: ")
    filtered = [x for x in data if str(x[key]) == val]
    print_db(filtered)


def select_attribute() -> str:
    print("\nОберіть атрибут:")
    print("1. Виробник (maker)")
    print("2. Об'єм (volume)")
    print("3. Енергоспоживання (energy)")
    print("4. Ціна (price)")
    ch = input("Ваш вибір: ")
    mapping = {"1": "maker", "2": "volume", "3": "energy", "4": "price"}
    return mapping.get(ch, "")


def main_menu():
    while True:
        print("\n--- МЕНЮ ---")
        print("a. Вивести список")
        print("b. Додати елемент")
        print("c. Сортувати")
        print("d. Видалити за атрибутом")
        print("e. Видалити за індексом")
        print("f. Знайти за атрибутом")
        print("q. Вихід")

        choice = input("Оберіть дію: ").lower()

        if choice == 'a':
            print_db(db)
        elif choice == 'b':
            add_item(db)
        elif choice == 'c':
            sort_db(db)
        elif choice == 'd':
            delete_by_attribute(db)
        elif choice == 'e':
            delete_by_index(db)
        elif choice == 'f':
            filter_by_attribute(db)
        elif choice == 'q':
            break
        else:
            print("Невідома команда")


if name == "main":
    main_menu()