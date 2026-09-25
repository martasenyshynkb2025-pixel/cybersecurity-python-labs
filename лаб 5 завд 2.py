
import pandas as pd
import numpy as np
from rich.console import Console
from rich.table import Table
import sys
from typing import Literal
def clean_numeric(value):
    if isinstance(value, (int, float)):
        return value
    if not isinstance(value, str):
        return np.nan
    value = value.strip()
    if value.lower() == 'n.a.' or value == '-':
        return np.nan
    value = value.replace('$', '').replace(',', '')
    try:
        if 'B' in value:
            value = float(value.replace('B', '')) * 1_000_000_000
        elif 'M' in value:
            value = float(value.replace('M', '')) * 1_000_000
        elif 'K' in value:
            # Видаляємо 'K' та множимо на 1 тисячу
            value = float(value.replace('K', '')) * 1_000
        else:
            value = float(value)
        return value
    except ValueError:
        return np.nan


def clean_employees(value):
    if isinstance(value, (int, float)):
        return value
    if not isinstance(value, str):
        return np.nan

    value = value.strip()
    if value.lower() == 'n.a.' or value == '-':
        return np.nan

    value = value.replace(',', '').replace(' employees', '')

    try:
        return float(value)
    except ValueError:
        return np.nan


def format_currency(amount):
    """Форматування числових значень у рядок валюти (наприклад, $1.23B)"""
    if pd.isna(amount):
        return 'N/A'

    if abs(amount) >= 1_000_000_000:
        return f"${amount / 1_000_000_000:,.2f}B"
    elif abs(amount) >= 1_000_000:
        return f"${amount / 1_000_000:,.2f}M"
    elif abs(amount) >= 1_000:
        return f"${amount / 1_000:,.2f}K"
    return f"${amount:,.2f}"


def format_per_employee(amount):
    """Форматування числових значень прибутку на працівника (наприклад, $1.23M)"""
    if pd.isna(amount):
        return 'N/A'

    if abs(amount) >= 1_000_000:
        return f"${amount / 1_000_000:,.2f}M"
    elif abs(amount) >= 1_000:
        return f"${amount / 1_000:,.2f}K"
    return f"${amount:,.2f}"


def display_rich_table(title, dataframe):
    console = Console()
    table = Table(title=title, show_header=True, header_style="bold magenta", show_lines=True)

    # Додаємо колонку 'Rank'
    table.add_column("Rank", style="dim", width=6, justify="right")

    # Додаємо інші колонки
    for column in dataframe.columns:
        justify_style: Literal["default", "left", "center", "right", "full"] = "left"

        # Спроба визначити, чи це числові дані для вирівнювання праворуч
        if pd.api.types.is_numeric_dtype(dataframe[column].dtype):
            justify_style = "right"
        elif column in ["Assets", "Profit", "Profit per Employee"]:  # Вирівнювання для форматованих колонок
            justify_style = "right"

        table.add_column(str(column), justify=justify_style)

    # Додаємо рядки
    for index, row in dataframe.iterrows():
        # index + 1 для відображення рангу
        row_items = [str(index + 1)] + [str(item) for item in row]
        table.add_row(*row_items)

    console.print(table)


def main():
    # Припускаємо, що файл знаходиться в корені проєкту або в поточному робочому каталозі
    # Якщо шлях до файлу відрізняється, замініть його.
    file_name = 'Fortune 500 Companies_2023.csv'
    try:
        df = pd.read_csv(file_name)
    except FileNotFoundError:
        print(f"Помилка: Файл '{file_name}' не знайдено.")
        print("Будь ласка, переконайтеся, що шлях до файлу правильний.")
        sys.exit(1)
    except Exception as e:
        print(f"Виникла помилка при читанні файлу: {e}")
        sys.exit(1)

    column_map = {}
    required_cols_keys = ['Name', 'Assets', 'Profit', 'Employees']

    # Автоматичне визначення назв колонок
    for col in df.columns:
        col_lower = col.lower()
        if 'name' in col_lower or 'company' in col_lower:
            column_map.setdefault('Name', col)
        elif 'assets' in col_lower or 'asset_mil' in col_lower:
            column_map['Assets'] = col
        elif 'profit' in col_lower:
            column_map['Profit'] = col
        elif 'employees' in col_lower:
            column_map['Employees'] = col

    missing_cols = [key for key in required_cols_keys if key not in column_map]
    if missing_cols:
        print(f"Помилка: Не вдалося знайти необхідні колонки: {missing_cols}")
        print(f"Доступні колонки: {df.columns.tolist()}")
        sys.exit(1)

    # Очищення та перетворення даних у числовий формат
    df['Assets_Numeric'] = df[column_map['Assets']].apply(clean_numeric)
    df['Profit_Numeric'] = df[column_map['Profit']].apply(clean_numeric)
    df['Employees_Numeric'] = df[column_map['Employees']].apply(clean_employees)

    # ----------------------------------------------------
    # Завдання 'g': Найкращі 10 компаній за активами
    # ----------------------------------------------------
    print("\nВиконується завдання 'g'...")
    # Сортування та вибір топ-10
    df_g = df.sort_values(by='Assets_Numeric', ascending=False).head(10).copy()

    # Форматування для відображення
    df_g['Assets_Formatted'] = df_g['Assets_Numeric'].apply(format_currency)

    display_df_g = df_g[[column_map['Name'], 'Assets_Formatted']].reset_index(drop=True)
    display_df_g.columns = ['Company Name', 'Assets']
    display_rich_table("g. Найкращі 10 компаній за активами (Top 10 by Assets)", display_df_g)

    print("-" * 50)

    # ----------------------------------------------------
    # Завдання 'n': Найкращі 10 компаній за прибутком на працівника
    # ----------------------------------------------------
    print("\nВиконується завдання 'n'...")

    # 1. Обчислення 'Profit per Employee'
    # Уникаємо ділення на нуль або N/A
    df['Profit_per_Employee'] = df.apply(
        lambda row: row['Profit_Numeric'] / row['Employees_Numeric']
        if row['Employees_Numeric'] > 0 and pd.notna(row['Profit_Numeric'])
        else np.nan,
        axis=1
    )

    # 2. Сортування та вибір топ-10
    # Пропускаємо NaN значення, оскільки вони не мають фінансового сенсу для цього розрахунку
    df_n = df.dropna(subset=['Profit_per_Employee']).sort_values(
        by='Profit_per_Employee', ascending=False
    ).head(10).copy()

    # 3. Форматування для відображення
    df_n['Profit_Formatted'] = df_n['Profit_Numeric'].apply(format_currency)
    df_n['Employees_Formatted'] = df_n['Employees_Numeric'].apply(lambda x: f"{int(x):,}" if pd.notna(x) else 'N/A')
    df_n['Profit_per_Employee_Formatted'] = df_n['Profit_per_Employee'].apply(format_per_employee)

    # 4. Підготовка DataFrame для відображення
    display_df_n = df_n[[
        column_map['Name'],
        'Profit_Formatted',
        'Employees_Formatted',
        'Profit_per_Employee_Formatted'
    ]].reset_index(drop=True)

    # Перейменування колонок
    display_df_n.columns = [
        'Company Name',
        'Profit',
        'Employees',
        'Profit per Employee'
    ]

    # 5. Відображення таблиці
    display_rich_table(
        "n. Найкращі 10 компаній за прибутком на працівника (Top 10 by Profit/Employee)",
        display_df_n
    )

    print("-" * 50)


if __name__ == "__main__":
    main()