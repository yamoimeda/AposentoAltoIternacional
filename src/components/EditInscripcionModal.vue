<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="show"
        @click.self="cerrar"
        class="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4 overflow-y-auto"
      >
        <div class="bg-white rounded-2xl shadow-2xl max-w-3xl w-full my-8 animate-fade-in-up overflow-hidden flex flex-col max-h-[90vh]">
          <!-- Header -->
          <div class="bg-gradient-to-r from-indigo-600 to-purple-600 p-6 flex-shrink-0">
            <div class="flex justify-between items-center">
              <h2 class="text-xl sm:text-2xl font-bold text-white flex items-center gap-2">
                <i class="fas fa-edit"></i>
                Editar Inscripción
              </h2>
              <button
                @click="cerrar"
                :disabled="guardando"
                class="text-white hover:bg-white/20 rounded-lg p-2 transition-colors disabled:opacity-50"
              >
                <i class="fas fa-times text-xl"></i>
              </button>
            </div>
          </div>

          <!-- Body -->
          <div class="p-6 overflow-y-auto flex-1 space-y-6">
            <!-- Informacion del Evento e ID -->
            <div class="bg-slate-50 border border-slate-200 p-4 rounded-xl flex flex-wrap justify-between items-center gap-2 text-xs text-slate-700">
              <div>
                <strong class="text-slate-900 font-semibold">Evento:</strong> {{ eventoTitulo || 'No especificado' }}
              </div>
              <div>
                <strong class="text-slate-900 font-semibold">ID Registro:</strong>
                <span class="font-mono text-indigo-600 ml-1">{{ formulario.registrationToken || 'N/A' }}</span>
              </div>
            </div>

            <!-- Trazabilidad / ¿Quién editó este registro? -->
            <div class="bg-amber-50/60 border border-amber-200/80 rounded-xl p-3.5 text-xs text-amber-950 flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 shadow-2xs">
              <div class="flex items-center gap-2.5 min-w-0">
                <div class="w-8 h-8 rounded-lg bg-amber-100/80 text-amber-700 flex items-center justify-center shrink-0">
                  <i class="fas fa-user-pen text-sm"></i>
                </div>
                <div class="truncate">
                  <div class="font-bold text-slate-800 flex items-center gap-1.5 flex-wrap">
                    <span>{{ auditoriaEdicion.tieneEdicionPrevia ? 'Última edición por:' : 'Registro original' }}</span>
                    <span class="px-2 py-0.5 rounded-md bg-amber-100 text-amber-900 font-mono font-semibold text-[11px]">
                      {{ auditoriaEdicion.editor || 'Asistente (Público)' }}
                    </span>
                  </div>
                  <div v-if="auditoriaEdicion.fecha" class="text-[11px] text-slate-500 mt-0.5">
                    <i class="fas fa-clock mr-1 text-slate-400"></i>{{ formatearFechaAuditoria(auditoriaEdicion.fecha) }}
                  </div>
                </div>
              </div>

              <!-- Indicador del usuario actual -->
              <div class="flex items-center gap-1.5 text-[11px] font-medium text-indigo-700 bg-indigo-50 border border-indigo-200 px-2.5 py-1 rounded-lg shrink-0 self-start sm:self-center">
                <i class="fas fa-shield-halved text-indigo-600"></i>
                <span>Editando como: <b>{{ usuarioActual }}</b></span>
              </div>
            </div>

            <!-- Adjuntos de la inscripción -->
            <div v-if="archivosAdjuntos.length > 0" class="bg-indigo-50/70 border border-indigo-100 p-4 rounded-xl">
              <label class="block text-xs font-bold text-indigo-900 uppercase tracking-wider mb-2">
                <i class="fas fa-paperclip mr-1 text-indigo-600"></i> Comprobante(s) de Pago Adjuntos
              </label>
              <FileViewer :files="archivosAdjuntos" />
            </div>

            <form id="editForm" @submit.prevent="guardar" class="space-y-6">
              <!-- Datos Personales -->
              <div>
                <h3 class="text-sm font-bold text-slate-800 uppercase tracking-wider mb-3 flex items-center gap-2 border-b pb-1">
                  <i class="fas fa-user-gear text-indigo-600"></i> Datos Personales
                </h3>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">
                      Nombre Completo <span class="text-rose-500">*</span>
                    </label>
                    <input
                      v-model="formulario.nombre"
                      type="text"
                      required
                      class="w-full px-3.5 py-2 border border-slate-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-slate-800 text-sm"
                    />
                  </div>

                  <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">
                      Cédula / Documento <span class="text-rose-500">*</span>
                    </label>
                    <input
                      v-model="formulario.cedula"
                      type="text"
                      required
                      class="w-full px-3.5 py-2 border border-slate-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-slate-800 text-sm font-mono"
                    />
                  </div>

                  <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">
                      Teléfono / WhatsApp <span class="text-rose-500">*</span>
                    </label>
                    <input
                      v-model="formulario.telefono"
                      type="tel"
                      required
                      class="w-full px-3.5 py-2 border border-slate-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-slate-800 text-sm"
                    />
                  </div>

                  <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">Edad</label>
                    <input
                      v-model.number="formulario.edad"
                      type="number"
                      min="0"
                      max="120"
                      class="w-full px-3.5 py-2 border border-slate-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-slate-800 text-sm"
                    />
                  </div>

                  <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">Correo Electrónico</label>
                    <input
                      v-model="formulario.correo"
                      type="email"
                      class="w-full px-3.5 py-2 border border-slate-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-slate-800 text-sm"
                    />
                  </div>

                  <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">Iglesia</label>
                    <input
                      v-model="formulario.iglesia"
                      type="text"
                      placeholder="Iglesia de origen..."
                      class="w-full px-3.5 py-2 border border-slate-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-slate-800 text-sm"
                    />
                  </div>

                  <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">Mentor / Líder</label>
                    <input
                      v-model="formulario.mentor"
                      type="text"
                      placeholder="Mentor asignado..."
                      class="w-full px-3.5 py-2 border border-slate-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-slate-800 text-sm"
                    />
                  </div>

                  <div class="md:col-span-2">
                    <label class="block text-xs font-semibold text-slate-700 mb-1">Nota / Observaciones</label>
                    <textarea
                      v-model="formulario.nota"
                      rows="2"
                      placeholder="Notas adicionales..."
                      class="w-full px-3.5 py-2 border border-slate-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-slate-800 text-sm"
                    ></textarea>
                  </div>
                </div>
              </div>

              <!-- Información de Pago y Boleto -->
              <div>
                <h3 class="text-sm font-bold text-slate-800 uppercase tracking-wider mb-3 flex items-center gap-2 border-b pb-1">
                  <i class="fas fa-ticket-alt text-indigo-600"></i> Boleto y Pago
                </h3>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">Tipo de Boleto</label>
                    <input
                      v-model="formulario.ticketType"
                      type="text"
                      class="w-full px-3.5 py-2 border border-slate-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-slate-800 text-sm"
                    />
                  </div>

                  <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">Monto / Precio ($)</label>
                    <input
                      v-model.number="formulario.totalPrice"
                      type="number"
                      step="0.01"
                      min="0"
                      class="w-full px-3.5 py-2 border border-slate-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-slate-800 text-sm font-bold text-emerald-700 bg-emerald-50/50"
                    />
                  </div>
                </div>
              </div>

              <!-- Mensaje de estado -->
              <div
                v-if="mensaje"
                :class="[
                  'p-3.5 rounded-xl text-xs font-semibold flex items-center gap-2',
                  mensaje.tipo === 'success' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-rose-50 text-rose-700 border border-rose-200'
                ]"
              >
                <i :class="['text-base', mensaje.tipo === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle']"></i>
                {{ mensaje.texto }}
              </div>
            </form>
          </div>

          <!-- Footer -->
          <div class="bg-slate-50 px-6 py-4 border-t border-slate-200 flex justify-end gap-3 flex-shrink-0">
            <button
              type="button"
              @click="cerrar"
              :disabled="guardando"
              class="px-5 py-2.5 border border-slate-300 text-slate-700 rounded-xl hover:bg-slate-100 font-semibold text-xs transition-colors disabled:opacity-50"
            >
              Cancelar
            </button>
            <button
              type="submit"
              form="editForm"
              :disabled="guardando"
              class="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl font-semibold text-xs shadow-md transition-colors disabled:opacity-50 flex items-center gap-2 cursor-pointer"
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
import { auth } from '../firebase'
import FileViewer from './FileViewer.vue'

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
  },
  eventoOpciones: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['close', 'save'])

