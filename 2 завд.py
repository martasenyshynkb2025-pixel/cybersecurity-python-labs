upp_char = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
low_char = "abcdefghijklmnopqrstuvwxyz"

required_length = 23

print("\nВАЛІДАЦІЯ ПАРОЛЮ (Варіант 8)")
print(f"Мінімальна довжина: {required_length} символів")
print("Вимоги: малі латинські літери + великі латинські літери")
print("\nНатисніть Enter для повторної перевірки або введіть 'exit' для виходу")

while True:
    password = input("\nВведіть пароль (або 'exit' для виходу): ")

    if password.lower() == 'exit':
        print("Програма завершена.")
        break


    if not password:
        print("Пароль не може бути порожнім. Спробуйте ще раз.")
        continue


    length_check = len(password) >= required_length
    low_check = bool(set(password) & set(low_char))
    upp_check = bool(set(password) & set(upp_char))

    all_valid = length_check and low_check and upp_check

    print("\nРЕЗУЛЬТАТИ ПЕРЕВІРКИ:")

    length_status = "PASS" if length_check else "FAIL"
    print(f"[{length_status}] Довжина >= {required_length}: {len(password)} символів")

    low_status = "PASS" if low_check else "FAIL"
    print(f"[{low_status}] Малі латинські літери (a-z)")

    upp_status = "PASS" if upp_check else "FAIL"
    print(f"[{upp_status}] Великі латинські літери (A-Z)")

    final_status = "ПАРОЛЬ ВАЛІДНИЙ" if all_valid else "ПАРОЛЬ НЕВАЛІДНИЙ"
    print(f"\n{final_status}")

    repeat = input("\nНатисніть Enter для нової перевірки або введіть 'exit' для виходу: ")
    if repeat.lower() == 'exit':
        print("Програма завершена.")
        break