// src/components/StockSearch.vue
<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Command } from '@/components/ui/command'
import { Loader2, Search } from 'lucide-vue-next'
import { useDebounce } from '@/composables/useDebounce'
import axios from 'axios'

const router = useRouter()
const searchQuery = ref('')
const suggestions = ref([])
const isLoading = ref(false)
const showSuggestions = ref(false)

const debouncedSearch = useDebounce(async (query) => {
  if (!query) {
    suggestions.value = []
    return
  }

  try {
    isLoading.value = true
    const response = await axios.get(`http://localhost:8000/api/v1/market/search?query=${query}`)
    suggestions.value = response.data
  } catch (error) {
    console.error('Search error:', error)
    suggestions.value = []
  } finally {
    isLoading.value = false
  }
}, 300)

watch(searchQuery, (newQuery) => {
  if (newQuery) {
    showSuggestions.value = true
    debouncedSearch(newQuery)
  } else {
    showSuggestions.value = false
    suggestions.value = []
  }
})

const handleSelect = (stock) => {
  router.push(`/symbol/${stock.symbol}`)
  searchQuery.value = ''
  showSuggestions.value = false
}

const handleClickOutside = () => {
  showSuggestions.value = false
}
</script>

<template>
  <div class="relative w-96">
    <div class="relative">
      <Input
        v-model="searchQuery"
        placeholder="Suche nach Symbol oder Firmenname..."
        class="w-full pr-10"
        @focus="showSuggestions = true"
      />
      <div class="absolute right-3 top-1/2 -translate-y-1/2">
        <Loader2 v-if="isLoading" class="h-4 w-4 animate-spin" />
        <Search v-else class="h-4 w-4 text-muted-foreground" />
      </div>
    </div>

    <!-- Suggestions Dropdown -->
    <div
      v-if="showSuggestions && suggestions.length > 0"
      class="absolute mt-1 w-full rounded-md border bg-popover shadow-md"
      v-click-outside="handleClickOutside"
    >
      <Command class="rounded-lg border shadow-md">
        <div class="max-h-[300px] overflow-auto p-2">
          <div
            v-for="stock in suggestions"
            :key="stock.symbol"
            class="flex cursor-pointer items-center rounded-sm px-2 py-1.5 hover:bg-accent"
            @click="handleSelect(stock)"
          >
            <div class="flex flex-col">
              <span class="font-medium">{{ stock.symbol }}</span>
              <span class="text-sm text-muted-foreground">{{ stock.name }}</span>
            </div>
            <div class="ml-auto text-sm text-muted-foreground">
              {{ stock.exchange }}
            </div>
          </div>
        </div>
      </Command>
    </div>
  </div>
</template>