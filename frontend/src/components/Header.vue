<!--<template>-->
<!--  <header class="border-b bg-background">-->
<!--    <div class="container mx-auto flex h-16 items-center justify-between px-4">-->
<!--      <router-link to="/dashboard" class="flex items-center space-x-2 hover:opacity-80">-->
<!--        <BarChart2 class="h-6 w-6" />-->
<!--        <span class="text-xl font-semibold">Market Analysis</span>-->
<!--      </router-link>-->

<!--      <div class="flex items-center space-x-4">-->
<!--        &lt;!&ndash; Suchfeld mit Dropdown &ndash;&gt;-->
<!--        <div v-if="authStore.isAuthenticated" class="relative w-96">-->
<!--          <Input-->
<!--            v-model="searchQuery"-->
<!--            placeholder="Suche Symbol (z.B. AAPL, GOOGL)..."-->
<!--            class="w-full"-->
<!--            @input="handleSearchInput"-->
<!--            @focus="showDropdown = true"-->
<!--          />-->

<!--          &lt;!&ndash; Loading Indicator &ndash;&gt;-->
<!--          <div v-if="isLoading" class="absolute right-3 top-1/2 -translate-y-1/2">-->
<!--            <Loader2 class="h-4 w-4 animate-spin" />-->
<!--          </div>-->

<!--          &lt;!&ndash; Search Dropdown &ndash;&gt;-->
<!--          <div-->
<!--            v-if="showDropdown && searchResults.length > 0"-->
<!--            class="absolute mt-1 w-full rounded-lg border bg-background shadow-lg z-50"-->
<!--            v-click-outside="() => showDropdown = false"-->
<!--          >-->
<!--            <div class="max-h-[300px] overflow-y-auto p-2">-->
<!--              <div-->
<!--                v-for="result in searchResults"-->
<!--                :key="result.symbol"-->
<!--                class="flex cursor-pointer items-center space-x-3 rounded-md p-2 hover:bg-accent"-->
<!--                @click="selectStock(result)"-->
<!--              >-->
<!--                <div class="flex-1">-->
<!--                  <div class="font-medium">{{ result.symbol }}</div>-->
<!--                  <div class="text-sm text-muted-foreground">{{ result.name }}</div>-->
<!--                </div>-->
<!--                <div class="text-xs text-muted-foreground">-->
<!--                  {{ result.exchange }}-->
<!--                </div>-->
<!--              </div>-->
<!--            </div>-->
<!--          </div>-->
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
<!--import { BarChart2, Search, Sun, Moon, LogIn, LogOut, Loader2 } from 'lucide-vue-next'-->
<!--import { Button } from '@/components/ui/button'-->
<!--import { Input } from '@/components/ui/input'-->
<!--import { useDebounce } from '@/composables/useDebounce'-->
<!--import axios from 'axios'-->

<!--const router = useRouter()-->
<!--const authStore = useAuthStore()-->
<!--const themeStore = useThemeStore()-->

<!--const searchQuery = ref('')-->
<!--const searchResults = ref([])-->
<!--const showDropdown = ref(false)-->
<!--const isLoading = ref(false)-->
<!--const isDark = ref(themeStore.isDark)-->

<!--// Debounced search function-->
<!--const debouncedSearch = useDebounce(async (query) => {-->
<!--  if (!query.trim()) {-->
<!--    searchResults.value = []-->
<!--    return-->
<!--  }-->

<!--  try {-->
<!--    isLoading.value = true-->
<!--    const response = await axios.get(`/api/v1/market/search?query=${query}`, {-->
<!--      headers: {-->
<!--        'Authorization': `Bearer ${authStore.token}`-->
<!--      }-->
<!--    })-->
<!--    searchResults.value = response.data-->
<!--  } catch (error) {-->
<!--    console.error('Search error:', error)-->
<!--    searchResults.value = []-->
<!--  } finally {-->
<!--    isLoading.value = false-->
<!--  }-->
<!--}, 300)-->

