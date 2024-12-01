# config.py
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:zc142500@localhost/car'  # Hive 连接字符串
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    KAFKA_BROKER_URL = '172.28.228.235:9092'