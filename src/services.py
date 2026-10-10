from typing import Any
from sqlite3 import IntegrityError
from src.database import get_connection

REQUEST_SELECT = """
SELECT r.request_id, r.title, r.description, r.created_at, r.user_id, r.category_id, r.status_id, r.assignee_id, s.name AS status, c.name AS category, u.full_name AS applicant, a.full_name AS assignee
FROM Requests r JOIN Statuses s ON s.status_id=r.status_id JOIN Categories c ON c.category_id=r.category_id JOIN Users u ON u.user_id=r.user_id LEFT JOIN Users a ON a.user_id=r.assignee_id
"""
class NotFoundError(Exception): pass
class ValidationError(Exception): pass

def list_requests(search: str | None=None, status_id: int | None=None, category_id: int | None=None) -> list[dict[str, Any]]:
    sql=REQUEST_SELECT+" WHERE 1=1"; params=[]
    if search and search.strip():
        term="%"+search.strip()+"%"; sql+=" AND (r.title LIKE ? OR r.description LIKE ? OR u.full_name LIKE ?)"; params.extend([term,term,term])
    if status_id is not None: sql+=" AND r.status_id=?"; params.append(status_id)
    if category_id is not None: sql+=" AND r.category_id=?"; params.append(category_id)
    sql+=" ORDER BY r.created_at DESC,r.request_id DESC"
    with get_connection() as db: return [dict(x) for x in db.execute(sql,params).fetchall()]

def get_request(request_id: int) -> dict[str, Any]:
    with get_connection() as db: row=db.execute(REQUEST_SELECT+" WHERE r.request_id=?",(request_id,)).fetchone()
    if row is None: raise NotFoundError("Заявка с ID "+str(request_id)+" не найдена")
    return dict(row)

def create_request(data: dict[str, Any]) -> dict[str, Any]:
    with get_connection() as db:
        if db.execute("SELECT 1 FROM Users WHERE user_id=?",(data['user_id'],)).fetchone() is None: raise ValidationError("Указанный заявитель не существует")
        if db.execute("SELECT 1 FROM Categories WHERE category_id=?",(data['category_id'],)).fetchone() is None: raise ValidationError("Указанная категория не существует")
        assignee=data.get('assignee_id')
        if assignee is not None:
            row=db.execute("SELECT role FROM Users WHERE user_id=?",(assignee,)).fetchone()
            if row is None or row['role'] not in ('Исполнитель','Оператор','Администратор'): raise ValidationError("Исполнитель не найден или не может быть назначен")
        try:
            cur=db.execute("INSERT INTO Requests(title,description,user_id,category_id,status_id,assignee_id) VALUES (?,?,?,?,1,?)",(data['title'],data['description'],data['user_id'],data['category_id'],assignee)); request_id=cur.lastrowid
        except IntegrityError as exc: raise ValidationError("Не удалось сохранить заявку: проверьте связанные данные") from exc
    return get_request(int(request_id))

def update_request(request_id: int, data: dict[str, Any]) -> dict[str, Any]:
    if not data: raise ValidationError("Не переданы поля для изменения")
    allowed={'title','description','category_id','assignee_id'}
    if set(data)-allowed: raise ValidationError("Переданы недопустимые поля")
    with get_connection() as db:
        if db.execute("SELECT 1 FROM Requests WHERE request_id=?",(request_id,)).fetchone() is None: raise NotFoundError("Заявка с ID "+str(request_id)+" не найдена")
        if 'category_id' in data and db.execute("SELECT 1 FROM Categories WHERE category_id=?",(data['category_id'],)).fetchone() is None: raise ValidationError("Указанная категория не существует")
        if 'assignee_id' in data and data['assignee_id'] is not None:
            row=db.execute("SELECT role FROM Users WHERE user_id=?",(data['assignee_id'],)).fetchone()
            if row is None or row['role'] not in ('Исполнитель','Оператор','Администратор'): raise ValidationError("Исполнитель не найден или не может быть назначен")
        cols=[key+"=?" for key in data]; vals=list(data.values())+[request_id]
        try: db.execute("UPDATE Requests SET "+", ".join(cols)+" WHERE request_id=?",vals)
        except IntegrityError as exc: raise ValidationError("Не удалось изменить заявку") from exc
    return get_request(request_id)

def change_status(request_id: int, status_id: int) -> dict[str, Any]:
    with get_connection() as db:
        if db.execute("SELECT 1 FROM Requests WHERE request_id=?",(request_id,)).fetchone() is None: raise NotFoundError("Заявка с ID "+str(request_id)+" не найдена")
        if db.execute("SELECT 1 FROM Statuses WHERE status_id=?",(status_id,)).fetchone() is None: raise ValidationError("Указанный статус не существует")
        db.execute("UPDATE Requests SET status_id=? WHERE request_id=?",(status_id,request_id))
    return get_request(request_id)

def list_users():
    with get_connection() as db: return [dict(x) for x in db.execute("SELECT user_id,full_name,email,role FROM Users ORDER BY full_name").fetchall()]
def list_statuses():
    with get_connection() as db: return [dict(x) for x in db.execute("SELECT status_id,name FROM Statuses ORDER BY status_id").fetchall()]
def list_categories():
    with get_connection() as db: return [dict(x) for x in db.execute("SELECT category_id,name,description FROM Categories ORDER BY name").fetchall()]
