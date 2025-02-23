import json
import time
from datetime import datetime
from pyflink.common import Types
from pyflink.datastream import RuntimeContext, KeyedProcessFunction, MapFunction
from pyflink.datastream.state import ValueStateDescriptor
from processing_plugins.base import ProcessingPlugin
from util.RedisUtil import RedisUtil


class AverageScorePlugin(ProcessingPlugin, KeyedProcessFunction,MapFunction):
    def __init__(self, window_size_ms=1000 * 3600 * 24 * 30):
        self.window_size_ms = window_size_ms  # 3个月的毫秒数

    def open(self, runtime_context: RuntimeContext):
        # 使用状态保存每个用户的油耗记录
        state_desc = ValueStateDescriptor("score_state", Types.LIST())
        self.fuel_state = runtime_context.get_state(state_desc)

    def process(self, data):
        c_name = data.get('c_name')
        if data.get('data_post') is not None:
            time_post = int(datetime.strptime(data.get('data_post'), "%Y-%m-%d %H:%M:%S").timestamp()) * 1000
        else:
            time_post = time.time() * 1000
        user_score = data.get('user_score')
        return (c_name, float(user_score), time_post)

    def process_element(self, value, ctx: 'KeyedProcessFunction.Context'):
        c_name, user_score, time_post = value
        # 按地域统计销售总量
        score_list = self.fuel_state.value()
        if score_list is None:
            score_list = []
        score_list.append(user_score)
        self.fuel_state.update(score_list)
        avg_score = sum(score_list) / len(score_list)
        score_avg_key = "car::score::avg"
        RedisUtil.redis_client.hset(score_avg_key, c_name, avg_score)
    def map(self, value):
        data = json.loads(value)
        return self.process(data)