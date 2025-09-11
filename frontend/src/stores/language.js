import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useLanguageStore = defineStore('language', () => {
  const currentLanguage = ref(localStorage.getItem('language') || 'en')
  
  const setLanguage = (lang) => {
    currentLanguage.value = lang
    localStorage.setItem('language', lang)
  }
  
  const toggleLanguage = () => {
    const newLang = currentLanguage.value === 'en' ? 'de' : 'en'
    setLanguage(newLang)
  }
  
  return {
    currentLanguage,
    setLanguage,
    toggleLanguage
  }
})
