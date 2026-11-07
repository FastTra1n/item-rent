from datetime import UTC, datetime

from django.shortcuts import render

from items.models import Item


def items_list(request):
    items = Item.objects.all().order_by("name")

    context = {
        "items": items,
    }

    return render(request, "items/item_list.html", context)


def item_detail(request, item_id):
    item = Item.objects.select_related("owner").filter(pk=item_id).first()
    if item is None:
        return render(request, "items/item_detail.html", context={}, status=404)

    today = datetime.now(tz=UTC).date().isoformat()
    is_occupied = item.bookings.filter(
        is_cancelled=False, start_date__lte=today, end_date__gte=today
    ).exists()

    context = {
        "item": item,
        "status": "доступно" if not is_occupied else "забронировано",
        "badge": "bg-success" if not is_occupied else "bg-danger",
    }

    return render(request, "items/item_detail.html", context, status=200)
