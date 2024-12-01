import logging

from pyflink.datastream import StreamExecutionEnvironment

env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)
logging.basicConfig(level=logging.DEBUG)
data = env.from_collection([1, 2, 3, 4, 5])
try:
    data.map(lambda x: x*x).print()  # 故意加入异常
except Exception as e:
    print("Caught Exception:", e)

env.execute("example")
