from flask import Flask
from pyflink.table import EnvironmentSettings, TableEnvironment
from pyflink.table.expressions import col

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'



env_settings = EnvironmentSettings.new_instance().in_batch_mode().build()
table_env = TableEnvironment.create(environment_settings=env_settings)

# 定义输入数据
data = [(1,), (2,), (3,), (4,), (5,)]
schema = ['number']

# 将数据转换为表
source_table = table_env.from_elements(data, schema)

# 定义查询逻辑：计算平方
result_table = source_table.select(col("number"), (col("number") * col("number")).alias("squared"))

# 打印结果
result_table.execute().print()
if __name__ == '__main__':
    app.run()