const guardando = ref(false)
const mensaje = ref(null)

const usuarioActual = computed(() => {
  return auth.currentUser?.email || auth.currentUser?.displayName || 'Administrador'
})

const auditoriaEdicion = computed(() => {
  if (!props.inscripcion) return { tieneEdicionPrevia: false, editor: null, fecha: null }
  const i = props.inscripcion
  const p = i.participante || {}
  const ultima = i.ultimaModificacion || p.ultimaModificacion || {}

  const editor = i.editadoPor || p.editadoPor || ultima.por || null
  const fecha = i.fechaEdicion || p.fechaEdicion || ultima.fecha || null

  return {
    tieneEdicionPrevia: !!editor,
    editor: editor,
    fecha: fecha
  }
})

const formatearFechaAuditoria = (fechaStr) => {
  if (!fechaStr) return ''
  try {
    const d = new Date(fechaStr)
    return d.toLocaleString('es-ES', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch (e) {
    return fechaStr
  }
}

const formulario = ref({
  nombre: '',
  cedula: '',
  telefono: '',
  edad: '',
  correo: '',
  nota: '',
  iglesia: '',
  mentor: '',
  ticketType: '',
  ticketPrice: 0,
  ticketQuantity: 1,
  totalPrice: 0,
  montoPagado: 0,
  registrationToken: ''
})

const archivosAdjuntos = computed(() => {
  if (!props.inscripcion) return []
  const urls = []
  const p = props.inscripcion.participante || {}
  if (Array.isArray(p.comprobantesUrls)) {
    urls.push(...p.comprobantesUrls)
  } else if (p.comprobanteUrl) {
    urls.push(p.comprobanteUrl)
  }
  const adicionales = props.inscripcion.comprobantesAdicionales || []
  for (const ca of adicionales) {
    if (ca.url) urls.push(ca.url)
  }
  return urls
})

watch(() => props.inscripcion, (nuevaInscripcion) => {
  if (nuevaInscripcion) {
    const p = nuevaInscripcion.participante || {}
    const candidatos = [
      p.montoPagado,
      p.monto,
      p.totalPrice,
      nuevaInscripcion.montoPagado,
      nuevaInscripcion.monto,
      nuevaInscripcion.totalPrice
    ]
    let montoNum = 0
    for (const c of candidatos) {
      if (c !== undefined && c !== null && c !== '') {
        const num = Number(c)
        if (!isNaN(num) && num > 0) {
          montoNum = num
          break
        }
      }
    }
    if (montoNum === 0) {
      const tPrice = Number(p.ticketPrice || 0)
      const tQty = Number(p.ticketQuantity || 1)
      if (tPrice > 0) montoNum = tPrice * tQty
    }

    formulario.value = {
      nombre: p.nombre || '',
      cedula: p.cedula || '',
      telefono: p.telefono || '',
      edad: p.edad ?? '',
      correo: p.correo || '',
      nota: p.nota || '',
      iglesia: p.iglesia || '',
      mentor: p.mentor || '',
      ticketType: p.ticketType || 'General',
      ticketPrice: montoNum,
      ticketQuantity: p.ticketQuantity ?? 1,
      totalPrice: montoNum,
      montoPagado: montoNum,
      registrationToken: p.registrationToken || ''
    }
  }
}, { immediate: true, deep: true })

const cerrar = () => {
  if (!guardando.value) {
    mensaje.value = null
    emit('close')
  }
}

const guardar = async () => {
  if (!formulario.value.nombre.trim()) {
    mensaje.value = { tipo: 'error', texto: 'El nombre es obligatorio.' }
    return
  }
  if (!formulario.value.cedula.trim()) {
    mensaje.value = { tipo: 'error', texto: 'La cédula es obligatoria.' }
    return
  }
  if (!formulario.value.telefono.trim()) {
    mensaje.value = { tipo: 'error', texto: 'El teléfono es obligatorio.' }
    return
  }

  guardando.value = true
  mensaje.value = null

  try {
    const ahora = new Date().toISOString()
    const editor = usuarioActual.value

    // Preservar la estructura completa de `participante` para no borrar campos existentes
    const participanteExistente = props.inscripcion?.participante || {}
    const montoFinal = Number(formulario.value.totalPrice ?? formulario.value.montoPagado ?? 0) || 0

    const participanteActualizado = {
      ...participanteExistente,
      nombre: formulario.value.nombre.trim(),
      cedula: formulario.value.cedula.trim().toUpperCase(),
      telefono: formulario.value.telefono.trim(),
      edad: formulario.value.edad !== '' ? Number(formulario.value.edad) : null,
      correo: formulario.value.correo.trim() || null,
      nota: formulario.value.nota.trim() || null,
      iglesia: formulario.value.iglesia.trim() || null,
      mentor: formulario.value.mentor.trim() || null,
      ticketType: formulario.value.ticketType.trim() || 'General',
      ticketPrice: montoFinal,
      ticketQuantity: Math.max(1, Number(formulario.value.ticketQuantity) || 1),
      totalPrice: montoFinal,
      montoPagado: montoFinal,
      monto: montoFinal,
      registrationToken: formulario.value.registrationToken || participanteExistente.registrationToken,
      editadoPor: editor,
      fechaEdicion: ahora
    }

    await emit('save', {
      id: props.inscripcion.id,
      participante: participanteActualizado,
      editadoPor: editor,
      fechaEdicion: ahora,
      ultimaModificacion: {
        por: editor,
        fecha: ahora
      }
    })

    mensaje.value = {
      tipo: 'success',
      texto: `Cambios guardados por ${editor}`
    }

    setTimeout(() => {
      cerrar()
    }, 1200)
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
  transition: opacity 0.25s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-fade-in-up {
  animation: fade-in-up 0.3s ease-out;
}
</style>
