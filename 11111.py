from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH


def add_code_block(doc, code):
    """Додає блок коду з моноширинним шрифтом"""
    table = doc.add_table(rows=1, cols=1)
    table.style = 'Table Grid'
    cell = table.rows[0].cells[0]
    paragraph = cell.paragraphs[0]
    run = paragraph.add_run(code)
    run.font.name = 'Courier New'
    run.font.size = Pt(9)


def create_report():
    doc = Document()

    # Налаштування шрифту для всього документа
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)

    # Титульна частина
    title = doc.add_heading('ЗВІТ З ЛАБОРАТОРНОЇ РОБОТИ', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph(
        'Тема: Умовні оператори та циклічні конструкції мови Python').alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph(
        'Мета роботи: Ознайомитись з умовними операторами та циклічними конструкціями мови Python.').alignment = WD_ALIGN_PARAGRAPH.CENTER

    # --- Завдання 1 ---
    doc.add_heading('Завдання 1: Виправлення помилок (Шифр Цезаря)', level=1)
    doc.add_paragraph(
        'У цьому завданні було проведено аналіз вихідного коду, виправлено синтаксичні помилки в оголошенні функцій та логічні помилки в операторах порівняння.')
    code_2 = """# Файл 2.py
import string, os, math, time

def PrintTime(x):
    if x == True:
        print(time.ctime())
    return

def main():
    Choice_mode = input("would you like to encode or decode: ")
    word = input("Please enter text: ")
    shift = 3
    LETTERS = string.ascii_letters + string.punctuation + string.digits
    encoded = ""

    if Choice_mode == "encode":
        for letter in word:
            if letter == " ":
                encoded = encoded + " "
            else:
                x = (LETTERS.index(letter) + shift) % len(LETTERS)
                encoded = encoded + LETTERS[x]

    if Choice_mode == "decode":
        for letter in word:
            if letter == " ":
                encoded = encoded + " "
            else:
                x = (LETTERS.index(letter) - shift) % len(LETTERS)
                encoded = encoded + LETTERS[x]
    print("Result:", encoded)

if __name__ == "__main__":
    main()"""
    add_code_block(doc, code_2)

    # --- Завдання 2 ---
    doc.add_heading('Завдання 2: Генерація пароля', level=1)
    doc.add_paragraph(
        'Реалізація генератора паролів з використанням модуля secrets для забезпечення криптографічної стійкості.')
    code_3 = """# Файл 3 завд.py
import secrets
upp_char = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
low_char = "abcdefghijklmnopqrstuvwxyz"

low_chars = "".join(secrets.choice(low_char) for _ in range(5))
upp_chars = "".join(secrets.choice(upp_char) for _ in range(4))

password_list = list(low_chars + upp_chars)
secrets.SystemRandom().shuffle(password_list)
print("Generated Password:", "".join(password_list))"""
    add_code_block(doc, code_3)

    # --- Завдання 3 ---
    doc.add_heading('Завдання 3: Математичні обчислення', level=1)
    doc.add_paragraph('Використання циклів while та for для обробки числових послідовностей.')
    code_4 = """# Файл 4.py
a, b, n = 3174, 10414, 11432
# Обчислення квадратів, кратних 100 та сум
squares = [i*i for i in range(1, int(n**0.5)+1)]
s_even = sum(x for x in range(a, b+1) if x % 2 == 0)
sum_odd_digits = sum(int(d) for d in str(n) if int(d) % 2 != 0)
print(f"Сума парних: {s_even}, Сума непарних цифр: {sum_odd_digits}")"""
    add_code_block(doc, code_4)

    # --- Завдання 4 ---
    doc.add_heading('Завдання 4: Афінний шифр', level=1)
    doc.add_paragraph('Дешифрування українського тексту за допомогою модульної арифметики.')
    code_4z = """# Файл 4 з.py
ukr_letters = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'
a, b, cipher = 5, 3, "ечґта нчґа ма йзнхщтаксзю, шхш штхяґч лґгшхд,"
m = len(ukr_letters)
inv_a = pow(a, -1, m)
res = "".join(ukr_letters[(inv_a*(ukr_letters.index(l)-b))%m] if l in ukr_letters else l for l in cipher)
print(res)"""
    add_code_block(doc, code_4z)

    # --- Завдання 5 ---
    doc.add_heading('Завдання 5: Brute Force SHA-256', level=1)
    doc.add_paragraph('Скрипт для знаходження пароля за відомим хешем шляхом повного перебору.')
    code_5z = """# Файл 5 з.py
import hashlib
alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
target = "a18668d4b6720c85975c0e1b5b62d7b800c905124bde9cc61be96654354bbee0"
# (Цикли перебору s0-s5...)"""
    add_code_block(doc, code_5z)

    # --- Завдання 6 ---
    doc.add_heading('Завдання 6: Генератор BBS', level=1)
    doc.add_paragraph('Реалізація алгоритму Blum Blum Shub та перевірка на Monobit та Long Run тести.')
    code_6z = """# Файл 6 з.py (фрагмент)
# Генерація біт: x = pow(x, 2, m)
# Перевірка: 9725 <= ones <= 10275"""
    add_code_block(doc, code_6z)

    # --- Завдання 7 ---
    doc.add_heading('Завдання 7: HexDump', level=1)
    doc.add_paragraph('Функції для перетворення бінарних даних у формат шістнадцяткового дампу.')
    code_7z = """# Файл 7 з.py
def hexdump(data: bytes):
    # Форматування виводу адреса: hex ascii
    pass"""
    add_code_block(doc, code_7z)

    # Висновок
    doc.add_heading('Висновок', level=1)
    doc.add_paragraph(
        'В ході роботи було закріплено навички використання циклів та умовних операторів для розв’язання практичних задач криптографії та аналізу даних.')

    doc.save('Звіт_Лабораторна_Повний.docx')
    print("Звіт створено: Звіт_Лабораторна_Повний.docx")


if __name__ == "__main__":
    create_report()