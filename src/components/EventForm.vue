<template>
  <div class="fixed inset-0 bg-black/50 bg-opacity-50 flex items-start sm:items-center justify-center z-50 py-12 px-4">
    <div class="bg-white rounded-3xl shadow-md p-6 w-full max-w-lg border border-gray-200 max-h-[80vh] overflow-y-auto">
      <div class="flex justify-between items-center mb-6">
        <h3 class="text-2xl font-bold text-gray-800">
          {{ isEditing ? 'Editar Evento' : 'Crear Nuevo Evento' }}
        </h3>
        <button @click="$emit('close')" class="text-gray-500 hover:text-red-500 text-2xl">
          <i class="fas fa-times"></i>
        </button>
      </div>

      <form @submit.prevent="submitForm">
        <div class="space-y-4 mb-6">
          <input v-model="localEvent.titulo" placeholder="Título del evento" class="w-full px-4 py-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-200 text-gray-800 placeholder-gray-400" required />
          <input v-model="localEvent.fecha" type="date" class="w-full px-4 py-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-200 text-gray-800" required />
          <input v-model="localEvent.lugar" placeholder="Lugar del evento" class="w-full px-4 py-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-200 text-gray-800 placeholder-gray-400" required />
          <textarea v-model="localEvent.descripcion" placeholder="Descripción del evento" rows="3" class="w-full px-4 py-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-200 text-gray-800 placeholder-gray-400"></textarea>

          <!-- Base price removed: ticket types are required now -->

          <div class="mt-4 border-t pt-4">
            <h4 class="text-md font-semibold text-gray-800 mb-2">Tipos de boletos (opcional)</h4>
            <div class="flex gap-2">
              <input v-model="newTicket.nombre" placeholder="Nombre (ej: General)" class="flex-1 px-3 py-2 rounded-lg border border-gray-300 text-gray-800 placeholder-gray-400" />
              <input v-model="newTicket.precio" type="number" step="0.01" min="0" placeholder="Precio" class="w-28 px-3 py-2 rounded-lg border border-gray-300 text-gray-800 placeholder-gray-400" />
              <button type="button" @click="addTicketType" class="px-4 py-2 rounded-lg bg-blue-600 text-white">Añadir</button>
            </div>

            <div v-if="localEvent.ticketTypes.length" class="mt-3 space-y-2">
              <div v-for="(t,i) in localEvent.ticketTypes" :key="i" class="flex items-center justify-between bg-white p-2 rounded border border-gray-100">
                <div class="text-sm text-gray-800 placeholder-gray-400">
                  <strong>{{ t.nombre }}</strong> — ${{ t.precio }}
                </div>
                <button type="button" @click="removeTicketType(i)" class="text-red-600">Eliminar</button>
              </div>
            </div>
          </div>

          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-800">Forma de pago / Instrucciones</label>
            <textarea v-model="localEvent.formaPago" rows="4" placeholder="Describe cómo se puede pagar (ej: datos de transferencia, instrucciones para pago presencial, link de pago, etc.)" class="w-full px-4 py-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-200 text-gray-800"></textarea>
          </div>

          <div class="mt-4 border-t pt-4">
            <h4 class="text-md font-semibold text-gray-800 mb-2">Opciones de Inscripción</h4>
            <div class="grid grid-cols-1 gap-2">
              <label class="flex items-center gap-3">
                <input type="checkbox" v-model="localEvent.opciones.habilitarIglesia" class="w-4 h-4" />
                <span class="text-sm text-gray-700">Habilitar campo Iglesia (dropdown en inscripción)</span>
              </label>

              <label class="flex items-center gap-3">
                <input type="checkbox" v-model="localEvent.opciones.habilitarMentor" class="w-4 h-4" />
                <span class="text-sm text-gray-700">Habilitar campo Mentor (dropdown en inscripción)</span>
              </label>

              <label class="flex items-center gap-3">
                <input type="checkbox" v-model="localEvent.opciones.adjuntoRequerido" class="w-4 h-4" />
                <span class="text-sm text-gray-700">Adjunto requerido</span>
              </label>

              <label class="flex items-center gap-3">
                <input type="checkbox" v-model="localEvent.opciones.permitirMultiplesAdjuntos" class="w-4 h-4" />
                <span class="text-sm text-gray-700">Permitir múltiples archivos en comprobante</span>
              </label>

              <label class="flex items-center gap-3">
                <input type="checkbox" v-model="localEvent.opciones.habilitarEdad" class="w-4 h-4" />
                <span class="text-sm text-gray-700">Habilitar campo Edad en inscripción</span>
              </label>

              <label class="flex items-center gap-3">
                <input type="checkbox" v-model="localEvent.opciones.habilitarCorreo" class="w-4 h-4" />
                <span class="text-sm text-gray-700">Habilitar campo Correo electrónico en inscripción</span>
              </label>

              <label class="flex items-center gap-3">
                <input type="checkbox" v-model="localEvent.opciones.habilitarNota" class="w-4 h-4" />
                <span class="text-sm text-gray-700">Habilitar campo Nota (multilínea) en inscripción</span>
              </label>
            </div>
          </div>

          <div class="flex items-center gap-3 mt-2">
            <input id="esFuturo" type="checkbox" v-model="localEvent.esFuturo" class="w-4 h-4" />
            <label for="esFuturo" class="text-sm text-gray-700">Evento activo / Futuro</label>
          </div>

          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-800">Banner del evento</label>
            <input 
              type="file" 
              @change="handleImageUpload" 
              accept="image/*"
              class="w-full px-4 py-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-200 text-gray-800"
            />
            <div v-if="previewUrl" class="mt-3 flex items-start gap-4">
              <img :src="previewUrl" alt="Preview" class="w-32 h-20 object-cover rounded" />
              <div class="flex flex-col gap-2">
                <button type="button" @click="removeSelectedImage" class="px-3 py-2 rounded bg-red-500 text-white">Eliminar imagen</button>
                <small class="text-xs text-gray-500">Esta imagen será reemplazada al guardar.</small>
              </div>
            </div>
          </div>
        </div>
        <div class="relative">
          <button :disabled="loading" type="submit" 
                  class="w-full py-3 rounded-lg bg-blue-600 text-white font-bold shadow-md hover:bg-blue-700 transition-all disabled:opacity-60 disabled:cursor-not-allowed">
            <i :class="isEditing ? 'fas fa-save' : 'fas fa-plus'" class="mr-2"></i>
            {{ isEditing ? 'Guardar Cambios' : 'Crear Evento' }}
          </button>
          <div v-if="loading" class="absolute inset-y-0 right-4 flex items-center">
            <svg class="animate-spin h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
            </svg>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'

