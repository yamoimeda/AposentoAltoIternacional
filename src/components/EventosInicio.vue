<template>
  <section class="py-20 bg-gray-50">
    <div class="container mx-auto px-4">
      <!-- Título de la sección -->
      <div class="text-center mb-16">
        <h2 class="text-4xl md:text-5xl font-bold text-gray-800 mb-4">
          Próximos Eventos
        </h2>
        <div class="w-24 h-1 bg-gradient-to-r from-blue-600 to-purple-600 mx-auto rounded-full"></div>
      </div>

      <!-- Carrusel de eventos -->
      <div v-if="proximosEventos.length > 0" class="relative max-w-7xl mx-auto">
        <!-- Botones de navegación -->
        <button 
          @click="anteriorSlide"
          :disabled="currentSlide === 0"
          class="absolute left-0 top-1/2 -translate-y-1/2 z-10 bg-white/90 hover:bg-white shadow-lg/40  rounded-full w-12 h-12 flex items-center justify-center transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <i class="fas fa-chevron-left text-gray-600"></i>
        </button>
        
        <button 
          @click="siguienteSlide"
          :disabled="currentSlide >= maxSlides - 1"
          class="absolute right-0 top-1/2 -translate-y-1/2 z-10 bg-white/90 hover:bg-white shadow-lg/40 rounded-full w-12 h-12 flex items-center justify-center transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <i class="fas fa-chevron-right text-gray-600"></i>
        </button>

        <!-- Contenedor del carrusel -->
        <div class="overflow-hidden mx-12 ">
          <div 
            class="flex transition-transform duration-500 ease-in-out"
            :style="{ transform: `translateX(-${currentSlide * slideWidth}%)` }"
          >
            <div 
              v-for="(evento, index) in proximosEventos" 
              :key="evento.id"
              class="flex-shrink-0 px-4"
              :class="slideItemClass"
              @click="verEvento(evento)"
            >
              <div class="overflow-hidden pt-2">
                <!-- Imagen del evento -->
                <div class="relative rounded-2xl shadow-lg/40 overflow-hidden h-84 transition-all duration-300 cursor-pointer group hover:-translate-y-1">
                  <!-- Imagen del evento o fondo de color si no hay imagen -->
                  <div v-if="evento.bannerUrl || evento.imagen" class="w-full h-full">
                    <img 
                      :src="evento.bannerUrl || evento.imagen" 
                      :alt="evento.titulo"
                      class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                    >
                  </div>
                  <div v-else class="w-full h-full bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center">
                    <i class="fas fa-calendar-alt text-white text-6xl opacity-30"></i>
                  </div>
                  <!-- Overlay gradient -->
                  <div class="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent"></div>
                  
                  <!-- Badge de fecha -->
                  <div class="absolute top-4 left-4">
                    <div class="bg-white/90 backdrop-blur-sm px-3 py-2 rounded-lg text-gray-800 font-semibold text-sm">
                      {{ formatearFecha(evento.fecha) }}
                    </div>
                  </div>
                </div>

                <!-- Contenido del evento -->
                <div class="p-6">
                  <h3 class="text-xl font-bold text-gray-800 mb-3 group-hover:text-blue-600 transition-colors text-center">
                    {{ evento.titulo }}
                  </h3>
                  
                  

                  <!-- Botón de acción -->
                  <div class="flex items-center justify-between justify-center">
                    <!-- <div class="flex items-center">
                      <div class="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"></div>
                      <span class="text-sm font-medium text-green-600">Disponible</span>
                    </div> -->
                    <!-- <button 
                      @click="verEvento(evento)"
                      class="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:from-blue-700 hover:to-purple-700 transition-all flex items-center"
                    >
                      Ver detalles
                      <i class="fas fa-arrow-right ml-2"></i>
                    </button> -->
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Indicadores de posición -->
        <div class="flex justify-center space-x-2 mt-8">
          <button
            v-for="slide in maxSlides"
            :key="slide"
            @click="currentSlide = slide - 1"
            :class="[
              'w-3 h-3 rounded-full transition-all',
              currentSlide === slide - 1 
                ? 'bg-gradient-to-r from-blue-600 to-purple-600' 
                : 'bg-gray-300 hover:bg-gray-400'
            ]"
          ></button>
        </div>
      </div>

      <!-- Mensaje cuando no hay eventos -->
      <div v-else class="text-center py-16">
        <div class="mb-6">
          <i class="fas fa-calendar-times text-6xl text-gray-300"></i>
        </div>
        <h3 class="text-2xl font-bold text-gray-600 mb-4">No hay eventos próximos</h3>
        <p class="text-gray-500 mb-8">Mantente atento a nuestras redes sociales para próximos anuncios</p>
        <!-- <router-link 
          to="/contacto"
          class="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-3 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all"
        >
          Mantenerme informado
        </router-link> -->
      </div>

      <!-- Botón para ver todos los eventos -->
      <div v-if="proximosEventos.length > 0" class="text-center mt-12">
        <router-link 
          to="/eventos" 
          class="inline-flex items-center bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-3 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all hover:shadow-lg"
        >
          Ver todos los eventos
          <i class="fas fa-arrow-right ml-2"></i>
        </router-link>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, computed, ref, onUnmounted } from 'vue'
