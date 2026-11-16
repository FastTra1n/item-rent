from django import forms

from items.models import Item
from users.models import User


class BookingFilterForm(forms.Form):
    date = forms.DateField(
        required=False,
        label="Дата аренды",
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={
                "type": "date",
                "class": "form-control",
            },
        ),
    )

    item = forms.ModelChoiceField(
        queryset=Item.objects.order_by("name", "pk"),
        required=False,
        label="Вещь",
        empty_label="Все вещи",
        widget=forms.Select(
            attrs={"class": "form-select"},
        ),
    )

    user = forms.ModelChoiceField(
        queryset=User.objects.order_by("name", "pk"),
        required=False,
        label="Арендатор",
        empty_label="Все арендаторы",
        widget=forms.Select(
            attrs={"class": "form-select"},
        ),
    )

    sort = forms.ChoiceField(
        required=False,
        label="Сортировка",
        choices=[
            ("date", "По дате начала"),
            ("date_desc", "По дате начала: сначала новые"),
            ("item", "По вещи"),
            ("user", "По арендатору"),
        ],
        widget=forms.Select(
            attrs={"class": "form-select"},
        ),
    )
