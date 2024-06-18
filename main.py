from fastapi import FastAPI
from fastapi.responses import FileResponse
from redis.client import Redis

app = FastAPI()
client = Redis(host="localhost", port=6379)
client.set("key1", "value1111")
client.set("key2", "value2222")
client.set("key3", "value3333")

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
