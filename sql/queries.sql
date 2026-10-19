-- Rently: SQL-запросы проекта

-- Получение списка всех вещей, доступных для аренды
SELECT
  id,
  name,
  price,
  deposit
FROM items
ORDER BY name;

-- Фильтрация вещей по имени (например, только 'лопата')
SELECT 
  id,
  name,
  price,
  deposit
FROM items
WHERE name LIKE 'лопата%'
  OR name LIKE '%лопата'
ORDER BY price;

-- Поиск вещей по стоимости аренды (например, ниже 1500 рублей в день)
SELECT 
  id,
  name,
  price,
  deposit
FROM items
WHERE price <= 1500
ORDER BY price DESC;

-- Получение активных бронирований
SELECT
  bookings.id,
  bookings.start_date,
  bookings.end_date,
  items.name,
  users.name
FROM bookings 
JOIN items ON bookings.item_id = items.id;
JOIN users ON bookings.user_id = users.id;
WHERE bookings.is_cancelled = 0;
ORDER BY bookings.start_date;

-- Поиск свободных вещей на конкретную дату (например, на 20 октября 2026 года)
SELECT
  id,
  name,
  price,
  deposit
FROM items 
WHERE id NOT IN (
    SELECT item_id
    FROM bookings
    WHERE booking_date = '2026-10-20' AND is_cancelled = 0
)
ORDER BY name;

-- Общее количество активных бронирований
SELECT COUNT(*)
FROM bookings
WHERE is_cancelled = 0;

-- Количество бронирований по каждой вещи
SELECT 
  items.name
  COUNT(bookings.id) AS bookings_count
FROM items
LEFT JOIN bookings ON items.id = bookings.item_id AND bookings.is_cancelled = 0
GROUP BY items.id, items.name
ORDER BY bookings_count DESC;

-- Популярные вещи с количеством бронирований больше заданного (к примеру, больше 3)
SELECT 
    items.name,
    COUNT(bookings.id) AS bookings_count
FROM items
JOIN bookings ON items.id = bookings.item_id
WHERE bookings.is_cancelled = 0
GROUP BY items.id, items.name
HAVING COUNT(bookings.id) >= 3
ORDER BY bookings_count DESC;

-- Средняя стоимость аренды вещей
SELECT
  AVG(price) AS avg_price
FROM items
ORDER BY avg_price DESC;