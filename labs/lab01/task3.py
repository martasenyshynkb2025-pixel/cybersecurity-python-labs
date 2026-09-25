import hashlib
import json
import os

HASH_ALGORITHM = "sha3_256"
MIN_PASSWORD_LENGTH = 16


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
USERS_FILE = os.path.join(DATA_DIR, "users.csv")
LOG_FILE = os.path.join(DATA_DIR, "log.json")


def hash_password(password: str) -> str:
    """Хешує пароль за допомогою алгоритму sha3_256."""
    return hashlib.sha3_256(password.encode("utf-8")).hexdigest()


def validate_password_strength(password: str) -> bool:
    """Перевіряє, чи відповідає пароль вимозі мінімальної довжини (16 символів)."""
    return len(password) >= MIN_PASSWORD_LENGTH


def init_storage():
    """Створює директорію data та базовий файл користувачів, якщо їх немає."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(USERS_FILE):
        default_admin_pass = "SuperSecureAdminPassword123!"
        hashed_pass = hash_password(default_admin_pass)
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            f.write("username,password_hash,role\n")
            f.write(f"admin,{hashed_pass},admin\n")


def log_event(username: str, action: str, status: str):
    """Записує події в журнал log.json."""
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logs = []

    logs.append({
        "username": username,
        "action": action,
        "status": status
    })

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)


def run_task3():
    print("--- Завдання 3: Хешування, бази даних та логування ---")
    init_storage()

    test_passwords = ["short", "1234567890123456", "VeryStrongPassword2026!"]
    for pwd in test_passwords:
        is_valid = validate_password_strength(pwd)
        print(f"Пароль: '{pwd}' | Довжина >= {MIN_PASSWORD_LENGTH}: {is_valid}")
        if is_valid:
            print(f"  Хеш ({HASH_ALGORITHM}): {hash_password(pwd)}")

    log_event("admin", "login", "success")
    log_event("guest", "login", "failed")
    print("\nПодії успішно записані в log.json та users.csv створено.")


if __name__ == "__main__":
    run_task3()