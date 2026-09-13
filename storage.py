import json


def load_items(filename: str) -> dict[int, dict]:
    """Загрузить вещи из JSON-файла в общий словарь."""
    try:
        with open(filename, mode="r", encoding="utf-8") as f:
            data = json.load(f)
            return {item["id"]: item for item in data}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_items(filename: str, items: dict[int, dict]) -> None:
    """Сохранить словарь вещей в JSON-файл."""
    with open(filename, mode="w", encoding="utf-8") as f:
        json.dumps(list(items.values()), f)


def load_bookings(filename: str) -> list[dict]:
    """Загрузить бронирования из JSON-файла."""
    try:
        with open(filename, mode="r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_bookings(filename: str, bookings: list[dict]) -> None:
    """Сохранить словарь бронирований в JSON-файл."""
    with open(filename, mode="w", encoding="utf-8") as f:
        json.dump(bookings, f)
