import json
import time
from datetime import datetime
from pyflink.common import Types
from pyflink.datastream import RuntimeContext, KeyedProcessFunction, MapFunction
from pyflink.datastream.state import ValueStateDescriptor

from processing_plugins.base import ProcessingPlugin
from util.RedisUtil import RedisUtil


class CarPriceScorePlugin(ProcessingPlugin, KeyedProcessFunction,MapFunction):
    def __init__(self, window_size_ms=1000 * 3600 * 24 * 30):
        self.window_size_ms = window_size_ms  # 3个月的毫秒数

    def open(self, runtime_context: RuntimeContext):
        # 使用状态保存每个用户的油耗记录
        state_desc = ValueStateDescriptor("car_price_score_state", Types.PICKLED_BYTE_ARRAY())
        self.fuel_state = runtime_context.get_state(state_desc)

    def process(self, data):
        user_score = data.get('user_score')
        if data.get('data_post') is not None:
            time_post = int(datetime.strptime(data.get('data_post'), "%Y-%m-%d %H:%M:%S").timestamp()) * 1000
        else:
            time_post = time.time() * 1000
        price_section = data.get('price_section')
        return (user_score, price_section, time_post)

    def process_element(self, value, ctx: 'KeyedProcessFunction.Context'):
        user_score, price_section, time_post = value
        # 按地域统计销售总量
        user_score_his = self.fuel_state.value()
        if user_score_his is None:
            user_score_his = []
        user_score_his.append(user_score)
        self.fuel_state.update(user_score_his)
        avg_score=sum(user_score_his)/len(user_score_his)
        price_score_key = "car::price::score"
        RedisUtil.redis_client.hincrby(price_score_key,ctx.get_current_key(),avg_score)
    def map(self, value):
        data = json.loads(value)
        return self.process(data)