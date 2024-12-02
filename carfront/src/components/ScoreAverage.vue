<template>
  <div>
    <h2>汽车平均评分统计</h2>
    <div id="container" ref="chartContainer" style="height: 200%;"></div>
    <div id="message"></div>
  </div>
</template>

<script>
import { onMounted, ref, onBeforeUnmount } from "vue";
import * as echarts from "echarts";
import "echarts/theme/vintage";

export default {
  name: "ScoreAverage",
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
            data: [],
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
              data: [],
              large: true
            }
          ]
        });
      }
    };

    // WebSocket 连接处理
    const connectWebSocket = () => {
      if ("WebSocket" in window) {
        websocket = new WebSocket("ws://localhost:8080/score-avg-web-socket");
        websocket.onmessage = (event) => {
          const jsonbean = JSON.parse(event.data);
          myChart.setOption({
            yAxis: {
              data: jsonbean.carNameList
            },
            series: [{
              data: jsonbean.scoreAvgList
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
