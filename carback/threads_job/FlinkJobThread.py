import json
import threading

from pyflink.common import JobExecutionResult, WatermarkStrategy, Duration, Row, Time
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import Source
from pyflink.datastream.functions import MapFunction, SinkFunction
from pyflink.datastream.window import SlidingEventTimeWindows

from processing_plugins.address_car_count_plugin import AddressCarCountPlugin
from processing_plugins.average_fuel_plugin import AverageFuelConsumptionPlugin
from processing_plugins.average_score_plugin import AverageScorePlugin
from processing_plugins.car_price_range_plugin import CarPriceRangePlugin
from processing_plugins.car_price_score_plugin import CarPriceScorePlugin
from processing_plugins.car_sale_count_plugin import CarSaleCountPlugin


class FlinkJobThread(threading.Thread):
    def __init__(self, job_name, config, plugins, source: Source, target: SinkFunction,watermark_strategy=WatermarkStrategy.for_bounded_out_of_orderness(Duration.of_hours(1))):
        super().__init__()
        self.job_name = job_name
        self.config = config  # 接受配置对象
        self.plugins = plugins  # 已加载的插件字典
        self._stop_event = threading.Event()
        self.env = StreamExecutionEnvironment.get_execution_environment().set_parallelism(1)
        self.watermark_strategy=watermark_strategy
        self.source = source
        self.target = target
        self.job_client = None

    def run(self):
        try:
            # 调用作业配置函数，传入执行环境和配置
            self.configure_job(self.config)
            # 执行作业
            execution_result = self.env.execute(self.job_name)  # type: JobExecutionResult
            self.job_client = execution_result.get_job_client()
            if self.job_client is not None:
                print("Flink 作业已启动，Job ID:", self.job_client.get_job_id())
            else:
                print("无法获取 JobClient，作业可能已完成或在本地执行环境中运行")
        except Exception as e:
            print(f"Flink 作业出现异常：{e}")

    def stop(self):
        if self.job_client:
            try:
                self.job_client.cancel()
                print("Flink 作业已请求取消")
            except Exception as e:
                print(f"取消 Flink 作业时出现异常：{e}")
        else:
            print("JobClient 不存在，无法取消作业")
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    # 修改作业配置函数，接受配置参数
    def configure_job(self, config):
        kafka_stream = self.env.from_source(self.source, self.watermark_strategy, self.job_name)
        # 获取插件名称
        plugin_name = config.get('plugin_name')
        if not plugin_name:
            raise ValueError("配置文件中缺少 'plugin_name' 字段")
        address_car_count=AddressCarCountPlugin()
        average_score=AverageScorePlugin()
        car_sale_count=CarSaleCountPlugin()
        car_price_range=CarPriceRangePlugin()
        car_price_score=CarPriceScorePlugin()
        average_fuel=AverageFuelConsumptionPlugin()
        kafka_stream.map(average_fuel).key_by(lambda x: x[0]).process(average_fuel)
        #按地域统计销售总量
        kafka_stream.map(address_car_count).key_by(lambda x: x.getString("buy_address")).window(SlidingEventTimeWindows.of(Time.days(365),Time.minutes(10))).allowed_lateness(24*60*60*1000).process(address_car_count)
        #每款车评分均值
        kafka_stream.map(average_score).key_by(lambda x: x.getString("c_name")).process(average_score)
        #每款车销量
        kafka_stream.map(car_sale_count).key_by(lambda x: x.getString("c_name")).process(car_sale_count)
        #汽车售价和销量对比分析
        kafka_stream.map(car_price_range).key_by(lambda x: x.getString("price_section")).process(car_price_range)
        #汽车售价和评分对比分析
        kafka_stream.map(car_price_score).key_by(lambda x: x.getString("price_section")).process(car_price_score)
