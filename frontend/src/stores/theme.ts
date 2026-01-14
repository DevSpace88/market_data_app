/**
 * Theme Store - Pinia store with TypeScript
 *
 * Handles application theme (light/dark mode) switching.
 */

import { defineStore } from 'pinia'
import { ref } from 'vue'

export type ThemeMode = 'light' | 'dark'

export const useThemeStore = defineStore('theme', () => {
  const isDark = ref<boolean>(false)

  /**
   * Toggle between light and dark theme
   */
  const toggleTheme = (): void => {
    isDark.value = !isDark.value
    document.documentElement.classList.toggle('dark', isDark.value)
    localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
  }

  /**
   * Initialize theme from localStorage or system preference
   */
  const initTheme = (): void => {
    const savedTheme = localStorage.getItem('theme') as ThemeMode | null

    if (savedTheme) {
      isDark.value = savedTheme === 'dark'
    } else {
      // Check system preference
      isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
    }

    // Apply theme to DOM
    if (isDark.value) {
      document.documentElement.classList.add('dark')
    }
  }

  /**
   * Set theme explicitly
   */
  const setTheme = (theme: ThemeMode): void => {
    isDark.value = theme === 'dark'
    if (theme === 'dark') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
    localStorage.setItem('theme', theme)
  }

  return {
    isDark,
    toggleTheme,
    initTheme,
    setTheme
  }
})
