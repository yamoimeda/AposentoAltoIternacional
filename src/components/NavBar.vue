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
              <p class="text-sm text-white">Ministerio Internacional</p>
            <h1 class="text-xl font-bold text-white group-hover:text-blue-600 transition-colors">
              El Aposento Alto
            </h1>
          </div>
        </router-link>

        <!-- Navegación Desktop -->
        <div class="hidden lg:flex items-center space-x-8 right-0 absolute">
          <router-link 
            to="/" 
            :class="['px-3 py-2 rounded-lg font-medium transition-colors hover:text-blue-600',
                     $route.path === '/' ? 'text-black bg-blue-50' : 'text-white']"
          >
            <i class="fas fa-home mr-2"></i>Inicio
          </router-link>
          <router-link 
            to="/eventos" 
            :class="['px-3 py-2 rounded-lg font-medium transition-colors hover:text-blue-600',
                     $route.path.includes('/eventos') || $route.path.includes('/evento') || $route.path.includes('/inscripcion') 
                     ? 'text-blue-600 bg-blue-50' : 'text-white']"
          >
            <i class="fas fa-calendar-alt mr-2"></i>Eventos
          </router-link>
          <router-link 
            to="/nosotros" 
            :class="['px-3 py-2 rounded-lg font-medium transition-colors hover:text-blue-600',
                     $route.path === '/nosotros' ? 'text-blue-600 bg-blue-50' : 'text-white']"
          >
            <i class="fas fa-users mr-2"></i>Nosotros
          </router-link>
          <router-link 
            to="/contacto" 
            :class="['px-3 py-2 rounded-lg font-medium transition-colors hover:text-blue-600',
                     $route.path === '/contacto' ? 'text-blue-600 bg-blue-50' : 'text-white']"
          >
            <i class="fas fa-envelope mr-2"></i>Contacto
          </router-link>
          
          <!-- Botón CTA -->
          <!-- <router-link 
            to="/eventos"
            class="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-2 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all shadow-md"
          >
            <i class="fas fa-user-plus mr-2"></i>Únete
          </router-link> -->
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
        class="lg:hidden bg-white border-t border-gray-200 py-4"
      >
        <div class="flex flex-col space-y-2">
          <router-link 
            to="/" 
            @click="menuMovilAbierto = false"
            :class="['px-4 py-3 rounded-lg font-medium transition-colors hover:bg-blue-50 hover:text-blue-600',
                     $route.path === '/' ? 'text-blue-600 bg-blue-50' : 'text-gray-700']"
          >
            <i class="fas fa-home mr-3"></i>Inicio
          </router-link>
          <router-link 
            to="/eventos" 
            @click="menuMovilAbierto = false"
            :class="['px-4 py-3 rounded-lg font-medium transition-colors hover:bg-blue-50 hover:text-blue-600',
                     $route.path.includes('/eventos') || $route.path.includes('/evento') || $route.path.includes('/inscripcion') 
                     ? 'text-blue-600 bg-blue-50' : 'text-gray-700']"
          >
            <i class="fas fa-calendar-alt mr-3"></i>Eventos
          </router-link>
          <router-link 
            to="/nosotros" 
            @click="menuMovilAbierto = false"
            :class="['px-4 py-3 rounded-lg font-medium transition-colors hover:bg-blue-50 hover:text-blue-600',
                     $route.path === '/nosotros' ? 'text-blue-600 bg-blue-50' : 'text-gray-700']"
          >
            <i class="fas fa-users mr-3"></i>Nosotros
          </router-link>
          <router-link 
            to="/contacto" 
            @click="menuMovilAbierto = false"
            :class="['px-4 py-3 rounded-lg font-medium transition-colors hover:bg-blue-50 hover:text-blue-600',
                     $route.path === '/contacto' ? 'text-blue-600 bg-blue-50' : 'text-gray-700']"
          >
            <i class="fas fa-envelope mr-3"></i>Contacto
          </router-link>
          
          <div class="px-4 py-2">
            <router-link 
              to="/eventos"
              @click="menuMovilAbierto = false"
              class="block bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all text-center"
            >
              <i class="fas fa-user-plus mr-2"></i>Únete a Nosotros
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Barra de información superior (opcional) -->
    <!-- <div class="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-2 text-center text-sm">
      <div class="container mx-auto px-4">
        <p>
          <i class="fas fa-calendar-alt mr-2"></i>
          Próximo Culto: Domingo 10:00 AM • 
          <i class="fas fa-map-marker-alt mx-2"></i>
          Av. Principal 123 • 
          <i class="fas fa-phone ml-2 mr-1"></i>
          +1 (555) 123-4567
        </p>
      </div>
    </div> -->
  </nav>

  
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const menuMovilAbierto = ref(false)
const mostrarNav = ref(true)
let ultimoScroll = window.scrollY

const handleScroll = () => {
  const actualScroll = window.scrollY
  if (actualScroll > ultimoScroll && actualScroll > 80) {
    mostrarNav.value = false // Oculta nav al bajar
  } else {
    mostrarNav.value = true // Muestra nav al subir
  }
  ultimoScroll = actualScroll
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>
