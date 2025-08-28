<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="container mx-auto px-4 pt-8">
      <!-- Breadcrumb -->
      <nav class="mb-8">
        <ol class="flex items-center space-x-2 text-sm text-gray-500">
          <li><router-link to="/eventos" class="hover:text-blue-600">Eventos</router-link></li>
          <li><i class="fas fa-chevron-right mx-2"></i></li>
          <li class="text-gray-700">{{ evento?.titulo }}</li>
        </ol>
      </nav>

      <div v-if="evento" class="max-w-4xl mx-auto">
        <!-- Imagen y título principal -->
        <div class="bg-white rounded-lg shadow-lg overflow-hidden mb-8">
          <div class="relative">
            <img 
              :src="evento.imagen" 
              :alt="evento.titulo"
              class="w-full h-80 object-cover"
            >
            <div class="absolute top-6 right-6">
              <span 
                :class="['px-4 py-2 rounded-full text-sm font-semibold', 
                         evento.esFuturo ? 'bg-green-500 text-white' : 'bg-gray-500 text-white']"
              >
                {{ evento.esFuturo ? 'Próximo Evento' : 'Evento Finalizado' }}
              </span>
            </div>
          </div>
          
          <div class="p-8">
            <h1 class="text-4xl font-bold text-gray-800 mb-6">{{ evento.titulo }}</h1>
            
            <!-- Información clave -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              <div class="bg-blue-50 p-4 rounded-lg">
                <div class="flex items-center text-blue-800 mb-2">
                  <i class="fas fa-calendar-alt mr-3 text-xl"></i>
                  <span class="font-semibold">Fecha y Hora</span>
                </div>
                <p class="text-blue-700">{{ formatearFecha(evento.fecha) }}</p>
                <p class="text-blue-700">{{ evento.hora }}</p>
              </div>
              
              <div class="bg-purple-50 p-4 rounded-lg">
                <div class="flex items-center text-purple-800 mb-2">
                  <i class="fas fa-map-marker-alt mr-3 text-xl"></i>
                  <span class="font-semibold">Ubicación</span>
                </div>
                <p class="text-purple-700">{{ evento.ubicacion }}</p>
              </div>
              
              <div v-if="evento.cupos" class="bg-green-50 p-4 rounded-lg">
                <div class="flex items-center text-green-800 mb-2">
                  <i class="fas fa-users mr-3 text-xl"></i>
                  <span class="font-semibold">Participantes</span>
                </div>
                <p class="text-green-700">{{ evento.inscritos }} de {{ evento.cupos }} inscritos</p>
                <div class="w-full bg-green-200 rounded-full h-2 mt-2">
                  <div 
                    class="bg-green-600 h-2 rounded-full transition-all"
                    :style="{ width: `${(evento.inscritos / evento.cupos) * 100}%` }"
                  ></div>
                </div>
              </div>
              
              <div class="bg-orange-50 p-4 rounded-lg">
                <div class="flex items-center text-orange-800 mb-2">
                  <i class="fas fa-tag mr-3 text-xl"></i>
                  <span class="font-semibold">Categoría</span>
                </div>
                <p class="text-orange-700 capitalize">{{ evento.categoria }}</p>
              </div>
            </div>

            <!-- Descripción -->
            <div class="mb-8">
              <h2 class="text-2xl font-bold text-gray-800 mb-4">Descripción del Evento</h2>
              <p class="text-gray-600 text-lg leading-relaxed">{{ evento.descripcion }}</p>
            </div>

            <!-- Detalles adicionales -->
            <div class="bg-gray-50 p-6 rounded-lg mb-8">
              <h3 class="text-xl font-semibold text-gray-800 mb-4">
                <i class="fas fa-info-circle mr-2 text-blue-600"></i>
                Información Importante
              </h3>
              <ul class="space-y-2 text-gray-700">
                <li class="flex items-start">
                  <i class="fas fa-check text-green-500 mr-2 mt-1"></i>
                  <span>La participación en este evento es completamente gratuita</span>
                </li>
                <li class="flex items-start">
                  <i class="fas fa-check text-green-500 mr-2 mt-1"></i>
                  <span>Se recomienda llegar 15 minutos antes del inicio</span>
                </li>
                <li class="flex items-start">
                  <i class="fas fa-check text-green-500 mr-2 mt-1"></i>
                  <span>Recibirás un correo de confirmación después de inscribirte</span>
                </li>
                <li v-if="evento.categoria === 'retiro'" class="flex items-start">
                  <i class="fas fa-check text-green-500 mr-2 mt-1"></i>
                  <span>Se incluye alimentación y materiales</span>
                </li>
                <li v-if="evento.categoria === 'educacion'" class="flex items-start">
                  <i class="fas fa-check text-green-500 mr-2 mt-1"></i>
                  <span>Los niños deben ser acompañados por un adulto responsable</span>
                </li>
              </ul>
            </div>

            <!-- Botones de acción -->
            <div class="flex flex-col sm:flex-row gap-4">
              <button 
                v-if="evento.esFuturo && evento.cupos && evento.inscritos < evento.cupos"
                @click="inscribirse"
                class="flex-1 bg-blue-600 text-white py-4 px-6 rounded-lg hover:bg-blue-700 transition-colors font-semibold text-lg"
              >
                <i class="fas fa-user-plus mr-2"></i>Inscribirse Ahora
              </button>
              <button 
                v-else-if="evento.esFuturo && evento.cupos && evento.inscritos >= evento.cupos"
                disabled
                class="flex-1 bg-gray-400 text-white py-4 px-6 rounded-lg cursor-not-allowed font-semibold text-lg"
              >
                <i class="fas fa-times mr-2"></i>Cupos Agotados
              </button>
              <button 
                @click="compartir"
                class="px-6 py-4 border-2 border-blue-600 text-blue-600 rounded-lg hover:bg-blue-50 transition-colors font-semibold"
              >
                <i class="fas fa-share-alt mr-2"></i>Compartir
              </button>
              <button 
                @click="$router.go(-1)"
                class="px-6 py-4 border-2 border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-semibold"
              >
                <i class="fas fa-arrow-left mr-2"></i>Volver
              </button>
            </div>
          </div>
        </div>

        <!-- Eventos relacionados -->
        <div v-if="eventosRelacionados.length > 0" class="bg-white rounded-lg shadow-lg p-6">
          <h2 class="text-2xl font-bold text-gray-800 mb-6">
            <i class="fas fa-calendar mr-2 text-blue-600"></i>
            Otros Eventos que te Pueden Interesar
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div 
              v-for="eventoRel in eventosRelacionados" 
              :key="eventoRel.id"
              class="border rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
              @click="$router.push(`/evento/${eventoRel.id}`)"
            >
              <img 
                :src="eventoRel.imagen" 
                :alt="eventoRel.titulo"
                class="w-full h-32 object-cover rounded mb-3"
              >
              <h3 class="font-semibold text-gray-800 mb-2">{{ eventoRel.titulo }}</h3>
              <p class="text-sm text-gray-600 mb-2">{{ formatearFecha(eventoRel.fecha) }}</p>
              <p class="text-xs text-gray-500">{{ eventoRel.ubicacion }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading state -->
      <div v-else class="flex justify-center items-center py-16">
        <i class="fas fa-spinner fa-spin text-4xl text-blue-600"></i>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useEventosStore } from '../stores/eventos'

const route = useRoute()
const router = useRouter()
const eventosStore = useEventosStore()

const evento = computed(() => {
  return eventosStore.obtenerEventoPorId(route.params.id)
})

const eventosRelacionados = computed(() => {
  if (!evento.value) return []
  
  return eventosStore.eventos
    .filter(e => e.id !== evento.value.id && e.esFuturo && e.categoria === evento.value.categoria)
    .slice(0, 2)
})

const formatearFecha = (fecha) => {
  return new Date(fecha).toLocaleDateString('es-ES', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const inscribirse = () => {
  router.push(`/inscripcion/${evento.value.id}`)
}

const compartir = async () => {
  if (navigator.share) {
    try {
      await navigator.share({
        title: evento.value.titulo,
        text: evento.value.descripcion,
        url: window.location.href
      })
    } catch (err) {
      console.log('Error al compartir:', err)
    }
  } else {
    // Fallback para navegadores que no soportan Web Share API
    const url = window.location.href
    navigator.clipboard.writeText(url).then(() => {
      alert('¡Enlace copiado al portapapeles!')
    })
  }
}

onMounted(() => { 
  console.log(evento.value);

  eventosStore.cargarEventos()
})
</script>
