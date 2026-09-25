import zipfile
import os

base_path = r"C:\Users\Romanivna\PycharmProjects\PythonProject\Variant 23.zip"

zip_path = r"C:\Users\Romanivna\PycharmProjects\PythonProject\Variant 27.zip"
dict_path = os.path.join(base_path, "10-million-password-list-top-100000.txt")
extract_path = base_path

# Перевірка чи файли існують
if not os.path.exists(zip_path):
    print(f" Архів не знайдено: {zip_path}")
    exit()
if not os.path.exists(dict_path):
    print(f" Словник не знайдено: {dict_path}")
    exit()


def password_seeking():
    """Пошук пароля для zip-архіву"""
    print("Розпочинаю перебір паролів...")

    zip_file = zipfile.ZipFile(zip_path, 'r')

    # Відкриваємо файл словника
    with open(dict_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            password = line.strip()


            if len(password) == 4:
                try:
                    # Спроба розпакувати
                    zip_file.extractall(extract_path, pwd=password.encode())
                    zip_file.close()
                    return password  # Якщо вийшло то повертаємо пароль
                except RuntimeError:
                    continue
                except Exception:
                    continue

    zip_file.close()
    return None



found_password = password_seeking()

if found_password:
    print(f" Password was found: {found_password}")
else:
    print(" Password not found in dictionary.")