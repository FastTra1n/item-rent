from django.contrib import admin
from django.db.models import Count, Q

from bookings.models import Booking

from .models import Item


class BookingInline(admin.TabularInline):
    model = Booking
    fields = ("user", "start_date", "end_date", "status")
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "owner",
        "price",
        "deposit",
        "active_bookings_count",
    )
    list_display_links = ("name",)
    list_editable = ("price", "deposit")
    search_fields = ("name", "owner__name")
    list_filter = ("owner",)
    ordering = ("name", "pk")
    list_per_page = 20

    readonly_fields = ("id", "slug", "first_day_total")
    inlines = (BookingInline,)
    view_on_site = True

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("owner")
            .annotate(
                active_bookings=Count(
                    "bookings",
                    filter=Q(
                        bookings__status=Booking.Status.ACTIVE,
                    ),
                ),
            )
        )

    @admin.display(
        description="Активных бронирований",
        ordering="active_bookings",
    )
    def active_bookings_count(self, obj):
        return obj.active_bookings
