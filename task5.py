grades = []


for i in range(5):
    grade = int(input(f"Введіть оцінку №{i + 1}: "))
    grades.append(grade)

average = sum(grades) / len(grades)


print("Усі оцінки:", grades)
print("Середнє значення оцінок:", average)

print("Оцінки, більші за середнє:")
for grade in grades:
    if grade > average:
        print(grade)
        