<!--const handleSearchInput = () => {-->
<!--  if (searchQuery.value) {-->
<!--    debouncedSearch(searchQuery.value)-->
<!--  } else {-->
<!--    searchResults.value = []-->
<!--  }-->
<!--}-->

<!--const selectStock = (stock) => {-->
<!--  router.push(`/symbol/${stock.symbol}`)-->
<!--  searchQuery.value = ''-->
<!--  showDropdown.value = false-->
<!--  searchResults.value = []-->
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

<!--<template>-->
<!--  <header class="border-b bg-background">-->
<!--    <div class="container mx-auto flex h-16 items-center justify-between px-4">-->
<!--      <router-link to="/dashboard" class="flex items-center space-x-2 hover:opacity-80">-->
<!--        <BarChart2 class="h-6 w-6" />-->
<!--        <span class="text-xl font-semibold">Market Analysis</span>-->
<!--      </router-link>-->

<!--      <div class="flex items-center space-x-4">-->
<!--        &lt;!&ndash; Suchfeld mit Dropdown &ndash;&gt;-->
<!--        <div v-if="authStore.isAuthenticated" class="relative w-96">-->
<!--          <Input-->
<!--            v-model="searchQuery"-->
<!--            placeholder="Suche Symbol (z.B. AAPL, GOOGL)..."-->
<!--            class="w-full"-->
<!--            @input="handleSearchInput"-->
<!--            @focus="handleFocus"-->
<!--          />-->

<!--          &lt;!&ndash; Loading Indicator &ndash;&gt;-->
<!--          <div v-if="isLoading" class="absolute right-3 top-1/2 -translate-y-1/2">-->
<!--            <Loader2 class="h-4 w-4 animate-spin" />-->
<!--          </div>-->

<!--          &lt;!&ndash; Search Dropdown &ndash;&gt;-->
<!--          <div-->
<!--            v-if="showDropdown && searchResults.length > 0"-->
<!--            class="absolute mt-1 w-full rounded-lg border bg-background shadow-lg z-50"-->
<!--            v-click-outside="handleClickOutside"-->
<!--          >-->
<!--            <div class="max-h-[300px] overflow-y-auto p-2">-->
<!--              <div-->
<!--                v-for="result in searchResults"-->
<!--                :key="result.symbol"-->
<!--                class="flex cursor-pointer items-center space-x-3 rounded-md p-2 hover:bg-accent"-->
<!--                @click="selectStock(result)"-->
<!--              >-->
<!--                <div class="flex-1">-->
<!--                  <div class="font-medium">{{ result.symbol }}</div>-->
<!--                  <div class="text-sm text-muted-foreground">{{ result.name }}</div>-->
<!--                </div>-->
<!--                <div class="text-xs text-muted-foreground">-->
<!--                  {{ result.exchange }}-->
<!--                </div>-->
<!--              </div>-->
<!--            </div>-->
<!--          </div>-->
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


<template>
  <header class="border-b bg-background">
    <div class="container mx-auto flex items-center justify-between h-16 px-4 sm:px-6 md:px-8">
      <!-- Logo und Navigation -->
      <router-link to="/dashboard" class="flex items-center space-x-2 hover:opacity-80">
        <BarChart2 class="h-6 w-6" />
        <span class="text-xl font-semibold">Market Analysis</span>
      </router-link>

      <!-- Hamburger Menü für mobile Geräte -->
      <div class="sm:hidden">
        <Button variant="outline" size="icon" @click="toggleMobileMenu">
          <Menu class="h-5 w-5" />
        </Button>
      </div>

      <!-- Suchfeld auf größeren Geräten -->
      <div v-if="authStore.isAuthenticated" class="relative hidden sm:block w-96">
        <Input
          v-model="searchQuery"
          :placeholder="t('dashboard.searchPlaceholder')"
          class="w-full"
          @input="handleSearchInput"
          @focus="handleFocus"
        />
        <div v-if="isLoading" class="absolute right-3 top-1/2 -translate-y-1/2">
          <Loader2 class="h-4 w-4 animate-spin" />
        </div>

        <!-- Dropdown für Suchergebnisse -->
        <div
          v-if="showDropdown && searchResults.length > 0"
          class="absolute mt-1 w-full rounded-lg border bg-background shadow-lg z-50"
          v-click-outside="handleClickOutside"
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

      <!-- Rechte Seite: Language Toggle, Theme Toggle und Auth Buttons -->
      <div class="flex items-center space-x-2">
        <!-- Language Toggle -->
        <LanguageToggle />
        
        <!-- Theme Toggle Button -->
        <Button variant="outline" size="icon" @click="toggleTheme">
          <Sun v-if="isDark" class="h-5 w-5" />
          <Moon v-else class="h-5 w-5" />
        </Button>

        <!-- Auth Buttons -->
        <div v-if="authStore.isAuthenticated" class="flex items-center space-x-2">
          <Button variant="outline" @click="router.push('/ai-settings')">
            <Settings class="h-4 w-4 mr-2" />
            {{ t('nav.settings') }}
          </Button>
          <Button variant="outline" @click="handleLogout">
            <LogOut class="h-4 w-4 mr-2" />
            {{ t('nav.logout') }}
          </Button>
        </div>
        <div v-else>
          <Button @click="router.push('/login')" class="px-4 py-2">
            <LogIn class="h-4 w-4 mr-2" />
            {{ t('nav.login') }}
          </Button>
        </div>
      </div>
    </div>

    <!-- Mobile Menu (Dropdown für kleine Bildschirme) -->
    <div v-if="isMobileMenuOpen" class="sm:hidden absolute top-16 left-0 w-full bg-background p-4">
      <div class="flex flex-col space-y-2">
        <router-link to="/dashboard" class="text-lg py-2">Dashboard</router-link>
        <router-link v-if="authStore.isAuthenticated" to="/ai-settings" class="text-lg py-2">Einstellungen</router-link>
        <Button variant="outline" @click="toggleTheme" class="w-full py-2">
          <Sun v-if="isDark" class="h-5 w-5" />
          <Moon v-else class="h-5 w-5" />
        </Button>
        <div v-if="authStore.isAuthenticated">
          <Button variant="outline" @click="handleLogout" class="w-full py-2">
            <LogOut class="h-4 w-4 mr-2" />
            Logout
          </Button>
        </div>
        <div v-else>
          <Button @click="router.push('/login')" class="w-full py-2">
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
import { useI18n } from 'vue-i18n'
import { useThemeStore } from '@/stores/theme'
import { useAuthStore } from '@/stores/auth'
import { BarChart2, Sun, Moon, LogIn, LogOut, Loader2, Settings, Menu } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { useDebounce } from '@/composables/useDebounce'
import LanguageToggle from '@/components/LanguageToggle.vue'
import axios from 'axios'

const router = useRouter()
const { t } = useI18n()
const authStore = useAuthStore()
const themeStore = useThemeStore()

const searchQuery = ref('')
const searchResults = ref([])
const showDropdown = ref(false)  // Dropdown zu Beginn auf false setzen
const isLoading = ref(false)
const isDark = ref(themeStore.isDark)
const isMobileMenuOpen = ref(false)

// Methode, um das Dropdown anzuzeigen oder zu verstecken
const toggleDropdown = (state) => {
  showDropdown.value = state
}

// Methode, die beim Fokussieren des Suchfeldes aufgerufen wird
const handleFocus = () => {
  // Zeige das Dropdown nur an, wenn es Suchergebnisse gibt oder der Benutzer Text eingibt
  if (searchQuery.value.trim() || searchResults.value.length > 0) {
    showDropdown.value = true
  }
}

// Methode, die aufgerufen wird, wenn ein Klick außerhalb erkannt wird
const handleClickOutside = () => {
  showDropdown.value = false  // Dropdown schließen, wenn außerhalb geklickt wird
}

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

  // Dropdown nur öffnen, wenn Ergebnisse vorhanden sind oder beim ersten Tippen
  if (searchQuery.value.trim() || searchResults.value.length > 0) {
    showDropdown.value = true
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

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  themeStore.isDark = savedTheme === 'dark'
  document.documentElement.classList.toggle('dark', themeStore.isDark)
})
</script>
