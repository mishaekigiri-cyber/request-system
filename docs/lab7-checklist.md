# Лабораторная работа №7 — REST API

Автор: **Привалов М.Ф., ИСИП-407**

## Запуск

```powershell
.\.venv\Scripts\python.exe -m uvicorn src.main:app --reload
```

Swagger UI: http://127.0.0.1:8000/docs  
OpenAPI JSON: http://127.0.0.1:8000/openapi.json

## Проверки перед сдачей

- [ ] Запустить приложение и открыть Swagger UI.
- [ ] Выполнить все 16 запросов коллекции `postman/RequestSystem_Lab7.postman_collection.json`.
- [ ] Проверить GET списка и объекта, POST, PATCH редактирования, PATCH статуса и DELETE.
- [ ] Проверить справочники `/users`, `/statuses`, `/categories` и endpoint `/health`.
- [ ] Проверить поиск `search` и фильтры `status_id`, `category_id`.
- [ ] Зафиксировать ответы 201, 204, 400, 404 и 422.
- [ ] Выполнить автоматические тесты командой `.\.venv\Scripts\python.exe -m pytest -q`.
- [ ] Сохранить реальные скриншоты успешных и ошибочных запросов в отчёт.
- [ ] Добавить в AI-журнал результат собственного запуска.
- [ ] Создать не менее трёх осмысленных коммитов и подготовить PR из `feature/lab7` в `develop`.

Не отмечайте пункты выполненными до фактической проверки в локальном окружении.

