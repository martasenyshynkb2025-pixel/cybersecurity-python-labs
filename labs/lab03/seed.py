import json
import sqlite3
from contextlib import closing
from labs.lab03.database import BASE_DIR, get_connection, initialize_database

SEED_PATH = BASE_DIR / "data" / "seed.json"


def seed_database() -> None:
    """Початкове заповнення бази в одній транзакції."""
    initialize_database()
    if not SEED_PATH.exists():
        print(f"Файл {SEED_PATH} не знайдено.")
        return

    data = json.loads(SEED_PATH.read_text(encoding="utf-8"))

    with closing(get_connection()) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM categories")
        if cursor.fetchone()[0] > 0:
            print("База даних вже містить дані. Пропуск повторного заповнення.")
            return

        try:
            with connection:
                connection.executemany(
                    "INSERT INTO categories (id, name) VALUES (?, ?)",
                    [(cat["id"], cat["name"]) for cat in data["categories"]],
                )
                connection.executemany(
                    "INSERT INTO records (code, title, category_id, value, status) VALUES (?, ?, ?, ?, ?)",
                    [
                        (
                            rec["code"],
                            rec["title"],
                            rec["category_id"],
                            rec["value"],
                            rec["status"],
                        )
                        for rec in data["records"]
                    ],
                )
            print("Успішно заповнено 3 категорії та 8 записів.")
        except sqlite3.IntegrityError as e:
            print(f"Помилка даних при сидингу: {e}")


if __name__ == "__main__":
    seed_database()