const props = defineProps({
  initialEvent: { type: Object, default: null }
})

const emit = defineEmits(['save', 'close'])

const isEditing = computed(() => !!props.initialEvent)

const defaultEvent = () => ({ titulo: '', fecha: '', lugar: '', descripcion: '', formaPago: '', esFuturo: true, precio: '', ticketTypes: [], opciones: { habilitarIglesia: false, habilitarMentor: false, adjuntoRequerido: true, permitirMultiplesAdjuntos: false, habilitarEdad: false, habilitarCorreo: false, habilitarNota: false } })

const localEvent = ref(props.initialEvent ? { ...props.initialEvent, ticketTypes: props.initialEvent.ticketTypes || [], opciones: { ...(props.initialEvent.opciones || {}), habilitarEdad: (props.initialEvent.opciones && props.initialEvent.opciones.habilitarEdad) || false, habilitarCorreo: (props.initialEvent.opciones && props.initialEvent.opciones.habilitarCorreo) || false, habilitarNota: (props.initialEvent.opciones && props.initialEvent.opciones.habilitarNota) || false } } : defaultEvent())
const newTicket = ref({ nombre: '', precio: '' })
const selectedImage = ref(null)
const loading = ref(false)
const error = ref('')
const previewUrl = ref('')

watch(() => props.initialEvent, (v) => {
  if (v) {
    localEvent.value = { ...v, ticketTypes: v.ticketTypes || [], opciones: { ...(v.opciones || {}), habilitarEdad: (v.opciones && v.opciones.habilitarEdad) || false, habilitarCorreo: (v.opciones && v.opciones.habilitarCorreo) || false, habilitarNota: (v.opciones && v.opciones.habilitarNota) || false } }
    // Si hay bannerUrl existente, mostrarla en el preview
    if (v.bannerUrl) {
      previewUrl.value = v.bannerUrl
    } else {
      previewUrl.value = ''
    }
  } else {
    localEvent.value = defaultEvent()
    previewUrl.value = ''
  }
  selectedImage.value = null
  newTicket.value = { nombre: '', precio: '' }
}, { immediate: true })

const addTicketType = () => {
  if (!newTicket.value.nombre || newTicket.value.precio === '') return
  localEvent.value.ticketTypes.push({ nombre: newTicket.value.nombre, precio: parseFloat(newTicket.value.precio).toFixed(2) })
  newTicket.value = { nombre: '', precio: '' }
}

const removeTicketType = (index) => {
  localEvent.value.ticketTypes.splice(index, 1)
}

const handleImageUpload = (e) => {
  const file = e.target.files[0]
  if (file) selectedImage.value = file
  if (file) {
    previewUrl.value = URL.createObjectURL(file)
  }
}

const removeSelectedImage = () => {
  selectedImage.value = null
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
    previewUrl.value = ''
  }
}

const submitForm = async () => {
  // validate required fields
  if (!localEvent.value.titulo || !localEvent.value.fecha || !localEvent.value.lugar) return

  // ticket types required
  if (!localEvent.value.ticketTypes || localEvent.value.ticketTypes.length === 0) {
    error.value = 'Agrega al menos un tipo de boleto.'
    return
  }

  error.value = ''
  loading.value = true

  // Use a promise/callback pattern: parent should return/resolve to indicate completion
  try {
    const maybePromise = emit('save', { eventData: { ...localEvent.value }, imageFile: selectedImage.value })
    // If parent returns a promise, await it; otherwise just proceed
    if (maybePromise && typeof maybePromise.then === 'function') {
      await maybePromise
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

</script>

<style scoped>
/* small helper: ensure modal sits above others if needed */
</style>
