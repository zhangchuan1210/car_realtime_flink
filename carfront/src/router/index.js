import { createRouter, createWebHistory } from "vue-router";
import OilAverage from "../components/OilAverage.vue";
import AddressSummary from "../components/AddressSummary.vue";
import CarCount from "../components/CarCount.vue";
import PriceRange from "../components/PriceRange.vue";
import ScoreAverage from "../components/ScoreAverage.vue";
import Home from "../components/Home.vue";

const routes = [
  {
    path: '/',
    name: "Home",
    component: Home
  },
  {
    path: "/oilavg",
    name: "OilAverage",
    component: OilAverage,
  },
  {
    path: "/scoreavg",
    name: "ScoreAverage",
    component: ScoreAverage,
  },
  {
    path: "/addresssum",
    name: "AddressSummary",
    component: AddressSummary,
  },
  {
    path: "/carcount",
    name: "CarCount",
    component: CarCount,
  },
  {
    path: "/pricerange",
    name: "PriceRange",
    component: PriceRange,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
