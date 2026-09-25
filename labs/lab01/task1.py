
import random
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from shared.student import GROUP_NAME, STUDENT_NAME, VARIANT_NUMBER

PASSWORDS = [
    "DataS3cur3!",
    "123",
    "Crypto@Analysis",
    "test123",
    "Quantum#2023",
    "access",
    "Security@Pro",
    "password1",
    "Adv@nced123",
    "guest123",
]

CRITERIA = {
    "min_length": 12,
    "require_digits": True,
    "require_upper": True,
    "require_special": True,
}

FORBIDDEN_PASSWORDS = {
    "123",
    "test123",
    "access",
    "password1",
    "guest123",
    "admin",
}


def evaluate_password_strength(password: str, all_passwords: list) -> str:
    """Оцінка надійності окремого пароля."""
    min_len = CRITERIA["min_length"]
    has_digit = any(c.isdigit() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_special = any(not c.isalnum() for c in password)

    if password in FORBIDDEN_PASSWORDS or len(password) < min_len:
        return "Заборонений"

    all_criteria_met = (
        has_digit and has_upper and has_lower and has_special
    )

    if (
        all_criteria_met
        and len(password) >= min_len + 4
        and all_passwords.count(password) == 1
    ):
        return "Дуже сильний"

    if all_criteria_met and len(password) < min_len + 4:
        return "Сильний"

    criteria_count = sum([has_digit, has_upper, has_lower, has_special])
    if criteria_count <= 1:
        return "Слабкий"

    return "Середній"


def run_task1() -> None:
    """Запуск аналізатора паролів."""
    print(f"--- Студент: {STUDENT_NAME} | Група: {GROUP_NAME} | Варіант: {VARIANT_NUMBER} ---")
    print("--- Завдання 1: Аналіз надійності паролів ---")

    working_passwords = PASSWORDS.copy()
    random_indices = random.sample(range(len(working_passwords)), 3)
    for idx in random_indices:
        working_passwords.append(working_passwords[idx])

    print(f"{'№':<3} | {'Пароль':<20} | {'Категорія надійності':<20}")
    print("-" * 50)
    for i, pwd in enumerate(working_passwords, 1):
        category = evaluate_password_strength(pwd, working_passwords)
        print(f"{i:<3} | {pwd:<20} | {category:<20}")


if __name__ == "__main__":
    run_task1()