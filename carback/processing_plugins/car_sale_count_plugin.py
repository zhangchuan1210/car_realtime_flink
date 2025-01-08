import json
import time
from datetime import datetime
from pyflink.common import Types
from pyflink.datastream import RuntimeContext, KeyedProcessFunction, MapFunction
from pyflink.datastream.state import ValueStateDescriptor

from processing_plugins.base import ProcessingPlugin
from util.RedisUtil import RedisUtil


class CarSaleCountPlugin(ProcessingPlugin, KeyedProcessFunction,MapFunction):
    def __init__(self, window_size_ms=1000 * 3600 * 24 * 30):
        self.window_size_ms = window_size_ms  # 3个月的毫秒数

    def open(self, runtime_context: RuntimeContext):
        # 使用状态保存每个用户的油耗记录
        state_desc = ValueStateDescriptor("car_sale_count_state", Types.LONG())
        self.fuel_state = runtime_context.get_state(state_desc)

    def process(self, data):
        c_name = data.get('c_name')
        if data.get('data_post') is not None:
            time_post = int(datetime.strptime(data.get('data_post'), "%Y-%m-%d %H:%M:%S").timestamp()) * 1000
        else:
            time_post = time.time() * 1000
        user_id = data.get('user_id')
        return (c_name, user_id, time_post)

    def process_element(self, value, ctx: 'KeyedProcessFunction.Context'):
        c_name, user_id, time_post = value
        # 按地域统计销售总量
        sale_count = self.fuel_state.value()
        if sale_count is None:
            sale_count = 0
        sale_count += 1
        self.fuel_state.update(sale_count)
        c_name_count_key = "car::c_name::num"
        RedisUtil.redis_client.hincrby(c_name_count_key,ctx.get_current_key(),sale_count)
    def map(self, value):
        data = json.loads(value)
        return self.process(data)