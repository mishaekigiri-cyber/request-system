PRAGMA foreign_keys = ON;

-- SELECT 1: все заявки
SELECT request_id, title, created_at FROM Requests ORDER BY request_id;

-- SELECT 2: заявки со статусом «Новая»
SELECT r.request_id, r.title
FROM Requests r JOIN Statuses s ON s.status_id = r.status_id
WHERE s.name = 'Новая';

-- SELECT 3: заявки конкретного заявителя
SELECT request_id, title FROM Requests WHERE user_id = 1;

-- SELECT 4: категории и количество заявок
SELECT c.name, COUNT(r.request_id) AS request_count
FROM Categories c LEFT JOIN Requests r ON r.category_id = c.category_id
GROUP BY c.category_id, c.name ORDER BY c.name;

-- SELECT 5: полная информация о заявках (JOIN)
SELECT r.request_id, r.title, s.name AS status, c.name AS category,
       u.full_name AS applicant, a.full_name AS assignee
FROM Requests r
JOIN Statuses s ON s.status_id = r.status_id
JOIN Categories c ON c.category_id = r.category_id
JOIN Users u ON u.user_id = r.user_id
LEFT JOIN Users a ON a.user_id = r.assignee_id
ORDER BY r.request_id;

-- UPDATE 1: изменить статус заявки (пример)
-- UPDATE Requests SET status_id = 2 WHERE request_id = 2;

-- UPDATE 2: назначить исполнителя (пример)
-- UPDATE Requests SET assignee_id = 3 WHERE request_id = 5;

-- DELETE 1: удалить комментарий по идентификатору (пример)
-- DELETE FROM Comments WHERE comment_id = 5;

-- DELETE 2: удалить заявку по идентификатору (пример; удалит связанные комментарии)
-- DELETE FROM Requests WHERE request_id = 5;

-- Дополнительные запросы с WHERE
SELECT request_id, title FROM Requests WHERE created_at >= '2026-01-01';
SELECT request_id, title FROM Requests WHERE category_id = 2 AND status_id IN (1, 2);

-- JOIN: комментарии с названиями заявок и авторами
SELECT c.comment_id, r.title, u.full_name, c.body
FROM Comments c
JOIN Requests r ON r.request_id = c.request_id
JOIN Users u ON u.user_id = c.user_id
ORDER BY c.comment_id;
