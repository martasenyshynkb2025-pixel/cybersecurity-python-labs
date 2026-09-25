variable_name: int = 10 / 2

def fmt(value: str, excitement: int = 10) -> str:
    return value - "!"*excitement

fmt('Hello', 'word!!!')

my_age: int | float = None
my_city: str = None

number = int | float
prices: number = [100, 105, 125.5]

Image = list[list[int]] 
image: Image = [*range(1000)]


from typing import TypeVar

T1 = TypeVar('T1')
DictWithIntKey[T1] = dict[int, T1]

a: DictWithIntKey[str] = {0: 'zero', 1: 'one'}
b: DictWithIntKey[bool] = {0: False, 1: True}
c: DictWithIntKey[int] = {0: 0, 1: 1}
d: DictWithIntKey[float] = {0: 0.0, 1: 1.0}

T2 = TypeVar('T2')
def combine(a: T2, b: T2) -> str:
    return str(a) + str(b)

print(combine(10, 20))
print(combine('hello', 2020))
print(combine('hello', 'word'))

lst_1: list = [1, "2"]
lst_2: [int] = [1, 2, 3, 4]
lst_3: list[[int]] = [[1, 2], [3, 4]]

tpl_1: tuple[int, ...] = 1, 2, 3, 4
tpl_2: tuple[list[int], list[str]] = ([1, 2], ['1', '2'], [1, 2])
tpl_3: tuple[list[int], list[int]] = ([1, 2], [3, 4], [5, 6])
tpl_4: tuple[int] = (1, 2, 3, 4)

dt_1: dict[str, int] = {"a": 1, "b": 2}

st_1: set[int, str] = {1, 2, '3', '4'}


from typing import Any

def get_first(items: list) -> Any:
    return items[0]

get_first(['1', 1])


from typing import Sequence, Mapping

def first_element(items: Sequence) -> Any:
    return items[0]

first_element((1, 2, 3))

def get_value(data: Mapping, key: str) -> Any:
    return data.get(key)

get_value({'1': 2.0, '3': 4.0}, key = '1')


from typing import Callable

def is_twice_as_big(num1: int, num2: int) -> bool:
    return num1 >= 2 * num2

def compare_nums(num1: int, num2: int, comp: Callable[int, int, bool]) -> int:
    if comp(num1, num2):
        return num1
    else:
        return num2

compare_nums(10, 3, is_twice_as_big)


from typing import Generator

def do_twice() -> Generator[int]:
    yield 1
    yield 2

def play(player_name) -> None:
    print(f"Хід {player_name}")

ret_val = play("Іван")


def calc_div(a: int, b: int) -> int:
    return a / b


ReadOnlyMode = Literal["r", "r+"]

def read_file(file_name: str, mode: ReadOnlyMode) -> None:
    return

read_file('data.txt', 'w')


from typing import Final

MAX_SIZE: Final = 1_000
MAX_SIZE += 1
