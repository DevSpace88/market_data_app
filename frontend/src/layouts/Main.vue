<template>
  <div class="min-h-screen bg-background text-foreground flex flex-col">
    <Header />
    <main class="container mx-auto p-4 flex-1">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    <Footer />
  </div>
</template>

<script setup>
import Header from "@/components/Header.vue"
import Footer from "@/components/Footer.vue"
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>