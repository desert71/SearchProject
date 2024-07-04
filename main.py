import uvicorn
import pandas as pd
import kaggle
import os
from datetime import datetime
from time import sleep
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from redis.client import Redis
from db.connection import RedisConnection

app = FastAPI()
client = RedisConnection.filling_redis()
templates = Jinja2Templates(directory="templates")

@app.get('/search/{search_item}')
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
    

@app.get('/')
async def download_data(request: Request):
    if os.path.isfile('./Free-to-play games'):
        return {"message": f"Файл уже скачан"}
    else:
        kaggle.api.authenticate()
        start_time = datetime.now().second
        kaggle.api.dataset_download_files('asferzafar/free-to-play-games-dataset', path='.', unzip=True)
        while datetime.now().second - start_time < 30:
            if os.path.isfile('./Free-to-play games'):
                return {"message": f"Теперь файл скачан"}
            else:
                return {"message": f"Подождите, файл скачивается"}
            sleep(1)
    return {"message": f"Произошла ошибка при скачивании файла. Попробуйте ещё раз."}
    #return templates.TemplateResponse(name='search.html', context={"request":request}, status_code=200)

@app.get('/get_data')
async def get_data(request: Request):
    if not os.path.isfile('./Free-to-play games'):
        return RedirectResponse('/')
    data_frame = pd.read_csv('./Free-to-play games')
    top_ten_rows = data_frame.head(10)
    print(top_ten_rows)
    return templates.TemplateResponse(name='show_data.html',
                                      context={"request":request, "rows": top_ten_rows},
                                      status_code=200
                                      )
    # return {"message": f"{data_frame.head(10)}",
    #         "length_data": f"{data_frame.shape[0]}"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
