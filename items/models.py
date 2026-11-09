from django.db import models, transaction
from django.db.models import F
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode

from users.models import User


class Item(models.Model):
    name = models.CharField("Название вещи", max_length=100)
    price = models.DecimalField("Цена аренды", max_digits=10, decimal_places=2, help_text="Стоимость одного дня аренды в рублях.",)
    deposit = models.PositiveIntegerField("Залог", default=0)
    owner = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="items", verbose_name="Владелец"
    )
    first_day_total = models.GeneratedField(
        expression=F("price") + F("deposit"),
        output_field=models.DecimalField(
            max_digits=12,
            decimal_places=2,
        ),
        db_persist=True,
        verbose_name="Один день аренды и залог",
    )
    slug = models.SlugField(
        "URL-идентификатор",
        max_length=180,
        blank=True,
        editable=False,
        unique=True
    )

    def save(self, *args, **kwargs):
        if self.slug:
            return super().save(*args, **kwargs)

        with transaction.atomic():
            super().save(*args, **kwargs)

            base_slug = slugify(unidecode(self.name))[:150] or "item"
            self.slug = f"{base_slug}-{self.pk}"

            super().save(update_fields=["slug"])


    def get_absolute_url(self):
        return reverse(
            "items:detail",
            kwargs={"slug": self.slug},
        )

    def __str__(self):
        return f"[{self.pk}] {self.name}"

    class Meta:
        ordering = ["name", "pk"]
        verbose_name = "Вещь"
        verbose_name_plural = "Вещи"
