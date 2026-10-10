from contextlib import asynccontextmanager
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from src.database import init_db
from src.models import RequestCreate, RequestUpdate, StatusChange, RequestRead
from src import services

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app=FastAPI(title='Система учёта заявок',version='0.6.0',description='Учебное приложение для регистрации и обработки заявок',lifespan=lifespan)

@app.exception_handler(services.NotFoundError)
async def not_found_handler(request: Request, exc: services.NotFoundError): return JSONResponse(status_code=404,content={'detail':str(exc)})
@app.exception_handler(services.ValidationError)
async def validation_handler(request: Request, exc: services.ValidationError): return JSONResponse(status_code=400,content={'detail':str(exc)})

@app.get('/',response_class=HTMLResponse,include_in_schema=False)
def home():
    return HTMLResponse('''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Система учёта заявок</title><style>body{font-family:Arial,sans-serif;background:#f3f6fa;color:#172033;margin:0}header{background:#183153;color:white;padding:24px 5%}main{max-width:1100px;margin:24px auto;padding:0 18px}.layout{display:grid;grid-template-columns:1fr 1fr;gap:18px}.panel{background:white;border-radius:12px;padding:20px;box-shadow:0 2px 10px #13274712}input,textarea,select,button{box-sizing:border-box;width:100%;padding:10px;margin:6px 0;border:1px solid #ccd5e0;border-radius:7px;font:inherit}button{background:#245c9c;color:white;border:0;cursor:pointer}.item{border:1px solid #e0e6ee;padding:12px;border-radius:8px;margin:9px 0}.meta{color:#53657a;font-size:13px}.filters{display:grid;grid-template-columns:2fr 1fr 1fr;gap:8px}@media(max-width:720px){.layout,.filters{grid-template-columns:1fr}}</style></head><body><header><h1>Система учёта заявок</h1><div>Регистрация, поиск и контроль состояния обращений</div></header><main><div class="layout"><section class="panel"><h2>Создать заявку</h2><form id="create"><label>Тема<input name="title" minlength="3" maxlength="150" required placeholder="Например, не работает принтер"></label><label>Описание<textarea name="description" minlength="5" maxlength="5000" required></textarea></label><label>Заявитель<select name="user_id" id="users" required></select></label><label>Категория<select name="category_id" id="categories" required></select></label><label>Исполнитель<select name="assignee_id" id="assignees"><option value="">Не назначен</option></select></label><button type="submit">Зарегистрировать</button><p id="message" role="status"></p></form></section><section class="panel"><h2>Заявки</h2><div class="filters"><input id="search" placeholder="Поиск по теме или описанию"><select id="status"><option value="">Все статусы</option></select><select id="categoryFilter"><option value="">Все категории</option></select></div><button id="refresh">Обновить список</button><div id="requests">Загрузка...</div></section></div></main><script>
const $=id=>document.getElementById(id);const esc=s=>String(s??'').replace(/[&<>"\x27]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"\x27":'&#39;'}[c]));async function get(url){const r=await fetch(url);const d=await r.json();if(!r.ok)throw Error(d.detail||'Ошибка запроса');return d}async function load(){try{const [users,cats,statuses]=await Promise.all([get('/users'),get('/categories'),get('/statuses')]);$('users').innerHTML=users.filter(x=>x.role==='Заявитель').map(x=>'<option value="'+x.user_id+'">'+esc(x.full_name)+'</option>').join('');$('assignees').innerHTML='<option value="">Не назначен</option>'+users.filter(x=>['Исполнитель','Оператор','Администратор'].includes(x.role)).map(x=>'<option value="'+x.user_id+'">'+esc(x.full_name)+'</option>').join('');$('categories').innerHTML=cats.map(x=>'<option value="'+x.category_id+'">'+esc(x.name)+'</option>').join('');$('categoryFilter').innerHTML='<option value="">Все категории</option>'+$('categories').innerHTML;$('status').innerHTML='<option value="">Все статусы</option>'+statuses.map(x=>'<option value="'+x.status_id+'">'+esc(x.name)+'</option>').join('');await refresh()}catch(e){$('requests').textContent=e.message}}
async function refresh(){const p=new URLSearchParams();if($('search').value.trim())p.set('search',$('search').value.trim());if($('status').value)p.set('status_id',$('status').value);if($('categoryFilter').value)p.set('category_id',$('categoryFilter').value);try{const rows=await get('/requests?'+p.toString());$('requests').innerHTML=rows.length?rows.map(x=>'<article class="item"><b>#'+x.request_id+' '+esc(x.title)+'</b><div class="meta">'+esc(x.category)+' · '+esc(x.status)+' · заявитель: '+esc(x.applicant)+'</div><p>'+esc(x.description)+'</p><label>Изменить статус<select data-status="'+x.request_id+'">'+window.statusOptions.map(s=>'<option value="'+s.status_id+'" '+(s.status_id===x.status_id?'selected':'')+'>'+esc(s.name)+'</option>').join('')+'</select></label></article>').join(''):'Заявок не найдено';}catch(e){$('requests').textContent=e.message}}
$('create').addEventListener('submit',async e=>{e.preventDefault();const f=new FormData(e.currentTarget);const body={title:f.get('title'),description:f.get('description'),user_id:Number(f.get('user_id')),category_id:Number(f.get('category_id')),assignee_id:f.get('assignee_id')?Number(f.get('assignee_id')):null};try{const res=await fetch('/requests',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});const d=await res.json();if(!res.ok)throw Error(d.detail||'Не удалось создать заявку');$('message').textContent='Заявка #'+d.request_id+' создана';e.currentTarget.reset();await load()}catch(err){$('message').textContent=err.message}});$('requests').addEventListener('change',async e=>{if(e.target.dataset.status){const id=e.target.dataset.status;try{const r=await fetch('/requests/'+id+'/status',{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({status_id:Number(e.target.value)})});const d=await r.json();if(!r.ok)throw Error(d.detail||'Ошибка');await refresh()}catch(err){alert(err.message)}}});$('refresh').addEventListener('click',refresh);$('search').addEventListener('input',refresh);$('status').addEventListener('change',refresh);$('categoryFilter').addEventListener('change',refresh);window.statusOptions=[];get('/statuses').then(x=>{window.statusOptions=x;load()});
</script></body></html>''')

@app.get('/requests',response_model=list[RequestRead])
def get_requests(search: str|None=Query(default=None,max_length=150),status_id: int|None=Query(default=None,gt=0),category_id: int|None=Query(default=None,gt=0)):
    return services.list_requests(search,status_id,category_id)
@app.get('/requests/{request_id}',response_model=RequestRead)
def get_request(request_id: int): return services.get_request(request_id)
@app.post('/requests',response_model=RequestRead,status_code=201)
def post_request(data: RequestCreate): return services.create_request(data.model_dump())
@app.patch('/requests/{request_id}',response_model=RequestRead)
def patch_request(request_id: int,data: RequestUpdate): return services.update_request(request_id,data.model_dump(exclude_unset=True))
@app.patch('/requests/{request_id}/status',response_model=RequestRead)
def patch_status(request_id: int,data: StatusChange): return services.change_status(request_id,data.status_id)
@app.get('/users')
def get_users(): return services.list_users()
@app.get('/statuses')
def get_statuses(): return services.list_statuses()
@app.get('/categories')
def get_categories(): return services.list_categories()
@app.get('/health')
def health(): return {'status':'ok'}
