import math
variant = 23
student = "Сенишин Марта"

x = float(input("Введіть x: "))
y = float(input("Введіть y: "))

part1 = y * (x * y)  (1/3)
part2 = y * math.sin(x * y)
part3 = math.exp(-y) * math.cos(x-52)
part4 = math.log(7.1 / (x * y), 7.1)

result = part1 + part2 - part3 + part4
result_floor = math.floor(result)

print(f"\nВаріант: {variant}")
print(f"Студент: {student}")
print("Формула: y * (xy)^(1/3) + y*sin(xy) - e^(-y)*cos(x^2) + log_base(7.1)(7.1/(xy))")
print(f"Введено: x = {x}, y = {y}")
print(f"Результат (до округлення): {result}")
print(f"Результат (округлення до меншого): {result_floor}")