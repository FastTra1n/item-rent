import json
from datetime import datetime

from models.bookings import Booking
from models.items import Item, find_item_by_id
from models.users import User, find_user


def load_items(filename: str, users: list[User]) -> list[Item]:
    """Загрузить вещи из JSON-файла в общий список."""
    items = []
    try:
        with open(filename, mode="r", encoding="utf-8") as f:
            data = json.load(f)
            for d in data:
                owner = find_user(users, d["owner_id"])
                if owner:
                    item = Item(
                        id=d["id"],
                        owner=owner,
                        name=d["name"],
                        price=d["price"],
                        deposit=d["deposit"],
                    )
                    items.append(item)
            return items
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_items(filename: str, items: list[Item]) -> None:
    """Сохранить список вещей в JSON-файл."""
    data = [
        {
            "id": i.id,
            "owner_id": i.owner.id,
            "name": i.name,
            "price": i.price,
            "deposit": i.deposit,
        }
        for i in items
    ]
    with open(filename, mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_users(filepath: str) -> list[User]:
    """Загрузить пользователей из JSON-файла в общий список."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [User.from_data(d) for d in data]
    except FileNotFoundError:
        return []


def save_users(filename: str, users: list[User]) -> None:
    """Сохранить список пользователей в JSON-файл."""
    data = [
        {"id": u.id, "name": u.name, "phone": u.phone, "rating": u.rating}
        for u in users
    ]
    with open(filename, mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_bookings(filename: str, items: list[Item], users: list[User]) -> list[Booking]:
    """Загрузить бронирования из JSON-файла."""
    bookings = []
    try:
        with open(filename, mode="r", encoding="utf-8") as f:
            data = json.load(f)
            for d in data:
                item = find_item_by_id(items, d["item_id"])
                user = find_user(users, d["user_id"])
                if item and user:
                    booking = Booking(
                        id=d["id"],
                        item=item,
                        start_date=datetime.strptime(d["start_date"], "%Y-%m-%d")
                        .astimezone()
                        .date(),
                        end_date=datetime.strptime(d["end_date"], "%Y-%m-%d")
                        .astimezone()
                        .date(),
                        user=user,
                    )
                    booking.is_cancelled = d.get("is_cancelled", False)
                    bookings.append(booking)
        return bookings
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_bookings(filename: str, bookings: list[Booking]) -> None:
    """Сохранить словарь бронирований в JSON-файл."""
    data = [
        {
            "id": b.id,
            "item_id": b.item.id,
            "start_date": b.start_date,
            "end_date": b.end_date,
            "user_id": b.user.id,
            "is_cancelled": b.is_cancelled,
        }
        for b in bookings
    ]
    with open(filename, mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False, default=str)
