from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Count, Avg, Min, Max, Sum, Q
from django.db.models.functions import Round
from django.shortcuts import render

from db.database import get_connection
from bookings.models import Booking
from items.models import Item
from users.models import User


def bookings_list(request):
    booking_date = request.GET.get("date", "").strip()
    item_id = request.GET.get("item", "").strip()
    user_id = request.GET.get("user", "").strip()
    sort = request.GET.get("sort", "date").strip()

    error = None

    bookings = Booking.objects.filter(
        is_cancelled=False,
    ).select_related("item", "user")

    if booking_date:
        try:
            selected_date = (
                datetime.strptime(
                    booking_date,
                    "%Y-%m-%d",
                )
                .date()
                .isoformat()
            )
        except ValueError:
            error = "Укажите корректную дату."
        else:
            bookings = bookings.filter(
                start_date__lte=selected_date,
                end_date__gte=selected_date,
            )

    try:
        if item_id:
            bookings = bookings.filter(item_id=int(item_id))

        if user_id:
            bookings = bookings.filter(user_id=int(user_id))
    except ValueError:
        error = "Некорректный идентификатор вещи или арендатора."

    if error:
        bookings = bookings.none()

    sort_fields = {
        "date": "start_date",
        "item": "item__name",
        "user": "user__name",
    }

    if sort not in sort_fields:
        sort = "date"

    bookings = bookings.order_by(sort_fields[sort], "pk")

    paginator = Paginator(bookings, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "booking_date": booking_date,
        "selected_item": item_id,
        "selected_user": user_id,
        "sort": sort,
        "error": error,
        "items": Item.objects.order_by("name", "pk"),
        "users": User.objects.order_by("name", "pk"),
    }

    return render(request, "bookings/booking_list.html", context)


def booking_detail(request, booking_id):
    booking = (
        Booking.objects.select_related("item", "user").filter(pk=booking_id).first()
    )

    if booking is None:
        return render(request, "bookings/booking_detail.html", context={}, status=404)

    context = {
        "booking": booking,
    }

    return render(request, "bookings/booking_detail.html", context, status=200)


def statistics(request):
    catalog = Item.objects.aggregate(
        items_count=Count("id"),
        avg_price=Round(Avg("price", default=0), 2),
        min_price=Min("price", default=0),
        max_price=Max("price", default=0),
        total_deposit=Sum("deposit", default=0),
    )

    active = Booking.objects.aggregate(
        active_bookings_count=Count("id", filter=Q(is_cancelled=False))
    )

    cancelled = Booking.objects.aggregate(
        cancelled_bookings_count=Count("id", filter=Q(is_cancelled=True))
    )

    users_total = User.objects.aggregate(users_count=Count("id"))
    per_item = (
        Item.objects.annotate(
            bookings_count=Count("bookings", filter=Q(bookings__is_cancelled=False))
        )
        .values("name", "bookings_count")
        .order_by("-bookings_count", "name", "pk")
    )
    popular = per_item.filter(bookings_count__gte=2)
    per_user = (
        User.objects.annotate(
            bookings_count=Count("bookings", filter=Q(bookings__is_cancelled=False))
        )
        .values("name", "bookings_count")
        .order_by("-bookings_count", "name", "pk")
    )
    top_expensive = Item.objects.order_by("-price", "name", "pk")[:3]

    context = {
        "summary": {
            "items_count": catalog["items_count"],
            "avg_price": catalog["avg_price"],
            "min_price": catalog["min_price"],
            "max_price": catalog["max_price"],
            "total_deposit": catalog["total_deposit"],
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
