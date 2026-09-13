from bookings import (
    cancel_booking,
    create_booking,
    get_booking_status,
    is_item_available,
)
from items import find_item
from storage import load_bookings, load_items, save_bookings
from utils import input_date, input_int

ITEMS_FILEPATH = "data/items.json"
BOOKINGS_FILEPATH = "data/bookings.json"


def show_items(items: dict[int, dict]) -> None:
    """Вывести список вещей."""
    print(
        "  ID  |" + " " * 19 + "Название вещи" + " " * 20 + "| Цена аренды (руб/сутки)"
    )
    for item in items.values():
        print(f"{item['id']:<5} | {item['name']:<50} | {item['price']}")


def display_menu() -> None:
    """Отобразить меню выбора опций системы бронирования вещей."""
    print("=== Система бронирования вещей ===")
    print("1. Показать все вещи")
    print("2. Найти вещь по названию")
    print("3. Проверить доступность вещи на даты")
    print("4. Забронировать вещь")
    print("5. Отменить бронирование вещи")
    print("0. Выход")


def main():
    items = load_items(ITEMS_FILEPATH)
    bookings = load_bookings(BOOKINGS_FILEPATH)

    while True:
        display_menu()

        user_choice = input_int("Введите номер опции: ")
        if user_choice == 1:
            show_items(items)

        elif user_choice == 2:
            query = input("Введите название вещи для поиска: ")
            found = find_item(items, query)
            show_items(found)

        elif user_choice == 3:
            item_id = input_int("Введите ID вещи: ")
            if item_id not in items:
                print(
                    "Вещи с указанным ID не нашлось. Проверьте корректность введённого ID."
                )
                continue
            print("Нашли вещь с указанным идентификатором -", items[item_id]["name"])
            start_booking = input_date("Укажите дату начала аренды: ")
            end_booking = input_date("Укажите дату окончания аренды: ")

            if start_booking > end_booking:
                print("Дата окончания не может быть раньше даты начала.")
                continue

            available = is_item_available(bookings, item_id, start_booking, end_booking)
            print(get_booking_status(available))

        elif user_choice == 4:
            item_id = input_int("Введите ID вещи: ")
            if item_id not in items:
                print(
                    "Вещи с указанным ID не нашлось. Проверьте корректность введённого ID."
                )
                continue
            print("Нашли вещь с указанным идентификатором -", items[item_id]["name"])
            start_booking = input_date("Укажите дату начала аренды: ")
            end_booking = input_date("Укажите дату окончания аренды: ")

            if start_booking > end_booking:
                print("Дата окончания не может быть раньше даты начала.")
                continue

            if is_item_available(bookings, item_id, start_booking, end_booking):
                create_booking(bookings, item_id, start_booking, end_booking)
                save_bookings(BOOKINGS_FILEPATH, bookings)

                days = (end_booking - start_booking).days
                days = 1 if days == 0 else days
                total_price = items[item_id]["price"] * days

                print(
                    f"Успешно забронировано! К оплате: {total_price} руб. + Залог: {items[item_id]['deposit']} руб."
                )
            else:
                print("Вещь уже занята в указанные даты.")

        elif user_choice == 5:
            booking_id = input_int("Введите ID бронирования для отмены: ")

            if cancel_booking(bookings, booking_id):
                save_bookings(BOOKINGS_FILEPATH, bookings)
                print("Бронирование успешно отменено.")
            else:
                print("Бронирование с указанным ID не нашлось.")

        elif user_choice == 0:
            print("Завершение работы програмы...")
            break

        else:
            print("Некорректный ввод.")


if __name__ == "__main__":
    main()
