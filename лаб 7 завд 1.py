from typing import TypeVar, Any, Sequence, Mapping, Callable, Generator, Literal, Final

# 1. Ділення (/) завжди повертає float. Змінив анотацію на float.
variable_name: float = 10 / 2

# 2. String не підтримує віднімання (-). Змінив на конкатенацію (+).
def fmt(value: str, excitement: int = 10) -> str:
    return value + "!" * excitement

# 3. Другий аргумент очікує int, а було передано str.
fmt('Hello', 5)

# 4. None не може бути присвоєно типу int/str без Optional (або | None).
my_age: int | float | None = None
my_city: str | None = None

# 5. prices - це список чисел, а не одне число.
number = int | float
prices: list[number] = [100, 105, 125.5]

# 6. Вхідні дані [*range] створюють одновимірний список, а не вкладений.
# Виправлено тип на list[int].
Image = list[int]
image: Image = [*range(1000)]

T1 = TypeVar('T1')
# 7. Синтаксис Generic Type Alias.
DictWithIntKey = dict[int, T1]

a: DictWithIntKey[str] = {0: 'zero', 1: 'one'}
b: DictWithIntKey[bool] = {0: False, 1: True}
c: DictWithIntKey[int] = {0: 0, 1: 1}
d: DictWithIntKey[float] = {0: 0.0, 1: 1.0}

T2 = TypeVar('T2')
def combine(a: T2, b: T2) -> str:
    return str(a) + str(b)

print(combine(10, 20))
# 8. combine очікує однакові типи (T2, T2). Змінив 2020 (int) на str.
print(combine('hello', '2020'))
print(combine('hello', 'word'))

lst_1: list = [1, "2"]
# 9. [int] — невірний синтаксис типу змінної, має бути list[int].
lst_2: list[int] = [1, 2, 3, 4]
# 10. list[[int]] — невірний синтаксис, має бути list[list[int]].
lst_3: list[list[int]] = [[1, 2], [3, 4]]

tpl_1: tuple[int, ...] = 1, 2, 3, 4
# 11. Кортежі мають 3 елементи, а описано було 2. Додано типи для третіх елементів.
tpl_2: tuple[list[int], list[str], list[int]] = ([1, 2], ['1', '2'], [1, 2])
tpl_3: tuple[list[int], list[int], list[int]] = ([1, 2], [3, 4], [5, 6])
# 12. tuple[int] означає кортеж з ОДНИМ елементом. Для багатьох треба tuple[int, ...].
tpl_4: tuple[int, ...] = (1, 2, 3, 4)

dt_1: dict[str, int] = {"a": 1, "b": 2}

# 13. Set приймає лише один аргумент типу. Для змішаних типів потрібен Union (|).
st_1: set[int | str] = {1, 2, '3', '4'}


def get_first(items: list) -> Any:
    return items[0]

get_first(['1', 1])


def first_element(items: Sequence) -> Any:
    return items[0]

first_element((1, 2, 3))

# Рекомендовано уточнювати типи Generic (Mapping[str, Any]), але не критично.
def get_value(data: Mapping, key: str) -> Any:
    return data.get(key)

get_value({'1': 2.0, '3': 4.0}, key = '1')


def is_twice_as_big(num1: int, num2: int) -> bool:
    return num1 >= 2 * num2

# 14. Callable має приймати список аргументів у квадратних дужках [[int, int], bool].
def compare_nums(num1: int, num2: int, comp: Callable[[int, int], bool]) -> int:
    if comp(num1, num2):
        return num1
    else:
        return num2

compare_nums(10, 3, is_twice_as_big)

# 15. Generator потребує 3 параметри: [YieldType, SendType, ReturnType].
def do_twice() -> Generator[int, None, None]:
    yield 1
    yield 2

# 16. Додано тип аргументу player_name: str.
def play(player_name: str) -> None:
    print(f"Хід {player_name}")

ret_val = play("Іван")

# 17. Ділення повертає float. Змінив Return Type.
def calc_div(a: int, b: int) -> float:
    return a / b


ReadOnlyMode = Literal["r", "r+"]

def read_file(file_name: str, mode: ReadOnlyMode) -> None:
    return

# 18. 'w' не входить у Literal["r", "r+"]. Змінив на 'r'.
read_file('data.txt', 'r')

MAX_SIZE: Final = 1_000
# 19. Змінну Final не можна змінювати. Видалено рядок MAX_SIZE += 1.