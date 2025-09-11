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
          class="hover:shadow-lg transition-all cursor-pointer group fade-in"
          @click="navigateToSymbol(item.symbol)"
        >
          <CardHeader class="pb-4">
            <div class="flex justify-between items-center">
              <div class="flex-1">
                <CardTitle class="text-lg">{{ item.symbol }}</CardTitle>
                <CardDescription class="text-sm text-muted-foreground">
                  {{ item.display_name || 'Benutzerdefiniert' }}
                </CardDescription>
                
                <!-- Chart Icon mit Prozentanzeige -->
                <div class="flex items-center gap-2 mt-2">
                  <div class="relative w-12 h-8">
                    <svg class="w-full h-full" viewBox="0 0 100 40" fill="none">
                      <!-- Chart Background -->
                      <rect width="100" height="40" fill="hsl(var(--muted))" rx="2"/>
                      
                      <!-- Chart Line -->
                      <path 
                        :d="getChartPath(item.symbol)" 
                        stroke="currentColor" 
                        stroke-width="2" 
                        fill="none"
                        :class="getChartColor(item.symbol)"
                      />
                      
                      <!-- Data Points -->
                      <circle 
                        v-for="(point, index) in getChartPoints(item.symbol)" 
                        :key="index"
                        :cx="point.x" 
                        :cy="point.y" 
                        r="1.5" 
                        :class="getChartColor(item.symbol)"
                        fill="currentColor"
                      />
                    </svg>
                  </div>
                  
                  <!-- Prozentanzeige -->
                  <div class="flex items-center gap-1">
                    <span 
                      class="text-sm font-medium"
                      :class="getPercentageColor(item.symbol)"
                    >
                      {{ getPercentageChange(item.symbol) }}
                    </span>
                    <svg 
                      v-if="getPercentageChange(item.symbol).startsWith('+')" 
                      class="w-3 h-3 text-green-500" 
                      fill="none" 
                      stroke="currentColor" 
                      viewBox="0 0 24 24"
                    >
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 17l9.2-9.2M17 17V7H7"/>
                    </svg>
                    <svg 
                      v-else-if="getPercentageChange(item.symbol).startsWith('-')" 
                      class="w-3 h-3 text-red-500" 
                      fill="none" 
                      stroke="currentColor" 
                      viewBox="0 0 24 24"
                    >
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 7l-9.2 9.2M7 7v10h10"/>
                    </svg>
                  </div>
                </div>
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

// Chart-Daten für Watchlist-Symbole
const watchlistChartData = ref({})

const fetchCustomWatchlist = async () => {
  try {
    const response = await fetch('/api/v1/watchlist/', {
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })
    
      if (response.ok) {
        customWatchlist.value = await response.json()
        // Lade Chart-Daten für alle Symbole parallel
        await loadWatchlistChartData()
      }
  } catch (err) {
    console.error('Error fetching custom watchlist:', err)
    // Ignoriere Fehler, da die API möglicherweise nicht verfügbar ist
  }
}

