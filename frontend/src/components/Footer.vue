<template>
  <footer class="bg-background border-t border-border mt-auto">
    <div class="container mx-auto px-4 py-8">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <!-- App Info -->
        <div class="space-y-4">
          <h3 class="text-lg font-semibold text-foreground">{{ t('footer.appName') }}</h3>
          <p class="text-sm text-muted-foreground">{{ t('footer.tagline') }}</p>
          <div class="flex items-center space-x-2 text-sm text-muted-foreground">
            <div class="w-2 h-2 bg-green-500 rounded-full"></div>
            <span>{{ t('footer.liveData') }}</span>
          </div>
        </div>

        <!-- Features -->
        <div class="space-y-4">
          <h3 class="text-lg font-semibold text-foreground">{{ t('footer.features') }}</h3>
          <ul class="space-y-2 text-sm text-muted-foreground">
            <li class="flex items-center space-x-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
              <span>{{ t('footer.realtimeCharts') }}</span>
            </li>
            <li class="flex items-center space-x-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
              </svg>
              <span>{{ t('footer.aiAnalysis') }}</span>
            </li>
            <li class="flex items-center space-x-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
              </svg>
              <span>{{ t('footer.watchlist') }}</span>
            </li>
            <li class="flex items-center space-x-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
              </svg>
              <span>{{ t('footer.hotStocks') }}</span>
            </li>
          </ul>
        </div>

        <!-- Data Sources & Info -->
        <div class="space-y-4">
          <h3 class="text-lg font-semibold text-foreground">{{ t('footer.dataSources') }}</h3>
          <div class="space-y-2 text-sm text-muted-foreground">
            <p>{{ t('footer.poweredBy', { provider: 'Yahoo Finance' }) }}</p>
            <p>{{ t('footer.aiVia', { provider: 'LangChain' }) }}</p>
            <p class="text-xs text-muted-foreground/70">{{ t('footer.updatedEvery') }}</p>
          </div>
          
          <!-- Cache Status -->
          <div class="pt-4 border-t border-border">
            <div class="flex items-center justify-between text-xs text-muted-foreground">
              <span>{{ t('footer.cacheStatus') }}</span>
              <div class="flex items-center space-x-1">
                <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span>{{ t('footer.active') }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Bottom Bar -->
      <div class="mt-8 pt-6 border-t border-border">
        <div class="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
          <div class="text-sm text-muted-foreground">
            © 2025 {{ t('footer.appName') }}. {{ t('footer.rights') }}
          </div>
          <div class="flex items-center space-x-4 text-sm text-muted-foreground">
            <span>{{ t('footer.version', { version: '1.0.0' }) }}</span>
            <!-- <span>•</span> -->
            <!-- <span>Made with ❤️</span> -->
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>
