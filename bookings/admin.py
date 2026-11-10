from django.contrib import admin, messages

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "item",
        "item_price",
        "user",
        "start_date",
        "end_date",
        "status",
    )
    list_display_links = ("id",)
    search_fields = ("item__name", "user__name")
    list_filter = ("status", "start_date")
    ordering = ("-start_date", "-pk")
    list_per_page = 20
    readonly_fields = ("id",)

    list_select_related = ("item", "user")
    date_hierarchy = "start_date"
    autocomplete_fields = ("item", "user")
    actions = ("cancel_bookings", "restore_bookings")

    @admin.display(
        description="Цена аренды",
        ordering="item__price",
    )
    def item_price(self, obj):
        return obj.item.price

    @admin.action(description="Отменить выбранные бронирования")
    def cancel_bookings(self, request, queryset):
        count = 0

        for booking in queryset:
            booking.cancel()
            count += 1

        self.message_user(
            request,
            f"Отменено бронирований: {count}.",
            messages.SUCCESS,
        )

    @admin.action(description="Вернуть в активные")
    def restore_bookings(self, request, queryset):
        count = queryset.update(status=Booking.Status.ACTIVE)

        self.message_user(
            request,
            f"Возвращено бронирований: {count}.",
            messages.SUCCESS,
        )
