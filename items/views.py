import sqlite3
from datetime import UTC, datetime

from django.shortcuts import render

from db.database import get_connection

DB_PATH = "data/rently.sqlite"


def items_list(request):
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    items = conn.execute("""
        SELECT
          id,
          name
        FROM items
        ORDER BY name;
    """).fetchall()
    conn.close()

    context = {
        "items": items,
    }

    return render(request, "items/item_list.html", context)


def item_detail(request, item_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    item = conn.execute(
        """
        SELECT
          items.id,
          items.name,
          items.price,
          items.deposit,
          users.name AS owner_name,
          users.phone AS owner_phone,
          users.rating AS owner_rating
        FROM items
        JOIN users ON items.owner_id = users.id
        WHERE items.id = ?;
    """,
        [item_id],
    ).fetchone()

    if item is None:
        conn.close()
        return render(request, "items/item_detail.html", context={}, status=404)

    today = datetime.now(tz=UTC).date().isoformat()
    active_booking = conn.execute(
        """
        SELECT 1
        FROM bookings
        WHERE item_id = ?
          AND is_cancelled = 0
          AND ? BETWEEN start_date AND end_date;
    """,
        [item_id, today],
    ).fetchone()
    conn.close()

    available = active_booking is None
    status = "доступно" if available else "забронировано"
    badge = "bg-success" if available else "bg-danger"
    context = {
        "item": item,
        "status": status,
        "badge": badge,
    }

    return render(request, "items/item_detail.html", context, status=200)
