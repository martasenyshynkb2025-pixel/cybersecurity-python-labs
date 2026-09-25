
n_start = 2
n_step = 3
n_count = 7

initial_list = []
n = n_start

print(f"--- Створення списку за формулою n^2 + 4n + 1 (n={n}, крок={n_step}) ---")
for _ in range(n_count):
    value = (n ** 2) + (4 * n) + 1
    initial_list.append(value)
    n += n_step

print(f"Початковий список ({len(initial_list)} елементів): \n{initial_list}\n")

print(f"a. Елементи з індексами від 3 до 5 (включно): \n{initial_list[3:6]}\n")

list_b = initial_list.copy()
list_b[0] = list_b[-1]
print(f"b. Список із заміненим першим елементом: \n{list_b}\n")

list_c = initial_list + list_b
print(f"c. Об'єднаний список (a + b): \n{list_c}\n")

first_three = list_c[:3]
list_c.extend(first_three)
print(f"d. Список з доданими першими трьома елементами: \n{list_c}\n")

max_val = max(list_c)
min_val = min(list_c)
print(f"e. Максимальне: {max_val}, Мінімальне: {min_val}\n")

if len(list_c) > 0:

    average = sum(list_c) / len(list_c)
    print(f"f. Середнє арифметичне: {average:.2f}")

    final_list = [item for item in list_c if item >= average]

    print(f"f. Фінальний список (видалено елементи < {average:.2f}): \n{final_list}\n")
else:
    print("f. Список порожній, видалення неможливе.")