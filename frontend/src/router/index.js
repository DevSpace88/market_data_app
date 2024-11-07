// // // frontend/src/router/index.js
// // import { createRouter, createWebHistory } from 'vue-router'
// //
// // const routes = [
// //   {
// //     path: '/',
// //     name: 'Dashboard',
// //     component: () => import('@/views/MarketDashboard.vue')
// //   },
// //   {
// //     path: '/symbol/:symbol',
// //     name: 'SymbolAnalysis',
// //     component: () => import('@/views/SymbolAnalysis.vue'),
// //     props: true  // Wichtig für Parameter-Übergabe
// //   },
// //   // Fallback Route
// //   {
// //     path: '/:pathMatch(.*)*',
// //     redirect: '/'
// //   }
// // ]
// //
// // const router = createRouter({
// //   history: createWebHistory(),
// //   routes
// // })
// //
// // // Optional: Navigation Guards
// // router.beforeEach((to, from, next) => {
// //   // Beispiel: Validiere Symbol-Format
// //   if (to.name === 'SymbolAnalysis' && to.params.symbol) {
// //     const symbol = to.params.symbol.toUpperCase()
// //     if (symbol !== to.params.symbol) {
// //       return next({ name: 'SymbolAnalysis', params: { symbol } })
// //     }
// //   }
// //   next()
// // })
// //
// // export default router
//
//
// // // src/router/index.js
// // import { createRouter, createWebHistory } from 'vue-router'
// // import { useAuthStore } from '@/stores/auth'
// // import HomeView from '@/views/HomeView.vue'
// // import LoginView from '@/views/LoginView.vue'
// // import MarketDashboard from '@/views/MarketDashboard.vue'
// //
// // const router = createRouter({
// //   history: createWebHistory(import.meta.env.BASE_URL),
// //   routes: [
// //     {
// //       path: '/',
// //       name: 'home',
// //       component: HomeView,
// //     },
// //     {
// //       path: '/login',
// //       name: 'login',
// //       component: LoginView,
// //       meta: { public: true, hideLayout: true }
// //     },
// //     {
// //       path: '/dashboard',
// //       name: 'dashboard',
// //       component: MarketDashboard,  // Verwendet MarketDashboard statt DashboardView
// //       meta: { requiresAuth: true }
// //     }
// //   ]
// // })
//
// import { createRouter, createWebHistory } from 'vue-router'
// import { useAuthStore } from '@/stores/auth'
// import HomeView from '@/views/HomeView.vue'
// import LoginView from '@/views/LoginView.vue'
// import MarketDashboard from '@/views/MarketDashboard.vue'
// import SymbolAnalysis from '@/views/SymbolAnalysis.vue'  // Deine existierende Komponente
//
// const router = createRouter({
//   history: createWebHistory(import.meta.env.BASE_URL),
//   routes: [
//     {
//       path: '/',
//       name: 'home',
//       component: HomeView,
//     },
//     {
//       path: '/login',
//       name: 'login',
//       component: LoginView,
//       meta: { public: true, hideLayout: true }
//     },
//     {
//       path: '/dashboard',
//       name: 'dashboard',
//       component: MarketDashboard,
//       meta: { requiresAuth: true }
//     },
//     {
//       path: '/symbol/:symbol',  // oder welchen Pfad du bevorzugst
//       name: 'symbol-analysis',
//       component: SymbolAnalysis,
//       meta: { requiresAuth: true }
//     }
//   ]
// })
//
// // Navigation Guard
// router.beforeEach(async (to, from, next) => {
//   const authStore = useAuthStore()
//
//   // Überprüfe Auth-Status wenn ein Token existiert
//   if (authStore.token && !authStore.user) {
//     await authStore.checkAuth()
//   }
//
//   // Handle protected routes
//   if (to.meta.requiresAuth && !authStore.isAuthenticated) {
//     next({ name: 'login', query: { redirect: to.fullPath } })
//     return
//   }
//
//   // Handle public only routes (like login)
//   if (to.meta.public && authStore.isAuthenticated) {
//     next({ name: 'dashboard' })
//     return
//   }
//
//   next()
// })
//
// export default router


// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import LoginView from '@/views/LoginView.vue'
import MarketDashboard from '@/views/MarketDashboard.vue'
import SymbolAnalysis from '@/views/SymbolAnalysis.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/dashboard'  // Redirect zur Dashboard-Ansicht
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { public: true, hideLayout: true }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: MarketDashboard,
      meta: { requiresAuth: true }
    },
    {
      path: '/symbol/:symbol',
      name: 'symbol-analysis',
      component: SymbolAnalysis,
      meta: { requiresAuth: true }
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  if (authStore.token && !authStore.user) {
    await authStore.checkAuth()
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
    return
  }

  next()
})

export default router