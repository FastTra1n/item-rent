from django import forms
from django.utils import timezone

from items.models import Item
from users.models import User

from .models import Booking


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


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking

        fields = [
            "item",
            "user",
            "start_date",
            "end_date",
        ]

        labels = {
            "item": "Вещь",
            "user": "Арендатор",
            "start_date": "Начало аренды",
            "end_date": "Окончание аренды",
        }

        help_texts = {
            "start_date": "Сегодняшняя или будущая дата.",
            "end_date": "Последний день аренды включается в период.",
        }

        widgets = {
            "item": forms.Select(
                attrs={"class": "form-select"},
            ),
            "user": forms.Select(
                attrs={"class": "form-select"},
            ),
            "start_date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                    "class": "form-control",
                },
            ),
            "end_date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                    "class": "form-control",
                },
            ),
        }

    def clean_start_date(self):
        start_date = self.cleaned_data["start_date"], "%Y-%m-%d"

        if start_date < timezone.localdate():
            raise forms.ValidationError("Нельзя начать аренду в прошлом.")

        return start_date
