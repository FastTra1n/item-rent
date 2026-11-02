from django.core.exceptions import ValidationError
from django.db import models

from items.models import Item
from users.models import User


class Booking(models.Model):
    item = models.ForeignKey(
        Item, on_delete=models.PROTECT, related_name="bookings", verbose_name="Вещь"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="bookings",
        verbose_name="Арендатор",
    )
    start_date = models.DateField("Дата начала аренды")
    end_date = models.DateField("Дата окончания аренды")
    is_cancelled = models.BooleanField("Бронирование отменено", default=False)

    def clean(self):
        super().clean()
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError({"end_date": "Окончание раньше начала аренды."})

    def cancel(self):
        self.is_cancelled = True
        self.save(update_fields=["is_cancelled"])

    def __str__(self):
        status = "Отменено" if self.is_cancelled else "Активно"
        return (
            f"Аренда #{self.pk}: {self.item.name} | "
            f"{self.start_date} - {self.end_date} | {self.user.name} [{status}]"
        )

    class Meta:
        ordering = ["start_date", "pk"]
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
