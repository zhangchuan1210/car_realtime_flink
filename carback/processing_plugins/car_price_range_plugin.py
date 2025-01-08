import json
import time
from datetime import datetime
from pyflink.common import Types
from pyflink.datastream import RuntimeContext, KeyedProcessFunction, MapFunction
from pyflink.datastream.state import ValueStateDescriptor

from processing_plugins.base import ProcessingPlugin
from util.RedisUtil import RedisUtil


class CarPriceRangePlugin(ProcessingPlugin, KeyedProcessFunction,MapFunction):
    def __init__(self, window_size_ms=1000 * 3600 * 24 * 30):
        self.window_size_ms = window_size_ms  # 3个月的毫秒数

    def open(self, runtime_context: RuntimeContext):
        # 使用状态保存每个用户的油耗记录
        state_desc = ValueStateDescriptor("car_price_range_state", Types.LONG())
        self.fuel_state = runtime_context.get_state(state_desc)

    def process(self, data):
        c_name = data.get('c_name')
        if data.get('data_post') is not None:
            time_post = int(datetime.strptime(data.get('data_post'), "%Y-%m-%d %H:%M:%S").timestamp()) * 1000
        else:
            time_post = time.time() * 1000
        price_section = data.get('price_section')
        return (c_name, price_section, time_post)

    def process_element(self, value, ctx: 'KeyedProcessFunction.Context'):
        # 按地域统计销售总量
        sale_count = self.fuel_state.value()
        if sale_count is None:
            sale_count = 0
        sale_count += 1
        self.fuel_state.update(sale_count)
        price_num_key = "car::price::num"
        RedisUtil.redis_client.hincrby(price_num_key,ctx.get_current_key(),sale_count)
    def map(self, value):
        data = json.loads(value)
        return self.process(data)