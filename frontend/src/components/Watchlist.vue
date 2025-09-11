<template>
  <div class="watchlist-container">
    <div class="watchlist-header">
      <h2 class="text-2xl font-bold mb-4">Meine Watchlist</h2>
      <div class="flex gap-2 mb-4">
        <input
          v-model="newSymbol"
          @keyup.enter="addToWatchlist"
          placeholder="Symbol hinzufügen (z.B. AAPL)"
          class="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          @click="addToWatchlist"
          :disabled="!newSymbol || isLoading"
          class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
          {{ isLoading ? 'Hinzufügen...' : 'Hinzufügen' }}
        </button>
      </div>
    </div>

    <div v-if="error" class="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
      {{ error }}
    </div>

    <div v-if="watchlist.length === 0" class="text-center py-8 text-gray-500">
      <p>Keine Symbole in der Watchlist. Fügen Sie welche hinzu!</p>
    </div>

    <div v-else class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="item in watchlist"
        :key="item.id"
        class="bg-white rounded-lg shadow-md p-4 border border-gray-200 hover:shadow-lg transition-shadow"
      >
        <div class="flex justify-between items-start mb-2">
          <div>
            <h3 class="text-lg font-semibold text-gray-900">
              {{ item.display_name || item.symbol }}
            </h3>
            <p class="text-sm text-gray-600">{{ item.symbol }}</p>
          </div>
          <button
            @click="removeFromWatchlist(item.id)"
            class="text-red-500 hover:text-red-700 p-1"
            title="Entfernen"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <div v-if="item.current_price" class="space-y-1">
          <div class="flex justify-between">
            <span class="text-sm text-gray-600">Aktueller Preis:</span>
            <span class="font-semibold">${{ item.current_price.toFixed(2) }}</span>
          </div>
          <div v-if="item.price_change !== null" class="flex justify-between">
            <span class="text-sm text-gray-600">Änderung:</span>
            <span :class="item.price_change >= 0 ? 'text-green-600' : 'text-red-600'">
              {{ item.price_change >= 0 ? '+' : '' }}{{ item.price_change.toFixed(2) }}
              ({{ item.price_change_percent?.toFixed(2) }}%)
            </span>
          </div>
          <div v-if="item.volume" class="flex justify-between">
            <span class="text-sm text-gray-600">Volumen:</span>
            <span class="text-sm">{{ formatNumber(item.volume) }}</span>
          </div>
        </div>

        <div v-else class="text-sm text-gray-500">
          Marktdaten nicht verfügbar
        </div>

        <div class="mt-3 flex gap-2">
          <button
            @click="viewDetails(item.symbol)"
            class="flex-1 px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded hover:bg-gray-200"
          >
            Details anzeigen
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'Watchlist',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const watchlist = ref([])
    const newSymbol = ref('')
    const isLoading = ref(false)
    const error = ref('')

    const fetchWatchlist = async () => {
      try {
        const response = await fetch('/api/v1/watchlist/with-data', {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        if (!response.ok) {
          throw new Error('Failed to fetch watchlist')
        }
        
        watchlist.value = await response.json()
      } catch (err) {
        console.error('Error fetching watchlist:', err)
        error.value = 'Fehler beim Laden der Watchlist'
      }
    }

    const addToWatchlist = async () => {
      if (!newSymbol.value.trim()) return
      
      isLoading.value = true
      error.value = ''
      
      try {
        const response = await fetch('/api/v1/watchlist/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authStore.token}`
          },
          body: JSON.stringify({
            symbol: newSymbol.value.trim().toUpperCase()
          })
        })
        
        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.detail || 'Failed to add symbol')
        }
        
        newSymbol.value = ''
        await fetchWatchlist()
      } catch (err) {
        console.error('Error adding to watchlist:', err)
        error.value = err.message
      } finally {
        isLoading.value = false
      }
    }

    const removeFromWatchlist = async (watchlistId) => {
      try {
        const response = await fetch(`/api/v1/watchlist/${watchlistId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })
        
        if (!response.ok) {
          throw new Error('Failed to remove symbol')
        }
        
        await fetchWatchlist()
      } catch (err) {
        console.error('Error removing from watchlist:', err)
        error.value = 'Fehler beim Entfernen des Symbols'
      }
    }

    const viewDetails = (symbol) => {
      router.push(`/analysis/${symbol}`)
    }

    const formatNumber = (num) => {
      if (num >= 1e9) return (num / 1e9).toFixed(1) + 'B'
      if (num >= 1e6) return (num / 1e6).toFixed(1) + 'M'
      if (num >= 1e3) return (num / 1e3).toFixed(1) + 'K'
      return num.toString()
    }

    onMounted(() => {
      fetchWatchlist()
    })

    return {
      watchlist,
      newSymbol,
      isLoading,
      error,
      addToWatchlist,
      removeFromWatchlist,
      viewDetails,
      formatNumber
    }
  }
}
</script>

<style scoped>
.watchlist-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

.watchlist-header {
  margin-bottom: 1.5rem;
}
</style>
