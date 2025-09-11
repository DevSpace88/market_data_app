<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-3xl font-bold">Market Dashboard</h2>
      <!-- <div class="flex items-center gap-3">
        <SymbolSearch :on-add="addToWatchlist" />
      </div> -->
    </div>

    <!-- Watchlist Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <Card
        v-for="symbol in watchlist"
        :key="symbol"
        class="hover:shadow-lg transition-all cursor-pointer group"
        @click="navigateToSymbol(symbol)"
      >
        <CardHeader class="pb-4">
          <div class="flex justify-between items-center">
            <CardTitle class="text-lg">{{ symbol }}</CardTitle>
            <svg class="w-5 h-5 text-muted-foreground group-hover:text-foreground transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </div>
        </CardHeader>
      </Card>
    </div>

    <!-- Hot Stocks Table -->
    <div class="mt-8">
      <HotStocks @watchlist-changed="fetchCustomWatchlist" />
    </div>

    <!-- Custom Watchlist Grid -->
    <div v-if="customWatchlist.length > 0" class="mt-8">
      <h3 class="text-xl font-semibold mb-4">Meine Symbole</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
        <Card
          v-for="item in customWatchlist"
          :key="item.id"
          class="hover:shadow-lg transition-all cursor-pointer group"
          @click="navigateToSymbol(item.symbol)"
        >
          <CardHeader class="pb-4">
            <div class="flex justify-between items-center">
              <div class="flex-1">
                <CardTitle class="text-lg">{{ item.symbol }}</CardTitle>
                <CardDescription class="text-sm text-muted-foreground">
                  {{ item.display_name || 'Benutzerdefiniert' }}
                </CardDescription>
              </div>
              <div class="flex items-center gap-2">
                <svg class="w-5 h-5 text-muted-foreground group-hover:text-foreground transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
                <button
                  @click.stop="removeFromWatchlist(item.id)"
                  class="text-destructive hover:text-destructive/80 p-1 opacity-0 group-hover:opacity-100 transition-opacity"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                </button>
              </div>
            </div>
          </CardHeader>
        </Card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { Card, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
// import SymbolSearch from '@/components/SymbolSearch.vue'
import HotStocks from '@/components/HotStocks.vue'

const router = useRouter()
const authStore = useAuthStore()

// Standard-Beispiele wie vorher
const watchlist = ref(['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA'])

// Benutzerdefinierte Watchlist
const customWatchlist = ref([])
const isLoading = ref(false)
const error = ref('')

const fetchCustomWatchlist = async () => {
  try {
    const response = await fetch('/api/v1/watchlist/', {
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })
    
    if (response.ok) {
      customWatchlist.value = await response.json()
    }
  } catch (err) {
    console.error('Error fetching custom watchlist:', err)
    // Ignoriere Fehler, da die API möglicherweise nicht verfügbar ist
  }
}

// const addToWatchlist = async (symbol, displayName = null) => {
//   if (!symbol.trim()) return
  
//   isLoading.value = true
//   error.value = ''
  
//   try {
//     const response = await fetch('/api/v1/watchlist/', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//         'Authorization': `Bearer ${authStore.token}`
//       },
//       body: JSON.stringify({
//         symbol: symbol.trim().toUpperCase(),
//         display_name: displayName
//       })
//     })
    
//     if (!response.ok) {
//       const errorData = await response.json()
//       throw new Error(errorData.detail || 'Failed to add symbol')
//     }
    
//     await fetchCustomWatchlist()
//   } catch (err) {
//     console.error('Error adding to watchlist:', err)
//     error.value = err.message
//     throw err // Re-throw für SymbolSearch-Komponente
//   } finally {
//     isLoading.value = false
//   }
// }

const removeFromWatchlist = async (watchlistId) => {
  try {
    const response = await fetch(`/api/v1/watchlist/${watchlistId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })
    
    if (response.ok) {
      await fetchCustomWatchlist()
    }
  } catch (err) {
    console.error('Error removing from watchlist:', err)
    error.value = 'Fehler beim Entfernen des Symbols'
  }
}

const navigateToSymbol = (symbol) => {
  router.push(`/symbol/${symbol}`)
}

onMounted(() => {
  fetchCustomWatchlist()
})
</script>