from models.users import User


class Item:
    """Вещь, доступная для аренды."""

    def __init__(
        self, id: int, owner: User, name: str, price: int, deposit: int
    ) -> None:
        self.id = id
        self.owner = owner
        self.name = name
        self.price = price
        self.deposit = deposit

    def __str__(self) -> str:
        return f"[{self.id}] {self.name}"


def add_item(
    items: list[Item], owner: User, name: str, price: int, deposit: int
) -> None:
    """Добавляет новую вещь в общий список items."""
    next_id = max([i.id for i in items], default=0) + 1
    new_item = Item(id=next_id, owner=owner, name=name, price=price, deposit=deposit)
    items.append(new_item)
    return new_item


def find_item(items: list[Item], query: str) -> list[Item]:
    """Найти конкретную вещь по подстроке в названии."""
    suitable_items = []
    for item in items:
        if query.lower() in item.name.lower():
            suitable_items.append(item)
    return suitable_items


def find_item_by_id(items: list[Item], item_id: int) -> Item | None:
    for item in items:
        if item.id == item_id:
            return item
    return None


def show_items(items: list[Item]) -> None:
    """Вывести список вещей."""
    print(
        "  ID  |"
        + " " * 19
        + "Название вещи"
        + " " * 20
        + "| Цена аренды (руб/сутки) |"
        + " " * 5
        + "Депозит"
        + " " * 5
        + "| Владелец вещи"
    )
    for item in items:
        print(
            f"{item.id:<5} | {item.name:<50} | {item.price:<23} | {item.deposit:<15} | {item.owner.name}"
        )
