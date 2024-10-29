<!--&lt;!&ndash; src/App.vue &ndash;&gt;-->
<!--<template>-->
<!--  <div class="min-h-screen bg-background text-foreground">-->
<!--    &lt;!&ndash; Header &ndash;&gt;-->
<!--    <header class="border-b bg-background">-->
<!--      <div class="container mx-auto flex h-16 items-center justify-between px-4">-->
<!--        &lt;!&ndash; Logo & Title &ndash;&gt;-->
<!--        <div class="flex items-center space-x-2">-->
<!--          <BarChart2 class="h-6 w-6" />-->
<!--          <span class="text-xl font-semibold">Market Analysis</span>-->
<!--        </div>-->

<!--        &lt;!&ndash; Search & Settings &ndash;&gt;-->
<!--        <div class="flex items-center space-x-4">-->
<!--          &lt;!&ndash; Search Box &ndash;&gt;-->
<!--          <div class="relative w-96">-->
<!--            <Input-->
<!--              v-model="searchQuery"-->
<!--              placeholder="Suche Symbol (z.B. AAPL, GOOGL)..."-->
<!--              class="w-full"-->
<!--            />-->
<!--            <Button-->
<!--              variant="ghost"-->
<!--              class="absolute right-0 top-0 h-full px-3"-->
<!--            >-->
<!--              <Search class="h-4 w-4" />-->
<!--            </Button>-->
<!--          </div>-->

<!--          &lt;!&ndash; Theme Toggle &ndash;&gt;-->
<!--          <Button variant="outline" size="icon" @click="toggleTheme">-->
<!--            <Sun v-if="isDark" class="h-5 w-5" />-->
<!--            <Moon v-else class="h-5 w-5" />-->
<!--          </Button>-->
<!--        </div>-->
<!--      </div>-->
<!--    </header>-->

<!--    &lt;!&ndash; Main Content &ndash;&gt;-->
<!--    <main class="container mx-auto p-4">-->
<!--      <Card class="p-4">-->
<!--        <h2 class="text-lg font-semibold">Willkommen bei Market Analysis</h2>-->
<!--        <p class="mt-2 text-muted-foreground">-->
<!--          Suchen Sie nach einem Symbol, um die Analyse zu starten.-->
<!--        </p>-->
<!--      </Card>-->
<!--    </main>-->
<!--  </div>-->
<!--</template>-->

<!--<script setup>-->
<!--import { ref, onMounted } from 'vue'-->
<!--import { BarChart2, Search, Sun, Moon } from 'lucide-vue-next'-->
<!--import { Button } from '@/components/ui/button'-->
<!--import { Input } from '@/components/ui/input'-->
<!--import { Card } from '@/components/ui/card'-->

<!--const searchQuery = ref('')-->
<!--const isDark = ref(false)-->

<!--// Theme Toggle-->
<!--const toggleTheme = () => {-->
<!--  isDark.value = !isDark.value-->
<!--  document.documentElement.classList.toggle('dark', isDark.value)-->
<!--  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')-->
<!--}-->

<!--// Initialize theme-->
<!--onMounted(() => {-->
<!--  // Start with light theme by default-->
<!--  document.documentElement.classList.remove('dark')-->
<!--  isDark.value = false-->
<!--})-->
<!--</script>-->


<!-- src/App.vue -->
<template>
  <div class="min-h-screen bg-background text-foreground">
    <!-- Header bleibt gleich -->
    <header class="border-b bg-background">
      <div class="container mx-auto flex h-16 items-center justify-between px-4">
        <!-- Logo & Title - jetzt mit Router Link -->
        <router-link to="/" class="flex items-center space-x-2 hover:opacity-80">
          <BarChart2 class="h-6 w-6" />
          <span class="text-xl font-semibold">Market Analysis</span>
        </router-link>

        <!-- Search & Settings -->
        <div class="flex items-center space-x-4">
          <!-- Search Box -->
          <div class="relative w-96">
            <Input
              v-model="searchQuery"
              placeholder="Suche Symbol (z.B. AAPL, GOOGL)..."
              class="w-full"
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

          <!-- Theme Toggle -->
          <Button variant="outline" size="icon" @click="toggleTheme">
            <Sun v-if="isDark" class="h-5 w-5" />
            <Moon v-else class="h-5 w-5" />
          </Button>
        </div>
      </div>
    </header>

    <!-- Main Content - jetzt mit Router View -->
    <main class="container mx-auto p-4">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { BarChart2, Search, Sun, Moon } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

const router = useRouter()
const searchQuery = ref('')
const isDark = ref(false)

// Theme Toggle
const toggleTheme = () => {
  isDark.value = !isDark.value
  document.documentElement.classList.toggle('dark', isDark.value)
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}

// Search Handler
const handleSearch = () => {
  const query = searchQuery.value.trim().toUpperCase()
  if (query) {
    router.push(`/symbol/${query}`)
    searchQuery.value = ''
  }
}

// Initialize theme
onMounted(() => {
  document.documentElement.classList.remove('dark')
  isDark.value = false
})
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>