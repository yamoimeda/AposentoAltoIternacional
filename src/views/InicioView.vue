<script setup>
import { onMounted, computed } from 'vue'
import { useEventosStore } from '../stores/eventos'
import { useRouter } from 'vue-router'
import EventosInicio from '../components/EventosInicio.vue'
import HorariosCultos from '../components/HorariosCultos.vue'

const eventosStore = useEventosStore()
const router = useRouter()

const proximosEventos = computed(() => {
  const ahora = new Date()
  return eventosStore.eventos
    .filter(evento => new Date(evento.fecha) >= ahora)
    .sort((a, b) => new Date(a.fecha) - new Date(b.fecha))
    .slice(0, 3)
})

const formatearFecha = (fecha) => {
  return new Date(fecha).toLocaleDateString('es-ES', {
    month: 'short',
    day: 'numeric'
  })
}

const verEvento = (evento) => {
  router.push(`/evento/${evento.id}`)
}

onMounted(() => {
  eventosStore.cargarEventos()
})
</script>

<template>
  <div class="min-h-screen">
    <!-- Hero Section moderna -->
    <section class="relative bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900 text-white py-32 overflow-hidden">
      <!-- Efectos de fondo -->
      <div class="absolute inset-0">
        <div class="absolute top-20 left-10 w-72 h-72 bg-gradient-to-r from-yellow-400 to-pink-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float"></div>
        <div class="absolute top-40 right-10 w-72 h-72 bg-gradient-to-r from-purple-400 to-blue-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float" style="animation-delay: 2s;"></div>
        <div class="absolute bottom-20 left-1/2 w-72 h-72 bg-gradient-to-r from-green-400 to-cyan-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float" style="animation-delay: 4s;"></div>
      </div>
      
      <!-- Partículas flotantes -->
      <div class="absolute inset-0 overflow-hidden">
        <div class="absolute top-1/4 left-1/4 w-2 h-2 bg-white rounded-full opacity-60 animate-pulse"></div>
        <div class="absolute top-1/3 right-1/4 w-1 h-1 bg-yellow-300 rounded-full opacity-80 animate-pulse" style="animation-delay: 1s;"></div>
        <div class="absolute bottom-1/3 left-1/3 w-3 h-3 bg-pink-300 rounded-full opacity-40 animate-pulse" style="animation-delay: 2s;"></div>
        <div class="absolute top-2/3 right-1/3 w-2 h-2 bg-blue-300 rounded-full opacity-70 animate-pulse" style="animation-delay: 3s;"></div>
      </div>

      <div class="relative container mx-auto px-4 text-center">
        <div class="animate-fade-in-up">
          <h1 class="text-6xl md:text-8xl font-black mb-8 leading-tight">
            Bienvenido a<br>
            <span class="bg-gradient-to-r from-yellow-400 via-pink-500 to-purple-500 bg-clip-text text-transparent animate-pulse">
              Aposento Alto Internacional
            </span>
          </h1>
          
          <div class="flex flex-col sm:flex-row gap-6 justify-center">
            <!-- <router-link 
              to="/eventos" 
              class="btn-modern bg-gradient-to-r from-yellow-400 via-orange-500 to-pink-500 text-black px-10 py-5 rounded-3xl font-bold text-xl hover:shadow-2xl hover:transform hover:scale-110 transition-all duration-300 inline-block relative overflow-hidden group"
            >
              <span class="relative z-10">
                <i class="fas fa-calendar-alt mr-3"></i>
                Explorar Eventos
              </span>
              <div class="absolute inset-0 bg-gradient-to-r from-pink-500 to-purple-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </router-link> -->
            <router-link 
              to="/eventos" 
              class="border-3 border-white/30 backdrop-blur-sm text-white px-10 py-5 rounded-3xl font-bold text-xl hover:bg-white hover:text-indigo-900 transition-all duration-300 inline-block hover:transform hover:scale-110"
            >
              <i class="fas fa-calendar-alt mr-3"></i>
              Explorar Eventos
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Próximos Eventos modernos -->
    <EventosInicio />

    <HorariosCultos/>

    <!-- Llamado a la Acción moderno -->
    <section class="py-24 relative">
      <div class="absolute inset-0 bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600"></div>
      <div class="absolute inset-0">
        <div class="absolute top-10 left-10 w-48 h-48 bg-white/10 rounded-full filter blur-3xl animate-float"></div>
        <div class="absolute bottom-10 right-10 w-48 h-48 bg-white/10 rounded-full filter blur-3xl animate-float" style="animation-delay: 2s;"></div>
      </div>
      
      <div class="relative container mx-auto px-4 text-center">
        <div class="animate-fade-in-up">
          <h2 class="text-5xl md:text-6xl font-black text-white mb-6">
            ¿Primera vez con nosotros?
          </h2>
          <p class="text-2xl text-blue-100 mb-12 max-w-3xl mx-auto font-light leading-relaxed">
            Te invitamos a conocer más sobre nuestra iglesia y cómo puedes ser parte de esta hermosa familia de fe
          </p>
          <div class="flex flex-col sm:flex-row gap-6 justify-center">
            <router-link 
              to="/nosotros" 
              class="bg-white text-blue-600 px-12 py-5 rounded-3xl font-bold text-xl hover:shadow-2xl hover:transform hover:scale-105 transition-all duration-300 inline-block"
            >
              <i class="fas fa-info-circle mr-3"></i>
              Conoce Nuestra Historia
            </router-link>
            <router-link 
              to="/contacto" 
              class="border-3 border-white/50 backdrop-blur-sm text-white px-12 py-5 rounded-3xl font-bold text-xl hover:bg-white hover:text-blue-600 transition-all duration-300 inline-block"
            >
              <i class="fas fa-phone mr-3"></i>
              Contáctanos
            </router-link>
          </div>
        </div>
      </div>
    </section>

   
  </div>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
