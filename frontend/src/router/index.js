// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/views/MarketDashboard.vue')
  },
  {
    path: '/symbol/:symbol',
    name: 'SymbolAnalysis',
    component: () => import('@/views/SymbolAnalysis.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router