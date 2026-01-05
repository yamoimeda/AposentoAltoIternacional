<template>
  <div>
    <!-- Botón para abrir el archivo -->
    <button
      @click="abrirVisor"
      class="px-3 py-1.5 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors text-sm flex items-center gap-2"
      :disabled="!fileUrl"
    >
      <i :class="iconoTipoArchivo"></i>
      <span>{{ textoBoton }}</span>
    </button>

    <!-- Modal Lightbox -->
    <Teleport to="body">
      <Transition name="fade">
        <div
          v-if="mostrarModal"
          @click.self="cerrarVisor"
          class="fixed inset-0 bg-black bg-opacity-80 z-50 flex items-center justify-center p-4"
        >
          <div class="relative max-w-6xl w-full max-h-[90vh] bg-white rounded-xl shadow-2xl overflow-hidden">
            <!-- Header del modal -->
            <div class="bg-gradient-to-r from-blue-600 to-indigo-600 p-4 flex justify-between items-center">
              <h3 class="text-white font-semibold flex items-center gap-2">
                <i :class="iconoTipoArchivo"></i>
                {{ tituloModal }}
              </h3>
              <div class="flex gap-2">
                <!-- Botón descargar -->
                <a
                  :href="fileUrl"
                  download
                  target="_blank"
                  class="px-3 py-1.5 bg-white text-blue-600 rounded-lg hover:bg-blue-50 transition-colors text-sm font-medium flex items-center gap-2"
                >
                  <i class="fas fa-download"></i>
                  Descargar
                </a>
                <!-- Botón cerrar -->
                <button
                  @click="cerrarVisor"
                  class="text-white hover:bg-white hover:bg-opacity-20 rounded-lg px-3 py-1.5 transition-colors"
                >
                  <i class="fas fa-times text-xl"></i>
                </button>
              </div>
            </div>

            <!-- Contenido del modal -->
            <div class="p-6 overflow-auto max-h-[calc(90vh-80px)]">
              <!-- Imagen -->
              <div v-if="esImagen" class="flex justify-center">
                <img
                  :src="fileUrl"
                  :alt="titulo"
                  class="max-w-full h-auto rounded-lg shadow-lg"
                  @load="imagenCargada = true"
                />
                <div v-if="!imagenCargada" class="flex items-center justify-center h-64">
                  <i class="fas fa-spinner fa-spin text-4xl text-gray-400"></i>
                </div>
              </div>

              <!-- PDF -->
              <div v-else-if="esPDF" class="w-full h-[70vh]">
                <iframe
                  :src="fileUrl"
                  class="w-full h-full border-0 rounded-lg"
                  @load="pdfCargado = true"
                />
                <div v-if="!pdfCargado" class="flex items-center justify-center h-64">
                  <i class="fas fa-spinner fa-spin text-4xl text-gray-400"></i>
                </div>
              </div>

              <!-- Tipo no soportado -->
              <div v-else class="text-center py-12">
                <i class="fas fa-file text-6xl text-gray-300 mb-4"></i>
                <p class="text-gray-600 mb-4">Vista previa no disponible para este tipo de archivo</p>
                <a
                  :href="fileUrl"
                  download
                  target="_blank"
                  class="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  <i class="fas fa-download"></i>
                  Descargar archivo
                </a>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  fileUrl: {
    type: String,
    default: ''
  },
  titulo: {
    type: String,
    default: 'Archivo'
  }
})

const mostrarModal = ref(false)
const imagenCargada = ref(false)
const pdfCargado = ref(false)

// Detectar tipo de archivo por extensión o MIME type
const tipoArchivo = computed(() => {
  if (!props.fileUrl) return 'unknown'
  
  const url = props.fileUrl.toLowerCase()
  
  if (url.match(/\.(jpg|jpeg|png|gif|webp|bmp|svg)(\?|$)/i)) return 'image'
  if (url.match(/\.pdf(\?|$)/i)) return 'pdf'
  if (url.match(/\.(doc|docx)(\?|$)/i)) return 'word'
  if (url.match(/\.(xls|xlsx)(\?|$)/i)) return 'excel'
  
  return 'unknown'
})

const esImagen = computed(() => tipoArchivo.value === 'image')
const esPDF = computed(() => tipoArchivo.value === 'pdf')

const iconoTipoArchivo = computed(() => {
  switch (tipoArchivo.value) {
    case 'image': return 'fas fa-image'
    case 'pdf': return 'fas fa-file-pdf'
    case 'word': return 'fas fa-file-word'
    case 'excel': return 'fas fa-file-excel'
    default: return 'fas fa-file'
  }
})

const textoBoton = computed(() => {
  switch (tipoArchivo.value) {
    case 'image': return 'Ver Imagen'
    case 'pdf': return 'Ver PDF'
    default: return 'Ver Archivo'
  }
})

const tituloModal = computed(() => {
  return props.titulo || 'Vista de archivo'
})

const abrirVisor = () => {
  mostrarModal.value = true
  imagenCargada.value = false
  pdfCargado.value = false
}

const cerrarVisor = () => {
  mostrarModal.value = false
}

// Cerrar con tecla Escape
const handleKeydown = (e) => {
  if (e.key === 'Escape' && mostrarModal.value) {
    cerrarVisor()
  }
}

// Agregar listener de teclado
if (typeof window !== 'undefined') {
  window.addEventListener('keydown', handleKeydown)
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
