from pyflink.common import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, StreamTableEnvironment, DataTypes
from pyflink.table.expressions import col, lit

env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)
env_settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
t_env = StreamTableEnvironment.create(env, environment_settings=env_settings)

# 定义订单流和支付流
order_stream = t_env.from_elements(
    [(1, 'order_1', '2025-01-01 12:00:00'), (2, 'order_2', '2025-01-01 12:05:00')],
    ['order_id', 'order_name', 'order_time']
)

payment_stream = t_env.from_elements(
    [(1, 'payment_1', '2025-01-01 12:05:00'), (2, 'payment_2', '2025-01-01 12:30:00')],
    ['payment_order_id', 'payment_name', 'payment_time']
)


# 定义事件时间列（字符串转为 TIMESTAMP 类型）
order_stream = order_stream.add_columns(col('order_time').cast(DataTypes.TIMESTAMP(3)).alias('event_time')) \
                           .drop_columns(col('order_time'))
payment_stream = payment_stream.add_columns(col('payment_time').cast(DataTypes.TIMESTAMP(3)).alias('payment_event_time')) \
                               .drop_columns(col('payment_time'))

# Join 操作，限制 10 分钟时间窗口
result = order_stream.join(payment_stream) \
    .where((col('order_id') == col('payment_order_id')) &
           (col('event_time') + lit(600).seconds() >= col('payment_event_time'))) \
    .select(
        col('order_id'),
        col('order_name'),
        col('payment_name')
    )


print(order_stream.get_schema())
print(payment_stream.get_schema())

# Convert the result table to a DataStream with type_info
t_env.to_append_stream(result).print()
env.execute("Flink Job Execution")
