import json
import time
from datetime import datetime
from pyflink.common import Types
from pyflink.datastream import RuntimeContext
from pyflink.datastream.state import ValueStateDescriptor

from processing_plugins.key_base import KeyProcessingPlugin
from util.RedisUtil import RedisUtil


class AverageScoreConsumption(KeyProcessingPlugin):
    def __init__(self, window_size_ms=1000 * 3600*24*30):
        self.window_size_ms = window_size_ms  # 3个月的毫秒数

    def open(self, runtime_context: RuntimeContext):
        # 使用状态保存每个用户的油耗记录
        state_desc = ValueStateDescriptor("score_state", Types.PICKLED_BYTE_ARRAY())
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
        c_name, user_score, timestamp = value
        current_time = ctx.timestamp()
        # 获取当前用户的油耗记录
        fuel_records = self.fuel_state.value()
        if fuel_records is None:
            fuel_records = []
        # 添加新的油耗记录
        fuel_records.append((timestamp, user_score))
        window_start = current_time - self.window_size_ms
        fuel_records = [record for record in fuel_records if record[0] >= window_start]
        self.fuel_state.update(fuel_records)
        total_score = sum([record[1] for record in fuel_records])
        count = len(fuel_records)
        average_score = total_score / count if count > 0 else 0.0
        print(c_name, average_score)
        var = {"c_name": c_name, "avg_score": average_score}
        RedisUtil.put("avg_score", json.dumps(var))