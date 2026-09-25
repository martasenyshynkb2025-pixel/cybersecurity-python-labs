

question = "Найдовша річка в Україні:"
options = ["Дунай", "Дніпро", "Дністер", "Прип'ять"]
right = "2"
false = "134"

while True:
    print(question)
    for i, opt in enumerate(options, start=1):
        print(f"{i}. {opt}")
    ans = input("Введіть номер відповіді (1–4): ")
    if ans not in false and ans not in right:
        print("Ви ввели недопустиме значення. Виберіть 1, 2, 3 або 4.\n")
        continue
    elif ans in right:
        print("Відповідь правильна! Тест завершено.")
    else:
        print(f"Відповідь не правильна! Правильна відповідь {right}! Тест завершено.")
    break