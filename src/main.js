
import { useEventosStore } from './stores/eventos'

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.use(router)

// Cargar eventos desde Firestore al iniciar
const eventosStore = useEventosStore()
eventosStore.cargarEventos()

app.mount('#app')
