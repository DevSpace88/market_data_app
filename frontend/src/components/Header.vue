<!--&lt;!&ndash;<template>&ndash;&gt;-->
<!--&lt;!&ndash;  <header class="border-b bg-background">&ndash;&gt;-->
<!--&lt;!&ndash;    <div class="container mx-auto flex h-16 items-center justify-between px-4">&ndash;&gt;-->
<!--&lt;!&ndash;      <router-link to="/" class="flex items-center space-x-2 hover:opacity-80">&ndash;&gt;-->
<!--&lt;!&ndash;        <BarChart2 class="h-6 w-6" />&ndash;&gt;-->
<!--&lt;!&ndash;        <span class="text-xl font-semibold">Market Analysis</span>&ndash;&gt;-->
<!--&lt;!&ndash;      </router-link>&ndash;&gt;-->

<!--&lt;!&ndash;      <div class="flex items-center space-x-4">&ndash;&gt;-->
<!--&lt;!&ndash;        <div class="relative w-96">&ndash;&gt;-->
<!--&lt;!&ndash;          <Input&ndash;&gt;-->
<!--&lt;!&ndash;            v-model="searchQuery"&ndash;&gt;-->
<!--&lt;!&ndash;            placeholder="Suche Symbol (z.B. AAPL, GOOGL)..."&ndash;&gt;-->
<!--&lt;!&ndash;            class="w-full"&ndash;&gt;-->
<!--&lt;!&ndash;            @keyup.enter="handleSearch"&ndash;&gt;-->
<!--&lt;!&ndash;          />&ndash;&gt;-->
<!--&lt;!&ndash;          <Button variant="ghost" class="absolute right-0 top-0 h-full px-3" @click="handleSearch">&ndash;&gt;-->
<!--&lt;!&ndash;            <Search class="h-4 w-4" />&ndash;&gt;-->
<!--&lt;!&ndash;          </Button>&ndash;&gt;-->
<!--&lt;!&ndash;        </div>&ndash;&gt;-->

<!--&lt;!&ndash;        &lt;!&ndash; Theme Toggle &ndash;&gt;&ndash;&gt;-->
<!--&lt;!&ndash;        <Button variant="outline" size="icon" @click="toggleTheme">&ndash;&gt;-->
<!--&lt;!&ndash;          <Sun v-if="isDark" class="h-5 w-5" />&ndash;&gt;-->
<!--&lt;!&ndash;          <Moon v-else class="h-5 w-5" />&ndash;&gt;-->
<!--&lt;!&ndash;        </Button>&ndash;&gt;-->
<!--&lt;!&ndash;      </div>&ndash;&gt;-->
<!--&lt;!&ndash;    </div>&ndash;&gt;-->
<!--&lt;!&ndash;  </header>&ndash;&gt;-->
<!--&lt;!&ndash;</template>&ndash;&gt;-->

<!--&lt;!&ndash;<script setup>&ndash;&gt;-->
<!--&lt;!&ndash;import { ref, onMounted } from 'vue'&ndash;&gt;-->
<!--&lt;!&ndash;import { useRouter } from 'vue-router'&ndash;&gt;-->
<!--&lt;!&ndash;import { useThemeStore } from '@/stores/theme'  // Darkmode Store importieren&ndash;&gt;-->
<!--&lt;!&ndash;import { BarChart2, Search, Sun, Moon } from 'lucide-vue-next'&ndash;&gt;-->
<!--&lt;!&ndash;import { Button } from '@/components/ui/button'&ndash;&gt;-->
<!--&lt;!&ndash;import { Input } from '@/components/ui/input'&ndash;&gt;-->

<!--&lt;!&ndash;const router = useRouter()&ndash;&gt;-->
<!--&lt;!&ndash;const searchQuery = ref('')&ndash;&gt;-->
<!--&lt;!&ndash;const themeStore = useThemeStore()&ndash;&gt;-->

<!--&lt;!&ndash;const isDark = ref(themeStore.isDark)&ndash;&gt;-->

