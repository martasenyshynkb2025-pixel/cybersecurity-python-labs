import pandas as pd

# 1. Завантаження даних
# Вказуємо ім'я файлу. Якщо файл в іншій папці, вкажіть повний шлях.
file_path = 'log_file_23 (1).csv'

try:
    df = pd.read_csv(file_path, parse_dates=["timestamp"])
    print("--- Дані успішно завантажено ---\n")
except FileNotFoundError:
    print(f"Помилка: Файл '{file_path}' не знайдено. Перевірте назву файлу.")
    exit()

# ---------------------------------------------------------
# ЗАВДАННЯ А: Підозрілі користувачі (>= 6 невдалих спроб)
# ---------------------------------------------------------
print("=== ЗАВДАННЯ А: Користувачі з >= 6 невдалих спроб ===")

# Фільтруємо лише невдалі спроби ('fail')
failed_logins = df[df['logon_status'] == 'fail']

# Групуємо за user_name і рахуємо кількість записів
# size() рахує кількість рядків у кожній групі
user_fail_counts = failed_logins.groupby('user_name').size()

# Знаходимо тих, у кого кількість невдач >= 6
suspicious_users = user_fail_counts[user_fail_counts >= 6]

# Отримуємо список імен цих користувачів
suspicious_user_names = suspicious_users.index.tolist()

print(f"Кількість знайдених користувачів: {len(suspicious_users)}")
print(f"Список користувачів: {suspicious_user_names}")
print("\nЛоги для цих користувачів:")

# Виводимо повні логи для знайдених користувачів
# Використовуємо .isin() для фільтрації оригінального датафрейму
logs_for_suspicious_users = df[df['user_name'].isin(suspicious_user_names)]
print(logs_for_suspicious_users)
print("-" * 50)


# ---------------------------------------------------------
# ЗАВДАННЯ Б: ІР-адреси з входами у >= 3 різних акаунти
# ---------------------------------------------------------
print("\n=== ЗАВДАННЯ Б: ІР-адреси з входами у >= 3 різних акаунти ===")

# Групуємо за IP та рахуємо кількість УНІКАЛЬНИХ (nunique) user_name
ip_account_counts = df.groupby('ip')['user_name'].nunique()

# Фільтруємо ті IP, де кількість унікальних акаунтів >= 3
suspicious_ips = ip_account_counts[ip_account_counts >= 3]

# Отримуємо список цих IP
suspicious_ip_list = suspicious_ips.index.tolist()

print(f"Кількість знайдених ІР-адрес: {len(suspicious_ips)}")
print(f"Список ІР-адрес: {suspicious_ip_list}")
print("\nЛоги для цих ІР-адрес:")

# Виводимо повні логи для знайдених IP
logs_for_suspicious_ips = df[df['ip'].isin(suspicious_ip_list)]
print(logs_for_suspicious_ips)
print("-" * 50)