<template>
  <section class="py-20 bg-white">
    <div class="container mx-auto px-4">
      <!-- Título principal -->
      <div class="text-center mb-16">
        <h2 class="text-5xl md:text-6xl font-black text-gray-800 mb-6">
          DESCUBRE
        </h2>
        <div class="w-32 h-1 bg-gradient-to-r from-blue-600 to-purple-600 mx-auto rounded-full"></div>
      </div>

      <!-- Pestañas de categorías -->
      <div class="flex justify-center mb-12 overflow-x-auto">
        <div class="flex space-x-1 bg-gray-100 p-1 rounded-xl min-w-max">
          <button
            v-for="categoria in categorias"
            :key="categoria.id"
            @click="cambiarCategoria(categoria.id)"
            :class="[
              'px-6 py-3 rounded-lg font-semibold transition-all duration-300 whitespace-nowrap',
              categoriaActiva === categoria.id
                ? 'bg-white text-gray-800 shadow-md'
                : 'text-gray-600 hover:text-gray-800 hover:bg-white/50'
            ]"
          >
            {{ categoria.nombre }}
          </button>
        </div>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="flex justify-center items-center py-20">
        <div class="text-center">
          <div class="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p class="text-gray-600">Cargando videos...</p>
        </div>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="text-center py-20">
        <div class="mb-6">
          <i class="fas fa-exclamation-triangle text-6xl text-red-400"></i>
        </div>
        <h3 class="text-2xl font-bold text-gray-600 mb-4">Error al cargar videos</h3>
        <p class="text-gray-500 mb-8">{{ error }}</p>
        <button 
          @click="cargarVideos"
          class="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-3 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all"
        >
          Intentar de nuevo
        </button>
      </div>

      <!-- Carrusel de videos -->
      <div v-else-if="videosActuales.length > 0" class="relative max-w-7xl mx-auto">
        <!-- Botones de navegación -->
        <button 
          @click="anteriorSlide"
          :disabled="currentSlide === 0"
          class="absolute left-0 top-1/2 -translate-y-1/2 z-10 bg-white/90 hover:bg-white shadow-lg rounded-full w-12 h-12 flex items-center justify-center transition-all disabled:opacity-30 disabled:cursor-not-allowed"
        >
          <i class="fas fa-chevron-left text-gray-600"></i>
        </button>
        
        <button 
          @click="siguienteSlide"
          :disabled="currentSlide >= maxSlides - 1"
          class="absolute right-0 top-1/2 -translate-y-1/2 z-10 bg-white/90 hover:bg-white shadow-lg rounded-full w-12 h-12 flex items-center justify-center transition-all disabled:opacity-30 disabled:cursor-not-allowed"
        >
          <i class="fas fa-chevron-right text-gray-600"></i>
        </button>

        <!-- Contenedor del carrusel -->
        <div class="overflow-hidden mx-12">
          <div 
            class="flex transition-transform duration-500 ease-in-out"
            :style="{ transform: `translateX(-${currentSlide * slideWidth}%)` }"
          >
            <div 
              v-for="video in videosActuales" 
              :key="video.id"
              class="flex-shrink-0 px-3"
              :class="slideItemClass"
            >
              <div class="group cursor-pointer" @click="abrirVideo(video)">
                <!-- Thumbnail del video -->
                <div class="relative overflow-hidden rounded-2xl shadow-lg mb-4 aspect-video">
                  <img 
                    :src="video.thumbnail" 
                    :alt="video.titulo"
                    class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                    @error="onImageError"
                  >
                  
                  <!-- Overlay con play button -->
                  <div class="absolute inset-0 bg-black/30 group-hover:bg-black/40 transition-colors flex items-center justify-center">
                    <div class="w-16 h-16 bg-red-600 rounded-full flex items-center justify-center transform group-hover:scale-110 transition-transform">
                      <i class="fas fa-play text-white text-xl ml-1"></i>
                    </div>
                  </div>

                  <!-- Duración del video -->
                  <div v-if="video.duracion" class="absolute bottom-4 right-4 bg-black/70 text-white px-2 py-1 rounded text-sm font-semibold">
                    {{ video.duracion }}
                  </div>

                  <!-- Badge de categoría -->
                  <div class="absolute top-4 left-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white px-3 py-1 rounded-lg text-xs font-semibold">
                    {{ obtenerCategoriaNombre(video.categoria) }}
                  </div>
                </div>

                <!-- Información del video -->
                <div class="space-y-2">
                  <h3 class="font-bold text-gray-800 line-clamp-2 group-hover:text-blue-600 transition-colors">
                    {{ video.titulo }}
                  </h3>
                  
                  <div class="flex items-center text-sm text-gray-500 space-x-4">
                    <span v-if="video.vistas" class="flex items-center">
                      <i class="fas fa-eye mr-1"></i>
                      {{ formatearVistas(video.vistas) }}
                    </span>
                    <span class="flex items-center">
                      <i class="fas fa-calendar mr-1"></i>
                      {{ formatearFecha(video.fechaPublicacion) }}
                    </span>
                  </div>

                  <p class="text-gray-600 text-sm line-clamp-2">
                    {{ video.descripcion }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Indicadores -->
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

      <!-- No hay videos -->
      <div v-else class="text-center py-20">
        <div class="mb-6">
          <i class="fas fa-video text-6xl text-gray-300"></i>
        </div>
        <h3 class="text-2xl font-bold text-gray-600 mb-4">No hay videos disponibles</h3>
        <p class="text-gray-500">Selecciona otra categoría o intenta más tarde</p>
      </div>

      <!-- Botón para ver más videos -->
      <div v-if="videosActuales.length > 0" class="text-center mt-12">
        <a 
          :href="canalYoutube" 
          target="_blank"
          class="inline-flex items-center bg-red-600 hover:bg-red-700 text-white px-8 py-4 rounded-xl font-semibold transition-all hover:shadow-lg transform hover:-translate-y-1"
        >
          <i class="fab fa-youtube mr-3 text-xl"></i>
          Ver más en YouTube
          <i class="fas fa-external-link-alt ml-2"></i>
        </a>
      </div>
    </div>

    <!-- Modal de video -->
    <div 
      v-if="videoModal.show" 
      class="fixed inset-0 bg-black/80 z-50 flex items-center justify-center p-4"
      @click="cerrarVideo"
    >
      <div class="relative max-w-4xl w-full" @click.stop>
        <button 
          @click="cerrarVideo"
          class="absolute -top-12 right-0 text-white hover:text-red-400 transition-colors"
        >
          <i class="fas fa-times text-2xl"></i>
        </button>
        
        <div class="relative aspect-video bg-black rounded-lg overflow-hidden">
          <iframe 
            v-if="videoModal.show"
            :src="videoModal.url" 
            class="w-full h-full"
            frameborder="0" 
            allowfullscreen
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          ></iframe>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'

// Configuración de YouTube API
const YOUTUBE_API_KEY = 'TU_API_KEY_AQUI' // Reemplaza con tu API key
const CHANNEL_ID = 'UC_x5XG1OV2P6uZZ5FSM9Ttw' // ID del canal (ejemplo)

// Estado reactivo
const categoriaActiva = ref('predicas')
const currentSlide = ref(0)
const itemsPerSlide = ref(3)
const loading = ref(false)
const error = ref(null)
const videos = ref([])

// Modal de video
const videoModal = ref({
  show: false,
  url: ''
})

// Configuración del canal
const canalYoutube = 'https://www.youtube.com/@aposentoaltointernacional'

// Categorías con palabras clave para filtrar
const categorias = [
  { 
    id: 'predicas', 
    nombre: 'Prédicas Semanales',
    palabrasClave: ['predica', 'sermon', 'predicacion', 'mensaje']
  },
  { 
    id: 'summer', 
    nombre: 'SSS Summer',
    palabrasClave: ['SSS', 'Summer', 'verano']
  },
  { 
    id: 'youth', 
    nombre: 'Youth',
    palabrasClave: ['youth', 'jovenes', 'joven']
  },
  { 
    id: 'sabiduria', 
    nombre: 'Semillas de Sabiduría',
    palabrasClave: ['sabiduria', 'semillas', 'enseñanza']
  },
  { 
    id: 'alabanza', 
    nombre: 'Alabanza y Adoración',
    palabrasClave: ['alabanza', 'adoracion', 'worship', 'musica']
  },
  { 
    id: 'cosecha', 
    nombre: 'Cosecha Mundial',
    palabrasClave: ['cosecha', 'mundial', 'evangelismo']
  }
]

// Computed properties
const videosActuales = computed(() => {
  if (categoriaActiva.value === 'predicas') {
    return videos.value // Mostrar todos si es "predicas"
  }
  
  const categoria = categorias.find(cat => cat.id === categoriaActiva.value)
  if (!categoria) return []
  
  return videos.value.filter(video => {
    const titulo = video.titulo.toLowerCase()
    const descripcion = video.descripcion.toLowerCase()
    
    return categoria.palabrasClave.some(palabra => 
      titulo.includes(palabra.toLowerCase()) || 
      descripcion.includes(palabra.toLowerCase())
    )
  })
})

const slideWidth = computed(() => 100 / itemsPerSlide.value)

const slideItemClass = computed(() => {
  return itemsPerSlide.value === 1 ? 'w-full' :
         itemsPerSlide.value === 2 ? 'w-1/2' : 'w-1/3'
})

const maxSlides = computed(() => {
  return Math.ceil(videosActuales.value.length / itemsPerSlide.value)
})

// Función para cargar videos de YouTube
const cargarVideos = async () => {
  loading.value = true
  error.value = null
  
  try {
    // Si no hay API key, usar datos de ejemplo
    if (!YOUTUBE_API_KEY || YOUTUBE_API_KEY === 'TU_API_KEY_AQUI') {
      console.warn('API Key de YouTube no configurada. Usando datos de ejemplo.')
      await cargarVideosEjemplo()
      return
    }

    const response = await fetch(
      `https://www.googleapis.com/youtube/v3/search?` +
      `key=${YOUTUBE_API_KEY}&` +
      `channelId=${CHANNEL_ID}&` +
      `part=snippet&` +
      `order=date&` +
      `maxResults=50&` +
      `type=video`
    )

    if (!response.ok) {
      throw new Error(`Error HTTP: ${response.status}`)
    }

    const data = await response.json()
    
    // Obtener detalles adicionales de los videos
    const videoIds = data.items.map(item => item.id.videoId).join(',')
    const detailsResponse = await fetch(
      `https://www.googleapis.com/youtube/v3/videos?` +
      `key=${YOUTUBE_API_KEY}&` +
      `id=${videoIds}&` +
      `part=statistics,contentDetails`
    )

    const detailsData = await detailsResponse.json()

    // Combinar datos
    videos.value = data.items.map((item, index) => {
      const details = detailsData.items[index]
      
      return {
        id: item.id.videoId,
        titulo: item.snippet.title,
        descripcion: item.snippet.description,
        thumbnail: item.snippet.thumbnails.maxres?.url || 
                  item.snippet.thumbnails.high?.url || 
                  item.snippet.thumbnails.medium.url,
        fechaPublicacion: item.snippet.publishedAt,
        categoria: 'predicas',
        youtubeId: item.id.videoId,
        vistas: details?.statistics?.viewCount ? parseInt(details.statistics.viewCount) : null,
        duracion: details?.contentDetails?.duration ? formatearDuracion(details.contentDetails.duration) : null
      }
    })

  } catch (err) {
    console.error('Error al cargar videos de YouTube:', err)
    error.value = 'No se pudieron cargar los videos. Verifica tu conexión a internet.'
    await cargarVideosEjemplo()
  } finally {
    loading.value = false
  }
}

// Función para cargar datos de ejemplo (fallback)
const cargarVideosEjemplo = async () => {
  // Simular delay de red
  await new Promise(resolve => setTimeout(resolve, 1000))
  
  videos.value = [
    {
      id: '1',
      titulo: 'Testigos de Cristo con Poder y Fuego | Guillermo Maldonado',
      descripcion: 'Una poderosa predicación sobre el testimonio cristiano y el poder del Espíritu Santo en nuestras vidas.',
      thumbnail: 'https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg',
      duracion: '35:02',
      vistas: 15420,
      fechaPublicacion: '2024-01-15T10:00:00Z',
      categoria: 'predicas',
      youtubeId: 'dQw4w9WgXcQ'
    },
    {
      id: '2',
      titulo: 'Por Qué el Honor Lo Cambia Todo | Guillermo Maldonado',
      descripcion: 'Una enseñanza profunda sobre la importancia del honor en la vida cristiana.',
      thumbnail: 'https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg',
      duracion: '01:17:54',
      vistas: 20150,
      fechaPublicacion: '2023-12-25T10:00:00Z',
      categoria: 'predicas',
      youtubeId: 'dQw4w9WgXcQ'
    },
    {
      id: '3',
      titulo: 'Youth Conference 2024 - Encuentro de Jóvenes',
      descripcion: 'Conferencia especial para jóvenes con mensaje de esperanza y propósito.',
      thumbnail: 'https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg',
      duracion: '45:30',
      vistas: 8500,
      fechaPublicacion: '2024-01-20T10:00:00Z',
      categoria: 'predicas',
      youtubeId: 'dQw4w9WgXcQ'
    },
    {
      id: '4',
      titulo: 'Semillas de Sabiduría - La Fe que Mueve Montañas',
      descripcion: 'Principios bíblicos para desarrollar una fe sólida y efectiva.',
      thumbnail: 'https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg',
      duracion: '28:15',
      vistas: 12300,
      fechaPublicacion: '2024-01-10T10:00:00Z',
      categoria: 'predicas',
      youtubeId: 'dQw4w9WgXcQ'
    }
  ]
}

// Función para convertir duración ISO 8601 a formato legible
const formatearDuracion = (duration) => {
  const match = duration.match(/PT(\d+H)?(\d+M)?(\d+S)?/)
  if (!match) return '00:00'
  
  const hours = parseInt(match[1]) || 0
  const minutes = parseInt(match[2]) || 0
  const seconds = parseInt(match[3]) || 0
  
  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
  }
  return `${minutes}:${seconds.toString().padStart(2, '0')}`
}

