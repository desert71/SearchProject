from redis.client import Redis
from redis.backoff import ExponentialBackoff
from redis.retry import Retry
from redis.exceptions import (
    BusyLoadingError,
    ConnectionError,
    TimeoutError,
)

RETRY = 3
TIMEOUT = 2

class RedisConnection:
    _instance = None
    @staticmethod
    def get_connection():
        if not RedisConnection._instance:
            RedisConnection._instance = Redis(
                host="localhost",
                port=6379,
                socket_timeout=TIMEOUT,
                retry=Retry(backoff=ExponentialBackoff(), retries=RETRY),
                retry_on_error=[BusyLoadingError, ConnectionError, TimeoutError],
            )
        return RedisConnection._instance
    
    @staticmethod
    def filling_redis():
        client = RedisConnection.get_connection()
        client.hset("Product_1_name", mapping={
            "description":"Some description",
            "const": "5000",
            "image": "Product_1_image.png"
            }
        )
        client.hset("Product_2_name", mapping={
            "description":"Some description for product_2",
            "const": "2020",
            "image": "Product_2_image.png"
            }
        )
        client.hset("Product_1_name", mapping={
            "description":"Some description about product_3",
            "const": "7707",
            "image": "Product_3_image.png"
            }
        )
        return client