from datetime import datetime

# Запитуємо ім'я та вік
name = input("Введіть ваше ім'я: ")
age = int(input("Введіть ваш вік: "))

# Обчислюємо рік народження
current_year = datetime.now().year
birth_year = current_year - age

# Виводимо повідомлення
print(f"Привіт, {name}! Ти народився у {birth_year} році.")

