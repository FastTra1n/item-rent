import pytest

from models.users import User, add_user, find_user


def test_user_creation():
    user = User(id=1, name="Иван", phone="+7 (999) 123-45-67", rating=4.5)
    assert user.id == 1
    assert user.name == "Иван"
    assert user.phone == "+7 (999) 123-45-67"
    assert user.rating == 4.5


def test_user_creation_default_rating():
    user = User(id=2, name="Анна", phone="+7 (000) 000-00-00")
    assert user.rating == 0.0


def test_user_str_representation():
    user = User(id=1, name="Иван", phone="+7 (999) 123-45-67", rating=4.5)
    assert str(user) == "Иван (+7 (999) 123-45-67) | Рейтинг: 4.5"


def test_user_from_data_valid():
    data = {"id": 1, "name": "Иван", "phone": "+7 (999) 123-45-67", "rating": 5.0}
    user = User.from_data(data)
    assert user.id == 1
    assert user.name == "Иван"


def test_user_from_data_invalid_missing_keys():
    data = {"id": 1, "name": "Иван", "phone": "+7 (999) 123-45-67"}
    with pytest.raises(ValueError, match="Неверная структура пользователя"):
        User.from_data(data)


def test_user_from_data_invalid_wrong_keys():
    data = {"id": 1, "name": "Иван", "email": "test@test.com", "age": 25}
    with pytest.raises(ValueError):
        User.from_data(data)


def test_add_user():
    users = []
    user = add_user(users, "Иван", "+79991234567", 5.0)
    assert len(users) == 1
    assert user.id == 1

    user2 = add_user(users, "Анна", "+79990000000")
    assert len(users) == 2
    assert user2.id == 2
    assert user2.rating == 0.0


def test_find_user_existing():
    users = [User(1, "Иван", "123", 5.0), User(2, "Анна", "456", 4.0)]
    found = find_user(users, 2)
    assert found is not None
    assert found.name == "Анна"


def test_find_user_not_existing():
    users = [User(1, "Иван", "123", 5.0)]
    found = find_user(users, 99)
    assert found is None
