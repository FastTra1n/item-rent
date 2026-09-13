def add_item(items: dict[int, dict], name: str, price: int, deposit: int) -> None:
    """Добавляет новую вещь в общий словарь items."""
    next_id = max(items.keys(), default=0) + 1
    items[next_id] = {"id": next_id, "name": name, "price": price, "deposit": deposit}


def find_item(items: dict[int, dict], query: str) -> dict[int, dict]:
    """Найти конкретную вещь по подстроке в названии."""
    query = query.lower()
    return {id: item for id, item in items.items() if query in item["name"].lower()}
