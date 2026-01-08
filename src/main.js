import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { useEventosStore } from './stores/eventos'
import '@fortawesome/fontawesome-free/css/all.css';
import router from './router'
import App from './App.vue'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

const eventosStore = useEventosStore()
if (typeof eventosStore.cargarEventos === 'function') {
	eventosStore.cargarEventos()
} else {
	console.warn('eventosStore.cargarEventos is not available')
}
app.mount('#app')
