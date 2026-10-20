import pytest

from models.items import Item, add_item, find_item, find_item_by_id
from models.users import User


@pytest.fixture
def owner():
    return User(1, "Иван", "+7 (999) 123-45-67", 5.0)


def test_item_creation(owner):
    item = Item(id=1, owner=owner, name="Перфоратор", price=500, deposit=5000)
    assert item.id == 1
    assert item.owner is owner
    assert item.name == "Перфоратор"
    assert item.price == 500
    assert item.deposit == 5000


def test_item_str_representation(owner):
    item = Item(id=10, owner=owner, name="Велосипед", price=1000, deposit=15000)
    assert str(item) == "[10] Велосипед"


def test_add_item(owner):
    items = []
    item = add_item(items, owner, "Палатка", 300, 3000)
    assert len(items) == 1
    assert item.id == 1
    assert item.name == "Палатка"

    item2 = add_item(items, owner, "Рюкзак", 100, 1000)
    assert len(items) == 2
    assert item2.id == 2


def test_find_item_by_substring(owner):
    items = [
        Item(1, owner, "Горный велосипед", 500, 5000),
        Item(2, owner, "Городской Велосипед", 400, 4000),
        Item(3, owner, "Палатка", 300, 3000),
    ]
    found = find_item(items, "велосипед")
    assert len(found) == 2
    assert found[0].id == 1
    assert found[1].id == 2


def test_find_item_no_match(owner):
    items = [Item(1, owner, "Палатка", 300, 3000)]
    found = find_item(items, "Каяк")
    assert len(found) == 0


def test_find_item_by_id_existing(owner):
    items = [Item(1, owner, "Палатка", 300, 3000), Item(5, owner, "Мангал", 100, 500)]
    found = find_item_by_id(items, 5)
    assert found is not None
    assert found.name == "Мангал"


def test_find_item_by_id_not_found(owner):
    items = [Item(1, owner, "Палатка", 300, 3000)]
    found = find_item_by_id(items, 99)
    assert found is None