import { useEventosStore } from '../stores/eventos'
import { useRouter } from 'vue-router'

const eventosStore = useEventosStore()
const router = useRouter()
const currentSlide = ref(0)

const proximosEventos = computed(() => {
  const ahora = new Date()
  return eventosStore.eventos
    .filter(evento => new Date(evento.fecha) >= ahora)
    .sort((a, b) => new Date(a.fecha) - new Date(b.fecha))
})

// Configuración responsive del carrusel
const itemsPerSlide = ref(3)
const slideWidth = computed(() => 100 / itemsPerSlide.value)
const slideItemClass = computed(() => {
  return itemsPerSlide.value === 1 ? 'w-full' :
         itemsPerSlide.value === 2 ? 'w-1/2' : 'w-1/3'
})

const maxSlides = computed(() => {
  return Math.ceil(proximosEventos.value.length / itemsPerSlide.value)
})

const siguienteSlide = () => {
  if (currentSlide.value < maxSlides.value - 1) {
    currentSlide.value++
  }
}

const anteriorSlide = () => {
  if (currentSlide.value > 0) {
    currentSlide.value--
  }
}

// Auto-play del carrusel
let autoPlayInterval = null

const iniciarAutoPlay = () => {
  autoPlayInterval = setInterval(() => {
    if (currentSlide.value < maxSlides.value - 1) {
      currentSlide.value++
    } else {
      currentSlide.value = 0
    }
  }, 5000) // Cambia cada 5 segundos
}

const detenerAutoPlay = () => {
  if (autoPlayInterval) {
    clearInterval(autoPlayInterval)
    autoPlayInterval = null
  }
}

// Responsive breakpoints
const actualizarItemsPorSlide = () => {
  const width = window.innerWidth
  if (width < 768) {
    itemsPerSlide.value = 1 // Mobile: 1 evento
  } else if (width < 1024) {
    itemsPerSlide.value = 2 // Tablet: 2 eventos
  } else {
    itemsPerSlide.value = 3 // Desktop: 3 eventos
  }
  
  // Ajustar slide actual si es necesario
  if (currentSlide.value >= maxSlides.value) {
    currentSlide.value = Math.max(0, maxSlides.value - 1)
  }
}

const formatearFecha = (fecha) => {
  return new Date(fecha).toLocaleDateString('es-ES', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  }).toUpperCase()
}

const formatearFechaCompleta = (fecha) => {
  return new Date(fecha).toLocaleDateString('es-ES', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const verEvento = (evento) => {
  router.push(`/inscripcion/${evento.id}`)
}

onMounted(() => {
  eventosStore.cargarEventos()
  actualizarItemsPorSlide()
//   iniciarAutoPlay()
  
  window.addEventListener('resize', actualizarItemsPorSlide)
})

onUnmounted(() => {
  detenerAutoPlay()
  window.removeEventListener('resize', actualizarItemsPorSlide)
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>