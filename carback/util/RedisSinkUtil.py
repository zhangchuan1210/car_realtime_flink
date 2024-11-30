import redis
from config import Config

class RedisSinkUtil:
    redis_client=redis.StrictRedis(Config.REDIS_HOST,Config.REDIS_PORT)
    @staticmethod
    def write_to_redis(key, value):
        RedisSinkUtil.redis_client.set(key, value)
