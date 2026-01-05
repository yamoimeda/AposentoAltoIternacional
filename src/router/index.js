import { createRouter, createWebHistory } from 'vue-router'
import InicioView from '../views/InicioView.vue'
import EventosView from '../views/EventosView.vue'
import EventoDetalleView from '../views/EventoDetalleView.vue'
import InscripcionView from '../views/InscripcionView.vue'
import VerificarInscripcionView from '../views/VerificarInscripcionView.vue'
import NosotrosView from '../views/NosotrosView.vue'
import ContactoView from '../views/ContactoView.vue'
import AdminLogin from '../views/AdminLogin.vue'
import AdminPanel from '../views/AdminPanel.vue'
import AdminInscripcionesView from '../views/AdminInscripcionesView.vue'
import { auth } from '../firebase'

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
        path: '/verificar-inscripcion/:eventoId?',
        name: 'VerificarInscripcion',
        component: VerificarInscripcionView
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
    {
        path: '/admin-login',
        name: 'AdminLogin',
        component: AdminLogin
    },
    {
        path: '/admin',
        name: 'AdminPanel',
        component: AdminPanel,
        meta: { requiresAuth: true }
    },
    {
        path: '/admin/inscripciones',
        name: 'AdminInscripciones',
        component: AdminInscripcionesView,
        meta: { requiresAuth: true }
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

// Protección de ruta admin
router.beforeEach((to, from, next) => {
    if (to.meta.requiresAuth) {
        const unsubscribe = auth.onAuthStateChanged(user => {
            unsubscribe()
            if (user) {
                next()
            } else {
                next('/admin-login')
            }
        })
    } else {
        next()
    }
})

export default router