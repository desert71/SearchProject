from fastapi import APIRouter

custom_router = APIRouter()

@custom_router.post('/') #TODO Добавить response_model
async def get_item():
    pass

