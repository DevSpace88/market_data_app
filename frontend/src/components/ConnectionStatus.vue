<!--<template>-->
<!--  <div class="flex items-center gap-2 text-sm">-->
<!--    <div-->
<!--      class="w-2 h-2 rounded-full"-->
<!--      :class="isConnected ? 'bg-green-500' : 'bg-red-500'"-->
<!--    ></div>-->
<!--    <span class="text-muted-foreground">-->
<!--      {{ isConnected ? 'Live Updates' : 'Connecting...' }}-->
<!--    </span>-->
<!--  </div>-->
<!--</template>-->

<!--<script setup>-->
<!--import { useMarketStore } from '@/store/market'-->
<!--import { storeToRefs } from 'pinia'-->

<!--const store = useMarketStore()-->
<!--const { isConnected } = storeToRefs(store)-->
<!--</script>-->


<template>
  <div class="flex items-center gap-2">
    <div
      class="w-2 h-2 rounded-full"
      :class="isConnected ? 'bg-green-500' : 'bg-red-500'"
    ></div>
    <span class="text-sm text-muted-foreground">
      {{ isConnected ? 'Live' : 'Connecting...' }}
    </span>
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { useMarketStore } from '@/store/market'

const store = useMarketStore()
const { isConnected } = storeToRefs(store)
</script>