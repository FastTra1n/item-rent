from django.db import models

from users.models import User


class Item(models.Model):
    name = models.CharField("Название вещи", max_length=100)
    price = models.DecimalField("Цена аренды", max_digits=10, decimal_places=2)
    deposit = models.PositiveIntegerField("Залог", default=0)
    owner = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="items", verbose_name="Владелец"
    )

    def __str__(self):
        return f"[{self.pk}] {self.name}"

    class Meta:
        ordering = ["name", "pk"]
        verbose_name = "Вещь"
        verbose_name_plural = "Вещи"
