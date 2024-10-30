// frontend/src/router/index.js
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
    component: () => import('@/views/SymbolAnalysis.vue'),
    props: true  // Wichtig für Parameter-Übergabe
  },
  // Fallback Route
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Optional: Navigation Guards
router.beforeEach((to, from, next) => {
  // Beispiel: Validiere Symbol-Format
  if (to.name === 'SymbolAnalysis' && to.params.symbol) {
    const symbol = to.params.symbol.toUpperCase()
    if (symbol !== to.params.symbol) {
      return next({ name: 'SymbolAnalysis', params: { symbol } })
    }
  }
  next()
})

export default router