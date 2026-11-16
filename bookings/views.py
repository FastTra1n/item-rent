from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Avg, Count, F, Max, Min, Q, Sum
from django.db.models.functions import Round
from django.shortcuts import render

from db.database import get_connection
from bookings.models import Booking
from items.models import Item
from users.models import User
from .forms import BookingFilterForm


def bookings_list(request):
    # booking_date = request.GET.get("date", "").strip()
    # item_id = request.GET.get("item", "").strip()
    # user_id = request.GET.get("user", "").strip()
    # sort = request.GET.get("sort", "date").strip()
    form = BookingFilterForm(request.GET or None)

    bookings = Booking.objects.active()

    booking_date = None
    item_id = None
    user_id = None
    sort = "date"
    error = None

    if form.is_valid():
        booking_date = form.cleaned_data["date"]
        item = form.cleaned_data["item"]
        user = form.cleaned_data["user"]
        sort = form.cleaned_data["sort"] or "date"

        item_id = item.pk if item else None
        user_id = user.pk if user else None

        if booking_date:
            bookings = bookings.for_date(booking_date)

        if item_id:
            bookings = bookings.filter(item_id=item_id)

        if user_id:
            bookings = bookings.filter(user_id=user_id)

    elif form.is_bound:
        error = "Проверьте корректность параметров фильтрации."

    if error:
        bookings = bookings.none()

    sort_fields = {
        "date": "start_date",
        "date_desc": "-start_date",
        "item": "item__name",
        "user": "user__name",
    }

    if sort not in sort_fields:
        sort = "date"

    bookings = (
        bookings.annotate(
            item_name=F("item__name"),
            user_name=F("user__name"),
        )
        .values(
            "id",
            "item_name",
            "user_name",
            "start_date",
            "end_date",
            "status",
        )
        .order_by(sort_fields[sort], "pk")
    )

    paginator = Paginator(bookings, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "form": form,
        "page_obj": page_obj,
        "error": error,
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

    statuses = Booking.objects.aggregate(
        active_bookings_count=Count(
            "id",
            filter=Q(status=Booking.Status.ACTIVE),
        ),
        cancelled_bookings_count=Count(
            "id",
            filter=Q(status=Booking.Status.CANCELLED),
        ),
        completed_bookings_count=Count(
            "id",
            filter=Q(status=Booking.Status.COMPLETED),
        ),
    )

    users_total = User.objects.aggregate(users_count=Count("id"))
    per_item = (
        Item.objects.annotate(
            bookings_count=Count(
                "bookings", filter=Q(bookings__status=Booking.Status.ACTIVE)
            )
        )
        .values("name", "bookings_count")
        .order_by("-bookings_count", "name", "pk")
    )
    popular = per_item.filter(bookings_count__gte=2)
    per_user = (
        User.objects.annotate(
            bookings_count=Count(
                "bookings", filter=Q(bookings__status=Booking.Status.ACTIVE)
            )
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
            "active_bookings_count": statuses["active_bookings_count"],
            "cancelled_bookings_count": statuses["cancelled_bookings_count"],
            "completed_bookings_count": statuses["completed_bookings_count"],
            "users_count": users_total["users_count"],
        },
        "per_item": per_item,
        "popular": popular,
        "per_user": per_user,
        "top_expensive": top_expensive,
    }

    return render(request, "bookings/statistics.html", context)
