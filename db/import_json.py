import json
import sqlite3

from db.database import get_connection

ITEMS_FILE = "data/items.json"
USERS_FILE = "data/users.json"
BOOKINGS_FILE = "data/bookings.json"


def load_json(filename: str) -> list[dict]:
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def import_users(conn: sqlite3.Connection) -> None:
    users = load_json(USERS_FILE)
    conn.executemany(
        """
        INSERT INTO users (
            id,
            name,
            phone,
            rating
        )
        VALUES (?, ?, ?, ?)
        """,
        [
            (
                user["id"],
                user["name"],
                user["phone"],
                user["rating"],
            )
            for user in users
        ],
    )


def import_items(conn: sqlite3.Connection) -> None:
    items = load_json(ITEMS_FILE)
    conn.executemany(
        """
        INSERT INTO items (
            id,
            owner_id,
            name,
            price,
            deposit
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (
                item["id"],
                item["owner_id"],
                item["name"],
                item["price"],
                item["deposit"],
            )
            for item in items
        ],
    )


def import_bookings(conn: sqlite3.Connection) -> None:
    bookings = load_json(BOOKINGS_FILE)
    conn.executemany(
        """
        INSERT INTO bookings (
            id,
            item_id,
            user_id,
            start_date,
            end_date,
            is_cancelled
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            (
                booking["id"],
                booking["item_id"],
                booking["user_id"],
                booking["start_date"],
                booking["end_date"],
                int(booking["is_cancelled"]),
            )
            for booking in bookings
        ],
    )


def main():
    conn = get_connection()
    try:
        import_users(conn)
        import_items(conn)
        import_bookings(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
