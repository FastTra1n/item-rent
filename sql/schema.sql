-- Rently: структура базы данных
-- Сущности: вещь, пользователь, бронирование

CREATE TABLE IF NOT EXISTS items ( 
  id INTEGER PRIMARY KEY,
  owner_id INTEGER NOT NULL, 
  name TEXT NOT NULL, 
  price INTEGER NOT NULL,
  deposit INTEGER NOT NULL DEFAULT 0,
  FOREIGN KEY (owner_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS users ( 
  id INTEGER PRIMARY KEY, 
  name TEXT NOT NULL, 
  phone TEXT NOT NULL,
  rating REAL NOT NULL DEFAULT 0.0
);

CREATE TABLE IF NOT EXISTS bookings ( 
  id INTEGER PRIMARY KEY, 
  item_id INTEGER NOT NULL, 
  user_id INTEGER NOT NULL, 
  start_date TEXT NOT NULL, 
  end_date TEXT NOT NULL, 
  is_cancelled INTEGER NOT NULL DEFAULT 0, 
  FOREIGN KEY (item_id) REFERENCES items(id), 
  FOREIGN KEY (user_id) REFERENCES users(id) 
);