import json
import threading

from pyflink.common import JobExecutionResult, WatermarkStrategy, Duration, Row
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import Source
from pyflink.datastream.functions import MapFunction, SinkFunction


class FlinkJobThread(threading.Thread):
    def __init__(self, job_name, config, plugins, source: Source, target: SinkFunction):
        super().__init__()
        self.job_name = job_name
        self.config = config  # 接受配置对象
        self.plugins = plugins  # 已加载的插件字典
        self._stop_event = threading.Event()
        self.env = StreamExecutionEnvironment.get_execution_environment().set_parallelism(1)
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
        watermark_strategy = WatermarkStrategy.for_bounded_out_of_orderness(Duration.of_hours(1))
        kafka_stream = self.env.from_source(self.source, watermark_strategy, self.job_name)
        # 获取插件名称
        plugin_name = config.get('plugin_name')
        if not plugin_name:
            raise ValueError("配置文件中缺少 'plugin_name' 字段")
        # 获取对应的插件实例
        plugin_instance = self.plugins.get(plugin_name)
        if not plugin_instance:
            raise ValueError(f"未找到名为 '{plugin_name}' 的插件")

        # 定义 MapFunction，使用插件的处理逻辑
        class PluginMapFunction(MapFunction):
            def map(self, value):
                data = json.loads(value)
                return plugin_instance.process(data)

        processed_stream = kafka_stream.map(PluginMapFunction())
        # 添加 Redis 数据汇
        processed_stream.process(self.target)
