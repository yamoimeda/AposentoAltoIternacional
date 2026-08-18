<template>
  <div class="fixed inset-0 bg-slate-950/60 backdrop-blur-xs flex items-center justify-center z-50 p-3 sm:p-6 overflow-y-auto">
    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-xl border border-slate-200 my-auto max-h-[90vh] overflow-y-auto relative p-0">
      <!-- Full-width Top-flush Sticky Header -->
      <div class="sticky top-0 z-20 bg-slate-900 text-white px-5 sm:px-6 py-4 rounded-t-2xl flex justify-between items-center shadow-md">
        <h3 class="text-lg sm:text-xl font-bold text-white tracking-tight flex items-center gap-2.5">
          <i :class="['text-indigo-400', isEditing ? 'fas fa-pen-to-square' : 'fas fa-calendar-plus']"></i>
          <span>{{ isEditing ? 'Editar Evento' : 'Crear Nuevo Evento' }}</span>
        </h3>
        <button type="button" @click="$emit('close')" class="w-8 h-8 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white flex items-center justify-center transition-colors cursor-pointer" title="Cerrar ventana">
          <i class="fas fa-times text-base"></i>
        </button>
      </div>

      <div class="p-5 sm:p-6">
        <!-- Error alert -->
        <div v-if="error" class="mb-4 p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-center gap-2">
          <i class="fas fa-circle-exclamation text-rose-500"></i>
          <span>{{ error }}</span>
        </div>

        <!-- Barra de Auditoría y Trazabilidad de Publicación/Evento -->
        <div class="mb-4 p-3.5 rounded-xl border border-slate-200 bg-slate-50 text-xs text-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 shadow-2xs">
          <div class="flex items-center gap-2.5 min-w-0">
            <div class="w-8 h-8 rounded-lg bg-indigo-100 text-indigo-700 flex items-center justify-center shrink-0">
              <i :class="['fas', isEditing ? 'fa-clock-rotate-left' : 'fa-sparkles', 'text-sm']"></i>
            </div>
            <div class="truncate">
              <!-- Si se está editando -->
              <template v-if="isEditing">
                <div class="font-bold text-slate-900 flex items-center gap-1.5 flex-wrap">
                  <span>{{ auditoriaEvento.editadoPor ? 'Última edición por:' : 'Creado por:' }}</span>
                  <span class="px-2 py-0.5 rounded-md bg-indigo-50 border border-indigo-200 text-indigo-800 font-mono font-semibold text-[11px]">
                    {{ auditoriaEvento.editadoPor || auditoriaEvento.creadoPor }}
                  </span>
                </div>
                <div v-if="auditoriaEvento.fechaEdicion || auditoriaEvento.fechaCreacion" class="text-[11px] text-slate-500 mt-0.5">
                  <i class="fas fa-calendar-check mr-1 text-slate-400"></i>
                  {{ formatearFechaAuditoria(auditoriaEvento.fechaEdicion || auditoriaEvento.fechaCreacion) }}
                </div>
              </template>
              <!-- Si es nueva publicación -->
              <template v-else>
                <div class="font-bold text-slate-900">Nueva Publicación / Evento</div>
                <div class="text-[11px] text-slate-500 mt-0.5">Se registrará a tu nombre al guardar</div>
              </template>
            </div>
          </div>

          <!-- Usuario activo -->
          <div class="flex items-center gap-1.5 text-[11px] font-medium text-slate-700 bg-white border border-slate-200 px-2.5 py-1 rounded-lg shrink-0 self-start sm:self-center">
            <i class="fas fa-user-check text-emerald-600"></i>
            <span>Operando como: <b>{{ usuarioActual }}</b></span>
          </div>
        </div>

      <form @submit.prevent="submitForm">
        <div class="space-y-4 mb-6">
          <input v-model="localEvent.titulo" placeholder="Título del evento *" class="w-full px-4 py-2.5 rounded-xl border border-slate-200 text-slate-900 placeholder-slate-400 text-sm focus:outline-none focus:border-indigo-600" required />
          <input v-model="localEvent.fecha" type="date" class="w-full px-4 py-2.5 rounded-xl border border-slate-200 text-slate-900 text-sm focus:outline-none focus:border-indigo-600" required />
          <input v-model="localEvent.lugar" placeholder="Lugar del evento *" class="w-full px-4 py-2.5 rounded-xl border border-slate-200 text-slate-900 placeholder-slate-400 text-sm focus:outline-none focus:border-indigo-600" required />
          <textarea v-model="localEvent.descripcion" placeholder="Descripción del evento" rows="3" class="w-full px-4 py-2.5 rounded-xl border border-slate-200 text-slate-900 placeholder-slate-400 text-sm focus:outline-none focus:border-indigo-600"></textarea>

          <!-- Tipos de Boletos -->
          <div class="mt-4 border-t border-slate-100 pt-4">
            <h4 class="text-sm font-bold text-slate-900 mb-1">Tipos de boletos (Requerido)</h4>
            <p class="text-xs text-slate-500 mb-3 leading-relaxed">
              <i class="fas fa-shield-alt text-indigo-500 mr-1"></i>
              Las inscripciones realizadas mantendrán su precio e historial de compra inmutable aun si modificas o archivas boletos.
            </p>

            <div class="flex flex-col sm:flex-row gap-2 mb-3">
              <input v-model="newTicket.nombre" placeholder="Nombre (ej: General / VIP)" class="flex-1 px-3.5 py-2.5 rounded-xl border border-slate-200 text-slate-900 placeholder-slate-400 text-sm focus:outline-none focus:border-indigo-600" />
              <div class="flex gap-2">
                <input v-model="newTicket.precio" type="number" step="0.01" min="0" placeholder="Precio ($)" class="w-full sm:w-28 px-3.5 py-2.5 rounded-xl border border-slate-200 text-slate-900 placeholder-slate-400 text-sm focus:outline-none focus:border-indigo-600" />
                <button type="button" @click="addTicketType" class="px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm transition-colors cursor-pointer shrink-0">Añadir</button>
              </div>
            </div>

            <!-- Sección Boletos Activos -->
            <div v-if="boletosActivos.length" class="space-y-2.5 mb-4">
              <div class="text-xs font-bold text-slate-700 uppercase tracking-wider mb-1 flex items-center gap-1.5">
                <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                <span>Boletos Activos ({{ boletosActivos.length }})</span>
              </div>
              <div
                v-for="t in boletosActivos"
                :key="t.id || t.nombre"
                class="flex flex-col bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs text-sm"
              >
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2.5">
                  <div class="flex-1 min-w-0">
                    <div class="font-bold text-slate-900 truncate">{{ t.nombre }}</div>
                    <div class="text-xs font-semibold text-indigo-600 mt-0.5">${{ t.precio }} USD</div>
                  </div>

                  <div class="flex items-center gap-2 self-end sm:self-center shrink-0">
                    <button
                      type="button"
                      @click="iniciarEdicionBoleto(t)"
                      class="text-xs font-semibold px-3 py-1.5 rounded-lg bg-indigo-50 text-indigo-700 border border-indigo-200 hover:bg-indigo-100 transition-colors cursor-pointer flex items-center gap-1"
                      title="Editar boleto"
                    >
                      <i class="fas fa-pen-to-square text-[11px]"></i>
                      <span>Editar</span>
                    </button>

                    <button
                      type="button"
                      @click="archivarBoleto(t.id || t.nombre)"
                      class="text-xs font-semibold px-3 py-1.5 rounded-lg bg-amber-50 text-amber-700 border border-amber-200 hover:bg-amber-100 transition-colors cursor-pointer flex items-center gap-1"
                      title="Archivar boleto"
                    >
                      <i class="fas fa-box-archive text-[11px]"></i>
                      <span>Archivar</span>
                    </button>

                    <button
                      type="button"
                      @click="eliminarBoletoPorId(t.id || t.nombre)"
                      class="text-xs font-semibold px-3 py-1.5 rounded-lg bg-rose-50 text-rose-600 border border-rose-100 hover:bg-rose-100 transition-colors cursor-pointer"
                      title="Eliminar boleto"
                    >
                      Eliminar
                    </button>
                  </div>
                </div>

                <!-- Formulario Inline de Edición -->
                <div v-if="editingTicketId === t.id" class="mt-3 pt-3 border-t border-slate-100 space-y-2">
                  <div class="text-xs font-bold text-indigo-900">Editar Boleto</div>
                  <div class="flex flex-col sm:flex-row gap-2">
                    <input v-model="editTicketForm.nombre" placeholder="Nombre del boleto" class="flex-1 px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-sm text-slate-900 focus:outline-none focus:border-indigo-600" />
                    <input v-model="editTicketForm.precio" type="number" step="0.01" min="0" placeholder="Precio ($)" class="w-full sm:w-28 px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-sm text-slate-900 focus:outline-none focus:border-indigo-600" />
                  </div>
                  <div class="flex items-center gap-2 justify-end pt-1">
                    <button type="button" @click="cancelarEdicionBoleto" class="px-3 py-1.5 text-xs font-medium text-slate-600 bg-slate-100 rounded-lg hover:bg-slate-200">Cancelar</button>
                    <button type="button" @click="guardarEdicionBoleto" class="px-3 py-1.5 text-xs font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 flex items-center gap-1">
                      <i v-if="procesandoEdicion" class="fas fa-circle-notch fa-spin text-xs"></i>
                      <span>Guardar</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Sección Boletos Archivados -->
            <div v-if="boletosArchivados.length" class="space-y-2.5 pt-3 border-t border-slate-100">
              <div class="text-xs font-bold text-amber-700 uppercase tracking-wider mb-1 flex items-center gap-1.5">
                <i class="fas fa-box-archive text-amber-600 text-xs"></i>
                <span>Boletos Archivados ({{ boletosArchivados.length }})</span>
              </div>
              <div
                v-for="t in boletosArchivados"
                :key="t.id || t.nombre"
                class="flex flex-col bg-slate-50/80 p-3.5 rounded-xl border border-amber-200/60 text-sm"
              >
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2.5">
                  <div class="flex-1 min-w-0">
                    <div class="font-bold text-slate-700 truncate opacity-75">{{ t.nombre }}</div>
                    <div class="text-xs font-semibold text-slate-500 mt-0.5">${{ t.precio }} USD</div>
                  </div>

                  <div class="flex items-center gap-2 self-end sm:self-center shrink-0">
                    <button
                      type="button"
                      @click="iniciarEdicionBoleto(t)"
                      class="text-xs font-semibold px-3 py-1.5 rounded-lg bg-indigo-50 text-indigo-700 border border-indigo-200 hover:bg-indigo-100 transition-colors cursor-pointer flex items-center gap-1"
                      title="Editar boleto"
                    >
                      <i class="fas fa-pen-to-square text-[11px]"></i>
                      <span>Editar</span>
                    </button>

                    <button
                      type="button"
                      @click="reactivarBoleto(t.id || t.nombre)"
                      class="text-xs font-semibold px-3 py-1.5 rounded-lg bg-emerald-50 text-emerald-700 border border-emerald-200 hover:bg-emerald-100 transition-colors cursor-pointer flex items-center gap-1"
                      title="Reactivar boleto"
                    >
                      <i class="fas fa-rotate-left text-[11px]"></i>
                      <span>Reactivar</span>
                    </button>

                    <button
                      type="button"
                      @click="eliminarBoletoPorId(t.id || t.nombre)"
                      class="text-xs font-semibold px-3 py-1.5 rounded-lg bg-rose-50 text-rose-600 border border-rose-100 hover:bg-rose-100 transition-colors cursor-pointer"
                      title="Eliminar boleto"
                    >
                      Eliminar
                    </button>
                  </div>
                </div>

                <!-- Formulario Inline de Edición -->
                <div v-if="editingTicketId === t.id" class="mt-3 pt-3 border-t border-amber-200/60 space-y-2">
                  <div class="text-xs font-bold text-indigo-900">Editar Boleto Archivación</div>
                  <div class="flex flex-col sm:flex-row gap-2">
                    <input v-model="editTicketForm.nombre" placeholder="Nombre del boleto" class="flex-1 px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-sm text-slate-900 focus:outline-none focus:border-indigo-600" />
                    <input v-model="editTicketForm.precio" type="number" step="0.01" min="0" placeholder="Precio ($)" class="w-full sm:w-28 px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-sm text-slate-900 focus:outline-none focus:border-indigo-600" />
                  </div>
                  <div class="flex items-center gap-2 justify-end pt-1">
                    <button type="button" @click="cancelarEdicionBoleto" class="px-3 py-1.5 text-xs font-medium text-slate-600 bg-white border border-slate-200 rounded-lg hover:bg-slate-100">Cancelar</button>
                    <button type="button" @click="guardarEdicionBoleto" class="px-3 py-1.5 text-xs font-semibold text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 flex items-center gap-1">
                      <i v-if="procesandoEdicion" class="fas fa-circle-notch fa-spin text-xs"></i>
                      <span>Guardar</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Opciones de Inscripción -->
          <div class="mt-4 border-t border-slate-100 pt-4">
            <h4 class="text-sm font-bold text-slate-900 mb-2">Opciones de Inscripción</h4>
            <div class="grid grid-cols-1 gap-2.5">
              <label class="flex items-center gap-3 cursor-pointer">
                <input type="checkbox" v-model="localEvent.opciones.habilitarIglesia" class="w-4 h-4 rounded text-indigo-600 focus:ring-indigo-500" />
                <span class="text-xs text-slate-700">Habilitar campo Iglesia en formulario de inscripción</span>
              </label>

              <label class="flex items-center gap-3 cursor-pointer">
                <input type="checkbox" v-model="localEvent.opciones.habilitarMentor" class="w-4 h-4 rounded text-indigo-600 focus:ring-indigo-500" />
                <span class="text-xs text-slate-700">Habilitar campo Mentor en formulario de inscripción</span>
              </label>

              <label class="flex items-center gap-3 cursor-pointer">
                <input type="checkbox" v-model="localEvent.opciones.adjuntoRequerido" class="w-4 h-4 rounded text-indigo-600 focus:ring-indigo-500" />
                <span class="text-xs text-slate-700">Comprobante de pago adjunto requerido</span>
              </label>

              <label class="flex items-center gap-3 cursor-pointer">
                <input type="checkbox" v-model="localEvent.opciones.permitirMultiplesAdjuntos" class="w-4 h-4 rounded text-indigo-600 focus:ring-indigo-500" />
                <span class="text-xs text-slate-700">Permitir múltiples archivos en el comprobante</span>
              </label>

              <label class="flex items-center gap-3 cursor-pointer">
                <input type="checkbox" v-model="localEvent.opciones.habilitarEdad" class="w-4 h-4 rounded text-indigo-600 focus:ring-indigo-500" />
                <span class="text-xs text-slate-700">Habilitar campo Edad en inscripción</span>
              </label>

              <label class="flex items-center gap-3 cursor-pointer">
                <input type="checkbox" v-model="localEvent.opciones.habilitarCorreo" class="w-4 h-4 rounded text-indigo-600 focus:ring-indigo-500" />
                <span class="text-xs text-slate-700">Habilitar campo Correo electrónico en inscripción</span>
              </label>

              <label class="flex items-center gap-3 cursor-pointer">
                <input type="checkbox" v-model="localEvent.opciones.habilitarNota" class="w-4 h-4 rounded text-indigo-600 focus:ring-indigo-500" />
                <span class="text-xs text-slate-700">Habilitar campo Nota especial en inscripción</span>
              </label>
            </div>
          </div>

          <div class="flex items-center gap-3 mt-2">
            <input id="esFuturo" type="checkbox" v-model="localEvent.esFuturo" class="w-4 h-4 rounded text-indigo-600 focus:ring-indigo-500" />
            <label for="esFuturo" class="text-xs font-semibold text-slate-800">Evento activo / Futuro</label>
          </div>

          <div class="space-y-2 border-t border-slate-100 pt-4">
            <label class="block text-xs font-bold text-slate-900">Banner del evento</label>
            <input 
              type="file" 
              @change="handleImageUpload" 
              accept="image/*"
              class="w-full px-4 py-2.5 rounded-xl border border-slate-200 text-slate-800 text-xs focus:outline-none focus:border-indigo-600"
            />
            <div v-if="previewUrl" class="mt-3 flex items-start gap-4">
              <img :src="previewUrl" alt="Preview" class="w-32 h-20 object-cover rounded-xl border border-slate-200" />
              <div class="flex flex-col gap-2">
                <button type="button" @click="removeSelectedImage" class="px-3 py-1.5 rounded-lg bg-rose-500 hover:bg-rose-600 text-white text-xs font-semibold">Eliminar imagen</button>
                <small class="text-xs text-slate-500">Se reemplazará la imagen al guardar.</small>
              </div>
            </div>
          </div>
        </div>

        <div class="relative pt-2">
          <button :disabled="loading" type="submit" 
                  class="w-full py-3.5 rounded-xl bg-indigo-600 text-white font-bold text-sm shadow-md hover:bg-indigo-700 transition-all disabled:opacity-60 disabled:cursor-not-allowed cursor-pointer flex items-center justify-center gap-2">
            <i :class="isEditing ? 'fas fa-save' : 'fas fa-plus'"></i>
            <span>{{ isEditing ? 'Guardar Cambios del Evento' : 'Crear Evento' }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>

    <!-- Modal de Confirmación de Actualización Masiva de Inscripciones -->
    <div v-if="mostrarModalActualizarPasadas" class="fixed inset-0 bg-slate-950/70 backdrop-blur-xs flex items-center justify-center z-[60] p-4">
      <div class="bg-white rounded-2xl p-6 w-full max-w-md shadow-2xl border border-slate-200">
        <div class="w-12 h-12 rounded-2xl bg-amber-50 border border-amber-200 text-amber-600 flex items-center justify-center text-xl mb-4">
          <i class="fas fa-triangle-exclamation"></i>
        </div>
        <h3 class="text-lg font-bold text-slate-900 mb-2">Inscripciones Existentes Detectadas</h3>
        <p class="text-xs text-slate-600 leading-relaxed mb-3">
          Se encontraron <strong class="text-indigo-600 font-bold">{{ conteoInscripcionesAfectadas }} inscripciones</strong> registradas previamente con el boleto <strong>"{{ ticketEnEdicionOriginal.nombre }}"</strong>.
        </p>
        <p class="text-xs text-slate-600 mb-6 bg-slate-50 p-3 rounded-xl border border-slate-200">
          ¿Deseas actualizar el precio en las inscripciones ya registradas de <strong>${{ ticketEnEdicionOriginal.precio }}</strong> a <strong>${{ editTicketForm.precio }} USD</strong>, o mantener su precio histórico?
        </p>

        <div class="flex flex-col gap-2">
          <button
            type="button"
            @click="confirmarActualizacionPasadas(true)"
            :disabled="procesandoActualizacionMasiva"
            class="w-full py-2.5 px-4 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs rounded-xl shadow-md transition-all cursor-pointer flex items-center justify-center gap-2"
          >
            <i v-if="procesandoActualizacionMasiva" class="fas fa-circle-notch fa-spin"></i>
            <i v-else class="fas fa-rotate"></i>
            <span>Sí, actualizar inscripciones registradas</span>
          </button>

          <button
            type="button"
            @click="confirmarActualizacionPasadas(false)"
            :disabled="procesandoActualizacionMasiva"
            class="w-full py-2.5 px-4 bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs rounded-xl transition-all cursor-pointer"
          >
            Mantener precio histórico (Recomendado)
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { db, auth } from '../firebase'
import { collection, query, where, getDocs, writeBatch, doc } from 'firebase/firestore'

const props = defineProps({
  initialEvent: { type: Object, default: null }
})

const emit = defineEmits(['save', 'close'])

const isEditing = computed(() => !!props.initialEvent)

const usuarioActual = computed(() => {
  return auth.currentUser?.email || auth.currentUser?.displayName || 'Administrador'
})

const auditoriaEvento = computed(() => {
  if (!props.initialEvent) {
    return {
      esNuevo: true,
      creadoPor: null,
      fechaCreacion: null,
      editadoPor: null,
      fechaEdicion: null
    }
  }
  const e = props.initialEvent
  const ultima = e.ultimaModificacion || {}
  return {
    esNuevo: false,
    creadoPor: e.creadoPor || 'Administración',
    fechaCreacion: e.createdAt || null,
    editadoPor: e.editadoPor || ultima.por || null,
    fechaEdicion: e.updatedAt || ultima.fecha || null
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

const defaultEvent = () => ({ titulo: '', fecha: '', lugar: '', descripcion: '', formaPago: '', esFuturo: true, precio: '', ticketTypes: [], opciones: { habilitarIglesia: false, habilitarMentor: false, adjuntoRequerido: true, permitirMultiplesAdjuntos: false, habilitarEdad: false, habilitarCorreo: false, habilitarNota: false } })

const localEvent = ref(props.initialEvent ? { ...props.initialEvent, ticketTypes: props.initialEvent.ticketTypes || [], opciones: { ...(props.initialEvent.opciones || {}), habilitarEdad: (props.initialEvent.opciones && props.initialEvent.opciones.habilitarEdad) || false, habilitarCorreo: (props.initialEvent.opciones && props.initialEvent.opciones.habilitarCorreo) || false, habilitarNota: (props.initialEvent.opciones && props.initialEvent.opciones.habilitarNota) || false } } : defaultEvent())
const newTicket = ref({ nombre: '', precio: '' })
const selectedImage = ref(null)
const loading = ref(false)
const error = ref('')
const previewUrl = ref('')

// Estados para edición inline de boleto
const editingTicketId = ref(null)
const editTicketForm = ref({ nombre: '', precio: '' })
const ticketEnEdicionOriginal = ref(null)
const procesandoEdicion = ref(false)

// Estados para actualización masiva de inscripciones pasadas
const mostrarModalActualizarPasadas = ref(false)
const conteoInscripcionesAfectadas = ref(0)
const inscripcionesDocsAfectados = ref([])
const procesandoActualizacionMasiva = ref(false)

watch(() => props.initialEvent, (v) => {
  if (v) {
    const types = (v.ticketTypes || []).map((t, idx) => ({
      id: t.id || 'tkt_' + idx + '_' + Date.now(),
      nombre: t.nombre,
      precio: t.precio,
      activo: t.activo !== false
    }))
    localEvent.value = {
      ...v,
      ticketTypes: types,
      opciones: {
        ...(v.opciones || {}),
        habilitarEdad: (v.opciones && v.opciones.habilitarEdad) || false,
        habilitarCorreo: (v.opciones && v.opciones.habilitarCorreo) || false,
        habilitarNota: (v.opciones && v.opciones.habilitarNota) || false
      }
    }
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

const boletosActivos = computed(() => {
  return (localEvent.value.ticketTypes || []).filter(t => t.activo !== false)
})

const boletosArchivados = computed(() => {
  return (localEvent.value.ticketTypes || []).filter(t => t.activo === false)
})

const addTicketType = () => {
  if (!newTicket.value.nombre || newTicket.value.precio === '') return
  const ticketId = 'tkt_' + Date.now() + '_' + Math.random().toString(36).substring(2, 7)
  localEvent.value.ticketTypes.push({
    id: ticketId,
    nombre: newTicket.value.nombre,
    precio: parseFloat(newTicket.value.precio).toFixed(2),
    activo: true
  })
  newTicket.value = { nombre: '', precio: '' }
}

const archivarBoleto = (identifier) => {
  const t = localEvent.value.ticketTypes.find(x => (x.id && x.id === identifier) || x.nombre === identifier)
  if (t) t.activo = false
}

const reactivarBoleto = (identifier) => {
  const t = localEvent.value.ticketTypes.find(x => (x.id && x.id === identifier) || x.nombre === identifier)
  if (t) t.activo = true
}

const eliminarBoletoPorId = (identifier) => {
  const index = localEvent.value.ticketTypes.findIndex(x => (x.id && x.id === identifier) || x.nombre === identifier)
  if (index !== -1) {
    localEvent.value.ticketTypes.splice(index, 1)
  }
}

const iniciarEdicionBoleto = (ticket) => {
  editingTicketId.value = ticket.id
  ticketEnEdicionOriginal.value = { ...ticket }
  editTicketForm.value = { nombre: ticket.nombre, precio: ticket.precio }
}

const cancelarEdicionBoleto = () => {
  editingTicketId.value = null
  ticketEnEdicionOriginal.value = null
  editTicketForm.value = { nombre: '', precio: '' }
}

const guardarEdicionBoleto = async () => {
  if (!editTicketForm.value.nombre || editTicketForm.value.precio === '') return
  procesandoEdicion.value = true

  const original = ticketEnEdicionOriginal.value
  const nuevoNombre = editTicketForm.value.nombre.trim()
  const nuevoPrecio = parseFloat(editTicketForm.value.precio).toFixed(2)

  const elPrecioCambio = parseFloat(original.precio) !== parseFloat(nuevoPrecio)
  const elNombreCambio = original.nombre !== nuevoNombre

  // Si no hay evento existente guardado aún, solo actualizar localEvent
  if (!props.initialEvent || (!elPrecioCambio && !elNombreCambio)) {
    const t = localEvent.value.ticketTypes.find(x => x.id === editingTicketId.value)
    if (t) {
      t.nombre = nuevoNombre
      t.precio = nuevoPrecio
    }
    cancelarEdicionBoleto()
    procesandoEdicion.value = false
    return
  }

  // Buscar en Firestore inscripciones existentes para este evento y boleto
  try {
    const eventId = props.initialEvent.id
    const q = query(collection(db, 'inscripciones'), where('eventoId', '==', eventId))
    const snapshot = await getDocs(q)
    const inscripcionesCoincidentes = snapshot.docs.filter(d => {
      const p = d.data().participante || {}
      const pTypeId = p.ticketTypeId || null
      const pTypeNameNorm = (p.ticketType || '').trim().toLowerCase()
      const origNameNorm = (original.nombre || '').trim().toLowerCase()

      // Coincide si tiene el mismo ticketTypeId o si coincide por el nombre del boleto (legacy)
      return (pTypeId && pTypeId === original.id) || (pTypeNameNorm && pTypeNameNorm === origNameNorm)
    })

    if (inscripcionesCoincidentes.length > 0) {
      conteoInscripcionesAfectadas.value = inscripcionesCoincidentes.length
      inscripcionesDocsAfectados.value = inscripcionesCoincidentes
      mostrarModalActualizarPasadas.value = true
    } else {
      // No hay inscripciones pasadas afectables, aplicar cambio directamente
      aplicarCambioBoletoLocal(nuevoNombre, nuevoPrecio)
      cancelarEdicionBoleto()
    }
  } catch (e) {
    console.error('Error verificando inscripciones pasadas:', e)
    aplicarCambioBoletoLocal(nuevoNombre, nuevoPrecio)
    cancelarEdicionBoleto()
  } finally {
    procesandoEdicion.value = false
  }
}

const aplicarCambioBoletoLocal = (nuevoNombre, nuevoPrecio) => {
  const t = localEvent.value.ticketTypes.find(x => x.id === editingTicketId.value)
  if (t) {
    t.nombre = nuevoNombre
    t.precio = nuevoPrecio
  }
}

const confirmarActualizacionPasadas = async (actualizarRegistradas) => {
  procesandoActualizacionMasiva.value = true
  const original = ticketEnEdicionOriginal.value
  const nuevoNombre = editTicketForm.value.nombre.trim()
  const nuevoPrecio = parseFloat(editTicketForm.value.precio).toFixed(2)

  try {
    if (actualizarRegistradas && inscripcionesDocsAfectados.value.length > 0) {
      // Actualizar en lotes (batch) de Firestore usando doc(db, 'inscripciones', id) para asegurar la misma instancia
      const batch = writeBatch(db)
      const ahora = new Date().toISOString()
      const usuarioActualEmail = auth.currentUser?.email || auth.currentUser?.displayName || 'Administrador'

      inscripcionesDocsAfectados.value.forEach(docSnap => {
        const data = docSnap.data()
        const p = data.participante || {}
        const qty = Number(p.ticketQuantity) || 1
        const nuevoTotal = (parseFloat(nuevoPrecio) * qty).toFixed(2)
        const docRef = doc(db, 'inscripciones', docSnap.id)

        batch.update(docRef, {
          'participante.ticketTypeId': original.id,
          'participante.ticketType': nuevoNombre,
          'participante.ticketPrice': Number(nuevoPrecio),
          'participante.totalPrice': nuevoTotal,
          'participante.montoPagado': nuevoTotal,
          'participante.monto': nuevoTotal,
          'editadoPor': usuarioActualEmail,
          'fechaEdicion': ahora,
          'ultimaModificacion': {
            por: usuarioActualEmail,
            fecha: ahora
          }
        })
      })
      await batch.commit()
    }

    aplicarCambioBoletoLocal(nuevoNombre, nuevoPrecio)
  } catch (e) {
    console.error('Error al realizar actualización masiva:', e)
    alert('Ocurrió un error al actualizar las inscripciones pasadas.')
  } finally {
    procesandoActualizacionMasiva.value = false
    mostrarModalActualizarPasadas.value = false
    cancelarEdicionBoleto()
  }
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
  if (!localEvent.value.titulo || !localEvent.value.fecha || !localEvent.value.lugar) return

  if (!localEvent.value.ticketTypes || localEvent.value.ticketTypes.length === 0) {
    error.value = 'Agrega al menos un tipo de boleto.'
    return
  }

  error.value = ''
  loading.value = true

  try {
    const maybePromise = emit('save', { eventData: { ...localEvent.value }, imageFile: selectedImage.value })
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
