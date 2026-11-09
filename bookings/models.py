from django.core.exceptions import ValidationError
from django.db import models

from items.models import Item
from users.models import User


class BookingQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=self.model.Status.ACTIVE)

    def cancelled(self):
        return self.filter(status=self.model.Status.CANCELLED)

    def completed(self):
        return self.filter(status=self.model.Status.COMPLETED)

    def for_date(self, selected_date):
        return self.filter(
            start_date__lte=selected_date,
            end_date__gte=selected_date,
        )


class BookingManager(
    models.Manager.from_queryset(BookingQuerySet)
):
    pass

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

    class Status(models.TextChoices):
        ACTIVE = "active", "Активно"
        CANCELLED = "cancelled", "Отменено"
        COMPLETED = "completed", "Завершено"

    status = models.CharField(
        "Статус бронирования",
        max_length=12,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    objects = BookingManager()

    def clean(self):
        super().clean()
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError({"end_date": "Окончание раньше начала аренды."})

    def cancel(self):
        self.status = self.Status.CANCELLED
        self.save(update_fields=["status"])

    def __str__(self):
        return (
            f"Аренда #{self.pk}: {self.item.name} | "
            f"{self.start_date} - {self.end_date} | "
            f"{self.user.name} [{self.get_status_display()}]"
        )

    class Meta:
        ordering = ["start_date", "pk"]
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
