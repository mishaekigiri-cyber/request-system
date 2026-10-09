PRAGMA foreign_keys = ON;

-- Скрипт запускать после schema.sql и seed.sql.
-- Все изменения находятся внутри транзакции и откатываются в конце.
BEGIN TRANSACTION;

-- UPDATE 1: изменить статус заявки №2 на «В работе» (status_id = 2).
UPDATE Requests SET status_id = 2 WHERE request_id = 2;
SELECT request_id, title, status_id FROM Requests WHERE request_id = 2;

-- UPDATE 2: назначить исполнителя №3 заявке №5.
UPDATE Requests SET assignee_id = 3 WHERE request_id = 5;
SELECT request_id, title, assignee_id FROM Requests WHERE request_id = 5;

-- DELETE 1: удалить комментарий №5.
DELETE FROM Comments WHERE comment_id = 5;
SELECT comment_id, request_id, body FROM Comments WHERE comment_id = 5;

-- DELETE 2: удалить заявку №5 (связанные комментарии удаляются каскадно).
DELETE FROM Requests WHERE request_id = 5;
SELECT request_id, title FROM Requests WHERE request_id = 5;

-- Откат всех тестовых изменений: исходные записи остаются в БД.
ROLLBACK;

-- Контроль: заявка №5 и комментарий №5 должны снова существовать.
SELECT request_id, title FROM Requests WHERE request_id = 5;
SELECT comment_id, request_id, body FROM Comments WHERE comment_id = 5;
