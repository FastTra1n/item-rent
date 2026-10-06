from django.urls import path

from . import views

urlpatterns = [
    path('', views.bookings_list, name='bookings'),
    path('<int:booking_id>/', views.booking_detail, name='booking_detail')
]