import redis

from config import Config


class RedisUtil:
    redis_client = redis.StrictRedis(Config.REDIS_HOST, Config.REDIS_PORT)

    @staticmethod
    def put(key, value):
        RedisUtil.redis_client.rpush(key, value)
        RedisUtil.redis_client.hincrby()
