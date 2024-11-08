// src/views/NotFound.vue
<script setup>
import { Button } from '@/components/ui/button'
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-background">
    <div class="text-center space-y-6">
      <h1 class="text-9xl font-bold text-primary">404</h1>
      <p class="text-2xl text-muted-foreground">Seite nicht gefunden</p>
      <div class="space-x-4">
        <Button @click="router.push('/dashboard')">
          Zum Dashboard
        </Button>
        <Button variant="outline" @click="router.back()">
          Zurück
        </Button>
      </div>
    </div>
  </div>
</template>