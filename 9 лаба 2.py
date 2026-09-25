from dis import name

import pandas as pd
import os

FILENAME = "nba_players.csv"
MY_TEAM = "Philadelphia 76ers"  # Варіант 23 (23-тя команда за алфавітом)


def analyze_nba():
    if not os.path.exists(FILENAME):
        print(f"Помилка: Файл {FILENAME} не знайдено.")
        return

    # Завантаження даних
    df = pd.read_csv(FILENAME)

    # 1. Вибірка даних для своєї команди
    team_data = df[df["Team"] == MY_TEAM].copy()
    print(f"--- Дані для команди {MY_TEAM} ({len(team_data)} гравців) ---")
    print(team_data.head())

    # Операції згідно з методичкою:
    print("\n1. Мінімальні значення (алфавітний порядок для рядків, числове для чисел):")
    print(team_data.min())

    print("\n2. Топ-3 гравці з найбільшою зарплатою:")
    print(team_data.nlargest(3, "Salary")[["Name", "Salary"]])

    print("\n3. Топ-3 гравці з найменшою зарплатою:")
    print(team_data.nsmallest(3, "Salary")[["Name", "Salary"]])

    print("\n4. Перші 3 рядки (Name та Position):")
    print(team_data[["Name", "Position"]].head(3))

    # Встановлення індексу для зручного доступу
    team_data_indexed = team_data.set_index("Name")

    print("\n5. Доступ через .at (Зарплата гравця Tobias Harris):")
    try:
        # Перевіримо, чи є такий гравець у вибірці
        player_name = "Tobias Harris"
        if player_name in team_data_indexed.index:
            print(f"{player_name}: {team_data_indexed.at[player_name, 'Salary']}")
        else:
            # Беремо першого доступного для прикладу
            first_player = team_data_indexed.index[0]
            print(f"{first_player}: {team_data_indexed.at[first_player, 'Salary']}")
    except Exception as e:
        print(e)

    print("\n6. Доступ через .loc (Інформація про гравця):")
    try:
        print(team_data_indexed.loc[team_data_indexed.index[0]])
    except IndexError:
        pass

    print("\n7. Перейменування стовпців (українською):")
    team_data_renamed = team_data.rename(columns={
        "Name": "Ім'я", "Team": "Команда", "Position": "Позиція",
        "Birthday": "Дата народження", "Salary": "Зарплата"
    })
    print(team_data_renamed.head(2))

    print("\n8. Створення нового стовпця 'Salary_k' (Зарплата в тисячах):")
    team_data_renamed["Salary_k"] = team_data_renamed["Зарплата"] / 1000
    print(team_data_renamed[["Ім'я", "Salary_k"]].head(2))

    print("\n9. Видалення стовпця 'Дата народження':")
    team_data_renamed = team_data_renamed.drop(columns=["Дата народження"])
    print(team_data_renamed.columns)


if name == "main":
    analyze_nba()