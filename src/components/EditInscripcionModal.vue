<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="show"
        @click.self="cerrar"
        class="fixed inset-0 bg-black/60 bg-opacity-50 z-50 flex items-center justify-center p-4 overflow-y-auto"
      >
        <div class="bg-white rounded-2xl shadow-2xl max-w-3xl w-full my-8 animate-fade-in-up">
          <!-- Header -->
          <div class="bg-gradient-to-r from-indigo-600 to-purple-600 p-6 rounded-t-2xl">
            <div class="flex justify-between items-center">
              <h2 class="text-2xl font-bold text-white flex items-center gap-2">
                <i class="fas fa-edit"></i>
                Editar Inscripción
              </h2>
              <button
                @click="cerrar"
                :disabled="guardando"
                class="text-white hover:bg-white hover:bg-opacity-20 rounded-lg p-2 transition-colors disabled:opacity-50"
              >
                <i class="fas fa-times text-xl"></i>
              </button>
            </div>
          </div>

          <!-- Body -->
          <div class="p-6 max-h-[70vh] overflow-y-auto">
            <form @submit.prevent="guardar" class="space-y-6">
              <!-- Información del Evento -->
              <div class="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
                <p class="text-sm text-gray-600">
                  <strong>Evento:</strong> {{ eventoTitulo }}
                </p>
                <p class="text-sm text-gray-600">
                  <strong>ID Registro:</strong> {{ formulario.registrationToken || 'N/A' }}
                </p>
              </div>

              <!-- Datos del Participante -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">
                    <i class="fas fa-user mr-2 text-indigo-600"></i>
                    Nombre Completo *
                  </label>
                  <input
                    v-model="formulario.nombre"
                    type="text"
                    required
                    class="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-600"
                  />
                </div>

                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">
                    <i class="fas fa-id-card mr-2 text-indigo-600"></i>
                    Cédula *
                  </label>
                  <input
                    v-model="formulario.cedula"
                    type="text"
                    required
                    class="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-600"
                  />
                </div>

                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">
                    <i class="fas fa-phone mr-2 text-indigo-600"></i>
                    WhatsApp * 
                  </label>
                  <input
                    v-model="formulario.telefono"
                    type="tel"
                    required
                    class="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-600"
                  />
                </div>

                <div v-if="effectiveOpciones.habilitarIglesia">
                  <label class="block text-sm font-semibold text-gray-700 mb-2">Iglesia</label>
                  <input v-model="formulario.iglesia" type="text" class="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-600" />
                </div>

                <div v-if="effectiveOpciones.habilitarMentor">
                  <label class="block text-sm font-semibold text-gray-700 mb-2">Mentor</label>
                  <input v-model="formulario.mentor" type="text" class="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-600" />
                </div>

                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-2">
                    <i class="fas fa-calendar mr-2 text-indigo-600"></i>
                    Edad
                  </label>
                  <input
                    v-model.number="formulario.edad"
                    type="number"
                    class="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-600"
                  />
                </div>
                <div v-if="effectiveOpciones.habilitarCorreo">
                  <label class="block text-sm font-semibold text-gray-700 mb-2">Correo electrónico</label>
                  <input v-model="formulario.correo" type="email" class="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-600" />
                </div>

                <div v-if="effectiveOpciones.habilitarNota" class="md:col-span-2">
                  <label class="block text-sm font-semibold text-gray-700 mb-2">Nota</label>
                  <textarea v-model="formulario.nota" rows="3" class="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-600"></textarea>
                </div>
              </div>

              <!-- Información del Ticket -->
              <div class="border-t pt-4">
                <h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
                  <i class="fas fa-ticket-alt text-indigo-600"></i>
                  Información del Ticket
                </h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-semibold text-gray-700 mb-2">Tipo de Ticket</label>
                    <input
                      v-model="formulario.ticketType"
                      type="text"
                      class="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-600"
                    />
                  </div>


                  <div>
                    <label class="block text-sm font-semibold text-gray-700 mb-2">Total Pagado ($)</label>
                    <input
                      v-model.number="formulario.totalPrice"
                      type="number"
                      step="0.01"
                      min="0"
                      class="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-600"
                    />
                  </div>
                </div>
              </div>

              <!-- Mensaje de error/éxito -->
              <div v-if="mensaje" :class="[
                'p-4 rounded-lg',
                mensaje.tipo === 'success' ? 'bg-green-50 text-green-700 border border-green-200' : 'bg-red-50 text-red-700 border border-red-200'
              ]">
                <i :class="['mr-2', mensaje.tipo === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle']"></i>
                {{ mensaje.texto }}
              </div>
            </form>
          </div>

          <!-- Footer -->
          <div class="bg-gray-50 px-6 py-4 rounded-b-2xl flex justify-end gap-3">
            <button
              type="button"
              @click="cerrar"
              :disabled="guardando"
              class="px-6 py-2 border-2 border-gray-300 text-gray-700 rounded-lg hover:bg-gray-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Cancelar
            </button>
            <button
              type="button"
              @click="guardar"
              :disabled="guardando"
              class="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center gap-2"
            >
              <i v-if="guardando" class="fas fa-spinner fa-spin"></i>
              <i v-else class="fas fa-save"></i>
              {{ guardando ? 'Guardando...' : 'Guardar Cambios' }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, watch, computed } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  inscripcion: {
    type: Object,
    default: null
  },
  eventoTitulo: {
    type: String,
    default: ''
  }
  ,
  eventoOpciones: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['close', 'save'])

