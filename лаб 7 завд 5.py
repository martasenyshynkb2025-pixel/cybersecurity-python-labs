
def print_table(data, col_width):
    pass


def task5():
    print_header("ЗАВДАННЯ 5: База даних 'Програмне забезпечення'")

    # Початкова база (локальна змінна всередині task5)
    software_db = [
        {"name": "Google Chrome", "type": "Browser", "users": 3000, "size": 150.0},
        {"name": "Windows 11", "type": "OS", "users": 1500, "size": 4500.0},
        {"name": "Notepad++", "type": "Editor", "users": 500, "size": 15.5},
        {"name": "Zoom", "type": "VoIP", "users": 2000, "size": 50.0},
        {"name": "Python", "type": "Lang", "users": 800, "size": 30.0}
    ]

    def show_db():
        """Внутрішня функція для відображення поточної бази"""
        print("\n--- Поточний стан БД ---")
        header = ["Назва", "Тип", "Користувачі", "Розмір (МБ)"]
        # Створення списку списків для print_table
        data = [[row["name"], row["type"], row["users"], row["size"]] for row in software_db]
        print_table(data, col_width=18)

    while True:
        print("\nМЕНЮ БД:")
        print("1. Показати список")
        print("2. Додати програму")
        print("3. Сортувати за кількістю користувачів")
        print("4. Видалити програму за назвою")
        print("0. Вихід з БД")

        choice = input("Ваш вибір > ")

        if choice == '1':
            show_db()

        elif choice == '2':
            try:
                n = input("Назва: ")
                t = input("Тип (Browser/OS/Editor...): ")
                u = int(input("Кількість користувачів (int): "))
                s = float(input("Розмір в МБ (float): "))
                software_db.append({"name": n, "type": t, "users": u, "size": s})
                print("Запис додано!")
            except ValueError:
                print("Помилка! Введіть коректні числа для користувачів та розміру.")

        elif choice == '3':
            # Сортування inplace
            software_db.sort(key=lambda x: x['users'], reverse=True)
            print("Базу відсортовано за спаданням кількості користувачів.")
            show_db()

        elif choice == '4':
            target = input("Введіть назву для видалення: ")
            initial_len = len(software_db)
            # Фільтрація списку (видалення)
            software_db[:] = [item for item in software_db if item['name'].lower() != target.lower()]

            if len(software_db) < initial_len:
                print(f"Програму '{target}' видалено.")
            else:
                print(f"Програму '{target}' не знайдено.")

        elif choice == '0':
            print("Вихід із завдання 5.")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")


def task4():
    pass


def print_header(param):
    pass


if __name__ == "__main__":
    # task1(), task2(), task3(), task4() мають бути визначені раніше
    try:
        task4()
        input("\nНатисніть Enter, щоб перейти до Завдання 5...")
        task5()
    except NameError as e:
        print(f"Помилка: Переконайтеся, що всі функції (task1-task5) визначені. {e}")

    print_header("Лабораторну роботу завершено!")