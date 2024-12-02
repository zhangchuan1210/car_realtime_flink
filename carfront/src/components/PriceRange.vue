<template>
  <div>
    <h2>汽车价格区间统计</h2>
    <div id="container" ref="chartContainer" style="height: 100%;"></div>
    <div id="message"></div>
  </div>
</template>

<script>
import { onMounted, ref, onBeforeUnmount } from "vue";
import * as echarts from "echarts";
import "echarts/theme/vintage";

export default {
  name: "PriceRange",
  setup() {
    const chartContainer = ref(null);
    let myChart = null;
    let websocket = null;

    // 初始化 ECharts
    const initChart = () => {
      if (chartContainer.value) {
        myChart = echarts.init(chartContainer.value, 'vintage');
        myChart.setOption({
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
              radius: "50%",
              data: [],
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
      }
    };

    // WebSocket 连接处理
    const connectWebSocket = () => {
      if ("WebSocket" in window) {
        websocket = new WebSocket("ws://localhost:8080/price-range-web-socket");
        websocket.onmessage = (event) => {
          const data = JSON.parse(event.data);
          myChart.setOption({
            series: [{
              data: data
            }]
          });
        };
      } else {
        alert("当前浏览器不支持 WebSocket");
      }
    };

    onMounted(() => {
      initChart();
      connectWebSocket();
    });

    onBeforeUnmount(() => {
      if (websocket) {
        websocket.close();
      }
    });

    return {
      chartContainer
    };
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
