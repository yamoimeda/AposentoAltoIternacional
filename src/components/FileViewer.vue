<template>
  <div class="flex items-center gap-2 flex-wrap">
    <!-- Badge con cantidad si hay más de 1 -->
    <button
      @click="abrirEn(0)"
      class="px-3 py-1.5 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors text-xs font-semibold flex items-center gap-1.5"
    >
      <i class="fas fa-image"></i>
      <span>Ver comprobante{{ files.length > 1 ? 's' : '' }}</span>
      <span v-if="files.length > 1" class="bg-blue-700 rounded-full px-1.5 py-0.5 text-[10px]">{{ files.length }}</span>
    </button>

    <!-- Lightbox modal -->
    <Teleport to="body">
      <Transition name="fade">
        <div
          v-if="mostrarModal"
          @click.self="cerrar"
          class="fixed inset-0 bg-black/85 z-[9999] flex items-center justify-center p-4"
        >
          <div class="relative w-full max-w-4xl max-h-[92vh] bg-white rounded-2xl shadow-2xl overflow-hidden flex flex-col">

            <!-- Header -->
            <div class="bg-gradient-to-r from-blue-600 to-indigo-600 px-5 py-3 flex items-center justify-between flex-shrink-0">
              <h3 class="text-white font-semibold text-sm flex items-center gap-2">
                <i class="fas fa-image"></i>
                Comprobante {{ files.length > 1 ? `${indiceActual + 1} de ${files.length}` : '' }}
              </h3>
              <div class="flex items-center gap-2">
                <a
                  :href="urlActual"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="px-3 py-1.5 bg-white/20 hover:bg-white/30 text-white rounded-lg text-xs font-medium flex items-center gap-1.5 transition-colors"
                >
                  <i class="fas fa-external-link-alt"></i> Abrir en pestaña
                </a>
                <button
                  @click="cerrar"
                  class="text-white hover:bg-white/20 rounded-lg p-1.5 transition-colors"
                >
                  <i class="fas fa-times text-lg"></i>
                </button>
              </div>
            </div>

            <!-- Imagen -->
            <div class="flex-1 overflow-auto flex items-center justify-center bg-gray-100 p-4 min-h-0">
              <div v-if="cargando" class="flex flex-col items-center gap-3 text-gray-400">
                <i class="fas fa-spinner fa-spin text-4xl"></i>
                <span class="text-sm">Cargando imagen...</span>
              </div>
              <img
                v-show="!cargando && !errorCarga"
                :src="urlActual"
                :key="urlActual"
                alt="Comprobante de pago"
                class="max-w-full max-h-[70vh] object-contain rounded-lg shadow-md"
                @load="cargando = false; errorCarga = false"
                @error="cargando = false; errorCarga = true"
              />
              <div v-if="errorCarga && !cargando" class="flex flex-col items-center gap-3 text-gray-500">
                <i class="fas fa-image-slash text-5xl text-gray-300"></i>
                <p class="text-sm font-medium">No se pudo cargar la imagen</p>
                <a :href="urlActual" target="_blank" class="text-blue-600 hover:underline text-xs">
                  Intentar abrir directamente →
                </a>
              </div>
            </div>

            <!-- Navegación (solo si hay más de 1) -->
            <div v-if="files.length > 1" class="flex items-center justify-between px-5 py-3 bg-gray-50 border-t border-gray-200 flex-shrink-0">
              <button
                @click="anterior"
                :disabled="indiceActual === 0"
                class="px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-2"
                :class="indiceActual === 0 ? 'text-gray-300 cursor-not-allowed' : 'text-gray-700 hover:bg-gray-200'"
              >
                <i class="fas fa-chevron-left"></i> Anterior
              </button>

              <!-- Miniaturas de puntos -->
              <div class="flex gap-1.5">
                <button
                  v-for="(_, i) in files"
                  :key="i"
                  @click="abrirEn(i)"
                  class="w-2.5 h-2.5 rounded-full transition-all"
                  :class="i === indiceActual ? 'bg-blue-600 scale-125' : 'bg-gray-300 hover:bg-gray-400'"
                />
              </div>

              <button
                @click="siguiente"
                :disabled="indiceActual === files.length - 1"
                class="px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-2"
                :class="indiceActual === files.length - 1 ? 'text-gray-300 cursor-not-allowed' : 'text-gray-700 hover:bg-gray-200'"
              >
                Siguiente <i class="fas fa-chevron-right"></i>
              </button>
            </div>

          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'

const props = defineProps({
  // Acepta un array de URLs (strings)
  files: {
    type: Array,
    default: () => []
  }
})

const mostrarModal = ref(false)
const indiceActual = ref(0)
const cargando     = ref(false)
const errorCarga   = ref(false)

const urlActual = computed(() => props.files[indiceActual.value] || '')

const abrirEn = (idx) => {
  indiceActual.value = idx
  cargando.value = true
  errorCarga.value = false
  mostrarModal.value = true
}

const cerrar = () => { mostrarModal.value = false }

const anterior = () => {
  if (indiceActual.value > 0) {
    cargando.value = true
    errorCarga.value = false
    indiceActual.value--
  }
}

const siguiente = () => {
  if (indiceActual.value < props.files.length - 1) {
    cargando.value = true
    errorCarga.value = false
    indiceActual.value++
  }
}

const handleKey = (e) => {
  if (!mostrarModal.value) return
  if (e.key === 'Escape')      cerrar()
  if (e.key === 'ArrowRight')  siguiente()
  if (e.key === 'ArrowLeft')   anterior()
}

window.addEventListener('keydown', handleKey)
onUnmounted(() => window.removeEventListener('keydown', handleKey))
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