// Métodos del carrusel
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

const abrirVideo = (video) => {
  videoModal.value = {
    show: true,
    url: `https://www.youtube.com/embed/${video.youtubeId}?autoplay=1`
  }
}

const cerrarVideo = () => {
  videoModal.value = {
    show: false,
    url: ''
  }
}

const obtenerCategoriaNombre = (categoriaId) => {
  const categoria = categorias.find(cat => cat.id === categoriaId)
  return categoria ? categoria.nombre : 'General'
}

const formatearVistas = (vistas) => {
  if (!vistas) return '0'
  if (vistas >= 1000000) {
    return Math.floor(vistas / 1000000) + 'M'
  } else if (vistas >= 1000) {
    return Math.floor(vistas / 1000) + 'K'
  }
  return vistas.toString()
}

const formatearFecha = (fecha) => {
  return new Date(fecha).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const onImageError = (event) => {
  event.target.src = 'https://via.placeholder.com/640x360/667eea/ffffff?text=Video+No+Disponible'
}

// Responsive
const actualizarItemsPorSlide = () => {
  const width = window.innerWidth
  if (width < 768) {
    itemsPerSlide.value = 1
  } else if (width < 1024) {
    itemsPerSlide.value = 2
  } else {
    itemsPerSlide.value = 3
  }
  
  if (currentSlide.value >= maxSlides.value) {
    currentSlide.value = Math.max(0, maxSlides.value - 1)
  }
}

// Cambiar categoría
const cambiarCategoria = (nuevaCategoria) => {
  categoriaActiva.value = nuevaCategoria
  currentSlide.value = 0
}

// Watcher para recargar videos cuando cambie la categoría
watch(categoriaActiva, () => {
  currentSlide.value = 0
})

// Lifecycle
onMounted(() => {
  cargarVideos()
  actualizarItemsPorSlide()
  window.addEventListener('resize', actualizarItemsPorSlide)
  
  // Cerrar modal con ESC
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && videoModal.value.show) {
      cerrarVideo()
    }
  })
})

onUnmounted(() => {
  window.removeEventListener('resize', actualizarItemsPorSlide)
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.aspect-video {
  aspect-ratio: 16 / 9;
}
</style>