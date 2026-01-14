<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-3xl font-bold">{{ t('dashboard.title') }}</h2>
    </div>

    <!-- Custom Watchlist Grid -->
    <div v-if="customWatchlist.length > 0" class="mt-8">
      <h3 class="text-xl font-semibold mb-4">{{ t('dashboard.mySymbols') }}</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        <Card
          v-for="item in customWatchlist"
          :key="item.id"
          class="hover:shadow-lg transition-all cursor-pointer group fade-in"
          @click="navigateToSymbol(item.symbol)"
        >
          <CardHeader class="pb-4">
            <div class="flex justify-between items-center">
              <div class="flex-1 min-w-0">
                <CardTitle class="text-lg truncate">{{ item.symbol }}</CardTitle>
                <CardDescription class="text-sm text-muted-foreground truncate">
                  {{ getDisplayName(item) }}
                </CardDescription>
              </div>
              <Button
                variant="ghost"
                size="sm"
                @click.stop="removeFromWatchlist(item.symbol)"
                class="text-muted-foreground hover:text-destructive flex-shrink-0"
                :title="t('dashboard.removeFromWatchlist')"
              >
                <Trash2 class="h-4 w-4" />
              </Button>
            </div>
          </CardHeader>
          <CardContent class="pt-0">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <!-- Mini Chart -->
                <div class="w-16 h-8">
                  <svg viewBox="0 0 100 40" class="w-full h-full">
                    <path
                      :d="getChartPath(item.symbol)"
                      :class="getChartColor(item.symbol)"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    />
                    <circle
                      v-for="point in getChartPoints(item.symbol)"
                      :key="point.x"
                      :cx="point.x"
                      :cy="point.y"
                      r="1.5"
                      :class="getChartColor(item.symbol)"
                      fill="currentColor"
                    />
                  </svg>
                </div>
                <div class="text-sm font-medium" :class="getPercentageColor(item.symbol)">
                  {{ getPercentageChange(item.symbol) }}
                </div>
              </div>
              <div class="text-right">
                <div class="text-xs text-muted-foreground">{{ t('timeframes.1D') }}</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>

    <!-- Hot Stocks Table -->
    <div class="mt-8">
      <HotStocks @watchlist-changed="fetchCustomWatchlist" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Trash2 } from 'lucide-vue-next'
import HotStocks from '@/components/HotStocks.vue'
import axios from 'axios'

const router = useRouter()
const { t } = useI18n()
const authStore = useAuthStore()

// Benutzerdefinierte Watchlist
const customWatchlist = ref([])
const isLoading = ref(false)
const error = ref('')
const watchlistChartData = ref({})

// Lade Watchlist beim Mount
onMounted(async () => {
  await fetchCustomWatchlist()
})

// Lade benutzerdefinierte Watchlist
const fetchCustomWatchlist = async () => {
  if (!authStore.isAuthenticated) return
  
  try {
    isLoading.value = true
    const response = await axios.get('/api/v1/watchlist/', {
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })
    customWatchlist.value = response.data
    
    // Lade Chart-Daten nach dem Laden der Watchlist
    await loadWatchlistChartData()
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
  
  let minPrice, maxPrice
  
  if (points.length === 1) {
    const point = points[0]
    const openPrice = parseFloat(point.open || point.Open || 0) || 0
    const closePrice = parseFloat(point.close || point.Close || 0) || 0
    minPrice = Math.min(openPrice, closePrice)
    maxPrice = Math.max(openPrice, closePrice)
    
    if (minPrice === maxPrice) {
      const variation = maxPrice * 0.01
      minPrice = maxPrice - variation
      maxPrice = maxPrice + variation
    }
  } else {
    minPrice = Math.min(...closePrices)
    maxPrice = Math.max(...closePrices)
  }
  
  const priceRange = maxPrice - minPrice || 1
  
  return points.map((point, index) => {
    const x = padding + (index / Math.max(points.length - 1, 1)) * (width - 2 * padding)
    const closePrice = parseFloat(point.close || point.Close || point.price || point.Price || point.value || point.Value || point.adjClose || point.AdjClose || 0) || 0
    const y = height - padding - ((closePrice - minPrice) / priceRange) * (height - 2 * padding)
    
    const validX = isNaN(x) ? padding + (index * 10) : x
    const validY = isNaN(y) ? height / 2 : Math.max(padding, Math.min(height - padding, y))
    
    return { x: validX, y: validY }
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

// Display Name für Aktien
const getDisplayName = (item) => {
  // Priorität: display_name > name > symbol
  return item.display_name || item.name || item.symbol
}

// Navigation zu Symbol
const navigateToSymbol = (symbol) => {
  router.push(`/symbol/${symbol}`)
}

// Entferne aus Watchlist
const removeFromWatchlist = async (symbol) => {
  if (!authStore.isAuthenticated) return
  
  try {
    await axios.delete(`/api/v1/watchlist/symbol/${symbol}/`, {
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })
    
    // Entferne aus lokaler Liste
    customWatchlist.value = customWatchlist.value.filter(item => item.symbol !== symbol)
    
    // Entferne Chart-Daten
    delete watchlistChartData.value[symbol]
  } catch (err) {
    console.error('Error removing from watchlist:', err)
  }
}
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
</style>