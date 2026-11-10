from django.contrib import admin

from bookings.models import Booking

from .models import User


class UserBookingInline(admin.TabularInline):
    model = Booking
    fk_name = "user"
    fields = ("item", "start_date", "end_date", "status")
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "rating")
    list_display_links = ("name",)
    search_fields = ("name", "phone")
    ordering = ("name", "pk")
    list_per_page = 20
    readonly_fields = ("id",)
    inlines = (UserBookingInline,)
