from kafka import KafkaProducer, KafkaConsumer
from config import Config


class KafkaUtil(object):
    @staticmethod
    def createKafkaConsumer(topic_name):
        consumer = KafkaConsumer(topic_name, bootstrap_servers=Config.KAFKA_BROKER_URL)
        return consumer

    @staticmethod
    def createKafkaProducer():
        producer = KafkaProducer(bootstrap_servers=Config.KAFKA_BROKER_URL)
        return producer
