from datetime import date

from models.items import Item
from models.users import User


class Booking:
    """Бронирование (аренда) вещи."""

    def __init__(
        self, id: int, item: Item, start_date: date, end_date: date, user: User
    ) -> None:
        self.id = id
        self.item = item
        self.start_date = start_date
        self.end_date = end_date
        self.user = user
        self.is_cancelled = False

    def cancel(self) -> None:
        """Отменить бронирование."""
        self.is_cancelled = True

    def __str__(self) -> str:
        status = "Отменено" if self.is_cancelled else "Активно"
        return f"Аренда #{self.id}: {self.item.name} | {self.start_date} - {self.end_date} | {self.user.name} [{status}]"


def is_item_available(
    bookings: list[Booking], item_id: int, start_date: date, end_date: date
) -> bool:
    """Проверить, доступна ли конкретная вещь для бронивания на указанную дату."""
    for booking in bookings:
        if booking.item.id == item_id:
            book_start = booking.start_date
            book_end = booking.end_date

            if (
                start_date <= book_end
                and end_date >= book_start
                and not booking.is_cancelled
            ):
                return False
    return True


def create_booking(
    bookings: list[Booking], item: Item, user: User, start_date: date, end_date: date
) -> Booking | None:
    """Создать новое бронирование."""
    if not is_item_available(bookings, item.id, start_date, end_date):
        return None

    next_id = max([b.id for b in bookings], default=0) + 1
    booking = Booking(next_id, item, start_date, end_date, user)
    bookings.append(booking)
    return booking


def cancel_booking(bookings: list[Booking], booking_id: int) -> bool:
    """Отменить бронирование."""
    for booking in bookings:
        if booking.id == booking_id and not booking.is_cancelled:
            booking.cancel()
            return True
    return False


def get_booking_status(is_available: bool) -> str:
    """Вернуть текстовый статус вещи."""
    if is_available:
        return "Вещь доступна для бронирования на выбранные даты."
    return "Вещь уже забронирована на этот период."
