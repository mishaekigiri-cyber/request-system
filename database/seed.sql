PRAGMA foreign_keys = ON;
INSERT OR IGNORE INTO Statuses(status_id,name) VALUES (1,'Новая'),(2,'В работе'),(3,'Выполнена'),(4,'Закрыта');
INSERT OR IGNORE INTO Categories(category_id,name,description) VALUES
(1,'Оборудование','Компьютеры, принтеры и периферия'),(2,'Программное обеспечение','Ошибки и установка программ'),(3,'Сеть','Доступ к сети и интернету'),(4,'Учётная запись','Пароли и права доступа');
INSERT OR IGNORE INTO Users(user_id,full_name,email,role) VALUES
(1,'Иванов Иван','ivanov@example.com','Заявитель'),(2,'Петрова Анна','petrova@example.com','Оператор'),(3,'Сидоров Максим','sidorov@example.com','Исполнитель'),(4,'Кузнецова Мария','kuznetsova@example.com','Заявитель'),(5,'Орлов Павел','orlov@example.com','Администратор');
INSERT INTO Requests(title,description,user_id,category_id,status_id,assignee_id) SELECT 'Не печатает принтер','Принтер не реагирует на отправку документов.',1,1,2,3 WHERE NOT EXISTS(SELECT 1 FROM Requests WHERE title='Не печатает принтер');
INSERT INTO Requests(title,description,user_id,category_id,status_id,assignee_id) SELECT 'Не запускается редактор','При запуске появляется сообщение об ошибке.',4,2,1,NULL WHERE NOT EXISTS(SELECT 1 FROM Requests WHERE title='Не запускается редактор');
INSERT INTO Requests(title,description,user_id,category_id,status_id,assignee_id) SELECT 'Нет доступа к Wi-Fi','Ноутбук не подключается к учебной сети.',1,3,3,3 WHERE NOT EXISTS(SELECT 1 FROM Requests WHERE title='Нет доступа к Wi-Fi');
INSERT INTO Requests(title,description,user_id,category_id,status_id,assignee_id) SELECT 'Сброс пароля','Не удаётся войти в рабочую учётную запись.',4,4,4,2 WHERE NOT EXISTS(SELECT 1 FROM Requests WHERE title='Сброс пароля');
INSERT INTO Requests(title,description,user_id,category_id,status_id,assignee_id) SELECT 'Установка приложения','Требуется установить приложение для работы.',1,2,1,NULL WHERE NOT EXISTS(SELECT 1 FROM Requests WHERE title='Установка приложения');
INSERT INTO Requests(title,description,user_id,category_id,status_id,assignee_id) SELECT 'Медленный компьютер','Компьютер долго загружает рабочий стол.',4,1,2,3 WHERE NOT EXISTS(SELECT 1 FROM Requests WHERE title='Медленный компьютер');
INSERT INTO Requests(title,description,user_id,category_id,status_id,assignee_id) SELECT 'Ошибка обновления','Обновление программы завершается ошибкой.',1,2,1,NULL WHERE NOT EXISTS(SELECT 1 FROM Requests WHERE title='Ошибка обновления');
INSERT INTO Requests(title,description,user_id,category_id,status_id,assignee_id) SELECT 'Нет сетевого доступа','Рабочее место не видит общую папку.',4,3,2,3 WHERE NOT EXISTS(SELECT 1 FROM Requests WHERE title='Нет сетевого доступа');
INSERT INTO Requests(title,description,user_id,category_id,status_id,assignee_id) SELECT 'Создание учётной записи','Нужна новая учётная запись сотрудника.',1,4,1,2 WHERE NOT EXISTS(SELECT 1 FROM Requests WHERE title='Создание учётной записи');
INSERT INTO Requests(title,description,user_id,category_id,status_id,assignee_id) SELECT 'Замена клавиатуры','Несколько клавиш перестали работать.',4,1,3,3 WHERE NOT EXISTS(SELECT 1 FROM Requests WHERE title='Замена клавиатуры');
