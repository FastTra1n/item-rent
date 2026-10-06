from django.http import HttpResponse
from django.shortcuts import render

def page(title, content):
    bootstrap = 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css'
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link href="{bootstrap}" rel="stylesheet">
</head>
<body>
  <nav class="nav container">
    <a href="/" class="nav-link">Главная</a>
    <a href="/items/" class="nav-link">Каталог вещей</a>
    <a href="/bookings/" class="nav-link">Бронирования</a>
  </nav>
  <main class="container">{content}</main>  
</body>
</html>"""

def index(request):
    content = """ 
    <h1 class="display-4">Rently</h1> 
    <p class="lead">Система бронирования вещей.</p> 
    <p>Основные разделы:</p> 
    <a href="/items/" class="btn btn-primary me-2">Вещи</a>
    <a href="/bookings/" class="btn btn-secondary">Бронирования</a> 
    """
    return HttpResponse(page("Главная", content))