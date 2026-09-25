import string
from typing import List, Tuple, Dict, Any

# Набори символів
LOW_CHARS: str = string.ascii_lowercase
UPP_CHARS: str = string.ascii_uppercase
NUM_CHARS: str = string.digits
SPC_CHARS: str = string.punctuation  # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~


def count_chars(text: str, char_set: str) -> int:
    """Підраховує кількість символів з char_set у тексті."""
    return sum(1 for char in text if char in char_set)


def get_max_char_frequency(text: str, char_set: str) -> int:
    """Знаходить максимальну кількість повторень одного й того ж символу з набору."""
    chars_in_text = [char for char in text if char in char_set]
    if not chars_in_text:
        return 0
    # Знаходимо символ, що зустрічається найчастіше
    return max(text.count(c) for c in set(chars_in_text))


def get_max_consecutive(text: str, char_set: str) -> int:
    """Знаходить максимальну довжину послідовності однакових символів з набору підряд."""
    if not text:
        return 0

    max_count = 0
    current_count = 0
    prev_char = ''

    for char in text:
        if char in char_set:
            if char == prev_char:
                current_count += 1
            else:
                current_count = 1
        else:
            current_count = 0

        if current_count > max_count:
            max_count = current_count
        prev_char = char

    return max_count


def check_rule(
        description: str,
        actual_value: Any,
        expected_condition: bool,
        expected_text: str
) -> Dict[str, Any]:
    """Формує словник з результатом перевірки одного правила."""
    return {
        "rule": description,
        "expected": expected_text,
        "actual": str(actual_value),
        "status": "OK" if expected_condition else "FAIL"
    }


def validate_password(password: str) -> List[Dict[str, Any]]:
    """
    Перевіряє пароль згідно правил Варіанту 23.
    Повертає список результатів перевірки.
    """
    results: List[Dict[str, Any]] = []

    # Підрахунок кількості типів символів
    low_count = count_chars(password, LOW_CHARS)
    upp_count = count_chars(password, UPP_CHARS)
    num_count = count_chars(password, NUM_CHARS)
    spc_count = count_chars(password, SPC_CHARS)
    total_len = len(password)

    # 1. Довжина паролю (Не більше 4 спеціальних символів)
    results.append(check_rule(
        "Довжина паролю", total_len, total_len == 3, "== 3"
    ))

    # Правила 3, 16 (Маленькі літери: min 4, max 7)
    results.append(check_rule(
        "К-сть маленьких літер", low_count, 4 <= low_count <= 7, "4..7"
    ))

    # Правила 6, 19 (Великі літери: min 3, max 6)
    results.append(check_rule(
        "К-сть великих літер", upp_count, 3 <= upp_count <= 6, "3..6"
    ))

    # Правила 10, 20 (Цифри: min 3, max 4)
    results.append(check_rule(
        "К-сть цифр", num_count, 3 <= num_count <= 4, "3..4"
    ))

    # Правила 11, 22 (Спецсимволи: min 2, max 3)
    results.append(check_rule(
        "К-сть спецсимволів", spc_count, 2 <= spc_count <= 3, "2..3"
    ))

    # Правило 29: Не більше 2 однакових спецсимволів (загальна частота)
    max_freq_spc = get_max_char_frequency(password, SPC_CHARS)
    results.append(check_rule(
        "Однакові спецсимволи (макс)", max_freq_spc, max_freq_spc <= 2, "<= 2"
    ))

    # Правило 33: Не більше 3 однакових цифр підряд
    max_cons_num = get_max_consecutive(password, NUM_CHARS)
    results.append(check_rule(
        "Однакові цифри підряд (макс)", max_cons_num, max_cons_num <= 3, "<= 3"
    ))

    # Перевірка на входження символів лише із дозволених наборів
    # (Набір символів low_char + num_char + spc_char + upp_char)
    allowed_chars = LOW_CHARS + UPP_CHARS + NUM_CHARS + SPC_CHARS
    invalid_chars = [c for c in password if c not in allowed_chars]
    results.append(check_rule(
        "Дозволені символи",
        "Всі ок" if not invalid_chars else f"Заборонені: {''.join(invalid_chars)}",
        len(invalid_chars) == 0,
        "Тільки low+upp+num+spc"
    ))

    return results