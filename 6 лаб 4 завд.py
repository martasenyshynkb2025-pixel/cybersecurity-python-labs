import csv
import random
import os

def print_table(headers, data, col_width=15):
    """Допоміжна функція для виводу таблиці"""
    header_line = " | ".join(h.ljust(col_width) for h in headers)
    print(header_line)
    print("-" * len(header_line))
    for row in data:
        print(" | ".join(str(item).ljust(col_width) for item in row))

def task4(print_header=None):
    if print_header:
        print_header("ЗАВДАННЯ 4: Аналіз лог-файлів CSV")
    else:
        print("\n=== ЗАВДАННЯ 4: Аналіз лог-файлів CSV ===")

    filename = "log_file_24.csv"
    M = 5  # Поріг невдалих спроб для Варіанту 23

    # 1. Генерація CSV
    if not os.path.exists(filename):
        print(f"[INFO] Створення файлу логів {filename}...")
        header = ["user_name", "timestamp", "ip_address", "status"]
        users = ["admin", "guest", "marta_s", "hacker_1", "test_user"]

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for _ in range(100):
                u = random.choice(users)
                # Логіка розподілу статусів
                if u == "hacker_1":
                    status = "fail" if random.random() > 0.1 else "success"
                elif u == "guest":
                    status = "fail" if random.random() > 0.6 else "success"
                else:
                    status = "success" if random.random() > 0.2 else "fail"

                writer.writerow([u, "2025-05-20 12:00:00", f"192.168.1.{random.randint(1,255)}", status])

    # 2. Аналіз
    print(f"Параметри варіанту 24: знайти користувачів, у яких >= {M} помилок (fail).\n")
    fail_counts = {}

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                user = row['user_name']
                status = row['status']
                if status == 'fail':
                    fail_counts[user] = fail_counts.get(user, 0) + 1
    except FileNotFoundError:
        print("Помилка: Файл не знайдено.")
        return

    # 3. Вивід статистики
    print("Статистика помилок по користувачах:")
    stats_data = [[u, c] for u, c in sorted(fail_counts.items(), key=lambda x: x[1], reverse=True)]
    print_table(["Користувач", "Помилок"], stats_data, col_width=15)

    # 4. Визначення підозрілих
    suspicious = [u for u, count in fail_counts.items() if count >= M]

    print(f"\nРЕЗУЛЬТАТ: Підозрілі користувачі (>= {M} помилок):")
    if suspicious:
        print(", ".join(suspicious))
    else:
        print("Підозрілих користувачів не виявлено.")

# Запуск функції
if __name__ == "__main__":
    task4()