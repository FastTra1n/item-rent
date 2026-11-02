from django.db import models


class User(models.Model):
    name = models.CharField("Имя пользователя", max_length=100)
    phone = models.CharField("Контактный номер", max_length=25)
    rating = models.FloatField("Рейтинг", default=0.0)

    def __str__(self):
        return f"{self.name} ({self.phone}) | Рейтинг: {self.rating}"

    class Meta:
        ordering = ["name", "pk"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
