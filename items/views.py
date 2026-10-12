from datetime import UTC, datetime

from django.shortcuts import render

from models.bookings import is_item_available
from models.items import find_item_by_id
from storage import load_bookings, load_items, load_users


def items_list(request):
    users_list = load_users("data/users.json")
    items_list = load_items("data/items.json", users_list)
    context = {
        "items": items_list,
    }

    return render(request, "items/item_list.html", context)

def item_detail(request, item_id):
    users_list = load_users("data/users.json")
    items_list = load_items("data/items.json", users_list)
    item = find_item_by_id(items_list, item_id)

    bookings_list = load_bookings("data/bookings.json", items_list, users_list)
    available = is_item_available(
        bookings_list, item_id, datetime.now(tz=UTC).date(), datetime.now(tz=UTC).date()
    )
    status = "доступно" if available else "забронировано"
    badge = "bg-success" if available else "bg-danger"
    context = {
        "item": item,
        "status": status,
        "badge": badge,
    }

    return render(request, "items/item_detail.html", context, status=404 if item is None else 200)
