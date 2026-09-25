import streamlit as st
import pandas as pd
from datetime import datetime

# --- НАЛАШТУВАННЯ СТОРІНКИ ---
st.set_page_config(page_title="Лабораторна робота БД", layout="wide")

# --- 1. ІНФОРМАЦІЯ ПРО СТУДЕНТА ---
# Змініть ці дані на свої
GROUP_NAME = "КБ-105"
STUDENT_NAME = "Сенишин Марта"

st.title("🗃 Управління базою даних (Streamlit)")
st.markdown(f"Виконав: {STUDENT_NAME} | Група: {GROUP_NAME}")
st.markdown(f"Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
st.divider()

# --- 2. ІНІЦІАЛІЗАЦІЯ БД (SESSION STATE) ---
# Використовуємо Варіант 1: Автомобіль
# Атрибути: Виробник, Модель, Рік випуску, Пробіг, Макс. швидкість

if 'df' not in st.session_state:
    # Початкове наповнення (щоб таблиця не була порожньою)
    data = {
        'Виробник': ['Toyota', 'BMW', 'Tesla', 'Audi', 'Mercedes'],
        'Модель': ['Camry', 'X5', 'Model 3', 'A4', 'C-Class'],
        'Рік випуску': [2018, 2020, 2021, 2016, 2019],
        'Пробіг': [45000, 25000, 15000, 80000, 30000],
        'Макс. швидкість': [210, 250, 260, 240, 250]
    }
    st.session_state.df = pd.DataFrame(data)


# Функція для скидання індексу після видалення/сортування
def reset_db_index():
    st.session_state.df = st.session_state.df.reset_index(drop=True)


# --- 3. БІЧНА ПАНЕЛЬ (МЕНЮ) ---
st.sidebar.header("Меню операцій")
choice = st.sidebar.radio(
    "Оберіть дію:",
    ["Перегляд БД", "Додати елемент", "Сортувати", "Пошук (фільтр)", "Видалити за атрибутом", "Видалити за індексом"]
)

# --- 4. ОСНОВНА ЧАСТИНА ---

# a. Вивести всю БД (відображається завжди)
st.subheader("Поточна База Даних")
st.dataframe(st.session_state.df, use_container_width=True)

# --- СТАТИСТИКА (Вимога завдання) ---
with st.expander("📊 Статистика бази даних", expanded=True):
    st.write(f"Загальна кількість записів: {len(st.session_state.df)}")

    # Автоматичний розрахунок статистики
    stats_cols = st.columns(len(st.session_state.df.columns))
    for i, col in enumerate(st.session_state.df.columns):
        with stats_cols[i]:
            if pd.api.types.is_numeric_dtype(st.session_state.df[col]):
                # Для числових: мін/макс
                min_val = st.session_state.df[col].min()
                max_val = st.session_state.df[col].max()
                st.info(f"{col}**\n\nMin: {min_val}\n\nMax: {max_val}")
            else:
                # Для текстових: кількість унікальних
                unique_count = st.session_state.df[col].nunique()
                st.success(f"{col}**\n\nУнікальних: {unique_count}")

st.divider()

# --- ЛОГІКА ОПЕРАЦІЙ ---

# b. Додавати елементи
if choice == "Додати елемент":
    st.subheader("Додавання нового запису")
    with st.form("add_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            new_maker = st.text_input("Виробник")
            new_model = st.text_input("Модель")
        with col2:
            new_year = st.number_input("Рік випуску", min_value=1900, max_value=2025, step=1)
            new_mileage = st.number_input("Пробіг (км)", min_value=0, step=1000)
        with col3:
            new_speed = st.number_input("Макс. швидкість (км/год)", min_value=0, step=10)

        submitted = st.form_submit_button("Зберегти")
        if submitted:
            new_row = pd.DataFrame([{
                'Виробник': new_maker,
                'Модель': new_model,
                'Рік випуску': new_year,
                'Пробіг': new_mileage,
                'Макс. швидкість': new_speed
            }])
            st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
            st.success("Запис додано!")
            st.rerun()

# c. Відсортувати БД
elif choice == "Сортувати":
    st.subheader("Сортування")
    col1, col2 = st.columns(2)
    with col1:
        sort_col = st.selectbox("Атрибут для сортування", st.session_state.df.columns)
    with col2:
        ascending = st.radio("Порядок", ["За зростанням", "За спаданням"]) == "За зростанням"
        if st.button("Застосувати сортування"):
            st.session_state.df = st.session_state.df.sort_values(by=sort_col, ascending=ascending)
            reset_db_index()
            st.rerun()

        # f. Виводити елементи за заданим атрибутом (Пошук)
        elif choice == "Пошук (фільтр)":
            st.subheader("Пошук записів")
            search_col = st.selectbox("Де шукати?", st.session_state.df.columns)

            if pd.api.types.is_numeric_dtype(st.session_state.df[search_col]):
                search_val = st.number_input(f"Введіть точне значення для '{search_col}'")
                res_df = st.session_state.df[st.session_state.df[search_col] == search_val]
            else:
                search_val = st.text_input(f"Введіть текст для пошуку в '{search_col}'")
                res_df = st.session_state.df[
                    st.session_state.df[search_col].astype(str).str.contains(search_val, case=False)]

            if search_val:
                st.write(f"Знайдено записів: {len(res_df)}")
                st.dataframe(res_df)

        # d. Видаляти елементи за атрибутом
        elif choice == "Видалити за атрибутом":
            st.subheader("Видалення за значенням")
            del_col = st.selectbox("Оберіть колонку", st.session_state.df.columns)
            unique_vals = st.session_state.df[del_col].unique()
            del_val = st.selectbox("Оберіть значення для видалення", unique_vals)

            if st.button("Видалити всі співпадіння"):
                st.session_state.df = st.session_state.df[st.session_state.df[del_col] != del_val]
                reset_db_index()
                st.warning("Записи видалено!")
                st.rerun()

        # e. Видаляти елемент за індексом
        elif choice == "Видалити за індексом":
            st.subheader("Видалення за номером (індексом)")
            if len(st.session_state.df) > 0:
                idx_to_del = st.number_input("Введіть індекс (номер зліва в таблиці)",
                                             min_value=0, max_value=len(st.session_state.df) - 1, step=1)

                if st.button("Видалити рядок"):
                    st.session_state.df = st.session_state.df.drop(index=idx_to_del)
                    reset_db_index()
                    st.warning(f"Рядок {idx_to_del} видалено!")
                    st.rerun()
            else:
                st.error("База даних порожня")