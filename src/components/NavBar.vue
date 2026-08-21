<template>
<nav
    :class="[
      'top-0 left-0 w-full z-50 shadow-none bg-gray-900/20 backdrop-blur-lg shadow-lg transition-transform duration-300',
      mostrarNav ? 'fixed translate-y-0' : 'fixed -translate-y-full'
    ]"
  >    <div class="w-full relative px-4">
      <div class="flex w-full relative justify-between items-center py-4">
        <!-- Logo y Nombre -->
        <router-link to="/" class="flex items-center space-x-3 group">
          <div class="w-12 h-12 bg-gradient-to-br from-blue-600 to-purple-600 rounded-full flex items-center justify-center">
            <i class="fas fa-church text-white text-xl"></i>
          </div>
          <div>
            <h1 class="text-xl font-bold text-white group-hover:text-blue-600 transition-colors">
              El Aposento Alto
            </h1>
              <p class="text-sm text-white">Internacional</p>
          </div>
        </router-link>

        <!-- Navegación Desktop -->
        <div class="hidden lg:flex items-center space-x-8 right-0 absolute">
          <router-link 
            to="/" 
            :class="['px-2 py-1 rounded-lg text-sm font-medium transition-colors',
                     $route.path === '/' ? 'text-purple-700 bg-purple-50' : 'text-white', 'hover:text-purple-500']"
          >
            <i class="fas fa-home mr-2"></i>Inicio
          </router-link>
          <router-link 
            to="/eventos" 
            :class="['px-2 py-1 rounded-lg text-sm font-medium transition-colors',
                     $route.path.includes('/eventos') || $route.path.includes('/evento') || $route.path.includes('/inscripcion') 
                     ? 'text-purple-700 bg-purple-50' : 'text-white', 'hover:text-purple-500']"
          >
            <i class="fas fa-calendar-alt mr-2"></i>Eventos
          </router-link>
          <div class="flex items-center space-x-2">
            <router-link 
              to="/nosotros" 
              :class="['px-2 py-1 rounded-lg text-sm font-medium transition-colors',
                       $route.path === '/nosotros' ? 'text-purple-700 bg-purple-50' : 'text-white', 'hover:text-purple-500']"
            >
              <i class="fas fa-users mr-2"></i>Nosotros
            </router-link>
            <span class="text-gray-400">|</span>
            <router-link 
              to="/contacto" 
              :class="['px-2 py-1 rounded-lg text-sm font-medium transition-colors',
                       $route.path === '/contacto' ? 'text-purple-700 bg-purple-50' : 'text-white', 'hover:text-purple-500']"
            >
              <i class="fas fa-envelope mr-2"></i>Contacto
            </router-link>
          </div>

          <!-- Enlaces para roles autenticados -->
          <router-link
            v-if="isLoggedIn && userRoles.includes('admin')"
            to="/conteo"
            :class="['px-2 py-1 rounded-lg text-sm font-medium transition-colors',
                     $route.path.startsWith('/conteo') ? 'text-purple-700 bg-purple-50' : 'text-white', 'hover:text-purple-500']"
            title="Conteo de eventos (Solo Administradores)"
          >
            <i class="fas fa-chart-pie mr-2"></i>Conteo
          </router-link>

          <router-link
            v-if="isLoggedIn && (userRoles.includes('qr') || userRoles.includes('admin'))"
            to="/escanear-qr"
            :class="['px-2 py-1 rounded-lg text-sm font-medium transition-colors',
                     $route.path === '/escanear-qr' ? 'text-purple-700 bg-purple-50' : 'text-white', 'hover:text-purple-500']"
            title="Escáner QR de boletos"
          >
            <i class="fas fa-qrcode mr-2"></i>Escanear QR
          </router-link>

          <!-- Opción Iniciar/Cerrar sesión -->
          <template v-if="isLoggedIn">
            <div class="flex items-center gap-2 px-2.5 py-1 bg-white/10 backdrop-blur-md rounded-lg border border-white/20 text-xs text-white">
              <i class="fas fa-user-shield text-indigo-300"></i>
              <span class="font-medium max-w-[140px] truncate">{{ userEmail }}</span>
            </div>
            <router-link
              to="/admin"
              :class="['px-3 py-1.5 rounded-lg text-sm font-medium transition-colors flex items-center gap-1.5',
                       $route.path.startsWith('/admin') ? 'text-indigo-700 bg-white font-semibold' : 'text-white hover:text-indigo-200']"
            >
              <i class="fas fa-grip"></i>
              <span>Panel Admin</span>
            </router-link>
            <button
              @click="logout"
              class="px-3 py-1.5 rounded-lg text-sm font-semibold transition-all text-white bg-rose-600/80 hover:bg-rose-600 flex items-center gap-1.5 cursor-pointer"
            >
              <i class="fas fa-sign-out-alt"></i>
              <span>Salir</span>
            </button>
          </template>
          <template v-else>
            <router-link 
              to="/admin-login" 
              :class="['px-2 py-1 rounded-lg text-sm font-medium transition-colors',
                       $route.path === '/admin-login' ? 'text-purple-700 bg-purple-50' : 'text-white', 'hover:text-purple-700']"
            >
              <i class="fas fa-sign-in-alt mr-2"></i>Iniciar sesión
            </router-link>
          </template>
        </div>

        <!-- Botón Menú Mobile -->
        <button 
          @click="menuMovilAbierto = !menuMovilAbierto"
          class="lg:hidden p-2 rounded-lg text-gray-600 hover:text-blue-600 hover:bg-gray-100 transition-colors"
        >
          <i :class="['fas text-xl', menuMovilAbierto ? 'fa-times' : 'fa-bars']"></i>
        </button>
      </div>

      <!-- Menú Mobile -->
      <div 
        v-show="menuMovilAbierto"
        class="lg:hidden bg-white border-t border-gray-200 py-4 px-4 shadow-xl"
      >
        <div class="flex flex-col space-y-2">
          <!-- Active User Session Header (Mobile Hamburger) -->
          <div v-if="isLoggedIn" class="p-3 bg-slate-50 border border-slate-200/80 rounded-xl mb-2 flex items-center gap-3">
            <div class="w-9 h-9 rounded-lg bg-indigo-50 border border-indigo-100 flex items-center justify-center text-indigo-600 text-sm shrink-0">
              <i class="fas fa-user-shield"></i>
            </div>
            <div class="overflow-hidden leading-tight">
              <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">Sesión Activa</span>
              <span class="text-xs font-semibold text-slate-800 truncate block">{{ userEmail }}</span>
            </div>
          </div>

          <router-link 
            to="/" 
            @click="menuMovilAbierto = false"
            :class="['px-3 py-2 rounded-lg text-sm font-medium transition-colors',
                     $route.path === '/' ? 'text-purple-700 bg-purple-50' : 'text-gray-700', 'hover:bg-purple-50 hover:text-purple-500']"
          >
            <i class="fas fa-home mr-3"></i>Inicio
          </router-link>
          <router-link 
            to="/eventos" 
            @click="menuMovilAbierto = false"
            :class="['px-3 py-2 rounded-lg text-sm font-medium transition-colors',
                     $route.path.includes('/eventos') || $route.path.includes('/evento') || $route.path.includes('/inscripcion') 
                     ? 'text-purple-700 bg-purple-50' : 'text-gray-700', 'hover:bg-purple-50 hover:text-purple-500']"
          >
            <i class="fas fa-calendar-alt mr-3"></i>Eventos
          </router-link>
          <router-link 
            to="/nosotros" 
            @click="menuMovilAbierto = false"
            :class="['px-3 py-2 rounded-lg text-sm font-medium transition-colors',
                     $route.path === '/nosotros' ? 'text-purple-700 bg-purple-50' : 'text-gray-700', 'hover:bg-purple-50 hover:text-purple-500']"
          >
            <i class="fas fa-users mr-3"></i>Nosotros
          </router-link>
          <router-link 
            to="/contacto" 
            @click="menuMovilAbierto = false"
            :class="['px-3 py-2 rounded-lg text-sm font-medium transition-colors',
                     $route.path === '/contacto' ? 'text-purple-700 bg-purple-50' : 'text-gray-700', 'hover:bg-purple-50 hover:text-purple-500']"
          >
            <i class="fas fa-envelope mr-3"></i>Contacto
          </router-link>

          <!-- Opciones para roles específicos en móvil -->
          <router-link 
            v-if="isLoggedIn && userRoles.includes('admin')"
            to="/conteo" 
            @click="menuMovilAbierto = false"
            :class="['px-3 py-2 rounded-lg text-sm font-medium transition-colors',
                     $route.path.startsWith('/conteo') ? 'text-purple-700 bg-purple-50' : 'text-gray-700', 'hover:bg-purple-50 hover:text-purple-500']"
          >
            <i class="fas fa-chart-pie mr-3"></i>Conteo (Admin)
          </router-link>

          <router-link 
            v-if="isLoggedIn && (userRoles.includes('qr') || userRoles.includes('admin'))"
            to="/escanear-qr" 
            @click="menuMovilAbierto = false"
            :class="['px-3 py-2 rounded-lg text-sm font-medium transition-colors',
                     $route.path === '/escanear-qr' ? 'text-purple-700 bg-purple-50' : 'text-gray-700', 'hover:bg-purple-50 hover:text-purple-500']"
          >
            <i class="fas fa-qrcode mr-3"></i>Escanear QR
          </router-link>

          <!-- Opción Iniciar/Cerrar sesión en Menú Móvil -->
          <template v-if="isLoggedIn">
            <div class="pt-2 border-t border-slate-100 flex flex-col gap-2">
              <router-link
                to="/admin"
                @click="menuMovilAbierto = false"
                class="px-3 py-2 rounded-lg text-sm font-semibold text-indigo-700 bg-indigo-50 flex items-center gap-2"
              >
                <i class="fas fa-grip"></i>
                <span>Panel de Administración</span>
              </router-link>
              <button
                @click="logout"
                class="w-full px-3 py-2 rounded-lg text-sm font-semibold text-rose-700 bg-rose-50 hover:bg-rose-100 transition-colors flex items-center justify-center gap-2 cursor-pointer"
              >
                <i class="fas fa-sign-out-alt"></i>
                <span>Cerrar sesión</span>
              </button>
            </div>
          </template>
          <template v-else>
            <router-link 
              to="/admin-login" 
              @click="menuMovilAbierto = false"
              :class="['px-3 py-2 rounded-lg text-sm font-medium transition-colors',
                       $route.path === '/admin-login' ? 'text-purple-700 bg-purple-50' : 'text-gray-700', 'hover:bg-purple-100 hover:text-purple-700']"
            >
              <i class="fas fa-sign-in-alt mr-3"></i>Iniciar sesión
            </router-link>
          </template>
        </div>
      </div>
    </div>
  </nav>

  
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { auth } from '../firebase'
import { signOut } from 'firebase/auth'
import { obtenerRolesUsuario } from '../utils/authRoles'

const menuMovilAbierto = ref(false)
const mostrarNav = ref(true)
let ultimoScroll = window.scrollY

const isLoggedIn = ref(false)
const userEmail = ref('')
const userRoles = ref([])

const handleScroll = () => {
  const actualScroll = window.scrollY
  if (actualScroll > ultimoScroll && actualScroll > 80) {
    mostrarNav.value = false // Oculta nav al bajar
  } else {
    mostrarNav.value = true // Muestra nav al subir
  }
  ultimoScroll = actualScroll
}

const logout = async () => {
  await signOut(auth)
  window.location.href = '/admin-login'
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  auth.onAuthStateChanged(async (user) => {
    isLoggedIn.value = !!user
    userEmail.value = user ? user.email : ''
    if (user) {
      userRoles.value = await obtenerRolesUsuario(user)
    } else {
      userRoles.value = []
    }
  })
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>
