<!--<template>-->
<!--  <div class="flex space-x-2">-->
<!--    <Button-->
<!--      v-for="tf in timeframes"-->
<!--      :key="tf"-->
<!--      :variant="selected === tf ? 'default' : 'outline'"-->
<!--      size="sm"-->
<!--      @click="handleSelect(tf)"-->
<!--    >-->
<!--      {{ tf }}-->
<!--    </Button>-->
<!--  </div>-->
<!--</template>-->

<!--<script setup>-->
<!--import { ref } from 'vue'-->
<!--import { Button } from '@/components/ui/button'-->

<!--const props = defineProps({-->
<!--  modelValue: String-->
<!--})-->

<!--const emit = defineEmits(['change'])-->

<!--const timeframes = ['1D', '1W', '1M', '3M', '6M', '1Y', 'YTD']-->
<!--const selected = ref(props.modelValue || '1D')-->

<!--const handleSelect = (tf) => {-->
<!--  selected.value = tf-->
<!--  emit('change', tf)-->
<!--}-->
<!--</script>-->


<template>
  <div class="flex flex-wrap space-x-2 sm:space-x-4 sm:flex-nowrap">
    <Button
      v-for="tf in timeframes"
      :key="tf"
      :variant="selected === tf ? 'default' : 'outline'"
      size="sm"
      class="mb-2 sm:mb-0"
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

const timeframes = ['1D', '1W', '1M', '3M', '6M', '1Y', 'YTD']
const selected = ref(props.modelValue || '1D')

const handleSelect = (tf) => {
  selected.value = tf
  emit('change', tf)
}
</script>
