import logging
import time
from typing import List, Optional

from redis import Redis, ConnectionPool

from app.helper.custom_exception import LockWaitTimeout
from setting import setting

redis_pool = ConnectionPool.from_url(setting.REDIS_ADDRESS)
_logger = logging.getLogger(__name__)


def init_redis_conn():
    pool = Redis(connection_pool=redis_pool)
    return pool


class RedisHelper:
    __LOCK = '1'
    __UNLOCK = '0'
    __TIMEOUT = 20

    @classmethod
    def get_lock_key(cls, keys: List[str]):
        return ['_lock_' + key for key in keys]

    @classmethod
    def _is_lock(cls, redis: Redis, keys: List[str]) -> bool:
        result = redis.exists(*keys)
        return result == len(keys)

    @classmethod
    def lock(cls, redis: Redis, keys: List[str]):
        counter = 0
        lock_keys = dict()
        for key in cls.get_lock_key(keys):
            lock_keys[key] = cls.__LOCK

        while redis.msetnx(lock_keys) == 0:
            time.sleep(1)
            counter += 1
            if counter == setting.REDIS_LOCK_TIMEOUT:
                raise LockWaitTimeout(keys[0])

        for key in lock_keys:
            redis.expire(key, cls.__TIMEOUT)

        return

    @classmethod
    def unlock(cls, redis: Redis, keys: List[str]):
        if len(keys) == 0:
            return

        redis.delete(*cls.get_lock_key(keys))
        return

    @classmethod
    def get(cls, redis: Redis, keys: List[str], lock: bool = True) -> List[Optional[str]]:
        if lock:
            cls.lock(redis, keys)

        results = redis.mget(*keys)
        list_values = []
        for value in results:
            if value:
                list_values.append(value.decode('utf-8'))
            else:
                list_values.append(None)
        _logger.debug(f"keys: {keys}, values: {list_values}")
        return list_values

    @classmethod
    def set(cls, redis: Redis, pairs: dict):
        redis.mset(pairs)
        return
