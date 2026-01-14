<!--// src/App.vue-->
<!--<script setup>-->
<!--import { onMounted } from 'vue'-->
<!--import { useAuthStore } from '@/stores/auth'-->
<!--import { Toaster } from '@/components/ui/toast'-->

<!--const authStore = useAuthStore()-->

<!--onMounted(async () => {-->
<!--  if (authStore.token) {-->
<!--    await authStore.checkAuth()-->
<!--  }-->
<!--})-->
<!--</script>-->

<!--<template>-->
<!--  <Main>-->
<!--    <RouterView />-->
<!--    <Toaster />-->
<!--  </Main>-->
<!--</template>-->

// src/App.vue
<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { Toaster } from '@/components/ui/toast'
import Main from '@/layouts/Main.vue'

const authStore = useAuthStore()

onMounted(async () => {
  // Check if we have a token in localStorage (before loading from store)
  const hasStoredToken = localStorage.getItem('auth_token')
  if (hasStoredToken || authStore.token) {
    await authStore.checkAuth()
  }
})
</script>

<template>
  <!-- Login-Seite ohne Main Layout -->
  <template v-if="$route.meta.hideLayout">
    <RouterView />
  </template>

  <!-- Alle anderen Seiten mit Main Layout -->
  <Main v-else />

  <Toaster />
</template>