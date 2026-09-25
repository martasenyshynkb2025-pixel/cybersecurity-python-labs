def print_set(message, data):
    """Допоміжна функція для гарного виводу відсортованої множини"""
    if isinstance(data, bool):
        print(f"{message}: {data}")
    else:

        print(f"{message}: {sorted(list(data))}")

# Вхідні дані
last_name = "Сенишин"
first_name = "Марта"
patronymic = "Романівна"
ukrainian_alphabet = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"

# Створення множин
set1 = set(last_name)
set2 = set(first_name)
set3 = set(patronymic)

print(f"Set1 (Прізвище): {sorted(set1)}")
print(f"Set2 (Ім'я): {sorted(set2)}")
print(f"Set3 (По батькові): {sorted(set3)}")
print("-" * 40)

task_a = set2 & set3
print_set("a. Спільні літери (set2 і set3)", task_a)

task_b = set1 | set2
print_set("b. Літери з set1 або set2", task_b)

task_c = set2 - set1
print_set("c. Літери set2, яких немає в set1", task_c)

task_d = set1.issubset(set3)
print_set("d. Чи є set1 підмножиною set3", task_d)

task_e = set1 ^ set2
print_set("e. Симетрична різниця set1 і set2", task_e)

only_in_1 = set1 - set2 - set3
only_in_2 = set2 - set1 - set3
only_in_3 = set3 - set1 - set2
task_f = only_in_1 | only_in_2 | only_in_3
print_set("f. Літери, унікальні для кожної множини", task_f)

all_names_letters = set1 | set2 | set3
alphabet_set = set(ukrainian_alphabet)
task_g = alphabet_set - all_names_letters
print_set("g. Літери алфавіту, яких немає в імені", task_g)