const guardando = ref(false)
const mensaje = ref(null)

const formulario = ref({
  nombre: '',
  cedula: '',
  telefono: '',
  edad: '',
  ticketType: '',
  ticketQuantity: 1,
  totalPrice: 0,
  registrationToken: ''
})

// Prefer explicitly passed-in prop `eventoOpciones`, fallback to `inscripcion.eventoOpciones` when available
const effectiveOpciones = computed(() => {
  if (props.eventoOpciones && Object.keys(props.eventoOpciones).length) return props.eventoOpciones
  if (props.inscripcion && props.inscripcion.eventoOpciones) return props.inscripcion.eventoOpciones
  return {}
})

// Cargar datos cuando cambia la inscripción
watch(() => props.inscripcion, (nuevaInscripcion) => {
  console.log('EditInscripcionModal: inscripcion changed:', nuevaInscripcion)
  if (nuevaInscripcion) {
    // La inscripción ya tiene la estructura correcta desde la BD
    const p = nuevaInscripcion.participante || {}
    formulario.value = {
      nombre: p.nombre || '',
      cedula: p.cedula || '',
      telefono: p.telefono || '',
        edad: p.edad || '',
        correo: p.correo || '',
        nota: p.nota || '',
      ticketType: p.ticketType || '',
      ticketQuantity: p.ticketQuantity || 1,
      totalPrice: p.totalPrice || 0,
      registrationToken: p.registrationToken || ''
    }
    console.log('Formulario cargado:', formulario.value)
  }
}, { immediate: true, deep: true })

const cerrar = () => {
  if (!guardando.value) {
    mensaje.value = null
    emit('close')
  }
}

const guardar = async () => {
  guardando.value = true
  mensaje.value = null

  try {
    // Emitir evento con los datos actualizados
    await emit('save', {
      id: props.inscripcion.id,
      participante: { 
        ...formulario.value,
        correo: formulario.value.correo || '',
        nota: formulario.value.nota || '',
        iglesia: formulario.value.iglesia || '',
        mentor: formulario.value.mentor || ''
      }
    })

    mensaje.value = {
      tipo: 'success',
      texto: 'Cambios guardados exitosamente'
    }

    // Cerrar modal después de 1.5 segundos
    setTimeout(() => {
      cerrar()
    }, 1500)
  } catch (error) {
    console.error('Error guardando cambios:', error)
    mensaje.value = {
      tipo: 'error',
      texto: 'Error al guardar los cambios. Intenta de nuevo.'
    }
  } finally {
    guardando.value = false
  }
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fade-in-up 0.4s ease-out;
}
</style>
