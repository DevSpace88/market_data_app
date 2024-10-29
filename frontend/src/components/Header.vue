<template>
  <header class="border-b">
    <div class="container flex h-16 items-center">
      <router-link to="/" class="flex items-center space-x-2">
        <LineChart class="h-6 w-6" />
        <span class="font-bold">Market Analysis</span>
      </router-link>
      <div class="ml-auto flex items-center space-x-4">
        <div class="relative">
          <Input
            v-model="searchQuery"
            placeholder="Search symbol..."
            class="w-64"
            @keyup.enter="handleSearch"
          />
          <Button
            variant="ghost"
            class="absolute right-0 top-0 h-full px-3"
            @click="handleSearch"
          >
            <Search class="h-4 w-4" />
          </Button>
        </div>
        <ThemeToggle />
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { LineChart, Search } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import ThemeToggle from './ThemeToggle.vue'

const router = useRouter()
const searchQuery = ref('')

const handleSearch = () => {
  if (searchQuery.value) {
    router.push(`/symbol/${searchQuery.value.toUpperCase()}`)
    searchQuery.value = ''
  }
}
</script>