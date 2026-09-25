#Задано каталог folder_1 з підкаталогами folder_2 і folder_3 (каталог є в матеріалах до
#лабораторної роботи у ВНС). Написати програму маніпулювання з файлами і каталогами
#відповідно до завдання в табл. 2.
import os
import shutil

# Налаштування шляхів
BASE_DIR = "folder_1"
DIR_2 = os.path.join(BASE_DIR, "folder_2")
DIR_3 = os.path.join(BASE_DIR, "folder_3")
DIR_4 = os.path.join(BASE_DIR, "folder_4")


def create_test_environment():
    """Створює тестові папки та файли для демонстрації роботи."""
    if os.path.exists(BASE_DIR):
        shutil.rmtree(BASE_DIR)  # Очищаємо, якщо вже існує

    os.makedirs(DIR_2, exist_ok=True)
    os.makedirs(DIR_3, exist_ok=True)

    # Створюємо файли у folder_2
    open(os.path.join(DIR_2, "test_file.docx"), 'w').close()
    open(os.path.join(DIR_2, "note.txt"), 'w').close()

    # Створюємо файли у folder_3
    open(os.path.join(DIR_3, "data.xlsx"), 'w').close()
    open(os.path.join(DIR_3, "report.pdf"), 'w').close()
    open(os.path.join(DIR_3, "document.doc"), 'w').close()
    open(os.path.join(DIR_3, "other.txt"), 'w').close()

    print("--- Тестове середовище (folder_1) створено успішно ---\n")


# --- Головна частина програми ---

# 0. Створення тестових даних (можна закоментувати, якщо у вас свої файли)
create_test_environment()

print("РОЗПОЧИНАЄМО ВИКОНАННЯ ОПЕРАЦІЙ ВАРІАНТА 23\n")

# Операція 1: Вивести вміст каталогу folder_1 і його підкаталогів
print("[Op 1] Вміст каталогу folder_1:")
for root, dirs, files in os.walk(BASE_DIR):
    level = root.replace(BASE_DIR, '').count(os.sep)
    indent = ' ' * 4 * (level)
    print(f"{indent}{os.path.basename(root)}/")
    subindent = ' ' * 4 * (level + 1)
    for f in files:
        print(f"{subindent}{f}")
print("-" * 20)

# Операція 2: Створити в каталогу folder_1 підкаталог folder_4
try:
    if not os.path.exists(DIR_4):
        os.mkdir(DIR_4)
        print(f"[Op 2] Каталог {DIR_4} створено.")
    else:
        print(f"[Op 2] Каталог {DIR_4} вже існує.")
except Exception as e:
    print(f"[Op 2] Помилка: {e}")

# Операція 12: Скопіювати в folder_4 всі файли з folder_3 з розширенням *.xlsx
print("[Op 12] Копіювання *.xlsx з folder_3 у folder_4...")
if os.path.exists(DIR_3):
    for filename in os.listdir(DIR_3):
        if filename.endswith(".xlsx"):
            src = os.path.join(DIR_3, filename)
            dst = os.path.join(DIR_4, filename)
            shutil.copy2(src, dst)
            print(f"   Скопійовано: {filename}")

# Операція 21: Перемістити в folder_4 всі файли з folder_3 з розширенням *.pdf
print("[Op 21] Переміщення *.pdf з folder_3 у folder_4...")
if os.path.exists(DIR_3):
    for filename in os.listdir(DIR_3):
        if filename.endswith(".pdf"):
            src = os.path.join(DIR_3, filename)
            dst = os.path.join(DIR_4, filename)
            shutil.move(src, dst)
            print(f"   Переміщено: {filename}")

# Операція 34: Перейменувати в folder_3 файли *.doc в ім’я файлу_2024.doc
print("[Op 34] Перейменування *.doc у folder_3...")
if os.path.exists(DIR_3):
    for filename in os.listdir(DIR_3):
        if filename.endswith(".doc"):
            base_name = os.path.splitext(filename)[0]
            new_name = f"{base_name}_2024.doc"
            os.rename(os.path.join(DIR_3, filename), os.path.join(DIR_3, new_name))
            print(f"   Перейменовано: {filename} -> {new_name}")

# Операція 47: Видалити в folder_2 всі файли з розширенням .docx
print("[Op 47] Видалення *.docx у folder_2...")
if os.path.exists(DIR_2):
    for filename in os.listdir(DIR_2):
        if filename.endswith(".docx"):
            os.remove(os.path.join(DIR_2, filename))
            print(f"   Видалено: {filename}")

# Операція 56: Видалити підкаталог folder_2
print("[Op 56] Видалення каталогу folder_2...")
if os.path.exists(DIR_2):
    try:
        shutil.rmtree(DIR_2)  # rmtree видаляє папку навіть якщо в ній залишились інші файли
        print(f"   Каталог {DIR_2} успішно видалено.")
    except Exception as e:
        print(f"   Помилка видалення каталогу: {e}")
else:
    print(f"   Каталог {DIR_2} не знайдено.")
    print("\n--- Роботу завершено ---")
    print("Фінальний вміст folder_1:")
    for root, dirs, files in os.walk(BASE_DIR):
        level = root.replace(BASE_DIR, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f"{indent}{os.path.basename(root)}/")
        for f in files:
            print(f"{' ' * 4 * (level + 1)}{f}")