// Lade Chart-Daten für alle Watchlist-Symbole
const loadWatchlistChartData = async () => {
  const promises = customWatchlist.value.map(async (item) => {
    try {
      // Lade mehr Daten für bessere Charts (5 Tage statt 1 Tag)
      const response = await fetch(`/api/v1/market/data/${item.symbol}?timeframe=5d`, {
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        
        // Prüfe verschiedene mögliche Datenstrukturen
        let chartData = null
        if (Array.isArray(data)) {
          chartData = data
        } else if (data.data && Array.isArray(data.data)) {
          chartData = data.data
        } else if (data.historical && Array.isArray(data.historical)) {
          chartData = data.historical
        } else if (data.prices && Array.isArray(data.prices)) {
          chartData = data.prices
        }
        
        if (chartData && chartData.length > 0) {
          watchlistChartData.value[item.symbol] = chartData
        }
      }
    } catch (err) {
      // Ignoriere Fehler für einzelne Symbole
    }
  })
  
  await Promise.all(promises)
}

// Chart-Pfad generieren
const getChartPath = (symbol) => {
  const data = watchlistChartData.value[symbol]
  if (!data || !data.length) {
    return 'M 10 20 L 90 20'
  }
  
  const points = data.slice(-10) // Letzte 10 Datenpunkte
  const width = 100
  const height = 40
  const padding = 5
  
  // Extrahiere Close-Preise mit verschiedenen möglichen Feldnamen
  const closePrices = points.map(p => {
    const price = p.close || p.Close || p.price || p.Price || p.value || p.Value || p.adjClose || p.AdjClose || 0
    return parseFloat(price) || 0
  }).filter(price => price > 0)
  
  if (closePrices.length === 0) {
    return 'M 10 20 L 90 20'
  }
  
  let minPrice, maxPrice
  
  if (points.length === 1) {
    // Bei nur einem Datenpunkt: Verwende Open und Close für den Bereich
    const point = points[0]
    const openPrice = parseFloat(point.open || point.Open || 0) || 0
    const closePrice = parseFloat(point.close || point.Close || 0) || 0
    minPrice = Math.min(openPrice, closePrice)
    maxPrice = Math.max(openPrice, closePrice)
    
    // Wenn Open und Close gleich sind, füge etwas Variation hinzu
    if (minPrice === maxPrice) {
      const variation = maxPrice * 0.01 // 1% Variation
      minPrice = maxPrice - variation
      maxPrice = maxPrice + variation
    }
  } else {
    minPrice = Math.min(...closePrices)
    maxPrice = Math.max(...closePrices)
  }
  
  const priceRange = maxPrice - minPrice || 1
  
  const pathData = points.map((point, index) => {
    const x = padding + (index / Math.max(points.length - 1, 1)) * (width - 2 * padding)
    const closePrice = parseFloat(point.close || point.Close || point.price || point.Price || point.value || point.Value || point.adjClose || point.AdjClose || 0) || 0
    const y = height - padding - ((closePrice - minPrice) / priceRange) * (height - 2 * padding)
    
    // Sicherstellen, dass x und y gültige Zahlen sind
    const validX = isNaN(x) ? padding + (index * 10) : x
    const validY = isNaN(y) ? height / 2 : Math.max(padding, Math.min(height - padding, y))
    
    return `${index === 0 ? 'M' : 'L'} ${validX} ${validY}`
  }).join(' ')
  
  return pathData
}

// Chart-Punkte für Kreise
const getChartPoints = (symbol) => {
  const data = watchlistChartData.value[symbol]
  if (!data || !data.length) {
    return []
  }
  
  const points = data.slice(-10)
  const width = 100
  const height = 40
  const padding = 5
  
  const closePrices = points.map(p => {
    const price = p.close || p.Close || p.price || p.Price || p.value || p.Value || p.adjClose || p.AdjClose || 0
    return parseFloat(price) || 0
  }).filter(price => price > 0)
  
  if (closePrices.length === 0) {
    return []
  }
  
  const minPrice = Math.min(...closePrices)
  const maxPrice = Math.max(...closePrices)
  const priceRange = maxPrice - minPrice || 1
  
  return points.map((point, index) => {
    const closePrice = parseFloat(point.close || point.Close || point.price || point.Price || point.value || point.Value || point.adjClose || point.AdjClose || 0) || 0
    const x = padding + (index / Math.max(points.length - 1, 1)) * (width - 2 * padding)
    const y = height - padding - ((closePrice - minPrice) / priceRange) * (height - 2 * padding)
    
    return {
      x: isNaN(x) ? padding + (index * 10) : x,
      y: isNaN(y) ? height / 2 : Math.max(padding, Math.min(height - padding, y))
    }
  })
}

// Chart-Farbe basierend auf Trend
const getChartColor = (symbol) => {
  const data = watchlistChartData.value[symbol]
  if (!data || data.length === 0) {
    return 'text-muted-foreground'
  }
  
  let firstPrice, lastPrice
  
  if (data.length === 1) {
    // Bei nur einem Datenpunkt: Vergleiche Close mit Open des gleichen Tages
    const point = data[0]
    firstPrice = parseFloat(point.open || point.Open || 0) || 0
    lastPrice = parseFloat(point.close || point.Close || 0) || 0
  } else {
    // Bei mehreren Datenpunkten: Vergleiche ersten mit letztem Close
    firstPrice = parseFloat(data[0].close || data[0].Close || 0) || 0
    lastPrice = parseFloat(data[data.length - 1].close || data[data.length - 1].Close || 0) || 0
  }
  
  if (isNaN(firstPrice) || isNaN(lastPrice)) {
    return 'text-muted-foreground'
  }
  
  if (lastPrice > firstPrice) {
    return 'text-green-500'
  } else if (lastPrice < firstPrice) {
    return 'text-red-500'
  }
  return 'text-muted-foreground'
}

// Prozentuale Änderung berechnen
const getPercentageChange = (symbol) => {
  const data = watchlistChartData.value[symbol]
  if (!data || data.length === 0) {
    return '+0.00%'
  }
  
  let firstPrice, lastPrice
  
  if (data.length === 1) {
    // Bei nur einem Datenpunkt: Vergleiche Close mit Open des gleichen Tages
    const point = data[0]
    firstPrice = parseFloat(point.open || point.Open || 0) || 0
    lastPrice = parseFloat(point.close || point.Close || 0) || 0
  } else {
    // Bei mehreren Datenpunkten: Vergleiche ersten mit letztem Close
    firstPrice = parseFloat(data[0].close || data[0].Close || 0) || 0
    lastPrice = parseFloat(data[data.length - 1].close || data[data.length - 1].Close || 0) || 0
  }
  
  if (firstPrice === 0 || isNaN(firstPrice) || isNaN(lastPrice)) {
    return '+0.00%'
  }
  
  const change = ((lastPrice - firstPrice) / firstPrice) * 100
  
  if (isNaN(change)) {
    return '+0.00%'
  }
  
  return `${change >= 0 ? '+' : ''}${change.toFixed(2)}%`
}

// Farbe für Prozentanzeige
const getPercentageColor = (symbol) => {
  const data = watchlistChartData.value[symbol]
  if (!data || data.length === 0) {
    return 'text-muted-foreground'
  }
  
  let firstPrice, lastPrice
  
  if (data.length === 1) {
    // Bei nur einem Datenpunkt: Vergleiche Close mit Open des gleichen Tages
    const point = data[0]
    firstPrice = parseFloat(point.open || point.Open || 0) || 0
    lastPrice = parseFloat(point.close || point.Close || 0) || 0
  } else {
    // Bei mehreren Datenpunkten: Vergleiche ersten mit letztem Close
    firstPrice = parseFloat(data[0].close || data[0].Close || 0) || 0
    lastPrice = parseFloat(data[data.length - 1].close || data[data.length - 1].Close || 0) || 0
  }
  
  if (isNaN(firstPrice) || isNaN(lastPrice)) {
    return 'text-muted-foreground'
  }
  
  if (lastPrice > firstPrice) {
    return 'text-green-500'
  } else if (lastPrice < firstPrice) {
    return 'text-red-500'
  }
  return 'text-muted-foreground'
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

onMounted(async () => {
  // Lade Watchlist zuerst (schneller)
  await fetchCustomWatchlist()
  
  // HotStocks lädt automatisch in der Komponente
})
</script>

<style scoped>
.fade-in {
  animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Staggered animation für Cards */
.fade-in:nth-child(1) { animation-delay: 0.1s; }
.fade-in:nth-child(2) { animation-delay: 0.2s; }
.fade-in:nth-child(3) { animation-delay: 0.3s; }
.fade-in:nth-child(4) { animation-delay: 0.4s; }
.fade-in:nth-child(5) { animation-delay: 0.5s; }
.fade-in:nth-child(6) { animation-delay: 0.6s; }
</style>