<template>
  <div
    style="
      text-align: center;
      background-image: url('./assets/car.jpg');
      background-size: cover;
      background-attachment: fixed;
      background-repeat: no-repeat;
    "
  >
    <!-- 顶部标题 -->
    <p
      align="center"
      style="font-size: 50px; background-color: rgba(255, 255, 255, 0.5); margin-bottom: 20px;"
    >
      汽车大数据实时看板系统
    </p>

    <!-- 主体内容 -->
    <div class="dashboard-grid">
      <router-link
        v-for="item in stats"
        :to="item.route"
        :key="item.route"
        class="dashboard-item"
      >
        <component :is="item.component" />
      </router-link>
    </div>
  </div>
</template>

<script>
import AddressSummary from "./components/AddressSummary.vue";
import CarCount from "./components/CarCount.vue";
import OilAverage from "./components/OilAverage.vue";
import PriceRange from "./components/PriceRange.vue";

export default {
  name: "App",
  components: {
    AddressSummary,
    CarCount,
    OilAverage,
    PriceRange,
  },
  setup() {
    // 定义组件数据和路由
    const stats = [
       {
        route: "/oilavg",
        img: "./assets/oilavg.png",
        alt: "油耗统计",
        component: OilAverage,
        description: "汽车平均油耗统计",
      },
      {
        route: "/scoreavg",
        img: "./assets/scoreavg.png",
        alt: "评分统计",
        component: AddressSummary,
        description: "汽车平均评分统计",
      },
      {
        route: "/addresssum",
        img: "./assets/addresssum.png",
        alt: "地址统计",
        component: CarCount,
        description: "汽车地址统计",
      },
      {
        route: "/pricerange",
        img: "./assets/addresssum.png",
        alt: "价格区间统计",
        component: PriceRange,
        description: "汽车价格区间统计",
      },
    ];

    return { stats };
  },
};
</script>

<style>
/* 全局样式 */
body {
  margin: 0;
  font-family: Arial, sans-serif;
}

/* 网格布局 */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr); /* 两列 */
  grid-gap: 20px; /* 项目间距 */
  padding: 20px;
  justify-items: center;
}

/* 每个网格项目的样式 */
.dashboard-item {
  width: 400px;
  height: 300px;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none; /* 去除链接样式 */
  color: inherit;
  transition: transform 0.2s ease-in-out;
}

.dashboard-item:hover {
  transform: scale(1.05); /* 鼠标悬停放大 */
}
</style>
