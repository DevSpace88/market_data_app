<template>
  <div class="space-y-4">
    <div class="flex justify-between items-center">
      <h3 class="text-xl font-semibold">Hot Stocks</h3>
      <div class="flex items-center gap-2">
        <select 
          v-model="sortBy" 
          @change="sortStocks"
          class="px-3 py-1 border border-input rounded-md bg-background text-foreground text-sm"
        >
          <option value="change_percent">Preisänderung %</option>
          <option value="volume">Volumen</option>
          <option value="price">Preis</option>
          <option value="symbol">Symbol</option>
        </select>
        <button
          @click="toggleSortOrder"
          class="p-1 hover:bg-accent rounded-md transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12"></path>
          </svg>
        </button>
        <button
          @click="refreshData"
          :disabled="isLoading"
          class="p-1 hover:bg-accent rounded-md transition-colors"
        >
          <svg v-if="isLoading" class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
          </svg>
          <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
          </svg>
        </button>
      </div>
    </div>

    <div class="bg-card rounded-lg border overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-muted/50">
            <tr>
              <th class="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Symbol</th>
              <th class="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Preis</th>
              <th class="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Änderung</th>
              <th class="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Volumen</th>
              <th class="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Chart</th>
              <th class="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Aktion</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border">
            <tr 
              v-for="stock in sortedStocks" 
              :key="stock.symbol"
              class="hover:bg-muted/50 transition-colors cursor-pointer"
              @click="navigateToSymbol(stock.symbol)"
            >
              <td class="px-4 py-3">
                <div class="flex items-center gap-2">
                  <div class="font-medium">{{ stock.symbol }}</div>
                  <div class="text-xs text-muted-foreground">{{ stock.name }}</div>
                </div>
              </td>
              <td class="px-4 py-3">
                <div class="font-medium">${{ formatNumber(stock.price) }}</div>
              </td>
              <td class="px-4 py-3">
                <div class="flex items-center gap-1">
                  <span 
                    class="text-sm font-medium"
                    :class="stock.change_percent >= 0 ? 'text-green-600' : 'text-red-600'"
                  >
                    {{ stock.change_percent >= 0 ? '+' : '' }}{{ stock.change_percent.toFixed(2) }}%
                  </span>
                  <span 
                    class="text-xs"
                    :class="stock.change_percent >= 0 ? 'text-green-600' : 'text-red-600'"
                  >
                    ({{ stock.change_percent >= 0 ? '+' : '' }}${{ formatNumber(stock.change) }})
                  </span>
                </div>
              </td>
              <td class="px-4 py-3">
                <div class="text-sm text-muted-foreground">
                  {{ formatVolume(stock.volume) }}
                </div>
              </td>
              <td class="px-4 py-3">
                <div class="w-16 h-8">
                  <MiniChart :data="stock.chartData" :isPositive="stock.change_percent >= 0" />
                </div>
              </td>
              <td class="px-4 py-3">
                <button
                  @click.stop="toggleWatchlist(stock)"
                  class="p-1 hover:bg-accent rounded-md transition-colors"
                  :class="stock.inWatchlist ? 'text-destructive' : 'text-muted-foreground'"
                >
                  <svg v-if="stock.inWatchlist" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                  </svg>
                  <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                  </svg>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import MiniChart from '@/components/MiniChart.vue'

const router = useRouter()
const authStore = useAuthStore()

const emit = defineEmits(['watchlist-changed'])

const stocks = ref([])
const sortBy = ref('change_percent')
const sortOrder = ref('desc')
const isLoading = ref(false)

