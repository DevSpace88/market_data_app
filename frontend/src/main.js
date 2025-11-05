// import { createApp } from 'vue'
// import { createPinia } from 'pinia'
// import App from './App.vue'
// import router from './router'
// import './assets/styles/main.css'
//
// const app = createApp(App)
// const pinia = createPinia()
//
// app.use(pinia)
// app.use(router)
// app.mount('#app')

// // main.js oder main.ts
// import { createApp } from 'vue';
// import App from './App.vue';
// import router from './router'; // Falls Sie Vue Router verwenden
// import { createPinia } from 'pinia';
// import './assets/styles/main.css'
//
// const app = createApp(App);
//
// // Definieren der v-click-outside-Direktive
// app.directive('click-outside', {
//   beforeMount(el, binding) {
//     el.clickOutsideHandler = (event) => {
//       // Prüfen, ob der Klick außerhalb des Elements erfolgt ist
//       if (!(el === event.target || el.contains(event.target))) {
//         binding.value(event); // Die übergebene Funktion ausführen
//       }
//     };
//     document.addEventListener('click', el.clickOutsideHandler);
//   },
//   unmounted(el) {
//     document.removeEventListener('click', el.clickOutsideHandler);
//     delete el.clickOutsideHandler;
//   }
// });
//
// app.use(router);
// app.use(createPinia());
// app.mount('#app');

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import './assets/styles/main.css'
import axios from 'axios'
import i18n from './i18n'

// Axios Konfiguration
axios.defaults.baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
axios.defaults.headers.common['Accept'] = 'application/json'
axios.interceptors.request.use(request => {
  const token = localStorage.getItem('token')
  if (token) {
    request.headers.Authorization = `Bearer ${token}`
  }
  return request
})

axios.interceptors.response.use(
  response => {
    return response
  },
  error => {
    return Promise.reject(error)
  }
)

const app = createApp(App)

// v-click-outside Direktive
app.directive('click-outside', {
  beforeMount(el, binding) {
    el.clickOutsideHandler = (event) => {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value(event)
      }
    }
    document.addEventListener('click', el.clickOutsideHandler)
  },
  unmounted(el) {
    document.removeEventListener('click', el.clickOutsideHandler)
    delete el.clickOutsideHandler
  }
})

app.use(router)
app.use(createPinia())
app.use(i18n)

// Set initial locale from localStorage
const savedLanguage = localStorage.getItem('language') || 'en'
i18n.global.locale.value = savedLanguage

app.mount('#app')