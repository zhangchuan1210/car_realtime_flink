<template>
  <div>
    <h2>汽车平均评分统计</h2>
    <div id="container" ref="chartContainer" style="height: 600px;"></div>
    <div id="message"></div>
  </div>
</template>

<script>
import * as echarts from "echarts";
import "echarts/theme/vintage";
import {io} from "socket.io-client";

export default {
  name: "ScoreAverage",
  data(){
     return {
      websocket: null,  // WebSocket
      myChart: null, // ECharts 实例
      carNameList:[28,89,90,35],
       scoreAvgList:[34.4,56.7,45.8,89.9]
    };
  },
  methods: {
    // 初始化 ECharts
    initChart() {
        this.myChart = echarts.init(this.$refs.chartContainer, 'vintage');
        this.myChart.setOption({
          title: {
            text: "汽车平均评分统计",
            left: 10
          },
          toolbox: {
            feature: {
              dataZoom: {
                yAxisIndex: false
              },
              saveAsImage: {
                pixelRatio: 2
              }
            }
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
          dataZoom: [
            {
              type: "inside",
              yAxisIndex: [0],
              left: "1%"
            },
            {
              type: "slider",
              yAxisIndex: [0]
            }
          ],
          yAxis: {
            data: this.carNameList,
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
              data: this.scoreAvgList,
              large: true
            }
          ]
        });
    },

    // WebSocket 连接处理
    connectWebSocket() {
      this.websocket = io('http://localhost:5000');
      this.websocket.onmessage = (event) => {
          const jsonbean = JSON.parse(event.data);
          this.myChart.setOption({
            yAxis: {
              data: jsonbean.carNameList
            },
            series: [{
              data: jsonbean.scoreAvgList
            }]
          });
        };

    }

  },
  mounted() {
      this.initChart();
      this.connectWebSocket();
  },
  beforeUnmount(){
      if (this.websocket) {
        this.websocket.close();
      }
  }
};
</script>

<style scoped>
  #container {
    width: 100%;
    height: 500px;
    margin-top: 20px;
  }
</style>
