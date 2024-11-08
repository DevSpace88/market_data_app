// src/views/SymbolNotFound.vue
<script setup>
import { Button } from '@/components/ui/button'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const symbol = route.params.symbol
</script>

<template>
  <div class="container mx-auto p-4">
    <div class="rounded-lg border bg-card p-8 text-center space-y-6">
      <h1 class="text-3xl font-bold">Symbol nicht gefunden</h1>
      <p class="text-xl text-muted-foreground">
        Das Symbol "{{ symbol }}" konnte nicht gefunden werden.
      </p>
      <div class="space-y-2">
        <p class="text-muted-foreground">
          Mögliche Gründe:
        </p>
        <ul class="text-sm text-muted-foreground">
          <li>Das Symbol existiert nicht</li>
          <li>Tippfehler im Symbol</li>
          <li>Das Symbol wird nicht mehr gehandelt</li>
        </ul>
      </div>
      <div class="space-x-4">
        <Button @click="router.push('/dashboard')">
          Zurück zum Dashboard
        </Button>
      </div>
    </div>
  </div>
</template>