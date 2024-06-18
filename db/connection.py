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
        client.set("key1", "value1234")
        client.set("key2", "value5678")
        client.set("key3", "value910")
        return client