from django.http import HttpResponse
from django.shortcuts import render

from homepage.views import page
from models.bookings import find_booking_by_id
from storage import load_bookings, load_items, load_users

def bookings_list(request):
    users_list = load_users("data/users.json")
    items_list = load_items("data/items.json", users_list)
    bookings_list = load_bookings('data/bookings.json', items_list, users_list)

    items = ''
    for booking in bookings_list:
        status = "отменено" if booking.is_cancelled else "активно"
        badge = "bg-secondary" if booking.is_cancelled else "bg-success"
        
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
          <a href="/bookings/{booking.id}/">{booking.item.name} | {booking.start_date} - {booking.end_date}</a>
          <span class="badge {badge}">{status}</span>
        </li>
        """
        
    content = f"<h1>Бронирования</h1><ul class='list-group'>{items}</ul>"
    return HttpResponse(page("Бронирования", content))

def booking_detail(request, booking_id):
    users_list = load_users("data/users.json")
    items_list = load_items("data/items.json", users_list)
    bookings_list = load_bookings('data/bookings.json', items_list, users_list)

    booking = find_booking_by_id(bookings_list, booking_id)

    if booking is None:
        return HttpResponse(page("Бронирование не найдено", "<h1 class='text-danger'>Бронирование не найдено</h1>"), status=404)
        
    status = "отменено" if booking.is_cancelled else "активно"
    badge = "bg-secondary" if booking.is_cancelled else "bg-success"

    content = f"""
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">Бронирование №{booking.id}</h5>
        <p class="card-text">Забронированная вещь: {booking.item.name}</p>
        <p class="card-text">Дата начала бронирования: {booking.start_date}</p>
        <p class="card-text">Дата окончания бронирования: {booking.end_date}</p>
        <p class="card-text">Арендатор: {booking.user.name}</p>
        <p class="card-text">Статус: <span class="badge {badge}">{status}</span></p>
        <a href="/bookings/" class="btn btn-outline-secondary">← к списку</a>
      </div>
    </div>
    """
    return HttpResponse(page(f"Бронирование №{booking.id}", content), status=200)