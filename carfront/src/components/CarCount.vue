<template>
  <div>
    <h2>汽车销量统计</h2>
    <div id="container" ref="chartContainer" style="height: 500px;"></div>
    <div id="message"></div>
  </div>
</template>

<script>
import { onMounted, ref, onBeforeUnmount } from "vue";
import * as echarts from "echarts";
import chinaMap from "@/assets/china.json";

export default {
  name: "CarCount",
  setup() {
    const chartContainer = ref(null);
    let myChart = null;
    let websocket = null;

    // 地图坐标数据
    const geoCoordMap = {
      "北京": [116.407526, 39.90403],
      "上海": [121.473701, 31.230416],
      "广州": [113.264385, 23.129112],
      "深圳": [114.057868, 22.543099],
      "杭州": [120.15507, 30.274085]
    };

    // 初始化 ECharts
    const initChart = () => {
      if (chartContainer.value) {
        myChart = echarts.init(chartContainer.value);
        echarts.registerMap("china", chinaMap);
        myChart.setOption({
          title: {
            text: "汽车销量统计",
            left: "center"
          },
          tooltip: {
            trigger: "item"
          },
          geo: {
            map: "china",
            roam: true,
            label: {
              emphasis: {
                show: false
              }
            },
            itemStyle: {
              normal: {
                areaColor: "#323c48",
                borderColor: "#111"
              },
              emphasis: {
                areaColor: "#2a333d"
              }
            }
          },
          series: [
            {
              name: "汽车销量",
              type: "scatter",
              coordinateSystem: "geo",
              data: [],
              symbolSize: 10,
              label: {
                show: false
              },
              itemStyle: {
                color: "#ff8003"
              }
            },
            {
              name: "Top 5",
              type: "effectScatter",
              coordinateSystem: "geo",
              data: [],
              symbolSize: function (val) {
                return val[2] <= 20 ? val[2] : 20;
              },
              showEffectOn: "emphasis",
              rippleEffect: {
                brushType: "stroke"
              },
              hoverAnimation: true,
              label: {
                formatter: "{b}",
                position: "right",
                show: false
              },
              itemStyle: {
                color: "#0000FF",
                shadowBlur: 10,
                shadowColor: "#333"
              },
              zlevel: 1
            }
          ]
        });
      }
    };

    // WebSocket 连接处理
    const connectWebSocket = () => {
      if ("WebSocket" in window) {
        websocket = new WebSocket("ws://localhost:8080/car-count-web-socket");
        websocket.onmessage = (event) => {
          const data = JSON.parse(event.data);
          myChart.setOption({
            series: [
              {data: convertData(data)},
              {
                data: convertData(
                    data.sort((a, b) => b.value - a.value).slice(0, 5)
                )
              }
            ]
          });
        };
      } else {
        alert("当前浏览器不支持 WebSocket");
      }
    };

    // 数据转换函数
    const convertData = (data) => {
      return data.map((item) => {
        const coord = geoCoordMap[item.name];
        if (coord) {
          return {
            name: item.name,
            value: [...coord, item.value]
          };
        }
        return null;
      }).filter(item => item !== null);
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
