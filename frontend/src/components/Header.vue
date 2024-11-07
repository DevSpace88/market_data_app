<!--<template>-->
<!--  <header class="border-b bg-background">-->
<!--    <div class="container mx-auto flex h-16 items-center justify-between px-4">-->
<!--      <router-link to="/" class="flex items-center space-x-2 hover:opacity-80">-->
<!--        <BarChart2 class="h-6 w-6" />-->
<!--        <span class="text-xl font-semibold">Market Analysis</span>-->
<!--      </router-link>-->

<!--      <div class="flex items-center space-x-4">-->
<!--        <div class="relative w-96">-->
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

<!--        &lt;!&ndash; Theme Toggle &ndash;&gt;-->
<!--        <Button variant="outline" size="icon" @click="toggleTheme">-->
<!--          <Sun v-if="isDark" class="h-5 w-5" />-->
<!--          <Moon v-else class="h-5 w-5" />-->
<!--        </Button>-->
<!--      </div>-->
<!--    </div>-->
<!--  </header>-->
<!--</template>-->

<!--<script setup>-->
<!--import { ref, onMounted } from 'vue'-->
<!--import { useRouter } from 'vue-router'-->
<!--import { useThemeStore } from '@/stores/theme'  // Darkmode Store importieren-->
<!--import { BarChart2, Search, Sun, Moon } from 'lucide-vue-next'-->
<!--import { Button } from '@/components/ui/button'-->
<!--import { Input } from '@/components/ui/input'-->

<!--const router = useRouter()-->
<!--const searchQuery = ref('')-->
<!--const themeStore = useThemeStore()-->

<!--const isDark = ref(themeStore.isDark)-->

<!--// Suche ausführen-->
<!--const handleSearch = () => {-->
<!--  if (searchQuery.value) {-->
<!--    router.push(`/symbol/${searchQuery.value.toUpperCase()}`)-->
<!--    searchQuery.value = ''-->
<!--  }-->
<!--}-->

<!--// Theme umschalten-->
<!--const toggleTheme = () => {-->
<!--  themeStore.toggleTheme()-->
<!--  isDark.value = themeStore.isDark-->
<!--}-->

<!--// Initiales Theme setzen-->
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
        <!-- Suchfeld nur anzeigen wenn eingeloggt -->
        <div v-if="authStore.isAuthenticated" class="relative w-96">
          <Input
            v-model="searchQuery"
            placeholder="Suche Symbol (z.B. AAPL, GOOGL)..."
            class="w-full"
            @keyup.enter="handleSearch"
          />
          <Button variant="ghost" class="absolute right-0 top-0 h-full px-3" @click="handleSearch">
            <Search class="h-4 w-4" />
          </Button>
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
import { BarChart2, Search, Sun, Moon, LogIn, LogOut } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()
const searchQuery = ref('')
const isDark = ref(themeStore.isDark)

const handleSearch = () => {
  if (searchQuery.value) {
    router.push(`/symbol/${searchQuery.value.toUpperCase()}`)
    searchQuery.value = ''
  }
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