
import csv
import functools
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from shared.student import VARIANT_NUMBER


class ValidationError(Exception):
    """Власний виняток для помилок валідації."""

    pass


HASH_ALGORITHM = "sha3_256"
MIN_PASSWORD_LEN = 16

SALT = str(VARIANT_NUMBER).zfill(5)
DATA_DIR = Path(__file__).parent / "data"
USERS_CSV_PATH = DATA_DIR / "users.csv"
LOG_JSON_PATH = DATA_DIR / "log.json"


def generate_hash(password: str, salt: str = "00000") -> str:
    """Генерація хешу пароля з сіллю."""
    if not password or not salt:
        raise ValueError("Пароль та сіль не можуть бути порожніми")
    if len(password) < MIN_PASSWORD_LEN:
        raise ValidationError(
            f"Пароль закороткий. Мінімальна довжина: {MIN_PASSWORD_LEN}"
        )

    salted_password = (password + salt).encode("utf-8")
    return hashlib.new(HASH_ALGORITHM, salted_password).hexdigest()


def log_event(func):
    """Декоратор для логування подій автентифікації."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        username = kwargs.get("username") or (args[0] if args else "unknown")
        result = "failure"
        try:
            res = func(*args, **kwargs)
            if res:
                result = "success"
            return res
        except Exception as e:
            result = f"failure ({e})"
            raise
        finally:
            log_entry = {
                "event": "login",
                "user": username,
                "result": result,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "args": [str(a) for a in args],
                "kwargs": {k: str(v) for k, v in kwargs.items()},
            }

            DATA_DIR.mkdir(parents=True, exist_ok=True)
            logs = []
            if LOG_JSON_PATH.exists():
                try:
                    with open(LOG_JSON_PATH, "r", encoding="utf-8") as f:
                        logs = json.load(f)
                except Exception:
                    logs = []

            logs.append(log_entry)
            with open(LOG_JSON_PATH, "w", encoding="utf-8") as f:
                json.dump(logs, f, indent=4, ensure_ascii=False)

    return wrapper


def create_user(username: str, password: str) -> tuple:
    """Створення облікового запису."""
    hash_val = generate_hash(password, SALT)
    return username, hash_val


def create_users(users_list: list) -> None:
    """Запис користувачів у CSV."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    valid_users = []
    for uname, pwd in users_list:
        try:
            valid_users.append(create_user(uname, pwd))
        except (ValueError, ValidationError) as e:
            print(f"Помилка створення {uname}: {e}")

    with open(USERS_CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "password_hash"])
        writer.writerows(valid_users)


def read_users_db() -> list:
    """Читання користувачів з CSV."""
    users_db = []
    if USERS_CSV_PATH.exists():
        with open(USERS_CSV_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                users_db.append(row)
    return users_db


@log_event
def login(username: str, password: str) -> bool:
    """Спроба входу в систему."""
    if not username or not password:
        raise ValueError("Логін та пароль не можуть бути порожніми")

    users_db = read_users_db()
    try:
        current_hash = generate_hash(password, SALT)
    except (ValidationError, ValueError):
        return False

    for user in users_db:
        if user["username"] == username and user["password_hash"] == current_hash:
            return True
    return False


def run_task3() -> None:
    """Запуск третього завдання."""
    print("\n--- Завдання 3: Хешування та Логування ---")

    users_to_register = (
        ("admin_user", "SuperSecretPassword123!"),
        ("analyst_sec", "SecureCryptoPass2023#"),
        ("dev_john", "ShortPass1!"),
        ("guest_acc", "GuestPassword987654321!"),
        ("user_1", "PasswordNumberOne12345!"),
        ("user_2", "PasswordNumberTwo67890!"),
        ("user_3", "PasswordNumberThree111!"),
        ("user_4", "PasswordNumberFour2222!"),
        ("user_5", "PasswordNumberFive3333!"),
        ("user_6", "PasswordNumberSix44444!"),
    )

    try:
        create_users(users_to_register)

        print("\nБаза даних користувачів (users.csv):")
        db = read_users_db()
        for row in db:
            print(f"User: {row['username']} | Hash: {row['password_hash'][:20]}...")

        print("\nПеревірка входу:")
        print("Вхід admin_user:", login("admin_user", "SuperSecretPassword123!"))
        print("Вхід з невірним паролем:", login("admin_user", "WrongPassword12345!"))

    except (FileNotFoundError, PermissionError, IOError) as e:
        print(f"Помилка файлової системи: {e}")
    except (ValidationError, ValueError) as e:
        print(f"Помилка валідації: {e}")


if __name__ == "__main__":
    run_task3()