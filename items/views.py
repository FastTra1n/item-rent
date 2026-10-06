from datetime import UTC, datetime

from django.http import HttpResponse

from homepage.views import page
from models.bookings import is_item_available
from models.items import find_item_by_id
from storage import load_bookings, load_items, load_users


def items_list(request):
    items = ""
    users_list = load_users("data/users.json")
    items_list = load_items("data/items.json", users_list)
    for item in items_list:
        text = f"{item.name} - {item.price} руб./д."
        items += (
            f'<li class="list-group-item"><a href="/items/{item.id}/">{text}</a></li>'
        )

    content = f"""
    <h1>Каталог вещей</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Вещи для аренды", content))


def item_detail(request, item_id):
    users_list = load_users("data/users.json")
    items_list = load_items("data/items.json", users_list)
    item = find_item_by_id(items_list, item_id)

    if item is None:
        content = """
        <h1 class="text-danger">Вещь не найдена</h1>
        <a href="/items/" class="btn btn-outline-secondary">← к каталогу</a>
        """
        return HttpResponse(page("Вещь не найдена", content), status=404)

    bookings_list = load_bookings("data/bookings.json", items_list, users_list)
    available = is_item_available(
        bookings_list, item_id, datetime.now(tz=UTC).date(), datetime.now(tz=UTC).date()
    )
    status = "доступно" if available else "забронировано"
    badge = "bg-success" if available else "bg-danger"

    content = f"""
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">{item.name}</h5>
        <p class="card-text">Цена аренды: <strong>{item.price} руб./д.</strong></p>
        <p class="card-text">Залоговая стоимость: <strong>{item.deposit} руб.</strong></p>
        <p class="card-text">Доступность на сегодня: <span class="badge {badge}">{status}</span></p>
        <p class="card-text">Владелец: {item.owner.name} (Рейтинг: {item.owner.rating}) | {item.owner.phone}</span></p>
        <a href="/items/" class="btn btn-outline-secondary">← к каталогу</a>
      </div>
    </div>
    """
    return HttpResponse(page(item.name, content), status=200)
