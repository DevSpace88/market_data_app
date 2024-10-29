<template>
  <div class="flex space-x-2">
    <Button
      v-for="tf in timeframes"
      :key="tf"
      :variant="selected === tf ? 'default' : 'outline'"
      size="sm"
      @click="handleSelect(tf)"
    >
      {{ tf }}
    </Button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Button } from '@/components/ui/button'

const props = defineProps({
  modelValue: String
})

const emit = defineEmits(['change'])

const timeframes = ['1D', '1W', '1M', '3M', 'YTD']
const selected = ref(props.modelValue || '1D')

const handleSelect = (tf) => {
  selected.value = tf
  emit('change', tf)
}
</script>