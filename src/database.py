import os
import sqlite3
from pathlib import Path

DB_PATH = Path(os.getenv("REQUESTS_DB_PATH", "data/requests.sqlite3"))

SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS Statuses (status_id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS Categories (category_id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE, description TEXT);
CREATE TABLE IF NOT EXISTS Users (user_id INTEGER PRIMARY KEY, full_name TEXT NOT NULL, email TEXT NOT NULL UNIQUE, role TEXT NOT NULL CHECK (role IN ('Заявитель','Оператор','Исполнитель','Администратор')));
CREATE TABLE IF NOT EXISTS Requests (request_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, user_id INTEGER NOT NULL REFERENCES Users(user_id), category_id INTEGER NOT NULL REFERENCES Categories(category_id), status_id INTEGER NOT NULL REFERENCES Statuses(status_id), assignee_id INTEGER REFERENCES Users(user_id));
CREATE TABLE IF NOT EXISTS Comments (comment_id INTEGER PRIMARY KEY AUTOINCREMENT, request_id INTEGER NOT NULL REFERENCES Requests(request_id) ON DELETE CASCADE, user_id INTEGER NOT NULL REFERENCES Users(user_id), body TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
"""

SEED_STATUSES = [(1, "Новая"), (2, "В работе"), (3, "Выполнена"), (4, "Закрыта")]
SEED_CATEGORIES = [(1, "Оборудование", "Компьютеры, принтеры и периферия"), (2, "Программное обеспечение", "Ошибки и установка программ"), (3, "Сеть", "Доступ к сети и интернету"), (4, "Учётная запись", "Пароли и права доступа")]
SEED_USERS = [(1, "Иванов Иван", "ivanov@example.com", "Заявитель"), (2, "Петрова Анна", "petrova@example.com", "Оператор"), (3, "Сидоров Максим", "sidorov@example.com", "Исполнитель"), (4, "Кузнецова Мария", "kuznetsova@example.com", "Заявитель"), (5, "Орлов Павел", "orlov@example.com", "Администратор")]
SEED_REQUESTS = [
 ("Не печатает принтер", "Принтер не реагирует на отправку документов.", 1, 1, 2, 3),
 ("Не запускается редактор", "При запуске появляется сообщение об ошибке.", 4, 2, 1, None),
 ("Нет доступа к Wi-Fi", "Ноутбук не подключается к учебной сети.", 1, 3, 3, 3),
 ("Сброс пароля", "Не удаётся войти в рабочую учётную запись.", 4, 4, 4, 2),
 ("Установка приложения", "Требуется установить приложение для работы.", 1, 2, 1, None),
 ("Медленный компьютер", "Компьютер долго загружает рабочий стол.", 4, 1, 2, 3),
 ("Ошибка обновления", "Обновление программы завершается ошибкой.", 1, 2, 1, None),
 ("Нет сетевого доступа", "Рабочее место не видит общую папку.", 4, 3, 2, 3),
 ("Создание учётной записи", "Нужна новая учётная запись сотрудника.", 1, 4, 1, 2),
 ("Замена клавиатуры", "Несколько клавиш перестали работать.", 4, 1, 3, 3),
]

def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def init_db() -> None:
    with get_connection() as connection:
        connection.executescript(SCHEMA)
        connection.executemany("INSERT OR IGNORE INTO Statuses(status_id,name) VALUES (?,?)", SEED_STATUSES)
        connection.executemany("INSERT OR IGNORE INTO Categories(category_id,name,description) VALUES (?,?,?)", SEED_CATEGORIES)
        connection.executemany("INSERT OR IGNORE INTO Users(user_id,full_name,email,role) VALUES (?,?,?,?)", SEED_USERS)
        count = connection.execute("SELECT COUNT(*) FROM Requests").fetchone()[0]
        if count == 0:
            connection.executemany("INSERT INTO Requests(title,description,user_id,category_id,status_id,assignee_id) VALUES (?,?,?,?,?,?)", [(t,d,u,c,s,a) for t,d,u,c,s,a in SEED_REQUESTS])
