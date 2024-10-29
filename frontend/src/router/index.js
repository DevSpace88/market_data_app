import { createRouter, createWebHistory } from 'vue-router'
import MarketDashboard from '../views/MarketDashboard.vue'
import SymbolAnalysis from '../views/SymbolAnalysis.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: MarketDashboard
  },
  {
    path: '/symbol/:symbol',
    name: 'SymbolAnalysis',
    component: SymbolAnalysis,
    props: true
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router