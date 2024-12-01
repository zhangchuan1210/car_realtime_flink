import redis
from pyflink.datastream import ProcessFunction

from config import Config


class RedisSinkUtil(ProcessFunction):

    def __init__(self, redis_host=Config.REDIS_HOST, redis_port=Config.REDIS_PORT):
        # 初始化 Redis 客户端
        self.redis_client = None
        self.redis_host = redis_host
        self.redis_port = redis_port

    def open(self, runtime_context):
        # 在任务开始时建立 Redis 连接
        self.redis_client = redis.StrictRedis(self.redis_host, self.redis_port)

    def process_element(self, value, ctx):
        # 处理每条数据并写入 Redis
        # 假设 value 是 Row 类型，第一个字段是 key，第二个字段是 value
        key = value[0]
        redis_value = value[1]
        self.redis_client.set(key, redis_value)

    def close(self):
        # 关闭 Redis 连接
        if self.redis_client:
            self.redis_client.close()
