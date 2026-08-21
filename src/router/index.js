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
import ConteoView from '../views/ConteoView.vue'
import EscanearQRView from '../views/EscanearQRView.vue'
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
        path: '/conteo/:eventoId?',
        name: 'Conteo',
        component: ConteoView,
        meta: { requiresAuth: true, requiredRole: 'admin' }
    },
    {
        path: '/escanear-qr',
        name: 'EscanearQR',
        component: EscanearQRView,
        meta: { requiresAuth: true, requiredRoles: ['qr', 'admin'] }
    },
    {
        path: '/admin/escanear-qr',
        redirect: '/escanear-qr'
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

import { obtenerRolesUsuario } from '../utils/authRoles'

// Protección de rutas por autenticación y roles
router.beforeEach((to, from, next) => {
    if (to.meta.requiresAuth) {
        const unsubscribe = auth.onAuthStateChanged(async (user) => {
            unsubscribe()
            if (!user) {
                return next({
                    path: '/admin-login',
                    query: { redirect: to.fullPath }
                })
            }

            // Validación granular por roles
            if (to.meta.requiredRole || to.meta.requiredRoles) {
                const roles = await obtenerRolesUsuario(user)

                // Si requiere rol admin estricto
                if (to.meta.requiredRole === 'admin' && !roles.includes('admin')) {
                    alert('⛔ Acceso restringido: Esta sección de conteo está reservada únicamente para Administradores.')
                    return next('/admin')
                }

                // Si requiere uno de los roles autorizados (ej. qr o admin)
                if (to.meta.requiredRoles && !to.meta.requiredRoles.some(r => roles.includes(r))) {
                    alert('⛔ Acceso restringido: Tu cuenta no tiene permisos para escanear boletos QR.')
                    return next('/admin')
                }
            }

            next()
        })
    } else {
        next()
    }
})

export default router