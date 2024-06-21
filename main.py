from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from redis.client import Redis
from db.connection import RedisConnection

app = FastAPI()
client = RedisConnection.filling_redis()
templates = Jinja2Templates(directory="templates")

@app.get('/{search_item}')
async def get_item(request: Request, search_item: str):
    try:
        value_d = client.hget(search_item, "description")
        if value_d:
            return templates.TemplateResponse(name='search.html', context={"request":request, "items":value_d},
                                              status_code=200)
        else:
            return {"message": f"По ключу {search_item} получено ПУСТОЕ значение"}
    except Exception as ex:
        return {"message": f"Ошибка извлечения данных из Redis {ex}"}
    
# @app.get('/')
# async def get_item(request: Request):
#     return templates.TemplateResponse(name='search.html', context={"request":request}, status_code=200)
