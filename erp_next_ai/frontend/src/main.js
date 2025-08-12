import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createHead } from '@vueuse/head'
import router from './router'
import App from './App.vue'

// Styles
import './assets/css/main.css'
import 'frappe-ui/style.css'

// Frappe UI
import { FrappeUI } from 'frappe-ui'

// Create Vue app
const app = createApp(App)

// Use plugins
app.use(createPinia())
app.use(createHead())
app.use(router)
app.use(FrappeUI)

// Global error handler
app.config.errorHandler = (err, vm, info) => {
  console.error('Global error:', err)
  console.error('Component:', vm)
  console.error('Info:', info)
}

// Mount app
app.mount('#app')