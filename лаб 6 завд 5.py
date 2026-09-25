
# 1. Ініціалізація бази даних (список словників)
# Атрибути: Виробник, об’єм (л), енергоспоживання (кВт·год/рік), ціна
database = [
    {"manufacturer": "Samsung", "volume": 350, "energy": 280, "price": 25000},
    {"manufacturer": "LG", "volume": 320, "energy": 260, "price": 24500},
    {"manufacturer": "Bosch", "volume": 400, "energy": 300, "price": 32000},
    {"manufacturer": "Indesit", "volume": 280, "energy": 240, "price": 12000},
    {"manufacturer": "Whirlpool", "volume": 340, "energy": 275, "price": 18500}
]

keys_mapping = {
    "1": "manufacturer",
    "2": "volume",
    "3": "energy",
    "4": "price"
}

keys_names = {
    "manufacturer": "Виробник",
    "volume": "Об'єм (л)",
    "energy": "Енергоспож.",
    "price": "Ціна (грн)"
}

while True:
    print("-" * 50)
    print("МЕНЮ КЕРУВАННЯ БАЗОЮ ДАНИХ (ХОЛОДИЛЬНИКИ):")
    print("a. Вивести весь список")
    print("b. Додати елемент")
    print("c. Відсортувати список за атрибутом")
    print("d. Видалити елементи за атрибутом")
    print("e. Видалити елемент за індексом")
    print("f. Пошук елементів за атрибутом")
    print("q. Вихід")
    print("-" * 50)

    choice = input("Ваш вибір: ").lower()

    # --- a. Вивести весь список ---
    if choice == 'a':
        print(f"\n{'№':<4} {'Виробник':<15} {'Об\'єм (л)':<10} {'Енерго (кВт)':<15} {'Ціна (грн)':<10}")
        print("-" * 60)
        for i in range(len(database)):
            item = database[ i ]
            print(f"{i:<4} {item['manufacturer']:<15} {item['volume']:<10} {item['energy']:<15} {item['price']:<10}")

    # --- b. Додати елемент ---
    elif choice == 'b':
        print("\nВведіть дані нового холодильника:")
        m_in = input("Виробник: ")

        # Перевірка на коректність чисел
        try:
            v_in = int(input("Об'єм (л): "))
            e_in = int(input("Енергоспоживання (кВт·год/рік): "))
            p_in = int(input("Ціна: "))

            new_record = {
                "manufacturer": m_in,
                "volume": v_in,
                "energy": e_in,
                "price": p_in
            }
            database.append(new_record)
            print("Запис додано!")
        except ValueError:
            print("Помилка! Об'єм, енергія та ціна мають бути числами.")

    # --- c. Відсортувати список ---
    elif choice == 'c':
        print("\nЗа яким атрибутом сортувати?")
        print("1 - Виробник, 2 - Об'єм, 3 - Енергоспоживання, 4 - Ціна")
        key_idx = input("Введіть номер: ")

        if key_idx in keys_mapping:
            sort_key = keys_mapping[key_idx]

            # Сортування бульбашкою (Bubble Sort) без використання функцій
            n = len(database)
            for i in range(n):
                for j in range(0, n - i - 1):
                    # Порівняння елементів
                    val1 = database[j][sort_key]
                    val2 = database[j + 1][sort_key]

                    # Для рядків приводимо до нижнього регістру для коректного сортування
                    if isinstance(val1, str):
                        val1 = val1.lower()
                        val2 = val2.lower()

                    if val1 > val2:
                        # Обмін місцями
                        database[j], database[j + 1] = database[j + 1], database[j]
            print(f"Список відсортовано за полем '{keys_names[sort_key]}'.")
        else:
            print("Невірний вибір атрибута.")

    # --- d. Видалити елементи за атрибутом ---
    elif choice == 'd':
        print("\nЗа яким атрибутом видаляти?")
        print("1 - Виробник, 2 - Об'єм, 3 - Енергоспоживання, 4 - Ціна")
        key_idx = input("Введіть номер атрибута: ")

        if key_idx in keys_mapping:
            target_key = keys_mapping[key_idx]
            val_to_del = input(f"Введіть значення для '{keys_names[target_key]}', яке треба видалити: ")

            # Створюємо новий список тільки з тих елементів, які НЕ треба видаляти
            new_database = []
            deleted_count = 0

            for item in database:
                current_val = str(item[target_key])  # Приводимо до рядка для порівняння
                if current_val.lower() != val_to_del.lower():
                    new_database.append(item)
                else:
                    deleted_count += 1

            database = new_database
            print(f"Видалено записів: {deleted_count}")
        else:
            print("Невірний атрибут.")

    # --- e. Видалити елемент за індексом ---
    elif choice == 'e':
        try:
            idx = int(input(f"Введіть індекс (0 - {len(database) - 1}): "))
            if 0 <= idx < len(database):
                removed = database.pop(idx)
                print(f"Видалено: {removed['manufacturer']}")
            else:
                print("Індекс виходить за межі списку.")
        except ValueError:
            print("Введіть ціле число.")

    # --- f. Пошук/Вивід елементів за атрибутом ---
    elif choice == 'f':
        print("\nЗа яким параметром шукати?")
        print("1 - Виробник, 2 - Об'єм, 3 - Енергоспоживання, 4 - Ціна")
        key_idx = input("Введіть номер атрибута: ")

        if key_idx in keys_mapping:
            search_key = keys_mapping[key_idx]
            search_val = input(f"Введіть значення для '{keys_names[search_key]}': ")

            print(f"\nРезультати пошуку:")
            print(f"{'№':<4} {'Виробник':<15} {'Об\'єм (л)':<10} {'Енерго (кВт)':<15} {'Ціна (грн)':<10}")
            print("-" * 60)

            found = False
            for i in range(len(database)):
                item = database[i]
                # Порівнюємо як рядки, щоб не було помилок типів
                if str(item[search_key]).lower() == search_val.lower():
                    print(
                        f"{i:<4} {item['manufacturer']:<15} {item['volume']:<10} {item['energy']:<15} {item['price']:<10}")
                    found = True

            if not found:
                print("Нічого не знайдено.")
        else:
            print("Невірний атрибут.")

    # --- Вихід ---
    elif choice == 'q':
        print("Роботу завершено.")
        break

    else:
        print("Невірна команда. Спробуйте ще раз.")