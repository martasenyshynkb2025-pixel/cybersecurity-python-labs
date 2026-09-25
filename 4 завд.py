dir = (
    "_file1.doc\n"
    "file2.pdf\n"
    "file222_.docx\n"
    "cmd.exe\n"
    "sys.dll\n"
    "FiLe7_5.txt\n"
    "foto1.jpg\n"
    "song1.mp3\n"
    "!!!song2.mp3\n"
    "video.avi\n"
    "file9.txt\n"
    "file_3_document.docx\n"
    "my_document!!!.ppt\n"
    "main.c\n"
    "lab3.py\n"
    "lookup.xml\n"
    "pic1.png\n"
    "pic2.bmp\n"
)

print("\nРОБОТА З ІМЕНАМИ ФАЙЛІВ (Варіант 8)")

print("\nПочатковий вміст каталогу")
print(dir, end='')

total_files = dir.count('\n')
print(f"У каталозі є {total_files} файлів")

bmp_count = dir.count('.bmp\n')
xml_count = dir.count('.xml\n')
print(f"\nФайлів з розширенням bmp: {bmp_count}")
print(f"Файлів з розширенням xml: {xml_count}")

dir_after_replace = dir.replace('.jpg\n', '.png\n')
print("\nКаталог після заміни розширення .jpg на .png")
print(dir_after_replace, end='')

dir_after_case = dir_after_replace.lower()
print("\nКаталог після приведення імен файлів до нижнього регістру")
print(dir_after_case, end='')

files_list = dir_after_case.split('\n')
filtered_files = [f for f in files_list if not f.endswith('.png')]
dir_after_delete = '\n'.join(filtered_files)

print("\nКаталог після видалення файлів з розширенням .png")
print(dir_after_delete, end='')

print("\nПІДСУМОК ОПЕРАЦІЙ")

print(f"1. Початкова кількість файлів: {total_files}")
print(f"2. Файлів .bmp: {bmp_count}, файлів .xml: {xml_count}")
print(f"3. Замінено розширення: .jpg → .png")
print(f"4. Регістр змінено на: нижній")
print(f"5. Видалено файли з розширенням: .png")
print(
    f"6. Залишилось файлів: {dir_after_delete.count('\n') + (1 if dir_after_delete and not dir_after_delete.endswith('\n') else 0)}")