<template>
  <div>
    <h2>汽车平均油耗统计</h2>
    <div id="container" ref="chartContainer" style="height: 400px;"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import { io } from 'socket.io-client';

export default {
  name: 'OilAverage',
  data() {
    return {
      socket: null,  // WebSocket
      myChart: null, // ECharts 实例
      carNames: ['byd','tesla'],   // 汽车名称列表
      oilAvg: ['23','25'],     // 汽车油耗列表
    };
  },
  methods: {
    // 初始化 ECharts 图表
     initChart() {
      if (this.$refs.chartContainer) {
        this.myChart = echarts.init(this.$refs.chartContainer, 'vintage');
        this.myChart.setOption({
          title: {
            text: "汽车平均油耗统计",
            subtext: "注：油耗为 0 的为新能源汽车",
            left: 10
          },
          tooltip: {
            trigger: "axis",
            axisPointer: {
              type: "shadow"
            }
          },
          grid: {
            bottom: 90
          },
          yAxis: {
            data: this.carNames,
            silent: false,
            splitLine: {
              show: false
            },
            splitArea: {
              show: false
            }
          },
          xAxis: {
            splitArea: {
              show: false
            }
          },
          series: [
            {
              type: "bar",
              data: this.oilAvg,
              large: true
            }
          ]
        });
      }
  },

    // 连接到 WebSocket 服务
    connectToSocket() {
      this.socket = io('http://localhost:5000'); // 替换为实际的 WebSocket 服务地址
      // 监听 WebSocket 消息
      this.socket.on('message', (data) => {
        console.log('Received from server:', data);
        // 假设 data 是一个包含车名和油耗数据的对象
        const { carNames, oilAvg } = data;
        // 更新 carNames 和 oilAvg
        this.carNames = carNames;
        this.oilAvg = oilAvg;
        // 更新图表
        this.updateChart();
      });
    },

    // 更新 ECharts 图表
    updateChart() {
      if (this.myChart) {
        this.myChart.setOption({
          xAxis: {
            data: this.carNames, // 更新 x 轴数据
          },
          series: [
            {
              data: this.oilAvg, // 更新 y 轴数据
            },
          ],
        });
      }
    },
  },

  mounted() {
    this.initChart(); // 初始化图表
    this.connectToSocket(); // 连接到 WebSocket
  },

  beforeUnmount() {
    if (this.socket) {
      this.socket.disconnect(); // 断开 WebSocket 连接
    }
  },
};
</script>

<style scoped>
#container {
  width: 100%;
  height: 400px;
  margin-top: 20px;
}
</style>