// Mock data für Hot Stocks (in einer echten App würde das von einer API kommen)
const mockStocks = [
  {
    symbol: 'NVDA',
    name: 'NVIDIA Corporation',
    price: 875.50,
    change: 45.20,
    change_percent: 5.45,
    volume: 45234567,
    chartData: [820, 835, 845, 860, 875, 870, 875],
    inWatchlist: false
  },
  {
    symbol: 'TSLA',
    name: 'Tesla Inc.',
    price: 245.80,
    change: -12.30,
    change_percent: -4.76,
    volume: 67890123,
    chartData: [258, 252, 248, 245, 242, 247, 245],
    inWatchlist: false
  },
  {
    symbol: 'AAPL',
    name: 'Apple Inc.',
    price: 195.25,
    change: 8.75,
    change_percent: 4.69,
    volume: 34567890,
    chartData: [186, 189, 192, 195, 198, 196, 195],
    inWatchlist: false
  },
  {
    symbol: 'AMZN',
    name: 'Amazon.com Inc.',
    price: 158.90,
    change: -3.20,
    change_percent: -1.97,
    volume: 23456789,
    chartData: [162, 160, 159, 158, 157, 159, 158],
    inWatchlist: false
  },
  {
    symbol: 'GOOGL',
    name: 'Alphabet Inc.',
    price: 142.15,
    change: 6.80,
    change_percent: 5.02,
    volume: 12345678,
    chartData: [135, 138, 140, 142, 145, 143, 142],
    inWatchlist: false
  },
  {
    symbol: 'MSFT',
    name: 'Microsoft Corporation',
    price: 425.60,
    change: 12.40,
    change_percent: 3.00,
    volume: 18765432,
    chartData: [413, 418, 422, 425, 428, 426, 425],
    inWatchlist: false
  },
  {
    symbol: 'META',
    name: 'Meta Platforms Inc.',
    price: 485.30,
    change: -8.90,
    change_percent: -1.80,
    volume: 15678901,
    chartData: [494, 490, 487, 485, 482, 484, 485],
    inWatchlist: false
  },
  {
    symbol: 'NFLX',
    name: 'Netflix Inc.',
    price: 625.40,
    change: 25.60,
    change_percent: 4.27,
    volume: 9876543,
    chartData: [600, 610, 615, 620, 625, 623, 625],
    inWatchlist: false
  }
]

const sortedStocks = computed(() => {
  const sorted = [...stocks.value].sort((a, b) => {
    let aVal = a[sortBy.value]
    let bVal = b[sortBy.value]
    
    if (sortBy.value === 'symbol') {
      aVal = aVal.toLowerCase()
      bVal = bVal.toLowerCase()
    }
    
    if (sortOrder.value === 'asc') {
      return aVal > bVal ? 1 : -1
    } else {
      return aVal < bVal ? 1 : -1
    }
  })
  
  return sorted
})

const formatNumber = (num) => {
  return num ? Number(num).toFixed(2) : '0.00'
}

const formatVolume = (volume) => {
  if (volume >= 1e9) return (volume / 1e9).toFixed(1) + 'B'
  if (volume >= 1e6) return (volume / 1e6).toFixed(1) + 'M'
  if (volume >= 1e3) return (volume / 1e3).toFixed(1) + 'K'
  return volume.toString()
}

const toggleSortOrder = () => {
  sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
}

const sortStocks = () => {
  // Sorting wird automatisch durch computed property gehandhabt
}

const navigateToSymbol = (symbol) => {
  router.push(`/symbol/${symbol}`)
}

const toggleWatchlist = async (stock) => {
  try {
    if (stock.inWatchlist) {
      // Remove from watchlist
      const response = await fetch(`/api/v1/watchlist/${stock.watchlistId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      })
      
      if (response.ok) {
        stock.inWatchlist = false
        stock.watchlistId = null
        // Emit event to parent to refresh watchlist
        emit('watchlist-changed')
      }
    } else {
      // Add to watchlist
      const response = await fetch('/api/v1/watchlist/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authStore.token}`
        },
        body: JSON.stringify({
          symbol: stock.symbol,
          display_name: stock.name
        })
      })
      
      if (response.ok) {
        const newItem = await response.json()
        stock.inWatchlist = true
        stock.watchlistId = newItem.id
        // Emit event to parent to refresh watchlist
        emit('watchlist-changed')
      }
    }
  } catch (err) {
    console.error('Error toggling watchlist:', err)
  }
}

const checkWatchlistStatus = async () => {
  try {
    const response = await fetch('/api/v1/watchlist/', {
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })
    
    if (response.ok) {
      const watchlist = await response.json()
      // Update watchlist status for each stock
      stocks.value.forEach(stock => {
        const watchlistItem = watchlist.find(item => item.symbol === stock.symbol)
        if (watchlistItem) {
          stock.inWatchlist = true
          stock.watchlistId = watchlistItem.id
        } else {
          stock.inWatchlist = false
          stock.watchlistId = null
        }
      })
    }
  } catch (err) {
    console.error('Error checking watchlist status:', err)
  }
}

const refreshData = async () => {
  isLoading.value = true
  // Simuliere API-Aufruf
  setTimeout(() => {
    // In einer echten App würde hier die API aufgerufen werden
    stocks.value = [...mockStocks]
    checkWatchlistStatus()
    isLoading.value = false
  }, 1000)
}

onMounted(() => {
  stocks.value = [...mockStocks]
  checkWatchlistStatus()
})
</script>
