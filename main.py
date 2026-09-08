from datetime import UTC, date, datetime

# Вещь для бронирования
item_name: str = "Снегоуборочная лопата"
price: int = 500
deposit: int = 3500
is_available: bool = True

# Даты бронирования
start_date: date = date(2026, 9, 9)
end_date: date = date(2026, 9, 10)


def calculate_rental_price(days: int, price_per_day: int) -> int:
    return days * price_per_day


def check_item_availability(start: date, end: date, is_free: bool) -> str:
    now = datetime.now(UTC).date()

    if not is_free:
        return "Вещь уже забронирована другим пользователем."
    elif start < now:
        return "Дата начала аренды не может быть в прошлом."
    elif end <= start:
        return "Дата окончания аренды должна быть позже даты начала аренды."
    else:
        days = (end - start).days
        total_price = calculate_rental_price(days, price)
        return f"Вещь успешно забронирована на {days} дней. Итоговая стоимость: {total_price} руб."


print(f"Предмет: {item_name}")
print(f"Стоимость: {price} руб./день")
print(f"Залоговая стоимость: {deposit} руб.")
print(f"Период: с {start_date.strftime('%Y.%m.%d')} по {end_date.strftime('%Y.%m.%d')}")
print(check_item_availability(start_date, end_date, is_available))
