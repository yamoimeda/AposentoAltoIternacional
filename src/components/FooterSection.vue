<template>
  <footer class="relative bg-gradient-to-br from-gray-900 via-indigo-900 to-purple-900 text-white py-10">
    <div class="container mx-auto px-4">
      <div class="flex flex-col md:flex-row md:justify-between md:items-center gap-8">
        <!-- Logo y redes -->
        <div class="flex flex-col items-center md:items-start gap-4">
          <h3 class="text-lg font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
            El Aposento Alto Internacional
          </h3>
          <div class="flex space-x-3">
            <a href="https://www.facebook.com/AposentoAltopty?_rdr" class="w-9 h-9 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center hover:scale-110 transition">
              <i class="fab fa-facebook-f text-white"></i>
            </a>
            <a href="https://www.instagram.com/aposentoaltopty" class="w-9 h-9 bg-gradient-to-r from-pink-500 to-rose-600 rounded-xl flex items-center justify-center hover:scale-110 transition">
              <i class="fab fa-instagram text-white"></i>
            </a>
            <a href="https://www.youtube.com/@AposentoAltoInternacional" class="w-9 h-9 bg-gradient-to-r from-red-500 to-red-600 rounded-xl flex items-center justify-center hover:scale-110 transition">
              <i class="fab fa-youtube text-white"></i>
            </a>
          </div>
        </div>
        <!-- Enlaces rápidos -->
        <div class="flex flex-col items-center md:items-start gap-2">
          <router-link to="/" class="text-gray-300 hover:text-white text-sm transition">Inicio</router-link>
          <router-link to="/nosotros" class="text-gray-300 hover:text-white text-sm transition">Nosotros</router-link>
          <router-link to="/eventos" class="text-gray-300 hover:text-white text-sm transition">Eventos</router-link>
          <router-link to="/contacto" class="text-gray-300 hover:text-white text-sm transition">Contacto</router-link>
        </div>
        <!-- Contacto -->
        <div class="flex flex-col items-center md:items-end gap-2 text-sm">
          <span class="text-gray-300">Calle 6ta, Pueblo Nuevo, Panamá</span>
          <a href="tel:+507000000" class="text-gray-300 hover:text-white transition">+507 000-000</a>
          <a href="mailto:info@aposentoalto.org" class="text-gray-300 hover:text-white transition">info@aposentoalto.org</a>
          <span class="text-gray-300">Dom: 10:00 AM | Mié/Vie: 7:00 PM</span>
        </div>
      </div>
      <div class="border-t border-white/10 mt-8 pt-4 flex flex-col md:flex-row justify-between items-center text-xs text-gray-400">
        <span>&copy; {{ new Date().getFullYear() }} El Aposento Alto Internacional. Todos los derechos reservados.</span>
        <a href="#" class="hover:text-white transition">Developer | Ing. Yamir Mena</a>
      </div>
    </div>
    <button 
      v-show="mostrarBotonArriba"
      @click="volverArriba"
      class="fixed bottom-8 right-8 w-12 h-12 bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-xl shadow-2xl hover:scale-110 transition z-50 flex items-center justify-center"
      title="Volver arriba"
    >
      <i class="fas fa-chevron-up"></i>
    </button>
  </footer>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const mostrarBotonArriba = ref(false)

const volverArriba = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

const manejarScroll = () => {
  mostrarBotonArriba.value = window.scrollY > 300
}

onMounted(() => {
  window.addEventListener('scroll', manejarScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', manejarScroll)
})
</script>