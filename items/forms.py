from django import forms

from .models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item

        fields = [
            "name",
            "price",
            "deposit",
            "owner",
            "image",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control"},
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                },
            ),
            "deposit": forms.NumberInput(
                attrs={"class": "form-control"},
            ),
            "owner": forms.Select(
                attrs={"class": "form-select"},
            ),
            "image": forms.ClearableFileInput(
                attrs={"class": "form-control"},
            ),
        }
