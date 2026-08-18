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
            <div class="bg-indigo-50/70 border border-indigo-100 p-4 rounded-xl space-y-3">
              <div class="flex items-center justify-between">
                <label class="block text-xs font-bold text-indigo-900 uppercase tracking-wider">
                  <i class="fas fa-paperclip mr-1 text-indigo-600"></i> Comprobante(s) de Pago
                </label>
                <span v-if="archivosAdjuntos.length > 0" class="text-[11px] font-semibold text-indigo-700 bg-indigo-100/80 px-2 py-0.5 rounded-md">
                  {{ archivosAdjuntos.length }} comprobante(s) registrado(s)
                </span>
              </div>

              <!-- Comprobantes ya guardados -->
              <div v-if="archivosAdjuntos.length > 0">
                <FileViewer :files="archivosAdjuntos" />
              </div>
              <div v-else class="text-xs text-slate-500 italic">
                No hay comprobantes guardados previamente.
              </div>

              <!-- Subida de nuevos comprobantes -->
              <div class="pt-3 border-t border-indigo-200/60">
                <label class="block text-xs font-semibold text-slate-700 mb-1.5 flex items-center justify-between">
                  <span>
                    <i class="fas fa-cloud-arrow-up text-indigo-600 mr-1"></i>
                    Adjuntar Nuevo(s) Comprobante(s)
                  </span>
                  <span class="text-[10px] text-slate-400 font-normal">PNG, JPG, PDF</span>
                </label>

                <div class="flex items-center gap-2">
                  <label class="cursor-pointer px-4 py-2 bg-white border-2 border-dashed border-indigo-300 hover:border-indigo-500 rounded-xl text-xs font-semibold text-indigo-700 hover:bg-indigo-50/50 transition-all flex items-center gap-2 shadow-2xs">
                    <i class="fas fa-plus-circle text-indigo-600"></i>
                    <span>Seleccionar Archivos</span>
                    <input
                      type="file"
                      multiple
                      accept="image/*,application/pdf"
                      class="hidden"
                      @change="handleArchivosNuevos"
                    />
                  </label>
                  <span v-if="archivosNuevos.length" class="text-xs text-indigo-700 font-bold">
                    {{ archivosNuevos.length }} archivo(s) por subir
                  </span>
                </div>

                <!-- Lista de archivos nuevos seleccionados -->
                <div v-if="archivosNuevos.length > 0" class="mt-2.5 space-y-1.5">
                  <div
                    v-for="(file, idx) in archivosNuevos"
                    :key="idx"
                    class="flex items-center justify-between bg-white px-3 py-1.5 rounded-lg border border-slate-200 text-xs shadow-2xs"
                  >
                    <div class="flex items-center gap-2 min-w-0">
                      <i :class="['text-indigo-600', file.type.includes('pdf') ? 'fas fa-file-pdf' : 'fas fa-file-image']"></i>
                      <span class="truncate font-medium text-slate-800">{{ file.name }}</span>
                      <span class="text-[10px] text-slate-400 font-mono">({{ (file.size / 1024).toFixed(0) }} KB)</span>
                    </div>
                    <button
                      type="button"
                      @click="eliminarArchivoNuevo(idx)"
                      class="text-rose-500 hover:text-rose-700 p-1 hover:bg-rose-50 rounded transition-colors ml-2 cursor-pointer"
                      title="Quitar archivo"
                    >
                      <i class="fas fa-times"></i>
                    </button>
                  </div>
                </div>
              </div>
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

                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <!-- Selector de Tipo de Boleto -->
                  <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">Tipo de Boleto</label>
                    <select
                      v-if="ticketsDisponibles.length > 0"
                      :value="formulario.ticketType"
                      @change="onCambioTipoBoleto($event.target.value)"
                      class="w-full px-3.5 py-2 border border-slate-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-slate-800 text-sm bg-white"
                    >
                      <option v-for="t in ticketsDisponibles" :key="t.id || t.nombre" :value="t.nombre">
                        {{ t.nombre }} (${{ Number(t.precio || 0).toFixed(2) }})
                      </option>
                    </select>
                    <input
                      v-else
                      v-model="formulario.ticketType"
                      type="text"
                      class="w-full px-3.5 py-2 border border-slate-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-slate-800 text-sm"
                    />
                  </div>

                  <!-- Precio del Boleto (Solo lectura / Bloqueado) -->
                  <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">
                      Precio del Boleto ($)
                      <span class="text-[10px] text-slate-400 font-normal ml-1">(Fijo)</span>
                    </label>
                    <input
                      :value="Number(formulario.ticketPrice || 0).toFixed(2)"
                      type="text"
                      disabled
                      readonly
                      class="w-full px-3.5 py-2 border border-slate-200 bg-slate-100/80 rounded-xl text-slate-600 text-sm font-bold cursor-not-allowed select-none"
                    />
                  </div>

                  <!-- Total Pagado (Editable) -->
                  <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">Total Pagado ($)</label>
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
import { auth, storage } from '../firebase'
import { ref as storageRef, uploadBytes, getDownloadURL } from 'firebase/storage'
import { useEventosStore } from '../stores/eventos'
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
  evento: {
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

const eventosStore = useEventosStore()
const guardando = ref(false)
const mensaje = ref(null)
const archivosNuevos = ref([])

const usuarioActual = computed(() => {
  return auth.currentUser?.email || auth.currentUser?.displayName || 'Administrador'
})

const handleArchivosNuevos = (event) => {
  const files = Array.from(event.target.files || [])
  for (const f of files) {
    if (f.size > 5 * 1024 * 1024) {
      mensaje.value = { tipo: 'error', texto: `El archivo "${f.name}" supera el límite de 5MB.` }
      continue
    }
    archivosNuevos.value.push(f)
  }
  event.target.value = ''
}

const eliminarArchivoNuevo = (index) => {
  archivosNuevos.value.splice(index, 1)
}

const obtenerEvento = () => {
  if (props.evento) return props.evento
  const evId = props.inscripcion?.eventoId
  if (!evId) return null
  return (
    eventosStore.obtenerEventoPorId(evId) ||
    eventosStore.eventos.find(e => e.id === evId || String(e.id) === String(evId)) ||
    null
  )
}

const obtenerListaTickets = (ev) => {
  if (!ev) return []
  const list = ev.ticketTypes || ev.tickets || []
  if (Array.isArray(list) && list.length > 0) {
    return list.filter(t => t.activo !== false)
  }
  if (ev.precio !== undefined && ev.precio !== null && ev.precio !== '' && !isNaN(Number(ev.precio)) && Number(ev.precio) > 0) {
    return [{ id: 'general', nombre: 'General', precio: Number(ev.precio) }]
  }
  return []
}

const ticketsDisponibles = computed(() => {
  const ev = obtenerEvento()
  return obtenerListaTickets(ev)
})

const onCambioTipoBoleto = (ticketNombre) => {
  formulario.value.ticketType = ticketNombre
  const t = ticketsDisponibles.value.find(tick => tick.nombre === ticketNombre || tick.id === ticketNombre)
  if (t && !isNaN(Number(t.precio))) {
    formulario.value.ticketPrice = Number(t.precio)
  }
}

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

const cargarFormulario = () => {
  if (!props.inscripcion) return
  const p = props.inscripcion.participante || {}
  const i = props.inscripcion
  const candidatos = [
    p.montoPagado,
    p.monto,
    p.totalPrice,
    i.montoPagado,
    i.monto,
    i.totalPrice
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

  let ticketCost = Number(p.ticketPrice || 0)
  const ev = obtenerEvento()
  const tickets = obtenerListaTickets(ev)
  
  if (tickets.length > 0) {
    const t = tickets.find(tick => 
      (p.ticketTypeId && String(tick.id) === String(p.ticketTypeId)) ||
      (p.ticketType && tick.nombre?.trim().toLowerCase() === p.ticketType?.trim().toLowerCase())
    )
    if (t && !isNaN(Number(t.precio)) && Number(t.precio) > 0) {
      ticketCost = Number(t.precio)
    } else if (ticketCost === 0 && Number(tickets[0].precio) > 0) {
      ticketCost = Number(tickets[0].precio)
    }
  }

  if (ticketCost === 0 && ev && !isNaN(Number(ev.precio)) && Number(ev.precio) > 0) {
    ticketCost = Number(ev.precio)
  }

  if (ticketCost === 0 && montoNum > 0) {
    ticketCost = montoNum
  }

  const tipoBoletoActual = p.ticketType || (ticketsDisponibles.value[0]?.nombre || 'General')

  formulario.value = {
    nombre: p.nombre || '',
    cedula: p.cedula || '',
    telefono: p.telefono || '',
    edad: p.edad ?? '',
    correo: p.correo || '',
    nota: p.nota || '',
    iglesia: p.iglesia || '',
    mentor: p.mentor || '',
    ticketType: tipoBoletoActual,
    ticketPrice: ticketCost,
    ticketQuantity: p.ticketQuantity ?? 1,
    totalPrice: montoNum,
    montoPagado: montoNum,
    registrationToken: p.registrationToken || ''
  }
  archivosNuevos.value = []
}

watch([() => props.inscripcion, () => props.show, () => props.evento], () => {
  cargarFormulario()
}, { immediate: true, deep: true })

const cerrar = () => {
  if (!guardando.value) {
    mensaje.value = null
    archivosNuevos.value = []
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

    // 1. Subir archivos nuevos a Storage si existen
    const nuevasUrls = []
    if (archivosNuevos.value.length > 0) {
      mensaje.value = { tipo: 'info', texto: `Subiendo ${archivosNuevos.value.length} comprobante(s)...` }
      const evId = props.inscripcion?.eventoId || 'general'
      for (const file of archivosNuevos.value) {
        const path = `inscripciones/${evId}/${Date.now()}_${file.name}`
        const sRef = storageRef(storage, path)
        await uploadBytes(sRef, file)
        const url = await getDownloadURL(sRef)
        nuevasUrls.push(url)
      }
    }

    // 2. Combinar comprobantes existentes con los recién subidos
    const urlsPrevias = [...archivosAdjuntos.value]
    const todasLasUrls = [...urlsPrevias, ...nuevasUrls]

    // 3. Preservar la estructura completa de `participante` para no borrar campos existentes
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
      ticketPrice: Number(formulario.value.ticketPrice) || 0,
      ticketQuantity: Math.max(1, Number(formulario.value.ticketQuantity) || 1),
      totalPrice: montoFinal,
      montoPagado: montoFinal,
      monto: montoFinal,
      comprobanteUrl: todasLasUrls[0] || null,
      comprobantesUrls: todasLasUrls,
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

    archivosNuevos.value = []

    mensaje.value = {
      tipo: 'success',
      texto: `Cambios guardados exitosamente por ${editor}`
    }

    setTimeout(() => {
      cerrar()
    }, 1200)
  } catch (error) {
    console.error('Error guardando cambios:', error)
    mensaje.value = {
      tipo: 'error',
      texto: 'Error al guardar los cambios o subir comprobantes. Intenta de nuevo.'
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
