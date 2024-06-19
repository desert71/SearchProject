from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from redis.client import Redis
from db.connection import RedisConnection

app = FastAPI()
client = RedisConnection.filling_redis()
templates = Jinja2Templates(directory="templates")

@app.get('/{search_item}')
async def get_item(search_item: str):
    try:
        value = client.hget(search_item, "description")
        if value:
            return {"message": f"По ключу {search_item} получено значение {value}"}
        else:
            return {"message": f"По ключу {search_item} получено ПУСТОЕ значение"}
    except Exception as ex:
        return {"message": "Ошибка извлечения данных из Redis"}
    
@app.get('/')
async def get_item(request: Request):
    return templates.TemplateResponse(name='search.html', context={"request":request}, status_code=200)
