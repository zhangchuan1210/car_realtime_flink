<template>
 <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>汽车大数据实时看板系统</title>
</head>
<div id="app">
    <router-view></router-view>
</div>
</template>
<script>
  export default {
  name: "App",
  setup() {
    // 定义组件数据和路由
    const stats = [
       {
        route: "/oilavg",
        img: "/oilavg.png",
        alt: "油耗统计",
        description: "汽车平均油耗统计",
      },
      {
        route: "/scoreavg",
        img: "./assets/scoreavg.png",
        alt: "评分统计",
        description: "汽车平均评分统计",
      },
      {
        route: "/addresssum",
        img: "./assets/addresssum.png",
        alt: "地址统计",
        description: "汽车地址统计",
      },
      {
        route: "/pricerange",
        img: "./assets/addresssum.png",
        alt: "价格区间统计",
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
</style>
