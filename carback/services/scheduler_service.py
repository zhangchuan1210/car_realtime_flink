import threading

import json
from services.car_service import CarService
from util.KafkaUtil import KafkaUtil


class SchedulerService:
    def consume_itcast_order_stream(self):
        # {"c_name": "423", "oil_consume": 2.8}
        print("消费线程运行")

    def consume_itcast_order(self):
        task_thread = threading.Thread(target=self.consume_itcast_order_stream, daemon=True)
        task_thread.start()
        print("Thread started, Flask app will now run.")

    # 从 MySQL 读取数据并发送到 Kafka
    def produce_itcast_order(self):
        global count
        topics = "itcast_order"
        # 计数器
        count = 0
        try:
            result = CarService().get_all_cars()
            if result:
                # 将数据转换为 JSON 格式并发送到 Kafka
                messages = json.dumps(result)
                for message in messages:
                    KafkaUtil.createKafkaProducer().send(topics, value=message)
                    print("数据发送到 Kafka: {message}")
                    count += 1  # 更新计数器
                print("发送数据条数为：" + str(count))
            else:
                print("未找到符合条件的数据。")
        except Exception as e:
            print("发生错误: {e}" + e)
