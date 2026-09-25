import hashlib
import requests
from typing import Dict, Optional

from настя import name


def check_password(password: str) -> int:
    """
    Перевіряє, чи був пароль зламаний через API HaveIBeenPwned.

    Args:
        password (str): Пароль для перевірки.

    Returns:
        int: Кількість витоків пароля, якщо він знайдений.
             0, якщо пароль не знайдений (безпечний).
            -1, якщо сталася помилка API.
    """
    # API вимагає перші 5 символів SHA-1 хешу пароля
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1_password[:5], sha1_password[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.RequestException:
        return -1

    # Відповідь містить список суфіксів хешів та кількість витоків
    hashes = (line.split(':') for line in response.text.splitlines())
    for h, count in hashes:
        if h == suffix:
            return int(count)
    return 0


def check_passwords(users: Dict[str, str]) -> Dict[str, Optional[bool]]:
    """
    Перевіряє словник паролів користувачів.

    Args:
        users (Dict[str, str]): Словник {user_name: password}.

    Returns:
        Dict[str, Optional[bool]]: Словник {user_name: Status}.
            True  - пароль безпечний (0 витоків).
            False - пароль знайдено в базі витоків.
            None  - помилка перевірки (сервіс недоступний).
    """
    results: Dict[str, Optional[bool]] = {}
    for user, pwd in users.items():
        status = check_password(pwd)
        if status == 0:
            results[user] = True
        elif status > 0:
            results[user] = False
        else:
            results[user] = None
    return results


# --- ТЕСТУВАННЯ ЗАВДАННЯ 3 ---
if name == "main":
    test_users = {
        "admin": "password123",  # Популярний пароль (False)
        "user_secure": "Xy9#mP2!vLqZ",  # Складний пароль (True)
        "guest": "qwerty"  # Популярний пароль (False)
    }

    print("--- Результати Завдання 3 ---")
    checked_results = check_passwords(test_users)
    for user, is_safe in checked_results.items():
        print(f"Користувач: {user:<12} | Безпечний: {is_safe}")