from datetime import date, datetime


def is_item_available(
    bookings: list[dict], item_id: int, start_date: date, end_date: date
) -> bool:
    """Проверить, доступна ли конкретная вещь для бронивания на указанную дату."""
    for booking in bookings:
        if booking["item_id"] == item_id:
            book_start = datetime.strptime(
                booking["start_booking_date"], "%Y-%m-%d"
            ).astimezone().date()
            book_end = datetime.strptime(booking["end_booking_date"], "%Y-%m-%d").astimezone().date()

            if start_date <= book_end and end_date >= book_start:
                return False
    return True


def create_booking(
    bookings: list[dict], item_id: int, start_date: date, end_date: date
) -> None:
    """Создать новое бронирование."""
    new_id = max((booking["id"] for booking in bookings), default=0) + 1
    bookings.append(
        {
            "id": new_id,
            "item_id": item_id,
            "start_booking_date": start_date.strftime("%Y-%m-%d"),
            "end_booking_date": end_date.strftime("%Y-%m-%d"),
        }
    )


def cancel_booking(bookings: list[dict], booking_id: int) -> bool:
    """Отменить бронирование."""
    for i, booking in enumerate(bookings):
        if booking["id"] == booking_id:
            del bookings[i]
            return True
    return False


def get_booking_status(is_available: bool) -> str:
    """Вернуть текстовый статус вещи."""
    if is_available:
        return "Вещь доступна для бронирования на выбранные даты."
    return "Вещь уже забронирована на этот период."