<!--&lt;!&ndash;// Suche ausführen&ndash;&gt;-->
<!--&lt;!&ndash;const handleSearch = () => {&ndash;&gt;-->
<!--&lt;!&ndash;  if (searchQuery.value) {&ndash;&gt;-->
<!--&lt;!&ndash;    router.push(`/symbol/${searchQuery.value.toUpperCase()}`)&ndash;&gt;-->
<!--&lt;!&ndash;    searchQuery.value = ''&ndash;&gt;-->
<!--&lt;!&ndash;  }&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->

<!--&lt;!&ndash;// Theme umschalten&ndash;&gt;-->
<!--&lt;!&ndash;const toggleTheme = () => {&ndash;&gt;-->
<!--&lt;!&ndash;  themeStore.toggleTheme()&ndash;&gt;-->
<!--&lt;!&ndash;  isDark.value = themeStore.isDark&ndash;&gt;-->
<!--&lt;!&ndash;}&ndash;&gt;-->

<!--&lt;!&ndash;// Initiales Theme setzen&ndash;&gt;-->
<!--&lt;!&ndash;onMounted(() => {&ndash;&gt;-->
<!--&lt;!&ndash;  const savedTheme = localStorage.getItem('theme')&ndash;&gt;-->
<!--&lt;!&ndash;  themeStore.isDark = savedTheme === 'dark'&ndash;&gt;-->
<!--&lt;!&ndash;  document.documentElement.classList.toggle('dark', themeStore.isDark)&ndash;&gt;-->
<!--&lt;!&ndash;})&ndash;&gt;-->
<!--&lt;!&ndash;</script>&ndash;&gt;-->


<!--// src/components/Header.vue-->
<!--<template>-->
<!--  <header class="border-b bg-background">-->
<!--    <div class="container mx-auto flex h-16 items-center justify-between px-4">-->
<!--      <router-link to="/dashboard" class="flex items-center space-x-2 hover:opacity-80">-->
<!--        <BarChart2 class="h-6 w-6" />-->
<!--        <span class="text-xl font-semibold">Market Analysis</span>-->
<!--      </router-link>-->

<!--      <div class="flex items-center space-x-4">-->
<!--        &lt;!&ndash; Suchfeld nur anzeigen wenn eingeloggt &ndash;&gt;-->
<!--        <div v-if="authStore.isAuthenticated" class="relative w-96">-->
<!--          <Input-->
<!--            v-model="searchQuery"-->
<!--            placeholder="Suche Symbol (z.B. AAPL, GOOGL)..."-->
<!--            class="w-full"-->
<!--            @keyup.enter="handleSearch"-->
<!--          />-->
<!--          <Button variant="ghost" class="absolute right-0 top-0 h-full px-3" @click="handleSearch">-->
<!--            <Search class="h-4 w-4" />-->
<!--          </Button>-->
<!--        </div>-->

<!--        <div class="flex items-center space-x-2">-->
<!--          &lt;!&ndash; Theme Toggle &ndash;&gt;-->
<!--          <Button variant="outline" size="icon" @click="toggleTheme">-->
<!--            <Sun v-if="isDark" class="h-5 w-5" />-->
<!--            <Moon v-else class="h-5 w-5" />-->
<!--          </Button>-->

<!--          &lt;!&ndash; Auth Buttons &ndash;&gt;-->
<!--          <Button-->
<!--            v-if="authStore.isAuthenticated"-->
<!--            variant="outline"-->
<!--            @click="handleLogout"-->
<!--          >-->
<!--            <LogOut class="h-4 w-4 mr-2" />-->
<!--            Logout-->
<!--          </Button>-->
<!--          <Button-->
<!--            v-else-->
<!--            @click="router.push('/login')"-->
<!--          >-->
<!--            <LogIn class="h-4 w-4 mr-2" />-->
<!--            Login-->
<!--          </Button>-->
<!--        </div>-->
<!--      </div>-->
<!--    </div>-->
<!--  </header>-->
<!--</template>-->

<!--<script setup>-->
<!--import { ref, onMounted } from 'vue'-->
<!--import { useRouter } from 'vue-router'-->
<!--import { useThemeStore } from '@/stores/theme'-->
<!--import { useAuthStore } from '@/stores/auth'-->
<!--import { BarChart2, Search, Sun, Moon, LogIn, LogOut } from 'lucide-vue-next'-->
<!--import { Button } from '@/components/ui/button'-->
<!--import { Input } from '@/components/ui/input'-->

<!--const router = useRouter()-->
<!--const authStore = useAuthStore()-->
<!--const themeStore = useThemeStore()-->
<!--const searchQuery = ref('')-->
<!--const isDark = ref(themeStore.isDark)-->

<!--const handleSearch = () => {-->
<!--  if (searchQuery.value) {-->
<!--    router.push(`/symbol/${searchQuery.value.toUpperCase()}`)-->
<!--    searchQuery.value = ''-->
<!--  }-->
<!--}-->

<!--const handleLogout = () => {-->
<!--  authStore.logout()-->
<!--  router.push('/login')-->
<!--}-->

<!--const toggleTheme = () => {-->
<!--  themeStore.toggleTheme()-->
<!--  isDark.value = themeStore.isDark-->
<!--}-->

<!--onMounted(() => {-->
<!--  const savedTheme = localStorage.getItem('theme')-->
<!--  themeStore.isDark = savedTheme === 'dark'-->
<!--  document.documentElement.classList.toggle('dark', themeStore.isDark)-->
<!--})-->
<!--</script>-->



// src/components/Header.vue
<template>
  <header class="border-b bg-background">
    <div class="container mx-auto flex h-16 items-center justify-between px-4">
      <router-link to="/dashboard" class="flex items-center space-x-2 hover:opacity-80">
        <BarChart2 class="h-6 w-6" />
        <span class="text-xl font-semibold">Market Analysis</span>
      </router-link>

      <div class="flex items-center space-x-4">
        <!-- Suchfeld mit Dropdown -->
        <div v-if="authStore.isAuthenticated" class="relative w-96">
          <Input
            v-model="searchQuery"
            placeholder="Suche Symbol (z.B. AAPL, GOOGL)..."
            class="w-full"
            @input="handleSearchInput"
            @focus="showDropdown = true"
          />

          <!-- Loading Indicator -->
          <div v-if="isLoading" class="absolute right-3 top-1/2 -translate-y-1/2">
            <Loader2 class="h-4 w-4 animate-spin" />
          </div>

          <!-- Search Dropdown -->
          <div
            v-if="showDropdown && searchResults.length > 0"
            class="absolute mt-1 w-full rounded-lg border bg-background shadow-lg"
            v-click-outside="() => showDropdown = false"
          >
            <div class="max-h-[300px] overflow-y-auto p-2">
              <div
                v-for="result in searchResults"
                :key="result.symbol"
                class="flex cursor-pointer items-center space-x-3 rounded-md p-2 hover:bg-accent"
                @click="selectStock(result)"
              >
                <div class="flex-1">
                  <div class="font-medium">{{ result.symbol }}</div>
                  <div class="text-sm text-muted-foreground">{{ result.name }}</div>
                </div>
                <div class="text-xs text-muted-foreground">
                  {{ result.exchange }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="flex items-center space-x-2">
          <!-- Theme Toggle -->
          <Button variant="outline" size="icon" @click="toggleTheme">
            <Sun v-if="isDark" class="h-5 w-5" />
            <Moon v-else class="h-5 w-5" />
          </Button>

          <!-- Auth Buttons -->
          <Button
            v-if="authStore.isAuthenticated"
            variant="outline"
            @click="handleLogout"
          >
            <LogOut class="h-4 w-4 mr-2" />
            Logout
          </Button>
          <Button
            v-else
            @click="router.push('/login')"
          >
            <LogIn class="h-4 w-4 mr-2" />
            Login
          </Button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useThemeStore } from '@/stores/theme'
import { useAuthStore } from '@/stores/auth'
import { BarChart2, Search, Sun, Moon, LogIn, LogOut, Loader2 } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { useDebounce } from '@/composables/useDebounce'
import axios from 'axios'

const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()

const searchQuery = ref('')
const searchResults = ref([])
const showDropdown = ref(false)
const isLoading = ref(false)
const isDark = ref(themeStore.isDark)

// Debounced search function
const debouncedSearch = useDebounce(async (query) => {
  if (!query.trim()) {
    searchResults.value = []
    return
  }

  try {
    isLoading.value = true
    const response = await axios.get(`/api/v1/market/search?query=${query}`, {
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })
    searchResults.value = response.data
  } catch (error) {
    console.error('Search error:', error)
    searchResults.value = []
  } finally {
    isLoading.value = false
  }
}, 300)

const handleSearchInput = () => {
  if (searchQuery.value) {
    debouncedSearch(searchQuery.value)
  } else {
    searchResults.value = []
  }
}

const selectStock = (stock) => {
  router.push(`/symbol/${stock.symbol}`)
  searchQuery.value = ''
  showDropdown.value = false
  searchResults.value = []
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const toggleTheme = () => {
  themeStore.toggleTheme()
  isDark.value = themeStore.isDark
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  themeStore.isDark = savedTheme === 'dark'
  document.documentElement.classList.toggle('dark', themeStore.isDark)
})
</script>