import json
import os

def task3(print_table=None, print_heade=None):
    print_heade("ЗАВДАННЯ 3: Робота з JSON (Країни)")



    filename = r"C:\Users\Romanivna\PycharmProjects\PythonProject\countries_data"



    if not os.path.exists(filename):
        print(f"[INFO] Файл {filename} відсутній. Генеруємо дані...")
        data = [
            {"name": "Ukraine", "population": 41000000, "area": 603500, "currency": "UAH", "languages": ["Ukrainian"]},
            {"name": "USA", "population": 331000000, "area": 9833520, "currency": "USD", "languages": ["English"]},
            {"name": "China", "population": 1440000000, "area": 9596961, "currency": "CNY", "languages": ["Chinese"]},
            {"name": "Germany", "population": 83000000, "area": 357022, "currency": "EUR", "languages": ["German"]},
            {"name": "France", "population": 67000000, "area": 551695, "currency": "EUR", "languages": ["French"]},
            {"name": "Poland", "population": 38000000, "area": 312696, "currency": "PLN", "languages": ["Polish"]},
            {"name": "UK", "population": 67000000, "area": 242495, "currency": "GBP", "languages": ["English"]},
            {"name": "Italy", "population": 60000000, "area": 301340, "currency": "EUR", "languages": ["Italian"]},
            {"name": "Canada", "population": 38000000, "area": 9984670, "currency": "CAD",
             "languages": ["English", "French"]},
            {"name": "Japan", "population": 125000000, "area": 377975, "currency": "JPY", "languages": ["Japanese"]}
        ]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    # Завантаження даних
    with open(filename, 'r', encoding='utf-8') as f:
        countries = json.load(f)

    # Функція для підготовки даних до таблиці
    def prep_data(country_list):
        return [[c['name'], c['population'], c.get('currency', '-')] for c in country_list]

    # a. Країна з найбільшим населенням
    max_pop = max(countries, key=lambda x: x['population'])
    print(f"\n1. Країна з найбільшим населенням: {max_pop['name']} ({max_pop['population']})")

    top5 = sorted(countries, key=lambda x: x['population'], reverse=True)[:5]
    print("\n2. Топ-5 країн за населенням:")
    print_table(["Назва", "Населення", "Валюта"], prep_data(top5))

    # c. Країни з валютою EUR
    eur_countries = [c for c in countries if c.get('currency') == 'EUR']
    print("\n3. Країни єврозони (EUR):")
    print_table(["Назва", "Населення", "Валюта"], prep_data(eur_countries))

    # Сумарне населення єврозони
    total_eur = sum(c['population'] for c in eur_countries)
    print(f"   -> Сумарне населення: {total_eur}")

    # d. Англомовні країни
    eng_countries = [c for c in countries if "English" in c.get('languages', [])]
    print("\n4. Англомовні країни:")
    print_table(["Назва", "Населення", "Валюта"], prep_data(eng_countries))