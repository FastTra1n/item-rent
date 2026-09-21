import re

from models.bookings import *
from models.items import *
from models.users import *
from storage import (
    load_bookings,
    load_items,
    load_users,
    save_bookings,
    save_items,
    save_users,
)
from utils import input_date, input_int

ITEMS_FILEPATH = "data/items.json"
BOOKINGS_FILEPATH = "data/bookings.json"
USERS_FILEPATH = "data/users.json"


def display_menu() -> None:
    """Отобразить меню выбора опций системы бронирования вещей."""
    print("=== Система бронирования вещей ===")
    print("1. Показать все вещи")
    print("2. Добавить вещь")
    print("3. Найти вещь по названию")
    print("4. Проверить доступность вещи на даты")
    print("5. Забронировать вещь")
    print("6. Отменить бронирование вещи")
    print("7. Показать всех пользователей")
    print("8. Добавить пользователя")
    print("9. Найти пользователя по ID")
    print("0. Выход")


def main():
    users = load_users(USERS_FILEPATH)
    items = load_items(ITEMS_FILEPATH, users)
    bookings = load_bookings(BOOKINGS_FILEPATH, items, users)

    while True:
        display_menu()

        user_choice = input_int("Введите номер опции: ")
        if user_choice == 1:
            show_items(items)

        elif user_choice == 2:
            item_name = input("Введите название вещи: ").strip()
            if not item_name:
                print("Название вещи не должно быть пустым.")
                continue

            item_price = input("Укажите стоимость аренды вещи (в руб/д): ").strip()
            try:
                item_price = int(item_price)
            except ValueError:
                print("Необходимо указать корректную стоимость аренды вещи.")
                continue

            item_deposit = input(
                "Укажите стоимость вещи (депозитная стоимость): "
            ).strip()
            try:
                item_deposit = int(item_deposit)
            except ValueError:
                print("Необходимо указать корректную стоимость вещи.")
                continue

            item_owner_id = input_int("Укажите ID владельца вещи: ")
            item_owner = find_user(users, item_owner_id)
            if item_owner is None:
                print(
                    "Пользователь с указанным идентификатором не найден. Убедитесь, что пользователь с указанным id существует."
                )
                continue
            add_item(items, item_owner, item_name, item_price, item_deposit)
            save_items(ITEMS_FILEPATH, items)
            print("Вещь успешно добавлена в общий список.")

        elif user_choice == 3:
            query = input("Введите название вещи для поиска: ")
            found = find_item(items, query)
            show_items(found)

        elif user_choice == 4:
            item_id = input_int("Введите ID вещи: ")
            selected_item = None
            for item in items:
                if item.id == item_id:
                    selected_item = item
                    break
            else:
                print(
                    "Вещи с указанным ID не нашлось. Проверьте корректность введённого ID."
                )
                continue
            print("Нашли вещь с указанным идентификатором -", selected_item.name)
            start_booking = input_date("Укажите дату начала аренды: ")
            end_booking = input_date("Укажите дату окончания аренды: ")

            if start_booking > end_booking:
                print("Дата окончания не может быть раньше даты начала.")
                continue

            available = is_item_available(bookings, item_id, start_booking, end_booking)
            print(get_booking_status(available))

        elif user_choice == 5:
            item_id = input_int("Введите ID вещи: ")
            selected_item = None
            for item in items:
                if item.id == item_id:
                    selected_item = item
                    break
            else:
                print(
                    "Вещи с указанным ID не нашлось. Проверьте корректность введённого ID."
                )
                continue
            print("Нашли вещь с указанным идентификатором -", selected_item.name)

            user_id = input_int("Укажите ID пользователя-арендатора: ")
            selected_user = None
            for user in users:
                if user.id == user_id:
                    selected_user = user
                    break
            else:
                print(
                    "Не нашли пользователя с указанным ID. Проверьте корректность введённого ID."
                )
                continue
            print(
                "Нашли пользователя с указанным идентификатором -", selected_user.name
            )

            start_booking = input_date("Укажите дату начала аренды: ")
            end_booking = input_date("Укажите дату окончания аренды: ")

            if start_booking > end_booking:
                print("Дата окончания не может быть раньше даты начала.")
                continue

            if is_item_available(bookings, item_id, start_booking, end_booking):
                create_booking(
                    bookings, selected_item, selected_user, start_booking, end_booking
                )
                save_bookings(BOOKINGS_FILEPATH, bookings)

                days = (end_booking - start_booking).days
                days = 1 if days == 0 else days
                total_price = item.price * days

                print(
                    f"Успешно забронировано! К оплате: {total_price} руб. + Залог: {item.deposit} руб."
                )
            else:
                print("Вещь уже занята в указанные даты.")

        elif user_choice == 6:
            booking_id = input_int("Введите ID бронирования для отмены: ")

            if cancel_booking(bookings, booking_id):
                save_bookings(BOOKINGS_FILEPATH, bookings)
                print("Бронирование успешно отменено.")
            else:
                print("Бронирование с указанным ID не нашлось.")

        elif user_choice == 7:
            show_users(users)

        elif user_choice == 8:
            user_name = input("Введите имя пользователя: ").strip()
            if not user_name:
                print("Имя пользователя не может быть пустым.")
                continue

            phone_raw = input("Введите номер телефона: ").strip()
            if not phone_raw:
                print("Необходимо указать контактный номер телефона для связи.")
                continue
            chars_to_remove = [" ", "+", "-", "(", ")"]
            table_clear = phone_raw.maketrans("", "", "".join(chars_to_remove))
            phone_cleared = phone_raw.translate(table_clear)
            regexp = r"(\d)(\d{3})(\d{3})(\d{2})(\d{2})"
            user_phone = re.sub(regexp, r"+\1 (\2) \3-\4-\5", phone_cleared)

            user_rating = input(
                "Укажите рейтинг пользователя (по умолчанию 0.0): "
            ).strip()
            if not user_rating:
                user_rating = 0.0
            else:
                try:
                    user_rating = float(user_rating)
                except ValueError:
                    print("Необходимо указать корректный рейтинг.")
                    continue

            add_user(users, user_name, user_phone, user_rating)
            save_users(USERS_FILEPATH, users)
            print("Пользователь успешно добавлен в общий список.")

        elif user_choice == 9:
            user_id = input_int("Введите ID пользователя для поиска: ")
            found = find_user(users, user_id)
            print("Информация о найденном пользователе:")
            print("Имя пользователя:", found.name)
            print("Номер телефона:", found.phone)
            print("Рейтинг:", found.rating)

        elif user_choice == 0:
            print("Завершение работы програмы...")
            break

        else:
            print("Некорректный ввод.")


if __name__ == "__main__":
    main()
