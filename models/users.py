from typing import Self


class User:
    """Пользователь системы аренды."""

    def __init__(self, id: int, name: str, phone: str, rating: float = 0.0) -> None:
        self.id = id
        self.name = name
        self.phone = phone
        self.rating = rating

    @classmethod
    def from_data(cls, data: dict) -> Self:
        """Создать пользователя из набора данных."""
        if (
            not {"id", "name", "phone", "rating"}.issubset(data)
            or len(data.keys()) != 4
        ):
            raise ValueError(
                "Неверная структура пользователя. Убедитесь, что переданный объект содержит исключительно: id, имя, телефон и рейтинг."
            )
        return cls(**data)

    def __str__(self) -> str:
        return f"{self.name} ({self.phone}) | Рейтинг: {self.rating}"


def find_user(users: list[User], user_id: int) -> User | None:
    for user in users:
        if user.id == user_id:
            return user
    return None


def add_user(users: list[User], name: str, phone: str, rating: float = 0.0) -> None:
    """Добавляет нового пользователя в общий список users."""
    next_id = max([u.id for u in users], default=0) + 1
    new_user = User(id=next_id, name=name, phone=phone, rating=rating)
    users.append(new_user)
    return new_user


def show_users(users: list[User]) -> None:
    """Вывести список пользователей."""
    print("  ID  |" + "   Имя пользователя   " + "|   Номер телефона   | Рейтинг")
    for user in users:
        print(f"{user.id:<5} | {user.name:<20} | {user.phone:<18} | {user.rating:<5}")
