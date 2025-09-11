// // // src/router/index.js
// // import { createRouter, createWebHistory } from 'vue-router'
// // import { useAuthStore } from '@/stores/auth'
// // import LoginView from '@/views/LoginView.vue'
// // import MarketDashboard from '@/views/MarketDashboard.vue'
// // import SymbolAnalysis from '@/views/SymbolAnalysis.vue'
// //
// // const router = createRouter({
// //   history: createWebHistory(import.meta.env.BASE_URL),
// //   routes: [
// //     {
// //       path: '/',
// //       redirect: '/dashboard'  // Redirect zur Dashboard-Ansicht
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
// //       component: MarketDashboard,
// //       meta: { requiresAuth: true }
// //     },
// //     {
// //       path: '/symbol/:symbol',
// //       name: 'symbol-analysis',
// //       component: SymbolAnalysis,
// //       meta: { requiresAuth: true }
// //     }
// //   ]
// // })
// //
// // router.beforeEach(async (to, from, next) => {
// //   const authStore = useAuthStore()
// //
// //   if (authStore.token && !authStore.user) {
// //     await authStore.checkAuth()
// //   }
// //
// //   if (to.meta.requiresAuth && !authStore.isAuthenticated) {
// //     next({ name: 'login', query: { redirect: to.fullPath } })
// //     return
// //   }
// //
// //   next()
// // })
// //
// // export default router
//
//
//
// // src/router/index.js
// import { createRouter, createWebHistory } from 'vue-router'
// import { useAuthStore } from '@/stores/auth'
// import LoginView from '@/views/LoginView.vue'
// import MarketDashboard from '@/views/MarketDashboard.vue'
// import SymbolAnalysis from '@/views/SymbolAnalysis.vue'
// import NotFound from '@/views/NotFound.vue'
//
// const router = createRouter({
//   history: createWebHistory(import.meta.env.BASE_URL),
//   routes: [
//     {
//       path: '/',
//       redirect: '/dashboard'
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
//       path: '/symbol/:symbol',
//       name: 'symbol-analysis',
//       component: SymbolAnalysis,
//       meta: { requiresAuth: true }
//     },
//     // 404 Route - muss immer als letzte Route definiert sein
//     {
//       path: '/:pathMatch(.*)*',
//       name: 'not-found',
//       component: NotFound,
//       meta: { hideLayout: true }  // Kein Header auf 404-Seite
//     }
//   ]
// })
//
// router.beforeEach(async (to, from, next) => {
//   const authStore = useAuthStore()
//
//   if (authStore.token && !authStore.user) {
//     await authStore.checkAuth()
//   }
//
//   if (to.meta.requiresAuth && !authStore.isAuthenticated) {
//     next({ name: 'login', query: { redirect: to.fullPath } })
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
import axios from 'axios'
import LoginView from '@/views/LoginView.vue'
import MarketDashboard from '@/views/MarketDashboard.vue'
import SymbolAnalysis from '@/views/SymbolAnalysis.vue'
import AISettings from '@/views/AISettings.vue'
import NotFound from '@/views/NotFound.vue'

// Component für "Symbol nicht gefunden"
const SymbolNotFound = {
  template: `
    <div class="container mx-auto p-4">
      <div class="rounded-lg border bg-card p-8 text-center space-y-6">
        <h1 class="text-3xl font-bold">Symbol nicht gefunden</h1>
        <p class="text-xl text-muted-foreground">
          Das Symbol "{{ $route.params.symbol }}" konnte nicht gefunden werden.
        </p>
        <div class="space-y-2">
          <p class="text-muted-foreground">
            Mögliche Gründe:
          </p>
          <ul class="text-sm text-muted-foreground">
            <li>Das Symbol existiert nicht</li>
            <li>Tippfehler im Symbol</li>
            <li>Das Symbol wird nicht mehr gehandelt</li>
          </ul>
        </div>
        <div class="space-x-4">
          <button class="px-4 py-2 bg-primary text-primary-foreground rounded-md" 
                  @click="$router.push('/dashboard')">
            Zurück zum Dashboard
          </button>
        </div>
      </div>
    </div>
  `
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/dashboard'
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
      meta: { requiresAuth: true },
      beforeEnter: async (to, from, next) => {
        try {
          const token = localStorage.getItem('token')
          const response = await axios.get(`http://localhost:8000/api/v1/market/data/${to.params.symbol}`, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          })
          if (response.data) {
            next()
          } else {
            next({ name: 'symbol-not-found', params: { symbol: to.params.symbol } })
          }
        } catch (error) {
          next({ name: 'symbol-not-found', params: { symbol: to.params.symbol } })
        }
      }
    },
    {
      path: '/symbol-not-found/:symbol',
      name: 'symbol-not-found',
      component: SymbolNotFound,
      meta: { requiresAuth: true }
    },
    {
      path: '/ai-settings',
      name: 'ai-settings',
      component: AISettings,
      meta: { requiresAuth: true }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: NotFound,
      meta: { hideLayout: true }
    }
  ]
})

// Auth Navigation Guard
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