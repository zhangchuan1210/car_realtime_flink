import importlib
import json
import os
import pkgutil

from flask import Flask
from flask_cors import CORS
from pyflink.common import SimpleStringSchema
from pyflink.datastream.connectors.kafka import KafkaSource

from FlinkJobThread import FlinkJobThread
from config import Config
from extensions import db
from processing_plugins.base import ProcessingPlugin
from util.RedisSinkUtil import RedisSinkUtil


def load_plugins(plugin_directory):
    plugins = {}
    for finder, name, ispkg in pkgutil.iter_modules([plugin_directory]):
        module_name = "processing_plugins."+name
        module = importlib.import_module(module_name)
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and issubclass(attr, ProcessingPlugin) and attr is not ProcessingPlugin:
                plugin_instance = attr()
                plugins[name] = plugin_instance
    return plugins

def create_kafka():
    kafka_source = KafkaSource.builder() \
        .set_bootstrap_servers(Config.KAFKA_BROKER_URL) \
        .set_topics("input_topic") \
        .set_group_id("flink_group") \
        .set_value_only_deserializer(SimpleStringSchema()) \
        .build()
    return kafka_source
def create_app():
    # 读取配置文件
    with open('.\\carback\\job_config.json', 'r') as f:
        config = json.load(f)
    # 插件目录
    plugin_directory = os.path.join(os.path.dirname(__file__), 'processing_plugins')
    # 加载插件
    plugins = load_plugins(plugin_directory)
    print("已加载的插件：{list(plugins.keys())}")
    # 创建 Flink 作业线程，传入配置对象和插件字典
    flink_thread = FlinkJobThread(job_name="My Flink Job",config=config, plugins=plugins,source=create_kafka(),target=RedisSinkUtil.write_to_redis)
    # 启动 Flink 作业线程
    flink_thread.start()
    app = Flask(__name__)
    app.config.from_object(Config)
    # 初始化数据库
    db.init_app(app)
    CORS(app)
    # 注册控制器
    from controllers.scheduler_controller import schedular_controller
    from controllers.car_controller import page_controller
    app.register_blueprint(schedular_controller)
    app.register_blueprint(page_controller)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, threaded=True)
