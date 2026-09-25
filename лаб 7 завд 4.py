import hashlib
from dis import name

import requests
from typing import Dict, Iterator


# --- Допоміжна функція (з попереднього кроку) ---
def check_password(password: str) -> int:
    """
    Перевіряє пароль через API HaveIBeenPwned.
    0 - безпечний, >0 - злитий, -1 - помилка.
    """
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1_password[:5], sha1_password[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"

    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return -1

        hashes = (line.split(':') for line in response.text.splitlines())
        for h_suffix, count in hashes:
            if h_suffix == suffix:
                return int(count)
        return 0
    except requests.RequestException:
        return -1


# --- Основна функція-генератор ---
def check_passwords(users: Dict[str, str]) -> Iterator[str]:
    """
    Генератор, який перевіряє паролі користувачів і повертає (yield)
    тільки імена тих, чий пароль пройшов перевірку (безпечний).

    Args:
        users (Dict[str, str]): Словник {user_name: password}.

    Yields:
        str: Ім'я користувача (user_name), якщо його пароль безпечний.
    """
    for username, password in users.items():
        # Виконуємо перевірку
        result = check_password(password)

        # Якщо результат 0, значить пароль не знайдено в базі (він безпечний)
        if result == 0:
            yield username


# --- Тестування ---
if name == "main":
    # Словник для тесту
    users_db = {
        "admin": "123456",  # Небезпечний (злитий)
        "oleh_petrenko": "Kyiv2024!Safe*",  # Ймовірно безпечний
        "manager": "password",  # Небезпечний (злитий)
        "developer": "Xy7#mL9@vZn1!qR",  # Ймовірно безпечний
        "guest": "guest123"  # Небезпечний
    }

    print("Перевірка паролів... Наступні користувачі мають безпечні паролі:")
    print("-" * 60)

    # Використання генератора
    safe_users_generator = check_passwords(users_db)

    # Ітеруємося по генератору
    for safe_user in safe_users_generator:
        print(f"Користувач '{safe_user}' пройшов перевірку.")

    print("-" * 60)
    print("Перевірку завершено.")
