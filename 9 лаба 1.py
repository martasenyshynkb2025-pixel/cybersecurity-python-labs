from os import name


class Refrigerator:
    """
    Клас, що описує Холодильник (Варіант 23).
    Атрибути: Виробник, Об’єм, Енергоспоживання, Ціна.
    Порівняння здійснюється за ціною.
    """

    def init(self, manufacturer, volume, energy_consumption, price):
        self.manufacturer = manufacturer
        self.volume = volume  # у літрах
        self.energy_consumption = energy_consumption  # кВт·год/рік
        self.price = price  # ціна

    def str(self):
        return (f"Холодильник {self.manufacturer}: {self.volume} л, "
                f"Споживання: {self.energy_consumption} кВт/рік, Ціна: {self.price} грн")

    def repr(self):
        return (f"Refrigerator(m='{self.manufacturer}', v={self.volume}, "
                f"e={self.energy_consumption}, p={self.price})")

    # Перевантаження операторів порівняння за ціною (self.price)
    def eq(self, other):
        if isinstance(other, Refrigerator):
            return self.price == other.price
        return NotImplemented

    def ne(self, other):
        if isinstance(other, Refrigerator):
            return self.price != other.price
        return NotImplemented

    def lt(self, other):
        if isinstance(other, Refrigerator):
            return self.price < other.price
        return NotImplemented

    def le(self, other):
        if isinstance(other, Refrigerator):
            return self.price <= other.price
        return NotImplemented

    def gt(self, other):
        if isinstance(other, Refrigerator):
            return self.price > other.price
        return NotImplemented

    def ge(self, other):
        if isinstance(other, Refrigerator):
            return self.price >= other.price
        return NotImplemented


# --- Демонстрація роботи ---
if name == "main":
    ref1 = Refrigerator("Samsung", 350, 280, 25000)
    ref2 = Refrigerator("LG", 320, 260, 23500)
    ref3 = Refrigerator("Bosch", 400, 300, 32000)
    ref4 = Refrigerator("Indesit", 300, 290, 25000)

    print("Список холодильників:")
    fridges = [ref1, ref2, ref3, ref4]
    for f in fridges:
        print(f)

    print("\nПорівняння:")
    print(f"{ref1.manufacturer} ({ref1.price}) > {ref2.manufacturer} ({ref2.price}): {ref1 > ref2}")
    print(f"{ref2.manufacturer} ({ref2.price}) < {ref3.manufacturer} ({ref3.price}): {ref2 < ref3}")
    print(f"{ref1.manufacturer} == {ref4.manufacturer}: {ref1 == ref4}")

    # Сортування списку об'єктів (автоматично використовує lt)
    print("\nВідсортовані за ціною (зростання):")
    fridges.sort()
    for f in fridges:
        print(f)