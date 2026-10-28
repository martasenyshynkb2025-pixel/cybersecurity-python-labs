from contextlib import closing
from typing import Any, Dict, List, Optional
from labs.lab03.database import get_connection


def get_all_categories() -> List[Dict[str, Any]]:
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM categories ORDER BY id ASC")
        rows = cursor.fetchall()
        return [{"id": r[0], "name": r[1]} for r in rows]


def create_category(name: str) -> Optional[Dict[str, Any]]:
    with closing(get_connection()) as conn:
        with conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
            cat_id = cursor.lastrowid
        return {"id": cat_id, "name": name}


def delete_category(category_id: int) -> bool:
    with closing(get_connection()) as conn:
        with conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
            return cursor.rowcount > 0


def get_records(
    category_id: Optional[int] = None,
    status: Optional[str] = None,
    min_value: Optional[float] = None,
    q: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
) -> List[Dict[str, Any]]:
    query = """
        SELECT r.id, r.code, r.title, r.category_id, r.value, r.status, c.name as category_name
        FROM records r
        JOIN categories c ON r.category_id = c.id
        WHERE 1=1
    """
    params: List[Any] = []

    if category_id is not None:
        query += " AND r.category_id = ?"
        params.append(category_id)
    if status is not None:
        query += " AND r.status = ?"
        params.append(status)
    if min_value is not None:
        query += " AND r.value >= ?"
        params.append(min_value)
    if q is not None:
        query += " AND instr(r.title, ?) > 0"
        params.append(q)

    query += " ORDER BY r.id ASC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [
            {
                "id": r[0],
                "code": r[1],
                "title": r[2],
                "category_id": r[3],
                "value": r[4],
                "status": r[5],
                "category_name": r[6],
            }
            for r in rows
        ]


def get_record_by_id(record_id: int) -> Optional[Dict[str, Any]]:
    query = """
        SELECT r.id, r.code, r.title, r.category_id, r.value, r.status, c.name as category_name
        FROM records r
        JOIN categories c ON r.category_id = c.id
        WHERE r.id = ?
    """
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (record_id,))
        r = cursor.fetchone()
        if not r:
            return None
        return {
            "id": r[0],
            "code": r[1],
            "title": r[2],
            "category_id": r[3],
            "value": r[4],
            "status": r[5],
            "category_name": r[6],
        }


def create_record(
    code: str, title: str, category_id: int, value: float, status: str
) -> Dict[str, Any]:
    with closing(get_connection()) as conn:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO records (code, title, category_id, value, status) VALUES (?, ?, ?, ?, ?)",
                (code, title, category_id, value, status),
            )
            rec_id = cursor.lastrowid
    return get_record_by_id(rec_id)  # type: ignore


def update_record(
    record_id: int, code: str, title: str, category_id: int, value: float, status: str
) -> Optional[Dict[str, Any]]:
    with closing(get_connection()) as conn:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE records SET code = ?, title = ?, category_id = ?, value = ?, status = ? WHERE id = ?",
                (code, title, category_id, value, status, record_id),
            )
            if cursor.rowcount == 0:
                return None
    return get_record_by_id(record_id)


def delete_record(record_id: int) -> bool:
    with closing(get_connection()) as conn:
        with conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM records WHERE id = ?", (record_id,))
            return cursor.rowcount > 0


def bulk_create_records(records_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Пакетне створення записів в єдиній транзакції."""
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        created_ids = []
        with conn:
            for rec in records_data:
                cursor.execute(
                    "INSERT INTO records (code, title, category_id, value, status) VALUES (?, ?, ?, ?, ?)",
                    (
                        rec["code"],
                        rec["title"],
                        rec["category_id"],
                        rec["value"],
                        rec["status"],
                    ),
                )
                created_ids.append(cursor.lastrowid)

    result = []
    for r_id in created_ids:
        rec = get_record_by_id(r_id)
        if rec:
            result.append(rec)
    return result
