<template>
  <div>
    <h2>按地域统计销售总量</h2>
    <div id="container" ref="chartContainer" style="height: 500px;"></div>
    <div id="message"></div>
  </div>
</template>

<script>
import { onMounted, ref, onBeforeUnmount } from "vue";
import * as echarts from "echarts";
import chinaMap from "../assets/china.json";

export default {
  name: "AddressSummary",
  setup() {
    const chartContainer = ref(null);
    let myChart = null;
    let websocket = null;

    // 地图坐标数据
    const geoCoordMap = {
      "海门": [121.15, 31.89],
      "鄂尔多斯": [109.781327, 39.608266],
      "招远": [120.38, 37.35],
      "舟山": [122.207216, 29.985295],
      "齐齐哈尔": [123.97, 47.33],
      "盐城": [120.13, 33.38],
      "赤峰": [118.87, 42.28],
      "青岛": [120.33, 36.07],
      "乳山": [121.52, 36.89],
      "金昌": [102.188043, 38.520089],
      "泉州": [118.58, 24.93],
      "莱西": [120.53, 36.86],
      "日照": [119.46, 35.42],
      "胶南": [119.97, 35.88],
      "南通": [121.05, 32.08],
      "拉萨": [91.11, 29.97],
      "云浮": [112.02, 22.93],
      "梅州": [116.1, 24.55],
      "文登": [122.05, 37.2],
      "上海": [121.48, 31.22],
      "攀枝花": [101.718637, 26.582347],
      "威海": [122.1, 37.5],
      "承德": [117.93, 40.97],
      "厦门": [118.1, 24.46],
      "汕尾": [115.375279, 22.786211],
      "潮州": [116.63, 23.68],
      "丹东": [124.37, 40.13],
      "太仓": [121.1, 31.45],
      "曲靖": [103.79, 25.51],
      "烟台": [121.39, 37.52],
      "福州": [119.3, 26.08],
      "瓦房店": [121.979603, 39.627114],
      "即墨": [120.45, 36.38],
      "抚顺": [123.97, 41.97],
      "玉溪": [102.52, 24.35],
      "张家口": [114.87, 40.82],
      "阳泉": [113.57, 37.85],
      "莱州": [119.942327, 37.177017],
      "湖州": [120.1, 30.86],
      "汕头": [116.69, 23.39],
      "昆山": [120.95, 31.39],
      "宁波": [121.56, 29.86],
      "湛江": [110.359377, 21.270708],
      "揭阳": [116.35, 23.55],
      "荣成": [122.41, 37.16],
      "连云港": [119.16, 34.59],
      "葫芦岛": [120.836932, 40.711052]
    };

    // 初始化 ECharts
    const initChart = () => {
      if (chartContainer.value) {
        myChart = echarts.init(chartContainer.value);
        echarts.registerMap("china", chinaMap);
        myChart.setOption({
          title: {
            text: "按地域统计销售总量",
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
              name: "销售数据",
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
        websocket = new WebSocket("ws://localhost:8080/address-sum-web-socket");
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
