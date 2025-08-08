import { createRouter, createWebHistory } from 'vue-router'
import InicioView from '../views/InicioView.vue'
import EventosView from '../views/EventosView.vue'
import EventoDetalleView from '../views/EventoDetalleView.vue'
import InscripcionView from '../views/InscripcionView.vue'
import NosotrosView from '../views/NosotrosView.vue'
import ContactoView from '../views/ContactoView.vue'

const routes = [
    {   
        path: '/',
        name: 'Inicio',
        component: InicioView
    },
    {
        path: '/eventos',
        name: 'Eventos',
        component: EventosView
    },
    {
        path: '/evento/:id',
        name: 'EventoDetalle',
        component: EventoDetalleView
    },
    {
        path: '/inscripcion/:id',
        name: 'Inscripcion',
        component: InscripcionView
    },
    {
        path: '/nosotros',
        name: 'Nosotros',
        component: NosotrosView
    },
    {
        path: '/contacto',
        name: 'Contacto',
        component: ContactoView
    },
    // Ruta de fallback para páginas no encontradas
    {
        path: '/:pathMatch(.*)*',
        redirect: '/'
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
    // Scroll behavior para mejor UX
    scrollBehavior(to, from, savedPosition) {
        if (savedPosition) {
            return savedPosition
        } else {
            return { top: 0 }
        }
    }
})

export default router