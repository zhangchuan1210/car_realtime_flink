import json
import time
from datetime import datetime
from pyflink.common import Types
from pyflink.datastream import RuntimeContext, KeyedProcessFunction, MapFunction
from pyflink.datastream.state import ValueStateDescriptor

from processing_plugins.base import ProcessingPlugin
from util.RedisUtil import RedisUtil
from util.WebsocketUtil import push_to_frontend


class AverageFuelConsumptionPlugin(ProcessingPlugin, KeyedProcessFunction,MapFunction):
    def __init__(self, window_size_ms=1000 * 3600):
        self.window_size_ms = window_size_ms  # 3个月的毫秒数

    def process(self, data):
        c_name = data.get('c_name')
        if data.get('data_post') is not None:
            time_post = int(datetime.strptime(data.get('data_post'), "%Y-%m-%d %H:%M:%S").timestamp())*1000
        else:
            time_post = time.time()*1000
        oil_consume = data.get('oil_consume')
        return (c_name, float(oil_consume), time_post)

    def open(self, runtime_context: RuntimeContext):
        # 使用状态保存每个用户的油耗记录
        state_desc = ValueStateDescriptor("fuel_state", Types.PICKLED_BYTE_ARRAY())
        self.fuel_state = runtime_context.get_state(state_desc)

    def process_element(self, value, ctx: 'KeyedProcessFunction.Context'):
        c_name, fuel_consumption, timestamp = value
        current_time = ctx.timestamp()
        # 获取当前用户的油耗记录
        fuel_records = self.fuel_state.value()
        if fuel_records is None:
            fuel_records = []
        # 添加新的油耗记录
        fuel_records.append((timestamp, fuel_consumption))
        # 过滤掉3个月前的记录
        window_start = current_time - self.window_size_ms
        fuel_records = [record for record in fuel_records if record[0] >= window_start]
        # 更新状态
        self.fuel_state.update(fuel_records)
        # 计算平均油耗
        total_fuel = sum([record[1] for record in fuel_records])
        count = len(fuel_records)
        average_fuel = total_fuel / count if count > 0 else 0.0
        print(c_name, average_fuel)
        var = {"c_name": c_name, "avg_oil_consume": average_fuel}
        push_to_frontend("oil-avg-web-socket",var)
        RedisUtil.put("haoyouliang",json.dumps(var))
        return value
    def map(self, value):
        data = json.loads(value)
        return self.process(data)