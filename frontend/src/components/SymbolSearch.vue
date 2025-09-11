<template>
  <div class="relative">
    <div class="flex gap-2">
      <div class="relative flex-1">
        <input
          v-model="searchQuery"
          @input="onSearch"
          @focus="showSuggestions = true"
          @blur="hideSuggestions"
          placeholder="Symbol, Name oder ISIN suchen (z.B. Apple, AAPL, US0378331005)"
          class="w-full px-3 py-2 border border-input rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
        />
        
        <!-- Loading indicator -->
        <div v-if="isLoading" class="absolute right-3 top-2.5">
          <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-primary"></div>
        </div>
        
        <!-- Suggestions dropdown -->
        <div
          v-if="showSuggestions && suggestions.length > 0"
          class="absolute z-10 w-full mt-1 bg-popover border border-border rounded-md shadow-lg max-h-60 overflow-y-auto"
        >
          <div
            v-for="suggestion in suggestions"
            :key="suggestion.symbol"
            @click="selectSymbol(suggestion)"
            class="px-4 py-2 hover:bg-accent cursor-pointer border-b border-border last:border-b-0"
          >
            <div class="flex justify-between items-center">
              <div>
                <div class="font-medium text-sm text-foreground">{{ suggestion.symbol }}</div>
                <div class="text-xs text-muted-foreground">{{ suggestion.name }}</div>
              </div>
              <div class="text-xs text-muted-foreground">
                {{ suggestion.exchange || 'Stock' }}
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <button
        @click="addSymbol"
        :disabled="!selectedSymbol || isAdding"
        class="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <svg v-if="isAdding" class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
        </svg>
        <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
        </svg>
      </button>
    </div>
    
    <!-- Error message -->
    <div v-if="error" class="mt-2 p-2 bg-destructive/10 border border-destructive/20 text-destructive rounded text-sm">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  onAdd: {
    type: Function,
    required: true
  }
})

const emit = defineEmits(['add'])

const searchQuery = ref('')
const suggestions = ref([])
const selectedSymbol = ref(null)
const showSuggestions = ref(false)
const isLoading = ref(false)
const isAdding = ref(false)
const error = ref('')

// Mock data für Symbol-Suche (in einer echten App würde das von einer API kommen)
const mockSymbols = [
  { symbol: 'AAPL', name: 'Apple Inc.', exchange: 'NASDAQ', isin: 'US0378331005' },
  { symbol: 'GOOGL', name: 'Alphabet Inc. Class A', exchange: 'NASDAQ', isin: 'US02079K3059' },
  { symbol: 'MSFT', name: 'Microsoft Corporation', exchange: 'NASDAQ', isin: 'US5949181045' },
  { symbol: 'AMZN', name: 'Amazon.com Inc.', exchange: 'NASDAQ', isin: 'US0231351067' },
  { symbol: 'TSLA', name: 'Tesla Inc.', exchange: 'NASDAQ', isin: 'US88160R1014' },
  { symbol: 'NVDA', name: 'NVIDIA Corporation', exchange: 'NASDAQ', isin: 'US67066G1040' },
  { symbol: 'META', name: 'Meta Platforms Inc.', exchange: 'NASDAQ', isin: 'US30303M1027' },
  { symbol: 'NFLX', name: 'Netflix Inc.', exchange: 'NASDAQ', isin: 'US64110L1061' },
  { symbol: 'ORCL', name: 'Oracle Corporation', exchange: 'NYSE', isin: 'US68389X1054' },
  { symbol: 'IBM', name: 'International Business Machines Corporation', exchange: 'NYSE', isin: 'US4592001014' },
  { symbol: 'SAP', name: 'SAP SE', exchange: 'XETRA', isin: 'DE0007164600' },
  { symbol: 'ASML', name: 'ASML Holding N.V.', exchange: 'XETRA', isin: 'NL0010408704' },
  { symbol: 'TSM', name: 'Taiwan Semiconductor Manufacturing Company Limited', exchange: 'NYSE', isin: 'US8740391003' },
  { symbol: 'BABA', name: 'Alibaba Group Holding Limited', exchange: 'NYSE', isin: 'US01609W1027' },
  { symbol: 'JPM', name: 'JPMorgan Chase & Co.', exchange: 'NYSE', isin: 'US46625H1005' }
]

const onSearch = () => {
  if (searchQuery.value.length < 2) {
    suggestions.value = []
    return
  }
  
  isLoading.value = true
  error.value = ''
  
  // Simuliere API-Aufruf
  setTimeout(() => {
    const query = searchQuery.value.toLowerCase()
    suggestions.value = mockSymbols.filter(symbol => 
      symbol.symbol.toLowerCase().includes(query) ||
      symbol.name.toLowerCase().includes(query) ||
      symbol.isin.toLowerCase().includes(query)
    ).slice(0, 8) // Max 8 Vorschläge
    
    isLoading.value = false
  }, 300)
}

const selectSymbol = (symbol) => {
  selectedSymbol.value = symbol
  searchQuery.value = `${symbol.symbol} - ${symbol.name}`
  showSuggestions.value = false
}

const hideSuggestions = () => {
  setTimeout(() => {
    showSuggestions.value = false
  }, 200)
}

const addSymbol = async () => {
  if (!selectedSymbol.value) return
  
  isAdding.value = true
  error.value = ''
  
  try {
    await props.onAdd(selectedSymbol.value.symbol, selectedSymbol.value.name)
    searchQuery.value = ''
    selectedSymbol.value = null
  } catch (err) {
    error.value = err.message
  } finally {
    isAdding.value = false
  }
}

// Reset when search query changes
watch(searchQuery, (newQuery) => {
  if (!newQuery) {
    selectedSymbol.value = null
  }
})
</script>
