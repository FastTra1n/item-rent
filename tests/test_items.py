from items import add_item, find_item


def test_add_item():
    items = {}
    add_item(items, "Перфоратор", 500, 3500)
    assert len(items) == 1
    assert items[1]["name"] == "Перфоратор"


def test_find_item():
    items = {}
    add_item(items, "Перфоратор", 500, 3500)
    add_item(items, "Дрель", 300, 5000)
    results = find_item(items, "перф")
    assert len(results) == 1
    assert results[1]["name"] == "Перфоратор"
