import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.bundle.js'
import 'remixicon/fonts/remixicon.css'
import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia';

const app = createApp(App)

app.use(router)
app.use(createPinia())
app.mount('#app')
