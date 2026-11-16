from django.urls import path

from . import views

app_name = "bookings"

urlpatterns = [
    path("", views.bookings_list, name="bookings"),
    path("<int:booking_id>/", views.booking_detail, name="detail"),
    path("create/", views.booking_create, name="booking_create"),
    path("<int:booking_id>/edit/", views.booking_update, name="booking_update"),
    path("<int:booking_id>/cancel/", views.booking_cancel, name="booking_cancel"),
    path("statistics/", views.statistics, name="statistics"),
]
