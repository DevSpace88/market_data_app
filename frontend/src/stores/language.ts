/**
 * Language Store - Pinia store with TypeScript
 *
 * Handles application language (English/German) switching.
 */

import { defineStore } from 'pinia'
import { ref } from 'vue'

export type SupportedLanguage = 'en' | 'de'

export const useLanguageStore = defineStore('language', () => {
  const currentLanguage = ref<SupportedLanguage>(
    (localStorage.getItem('language') as SupportedLanguage) || 'en'
  )

  /**
   * Set the application language
   */
  const setLanguage = (lang: SupportedLanguage): void => {
    currentLanguage.value = lang
    localStorage.setItem('language', lang)
  }

  /**
   * Toggle between English and German
   */
  const toggleLanguage = (): void => {
    const newLang: SupportedLanguage = currentLanguage.value === 'en' ? 'de' : 'en'
    setLanguage(newLang)
  }

  return {
    currentLanguage,
    setLanguage,
    toggleLanguage
  }
})
