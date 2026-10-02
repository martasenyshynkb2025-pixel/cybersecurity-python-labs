
import os
import random
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
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


def has_digit(password: str) -> bool:
    """Return True if the password contains at least one digit."""
    return any(char.isdigit() for char in password)


def has_upper(password: str) -> bool:
    """Return True if the password contains at least one uppercase letter."""
    return any(char.isupper() for char in password)


def has_special(password: str) -> bool:
    """Return True if the password contains at least one special character."""
    return any(not char.isalnum() for char in password)


def count_character_criteria(password: str) -> int:
    """Count how many character-group criteria the password satisfies."""
    checks = [
        has_digit(password),
        has_upper(password),
        has_special(password),
    ]
    return sum(checks)


def is_forbidden(password: str) -> bool:
    """Return True if the password is forbidden by list or length."""
    return (
        password in FORBIDDEN_PASSWORDS
        or len(password) < CRITERIA["min_length"]
    )


def classify_password(password: str, all_passwords: list) -> str:
    """Classify one password using the laboratory strength rules."""
    if is_forbidden(password):
        return "Forbidden"

    character_criteria_count = count_character_criteria(password)
    all_character_criteria = character_criteria_count == 3
    min_length = CRITERIA["min_length"]
    occurrences = all_passwords.count(password)

    if all_character_criteria and len(password) >= min_length + 4:
        if occurrences == 1:
            return "Very Strong"
        return "Strong"

    if all_character_criteria:
        return "Strong"

    if 0 < character_criteria_count < 3:
        return "Medium"

    return "Weak"


def add_random_duplicates(passwords: list) -> list:
    """Append duplicates of three randomly selected original passwords."""
    original_count = len(passwords)
    random_indexes = random.sample(range(original_count), 3)
    for index in random_indexes:
        passwords.append(passwords[index])
    return random_indexes


def print_table(passwords: list) -> None:
    """Print a readable table with password analysis results."""
    header = (
        f"{'Password':<18}"
        f"{'Length':<8}"
        f"{'Digit':<7}"
        f"{'Uppercase':<11}"
        f"{'Special':<9}"
        f"{'Occurrences':<13}"
        f"{'Strength':<12}"
    )
    print(header)
    print("-" * len(header))
    for pwd in passwords:
        print(
            f"{pwd:<18}"
            f"{len(pwd):<8}"
            f"{str(has_digit(pwd)):<7}"
            f"{str(has_upper(pwd)):<11}"
            f"{str(has_special(pwd)):<9}"
            f"{passwords.count(pwd):<13}"
            f"{classify_password(pwd, passwords):<12}"
        )


def run_task1() -> None:
    """Run Task 1 for Variant 5."""
    random.seed(42)
    passwords = PASSWORDS.copy()
    duplicate_indexes = add_random_duplicates(passwords)

    print("Laboratory Work #1 - Task 1")
    print(f"Student: {STUDENT_NAME}")
    print(f"Group: {GROUP_NAME}")
    print(f"Variant: {VARIANT_NUMBER}\n")
    print(f"Random indexes used for duplicates: {duplicate_indexes}\n")
    print_table(passwords)


if __name__ == "__main__":
    run_task1()