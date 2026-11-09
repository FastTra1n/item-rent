import re
from datetime import UTC, datetime

from django.http import Http404
from django.shortcuts import get_object_or_404, render

from items.models import Item
from bookings.models import Booking


def items_list(request):
    q = request.GET.get("q", "").strip()[:200]
    items = Item.objects.all().order_by("name")
    if q:
        items = items.filter(name__iregex=re.escape(q))

    context = {"items": items, "q": q}

    return render(request, "items/item_list.html", context)


def item_detail(request, slug):
    try:
        item = get_object_or_404(
            Item.objects.select_related("owner"),
            slug=slug,
        )
    except Http404:
        return render(
            request,
            "items/item_detail.html",
            {"item": None},
            status=404,
        )

    today = datetime.now(tz=UTC).date().isoformat()
    is_occupied = item.bookings.active().for_date(today).exists()

    context = {
        "item": item,
        "status": "доступно" if not is_occupied else "забронировано",
        "badge": "bg-success" if not is_occupied else "bg-danger",
    }

    return render(request, "items/item_detail.html", context, status=200)


def available_items(request):
    start_date = request.GET.get("start_date", "").strip()
    end_date = request.GET.get("end_date", "").strip()

    items_list = []
    error = None

    if start_date or end_date:
        if not start_date or not end_date:
            error = "Укажите дату начала и дату окончания."
        else:
            try:
                start = (
                    datetime.strptime(
                        start_date,
                        "%Y-%m-%d",
                    )
                    .date()
                    .isoformat()
                )
                end = (
                    datetime.strptime(
                        end_date,
                        "%Y-%m-%d",
                    )
                    .date()
                    .isoformat()
                )
            except ValueError:
                error = "Укажите корректную дату."
            else:
                booked_item_ids = (
                    Booking.objects
                    .active()
                    .filter(
                        start_date__lte=end,
                        end_date__gte=start,
                    )
                    .values_list("item_id", flat=True)
                )

                items_list = Item.objects.exclude(
                    pk__in=booked_item_ids,
                ).order_by("name", "pk")

    context = {
        "items": items_list,
        "start_date": start_date,
        "end_date": end_date,
        "error": error,
    }

    return render(request, "items/available.html", context)
