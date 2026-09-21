import pytest
from datetime import date
from models.users import User
from models.items import Item
from models.bookings import Booking, is_item_available, create_booking, cancel_booking, get_booking_status

@pytest.fixture
def owner():
    return User(1, "Владелец", "+7 (111) 111-11-11", 5.0)

@pytest.fixture
def client():
    return User(2, "Арендатор", "+7 (222) 222-22-22", 4.8)

@pytest.fixture
def item(owner):
    return Item(1, owner, "Сапборд", 1000, 10000)

@pytest.fixture
def active_booking(item, client):
    return Booking(1, item, date(2026, 9, 10), date(2026, 9, 15), client)

def test_booking_creation_and_str(item, client):
    booking = Booking(1, item, date(2026, 9, 1), date(2026, 9, 5), client)
    assert booking.id == 1
    assert booking.is_cancelled is False
    expected_str = "Аренда #1: Сапборд | 2026-09-01 - 2026-09-05 | Арендатор [Активно]"
    assert str(booking) == expected_str

def test_booking_cancel_changes_status(active_booking):
    active_booking.cancel()
    assert active_booking.is_cancelled is True
    assert "[Отменено]" in str(active_booking)

def test_is_item_available_no_bookings(item):
    bookings = []
    assert is_item_available(bookings, item.id, date(2026, 9, 10), date(2026, 9, 15)) is True

def test_is_item_available_no_overlap(item, active_booking):
    bookings = [active_booking]
    assert is_item_available(bookings, item.id, date(2026, 9, 1), date(2026, 9, 9)) is True
    assert is_item_available(bookings, item.id, date(2026, 9, 16), date(2026, 9, 20)) is True

def test_is_item_available_with_overlap(item, active_booking):
    bookings = [active_booking]
    assert is_item_available(bookings, item.id, date(2026, 9, 9), date(2026, 9, 11)) is False
    assert is_item_available(bookings, item.id, date(2026, 9, 14), date(2026, 9, 16)) is False
    assert is_item_available(bookings, item.id, date(2026, 9, 11), date(2026, 9, 12)) is False
    assert is_item_available(bookings, item.id, date(2026, 9, 9), date(2026, 9, 16)) is False

def test_is_item_available_ignores_cancelled(item, active_booking):
    active_booking.cancel()
    bookings = [active_booking]
    assert is_item_available(bookings, item.id, date(2026, 9, 10), date(2026, 9, 15)) is True

def test_create_booking_success(item, client):
    bookings = []
    booking = create_booking(bookings, item, client, date(2026, 10, 1), date(2026, 10, 5))
    assert booking is not None
    assert booking.id == 1
    assert len(bookings) == 1
    assert bookings[0] is booking

def test_create_booking_fails_when_unavailable(item, client, active_booking):
    bookings = [active_booking]
    booking = create_booking(bookings, item, client, date(2026, 9, 10), date(2026, 9, 15))
    assert booking is None
    assert len(bookings) == 1

def test_cancel_booking_success(active_booking):
    bookings = [active_booking]
    result = cancel_booking(bookings, active_booking.id)
    assert result is True
    assert active_booking.is_cancelled is True

def test_cancel_booking_already_cancelled(active_booking):
    active_booking.cancel()
    bookings = [active_booking]
    result = cancel_booking(bookings, active_booking.id)
    assert result is False

def test_cancel_booking_not_found():
    bookings = []
    result = cancel_booking(bookings, 99)
    assert result is False

def test_get_booking_status():
    assert get_booking_status(True) == "Вещь доступна для бронирования на выбранные даты."
    assert get_booking_status(False) == "Вещь уже забронирована на этот период."