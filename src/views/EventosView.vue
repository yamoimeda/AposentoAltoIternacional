<template>
  <div class="min-h-screen">
    <!-- Header de la sección moderno -->
    <div class="relative bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900 text-white py-24 overflow-hidden">
      <!-- Efectos de fondo -->
      <div class="absolute inset-0">
        <div class="absolute top-20 left-10 w-64 h-64 bg-gradient-to-r from-yellow-400 to-pink-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float"></div>
        <div class="absolute bottom-20 right-10 w-64 h-64 bg-gradient-to-r from-blue-400 to-purple-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float" style="animation-delay: 2s;"></div>
      </div>

      <div class="relative container mx-auto px-4 text-center pt-[50px]">
        <div class="animate-fade-in-up">
          <div class="inline-flex items-center bg-white/10 backdrop-blur-sm text-white px-6 py-3 rounded-full text-sm font-semibold mb-6 border border-white/20">
            <i class="fas fa-calendar-alt mr-2"></i>
            Eventos
          </div>
          <h1 class="text-5xl md:text-7xl font-black mb-6">
            <span class="bg-gradient-to-r from-yellow-400 via-pink-500 to-purple-500 bg-clip-text text-transparent">
              Eventos Especiales
            </span>
          </h1>
          <p class="text-2xl text-indigo-200 max-w-3xl mx-auto font-light">
            Únete a nuestras actividades y crece en comunidad con experiencias transformadoras
          </p>
        </div>

        
      </div>
    </div>

    <!-- Filtros modernos -->
    <div class="py-12 relative">
      <div class="absolute inset-0 bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50"></div>
      <div class="relative container mx-auto px-4">
        <div class="flex flex-wrap gap-4 justify-center">
          <button 
            @click="filtroActivo = 'todos'"
            :class="['px-8 py-4 rounded-3xl font-bold transition-all duration-300 hover:transform hover:scale-105 shadow-lg',
                     filtroActivo === 'todos' 
                     ? 'bg-gradient-to-r from-indigo-500 to-purple-600 text-white shadow-xl' 
                     : 'bg-white/80 backdrop-blur-sm text-gray-700 hover:bg-white border border-gray-200']"
          >
            <i class="fas fa-globe mr-2"></i>
            Todos los Eventos
          </button>
          <button 
            @click="filtroActivo = 'proximos'"
            :class="['px-8 py-4 rounded-3xl font-bold transition-all duration-300 hover:transform hover:scale-105 shadow-lg',
                     filtroActivo === 'proximos' 
                     ? 'bg-gradient-to-r from-green-500 to-emerald-600 text-white shadow-xl' 
                     : 'bg-white/80 backdrop-blur-sm text-gray-700 hover:bg-white border border-gray-200']"
          >
            <i class="fas fa-calendar-plus mr-2"></i>
            Próximos Eventos
          </button>
          <button 
            @click="filtroActivo = 'pasados'"
            :class="['px-8 py-4 rounded-3xl font-bold transition-all duration-300 hover:transform hover:scale-105 shadow-lg',
                     filtroActivo === 'pasados' 
                     ? 'bg-gradient-to-r from-orange-500 to-red-600 text-white shadow-xl' 
                     : 'bg-white/80 backdrop-blur-sm text-gray-700 hover:bg-white border border-gray-200']"
          >
            <i class="fas fa-history mr-2"></i>
            Eventos Pasados
          </button>
        </div>
      </div>
    </div>

    <!-- Grid de eventos moderno -->
    <div class="pb-20 relative">
      <div class="absolute inset-0 bg-gradient-to-b from-transparent to-gray-100"></div>
      <div class="relative container mx-auto px-4">
        <div v-if="eventosFiltrados.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div 
            v-for="(evento, index) in eventosFiltrados" 
            :key="evento.id"
            class="card-modern overflow-hidden hover-lift animate-fade-in-up group"
            :style="`animation-delay: ${index * 0.1}s`"
          >
            <div class="relative overflow-hidden">
              <img 
                :src="evento.imagen" 
                :alt="evento.titulo"
                class="w-full h-56 object-cover group-hover:scale-110 transition-transform duration-500"
              >
              <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
              
              <!-- Badge de estado -->
              <div class="absolute top-4 right-4">
                <span 
                  :class="['px-4 py-2 rounded-2xl text-sm font-bold shadow-lg',
                           evento.esFuturo 
                           ? 'bg-gradient-to-r from-green-400 to-emerald-500 text-white' 
                           : 'bg-gradient-to-r from-gray-400 to-gray-600 text-white']"
                >
                  {{ evento.esFuturo ? 'Próximo' : 'Finalizado' }}
                </span>
              </div>

              <!-- Fecha destacada -->
              <div class="absolute bottom-4 left-4">
                <div class="bg-white/90 backdrop-blur-sm px-4 py-2 rounded-2xl">
                  <div class="text-center">
                    <div class="text-2xl font-black text-indigo-600">
                      {{ new Date(evento.fecha).getDate() }}
                    </div>
                    <div class="text-xs font-semibold text-gray-600 uppercase">
                      {{ new Date(evento.fecha).toLocaleDateString('es-ES', { month: 'short' }) }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="p-8">
              <h3 class="text-2xl font-bold text-gray-800 mb-4 group-hover:bg-gradient-to-r group-hover:from-indigo-600 group-hover:to-purple-600 group-hover:bg-clip-text group-hover:text-transparent transition-all duration-300">
                {{ evento.titulo }}
              </h3>
              <p class="text-gray-600 mb-6 line-clamp-3 leading-relaxed">{{ evento.descripcion }}</p>
              
              <div class="space-y-3 mb-6">
                <div class="flex items-center text-gray-700">
                  <div class="w-10 h-10 bg-gradient-to-r from-blue-400 to-indigo-500 rounded-2xl flex items-center justify-center mr-3">
                    <i class="fas fa-calendar text-white text-sm"></i>
                  </div>
                  <span class="font-medium">{{ formatearFecha(evento.fecha) }}</span>
                </div>
                <div class="flex items-center text-gray-700">
                  <div class="w-10 h-10 bg-gradient-to-r from-green-400 to-emerald-500 rounded-2xl flex items-center justify-center mr-3">
                    <i class="fas fa-clock text-white text-sm"></i>
                  </div>
                  <span class="font-medium">{{ evento.hora }}</span>
                </div>
                <div class="flex items-center text-gray-700">
                  <div class="w-10 h-10 bg-gradient-to-r from-red-400 to-pink-500 rounded-2xl flex items-center justify-center mr-3">
                    <i class="fas fa-map-marker-alt text-white text-sm"></i>
                  </div>
                  <span class="font-medium">{{ evento.ubicacion }}</span>
                </div>
                <div v-if="evento.cupos" class="flex items-center text-gray-700">
                  <div class="w-10 h-10 bg-gradient-to-r from-purple-400 to-pink-500 rounded-2xl flex items-center justify-center mr-3">
                    <i class="fas fa-users text-white text-sm"></i>
                  </div>
                  <div class="flex-1">
                    <span class="font-medium">{{ evento.inscritos }}/{{ evento.cupos }} participantes</span>
                    <div class="w-full bg-gray-200 rounded-full h-2 mt-1">
                      <div 
                        class="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full transition-all duration-500"
                        :style="{ width: `${Math.min((evento.inscritos / evento.cupos) * 100, 100)}%` }"
                      ></div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="flex gap-3">
                <button 
                  v-if="evento.esFuturo"
                  @click="inscribirse(evento)"
                  class="flex-1 bg-gradient-to-r from-green-500 to-emerald-600 text-white py-3 px-6 rounded-2xl hover:shadow-xl hover:transform hover:scale-105 transition-all duration-300 font-bold"
                >
                  <i class="fas fa-user-plus mr-2"></i>Inscribirse
                </button>
                <button 
                  v-else-if="evento.esFuturo && evento.cupos && evento.inscritos >= evento.cupos"
                  disabled
                  class="flex-1 bg-gray-400 text-white py-3 px-6 rounded-2xl cursor-not-allowed font-bold opacity-60"
                >
                  <i class="fas fa-times mr-2"></i>Cupos Llenos
                </button>
                <button 
                  @click="verDetalles(evento)"
                  class="px-6 py-3 border-2 border-indigo-500 text-indigo-600 rounded-2xl hover:bg-indigo-500 hover:text-white transition-all duration-300 font-bold hover:transform hover:scale-105"
                >
                  <i class="fas fa-eye mr-2"></i>Ver Más
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Mensaje si no hay eventos -->
        <div v-else class="text-center py-24 animate-fade-in-up">
          <div class="w-32 h-32 bg-gradient-to-br from-gray-300 to-gray-400 rounded-3xl flex items-center justify-center mx-auto mb-8">
            <i class="fas fa-calendar-times text-5xl text-white"></i>
          </div>
          <h3 class="text-3xl font-bold text-gray-600 mb-4">No hay eventos disponibles</h3>
          <p class="text-gray-500 text-lg max-w-md mx-auto">No se encontraron eventos para el filtro seleccionado. ¡Pronto tendremos nuevas actividades!</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useEventosStore } from '../stores/eventos'
import { useRouter } from 'vue-router'

const eventosStore = useEventosStore()
const router = useRouter()
const filtroActivo = ref('todos')

const eventosFiltrados = computed(() => {
  const eventos = eventosStore.eventos
  const ahora = new Date()
  
  switch (filtroActivo.value) {
    case 'proximos':
      return eventos.filter(evento => new Date(evento.fecha) >= ahora)
    case 'pasados':
      return eventos.filter(evento => new Date(evento.fecha) < ahora)
    default:
      return eventos
  }
})

const formatearFecha = (fecha) => {
  return new Date(fecha).toLocaleDateString('es-ES', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const inscribirse = (evento) => {
  router.push(`/inscripcion/${evento.id}`)
}

const verDetalles = (evento) => {
  router.push(`/evento/${evento.id}`)
}

onMounted(() => {
  eventosStore.cargarEventos()
})
</script>
