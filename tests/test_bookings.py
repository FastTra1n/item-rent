from datetime import date

from bookings import cancel_booking, create_booking, is_item_available


def test_is_item_available_empty():
    bookings = []
    start = date(2026, 9, 15)
    end = date(2026, 9, 20)
    assert is_item_available(bookings, 1, start, end) is True


def test_create_booking():
    bookings = []
    create_booking(bookings, 1, date(2026, 9, 15), date(2026, 9, 20))

    assert len(bookings) == 1
    assert bookings[0]["item_id"] == 1
    assert bookings[0]["start_booking_date"] == "2026-09-15"
    assert bookings[0]["end_booking_date"] == "2026-09-20"


def test_booking_overlap_forbidden():
    bookings = []
    create_booking(bookings, 1, date(2026, 9, 15), date(2026, 9, 20))

    assert not is_item_available(bookings, 1, date(2026, 9, 16), date(2026, 9, 18))
    assert not is_item_available(bookings, 1, date(2026, 9, 10), date(2026, 9, 16))
    assert not is_item_available(bookings, 1, date(2026, 9, 19), date(2026, 9, 25))


def test_booking_no_overlap_allowed():
    bookings = []
    create_booking(bookings, 1, date(2026, 9, 15), date(2026, 9, 20))

    assert is_item_available(bookings, 1, date(2026, 9, 1), date(2026, 9, 10))
    assert is_item_available(bookings, 1, date(2026, 9, 25), date(2026, 9, 30))


def test_cancel_booking():
    bookings = [
        {
            "id": 1,
            "item_id": 1,
            "start_booking_date": "2026-09-15",
            "end_booking_date": "2026-09-20",
        }
    ]

    assert cancel_booking(bookings, 999) is False
    assert len(bookings) == 1

    assert cancel_booking(bookings, 1) is True
    assert len(bookings) == 0
