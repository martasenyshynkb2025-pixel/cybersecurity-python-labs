import json
from typing import List

SUSPICIOUS_USERS = ["service", "unknown", "juliewatson"]
SUSPICIOUS_EXTENSIONS = [".js", ".exe", ".sh"]  # Підозрілі файли


def is_suspicious_username(username: str) -> bool:
    return username in SUSPICIOUS_USERS


def is_suspicious_files(files: List[str]) -> bool:
    # Наприклад, якщо файл має підозріле розширення або знаходиться в tmp
    for f in files:
        if any(f.endswith(ext) for ext in SUSPICIOUS_EXTENSIONS):
            return True
    return False


def analyze_logs(filename: str) -> None:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            logs = json.load(f)

        print("\n--- Log Analysis (Variant 23) ---")
        found_pids: List[int] = []

        for entry in logs:
            # b. Фільтрація по username
            susp_user = is_suspicious_username(entry.get("username", ""))
            # c. Фільтрація по open_files
            susp_files = is_suspicious_files(entry.get("open_files", []))

            # Шукаємо записи, що містять ОБИДВІ ознаки (згідно умови "дві підозрілі ознаки")
            if susp_user and susp_files:
                found_pids.append(entry.get("pid"))

        print(f"Підозрілі PID (User + Files): {found_pids}")

    except FileNotFoundError:
        print("Файл system_logs.json не знайдено.")


analyze_logs("system_logs.json")