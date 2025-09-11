<template>
  <div class="relative">
    <button
      @click="toggleLanguage"
      class="flex items-center space-x-2 px-3 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md transition-colors"
    >
      <Globe class="w-4 h-4" />
      <span>{{ currentLanguage === 'en' ? 'EN' : 'DE' }}</span>
      <ChevronDown class="w-3 h-3" />
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useLanguageStore } from '@/stores/language'
import { Globe, ChevronDown } from 'lucide-vue-next'

const { locale } = useI18n()
const languageStore = useLanguageStore()

const currentLanguage = computed(() => locale.value)

const toggleLanguage = () => {
  const newLang = locale.value === 'en' ? 'de' : 'en'
  locale.value = newLang
  languageStore.setLanguage(newLang)
}
</script>
