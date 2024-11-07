// src/views/HomeView.vue
<script setup>
import { useAuthStore } from '@/stores/auth'
import { Button } from '@/components/ui/button'
import { useRouter } from 'vue-router'

const router = useRouter()
const authStore = useAuthStore()
</script>

<template>
  <div class="min-h-screen bg-background">
    <!-- Navigation -->
    <nav class="border-b">
      <div class="container mx-auto px-4 py-4 flex justify-between items-center">
        <h1 class="text-xl font-bold">Market Analysis</h1>
        <div v-if="authStore.isAuthenticated" class="flex items-center gap-4">
          <span>Welcome, {{ authStore.user?.username }}</span>
          <Button variant="outline" @click="authStore.logout">Logout</Button>
        </div>
        <Button v-else @click="router.push('/login')">Login</Button>
      </div>
    </nav>

    <!-- Content -->
    <div class="container mx-auto px-4 py-8">
      <div v-if="authStore.isAuthenticated">
        <h2 class="text-2xl font-bold mb-4">Dashboard</h2>
        <!-- Hier kommen deine Market Analysis Komponenten -->
        <p>Your market analysis dashboard content will appear here.</p>
      </div>
      <div v-else class="text-center py-16">
        <h2 class="text-3xl font-bold mb-4">Welcome to Market Analysis</h2>
        <p class="mb-8 text-muted-foreground">
          Please login to access your market analysis dashboard.
        </p>
        <Button @click="router.push('/login')">
          Get Started
        </Button>
      </div>
    </div>
  </div>
</template>