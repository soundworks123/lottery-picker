import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import(
      /* webpackChunkName: "home" */
      /* webpackPrefetch: true */
      '../views/HomeView.vue'
    ),
  },
  {
    path: '/lottery',
    name: 'Lottery',
    component: () => import(
      /* webpackChunkName: "lottery" */
      /* webpackPrefetch: true */
      '../views/LotteryView.vue'
    ),
  },
  {
    path: '/analysis',
    name: 'Analysis',
    component: () => import(
      /* webpackChunkName: "analysis" */
      /* webpackPrefetch: true */
      '../views/AnalysisView.vue'
    ),
  },
  {
    path: '/prediction',
    name: 'Prediction',
    component: () => import(
      /* webpackChunkName: "prediction" */
      /* webpackPrefetch: true */
      '../views/PredictionView.vue'
    ),
  },
  {
    path: '/discussion',
    name: 'Discussion',
    component: () => import(
      /* webpackChunkName: "discussion" */
      /* webpackPrefetch: true */
      '../views/DiscussionView.vue'
    ),
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
  // 滚动行为
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { x: 0, y: 0 }
    }
  },
})

export default router
