from fastapi import FastAPI
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
        return {"message": f"По ключу {search_item} получено значение {value}"}
    except Exception as ex:
        return {"message": "Что-то пошло не так"}

# print(client.get("key2"), client.get("key3"), client.get("key1"))
