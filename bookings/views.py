from django.shortcuts import render
import sqlite3

from db.database import get_connection

def bookings_list(request):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    
    bookings = conn.execute("""
        SELECT
          bookings.id,
          strftime('%d.%m.%Y', bookings.start_date)
            AS start_date_display,
          strftime('%d.%m.%Y', bookings.end_date)
            AS end_date_display,
          bookings.is_cancelled,
          items.name AS item_name
        FROM bookings
        JOIN items ON bookings.item_id = items.id
        ORDER BY bookings.id DESC;
    """).fetchall()
    conn.close()
    
    context = {
        "bookings": bookings,
    }
    
    return render(request, "bookings/booking_list.html", context)


def booking_detail(request, booking_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    booking = conn.execute("""
        SELECT
          bookings.id,
          bookings.start_date,
          bookings.end_date,
          bookings.is_cancelled,
          items.name AS item_name,
          users.name AS user_name
        FROM bookings
        JOIN items ON bookings.item_id = items.id
        JOIN users ON bookings.user_id = users.id
        WHERE bookings.id = ?;
    """, [booking_id]).fetchone()
    conn.close()

    if booking is None:
        return render(request, "bookings/booking_detail.html", context={}, status=404)

    context = {
        "booking": booking,
    }

    return render(request, "bookings/booking_detail.html", context, status=200)

def statistics(request):
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    catalog = conn.execute("""
        SELECT
          COUNT(*) AS items_count,
          ROUND(AVG(price), 2) AS avg_price,
          MIN(price) AS min_price,
          MAX(price) AS max_price,
          SUM(deposit) AS total_deposit
        FROM items;
    """).fetchone()

    active = conn.execute(
        """
        SELECT
          COUNT(*) AS active_bookings_count
        FROM bookings
        WHERE is_cancelled = 0;
        """
    ).fetchone()

    cancelled = conn.execute(
        """
        SELECT
          COUNT(*) AS cancelled_bookings_count
        FROM bookings
        WHERE is_cancelled = 1;
        """
    ).fetchone()

    users_total = conn.execute(
        """
        SELECT
          COUNT(*) AS users_count
        FROM users;
        """
    ).fetchone()
    per_item = conn.execute(
        """
        SELECT
          items.name AS item_name,
          COUNT(bookings.id) AS bookings_count
        FROM items
        LEFT JOIN bookings ON items.id = bookings.item_id
          AND bookings.is_cancelled = 0
        GROUP BY items.id, items.name
        ORDER BY bookings_count DESC, item_name;
        """
    ).fetchall()

    popular = conn.execute(
        """
        SELECT
            items.name AS item_name,
            COUNT(bookings.id) AS bookings_count
        FROM items
        JOIN bookings
            ON items.id = bookings.item_id
        WHERE bookings.is_cancelled = 0
        GROUP BY items.id, items.name
        HAVING COUNT(bookings.id) >= 2
        ORDER BY bookings_count DESC;
        """
    ).fetchall()

    per_user = conn.execute(
        """
        SELECT
          users.name AS user_name,
          COUNT(bookings.id) AS bookings_count
        FROM users
        LEFT JOIN bookings ON users.id = bookings.user_id
          AND bookings.is_cancelled = 0
        GROUP BY users.id, users.name
        ORDER BY bookings_count DESC, user_name;
        """
    ).fetchall()

    top_expensive = conn.execute(
        """
        SELECT
          id,
          name,
          price
        FROM items
        ORDER BY price DESC, name
        LIMIT 3;
        """
    ).fetchall()
    conn.close()

    context = {
        "summary": {
            "items_count": catalog["items_count"],
            "avg_price": catalog["avg_price"] or 0,
            "min_price": catalog["min_price"] or 0,
            "max_price": catalog["max_price"] or 0,
            "total_deposit": catalog["total_deposit"] or 0,
            "active_bookings_count": active["active_bookings_count"],
            "cancelled_bookings_count": cancelled["cancelled_bookings_count"],
            "users_count": users_total["users_count"],
        },
        "per_item": per_item,
        "popular": popular,
        "per_user": per_user,
        "top_expensive": top_expensive,
    }
    
    return render(request, "bookings/statistics.html", context)
