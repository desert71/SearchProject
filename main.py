from fastapi import FastAPI
from fastapi.responses import FileResponse
from redis.client import Redis
from db.connection import RedisConnection

app = FastAPI()
client = RedisConnection.filling_redis()

@app.get('/{search_item}')
async def get_item(search_item: str):
    try:
        value = client.get(search_item)
        if value:
            return {"message": f"По ключу {search_item} получено значение {value}"}
        else:
            return {"message": f"По ключу {search_item} получено ПУСТОЕ значение"}
    except Exception as ex:
        return {"message": "Ошибка извлечения данных из Redis"}
    
@app.get('/')
async def get_item():
    return FileResponse(path='index.html', status_code=200)
