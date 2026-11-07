from django.urls import path

from . import views

app_name = "items"

urlpatterns = [
    path("", views.items_list, name="list"),
    path("available/", views.available_items, name="available"),
    path("<int:item_id>/", views.item_detail, name="detail"),
]
