<template>
  <div>
    <h2>汽车价格区间统计</h2>
    <div id="container" ref="chartContainer" style="height: 600px;"></div>
    <div id="message"></div>
  </div>
</template>

<script>
import * as echarts from "echarts";
import "echarts/theme/vintage";
import {io} from "socket.io-client";

export default {
  name: "PriceRange",
  data(){
    return {
      socket: null,  // WebSocket
      myChart: null, // ECharts 实例
      priceData:[28,89,90,35]
    };
  },
  methods:{
    // 初始化 ECharts
    initChart() {
        this.myChart = echarts.init(this.$refs.chartContainer, 'vintage');
        this.myChart.setOption({
          title: {
            text: "汽车价格区间统计",
            left: "center"
          },
          tooltip: {
            trigger: "item"
          },
          legend: {
            orient: "vertical",
            left: "left"
          },
          series: [
            {
              name: "价格区间",
              type: "pie",
              radius: "80%",
              data: this.priceData,
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: "rgba(0, 0, 0, 0.5)"
                }
              }
            }
          ]
        });
    },
    // WebSocket 连接处理
    connectWebSocket() {
        this.socket = io('http://localhost:5000')
        this.socket.onmessage = (event) => {
          this.priceData = JSON.parse(event.data);
          this.myChart.setOption({
            series: [{
              data: this.priceData
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
      if (this.socket) {
      this.socket.disconnect(); // 断开 WebSocket 连接
      }
  }
};
</script>

<style scoped>
  #container {
    width: 100%;
    height: 100%;
    margin-top: 120px;
  }
</style>
