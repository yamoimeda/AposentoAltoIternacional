<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="container mx-auto px-4 pt-[80px]">
      <div v-if="evento" class="max-w-4xl mx-auto">
        <!-- Información del evento -->
        <div class="bg-white rounded-lg shadow-lg overflow-hidden mb-8">
          <img  v-if="evento.bannerUrl || evento.imagen"
            :src="evento.bannerUrl || evento.imagen || ''" 
            :alt="evento.titulo"
            class="w-full h-64 object-cover"
          >
          <div class="p-6">
            <h1 class="text-3xl font-bold text-gray-800 mb-4">{{ evento.titulo }}</h1>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              <div class="flex items-center text-gray-700">
                <i class="fas fa-calendar mr-3 text-blue-600"></i>
                {{ formatearFecha(evento.fecha) }}
              </div>
              <div class="flex items-center text-gray-700">
                <i class="fas fa-map-marker-alt mr-3 text-blue-600"></i>
                {{ evento.lugar }}
              </div>
              
            </div>
            <p class="text-gray-600 whitespace-pre-line">{{ evento.descripcion }}</p>
            

            <!-- Cantidad y total -->
            <!-- <div v-if="ticketTypes.length" class="mt-4 flex items-center gap-4">
              <div class="w-40">
                <label class="block text-sm font-medium text-gray-700 mb-2">Cantidad</label>
                <input type="number" min="1" v-model.number="ticketQuantity" class="w-full px-3 py-2 border border-gray-300 rounded-lg" />
              </div>
              <div class="flex-1">
                <label class="block text-sm font-medium text-gray-700 mb-2">Total estimado</label>
                <div class="text-xl font-bold text-gray-800">${{ totalPrice }}</div>
              </div>
            </div> -->

            <!-- Información de pago -->
            <div class="bg-blue-50 p-6 rounded-lg mt-6">
              <h3 class="text-xl font-semibold text-gray-800 mb-4">
                <i class="fas fa-credit-card mr-2 text-blue-600"></i>
                Información de Pago
              </h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-700">
                <!--<div>
                   <strong>Yappy:</strong> 6305-1268<br>
                  <strong>ACH:</strong> Banco General - 04-99-99-999999-9
                </div>
                <div>
                  <strong>Concepto:</strong> Inscripción {{ evento.titulo }}<br>
                </div> -->
                <div v-if="evento.formaPago" class="text-sm text-gray-700 whitespace-pre-line">
                  {{ evento.formaPago }}
                </div>
              </div>
            </div>

            <div v-if="evento.opciones.adjuntoRequerido" class="bg-gray-50 p-6 rounded-lg mt-6">
              <h3 class="text-xl font-semibold text-gray-800 mb-4">
                <i class="fas fa-info-circle mr-2 text-blue-600"></i>
                Información Importante
              </h3>
              <ul class="space-y-2 text-gray-700">
                <li class="flex items-start">
                  <i class="fas fa-check text-green-500 mr-2 mt-1"></i>
                  <span>Realiza el pago antes de completar la inscripción</span>
                </li>
                <li class="flex items-start">
                  <i class="fas fa-check text-green-500 mr-2 mt-1"></i>
                  <span>Adjunta la captura de pantalla del pago</span>
                </li>
                <li class="flex items-start">
                  <i class="fas fa-times text-red-500 mr-2 mt-1"></i>
                  <span>Los boletos no son reembolsables</span>
                </li>
              </ul>
            </div>
            <div v-else class="bg-gray-50 p-6 rounded-lg mt-6">
              <h3 class="text-xl font-semibold text-gray-800 mb-4">
                <i class="fas fa-info-circle mr-2 text-blue-600"></i>
                Información Importante
              </h3>
              <ul class="space-y-2 text-gray-700">
                <li class="flex items-start">
                  <i class="fas fa-check text-green-500 mr-2 mt-1"></i>
                  <span>Puede completar la inscripción sin previo abono.</span>
                </li>
                <li class="flex items-start">
                  <i class="fas fa-check text-green-500 mr-2 mt-1"></i>
                  <span>Al completar esta inscripción, usted garantiza su participación.</span>
                </li>
                <li class="flex items-start">
                  <i class="fas fa-times text-red-500 mr-2 mt-1"></i>
                  <span>Los boletos no son reembolsables</span>
                </li>
              </ul>
            </div>

            <div class="mt-6">
            <button
              type="button"
              @click="$router.push({ name: 'VerificarInscripcion', params: { eventoId: evento.id } })"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none"
            >
              Verificar Inscripción
            </button>
          </div>
          
          </div>
        </div>

        <!-- Formulario de inscripción -->
        <div v-if="evento.esFuturo" class="bg-white rounded-lg shadow-lg p-6">
          <h2 class="text-2xl font-bold text-gray-800 mb-6">
            <i class="fas fa-user-plus mr-2 text-blue-600"></i>
            Formulario de Inscripción
          </h2>
          

          <form @submit.prevent="enviarInscripcion" class="space-y-6">
            <!-- Información Personal -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Nombre Completo *
                </label>
                <input 
                  v-model="formulario.nombre"
                  type="text" 
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-800 placeholder-gray-400"
                  placeholder="Tu nombre completo"
                >
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Cédula *
                </label>
                                <input 
                                  ref="cedulaInput"
                                  v-model="formulario.cedula"
                                  type="text" 
                                  required
                                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-800 placeholder-gray-400"
                                  placeholder="con guiones ejemplo 0-123-4567"
                                  @input="cedulaError = ''"
                                >
                <p v-if="cedulaError" class="text-sm text-red-600 mt-2">{{ cedulaError }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  whatsapp *
                </label>
                <input 
                  v-model="formulario.telefono"
                  type="tel" 
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-800 placeholder-gray-400"
                  placeholder="+507 6305-1268"
                >
              </div>
              <!-- Dropdowns condicionados por opciones del evento -->
              <div v-if="evento && evento.opciones && evento.opciones.habilitarIglesia">
                <label class="block text-sm font-medium text-gray-700 mb-2">Iglesia *</label>
                <select v-model="formulario.iglesia" required class="w-full px-3 py-2 border border-gray-300 rounded-lg text-gray-800 placeholder-gray-400">
                  <option value="">Selecciona una iglesia</option>
                  <option v-for="(i, idx) in iglesias" :key="idx" :value="i">{{ i }}</option>
                </select>
              </div>

              <div v-if="evento && evento.opciones && evento.opciones.habilitarMentor && formulario.iglesia === 'Panamá'">
                <label class="block text-sm font-medium text-gray-700 mb-2">Mentor *</label>
                <select v-model="formulario.mentor" required class="w-full px-3 py-2 border border-gray-300 rounded-lg text-gray-800 placeholder-gray-400">
                  <option value="">Selecciona un mentor</option>
                  <option v-for="(m, idx) in mentores" :key="idx" :value="m">{{ m }}</option>
                </select>
              </div>
              <!-- Edad, Correo y Nota condicionales -->
              <div v-if="evento && evento.opciones && evento.opciones.habilitarEdad">
                <label  class="block text-sm font-medium text-gray-700 mb-2">Edad *</label>
                <input required v-model="formulario.edad" type="number" min="1" max="120" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-800 placeholder-gray-400" placeholder="Ej: 30" />
              </div>

              <div v-if="evento && evento.opciones && evento.opciones.habilitarCorreo">
                <label class="block text-sm font-medium text-gray-700 mb-2">Correo electrónico *</label>
                <input required v-model="formulario.correo" type="email" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-800 placeholder-gray-400" placeholder="tu@correo.com" />
              </div>

              <div v-if="evento && evento.opciones && evento.opciones.habilitarNota">
                <label class="block text-sm font-medium text-gray-700 mb-2">Nota (opcional)</label>
                <textarea v-model="formulario.nota" rows="3" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-800 placeholder-gray-400" placeholder="Alguna nota o información adicional..."></textarea>
              </div>
              <!-- <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Edad
                </label>
                <input 
                  v-model="formulario.edad"
                  type="number" 
                  min="1" 
                  max="120"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="25"
                >
              </div> -->
            </div>
            <!-- Selector de tipo de boleto -->
           <div class="border-t pt-6">
            
              <h3 class="text-md font-semibold text-gray-800 mb-4">
                Selecciona tipo de boleto * 
              </h3>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                <label v-for="(t, idx) in evento.ticketTypes" :key="t.nombre + '-' + idx" class="flex items-center p-3 border rounded cursor-pointer text-gray-700" :class="selectedTicketIndex === idx ? 'border-blue-500 bg-blue-50' : ''">
                  <input type="radio" :value="idx" v-model="selectedTicketIndex" class="mr-3" />
                  <div>
                    <div class="font-semibold">{{ t.nombre }}</div>
                    <div class="text-sm text-gray-600">${{ t.precio }}</div>
                  </div>
                </label>
              </div>
            </div>
            <!-- Comprobante de Pago -->
            <div class="border-t pt-6">
              <h3 class="text-md font-semibold text-gray-800 mb-4">
                <i class="fas fa-receipt mr-2 text-green-500"></i>
                Comprobante de Pago {{ evento.opciones.adjuntoRequerido ? '*' : '(puede inscribirse sin pago)' }}
              </h3>
              
              <div class="space-y-4">
                <!-- Upload de imagen -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Adjuntar archivo(s)
                  </label>
                  <div class="flex items-center justify-center w-full">
                    <label 
                      for="comprobante-upload"
                      :class="[
                        'flex flex-col items-center justify-center w-full h-32 border-2 border-dashed rounded-lg cursor-pointer transition-colors',
                        formulario.comprobante && formulario.comprobante.length ? 'border-green-300 bg-green-50' : 'border-gray-300 bg-gray-50 hover:bg-gray-100'
                      ]"
                    >
                      <div class="flex flex-col items-center justify-center pt-5 pb-6">
                        <i :class="['text-3xl mb-2', formulario.comprobante && formulario.comprobante.length ? 'fas fa-check-circle text-green-500' : 'fas fa-cloud-upload-alt text-gray-400']"></i>
                        <p class="mb-2 text-sm text-gray-500">
                          <span class="font-semibold">
                          {{ formulario.comprobante && formulario.comprobante.length ? 'Archivo(s) cargado(s)' : 'Click para subir' }}
                          </span> 
                          {{ !(formulario.comprobante && formulario.comprobante.length) ? 'o arrastra y suelta' : '' }}
                        </p>
                        <p class="text-xs text-gray-500">PNG, JPG o JPEG (MAX. 5MB cada uno)</p>
                      </div>
                      <input 
                        id="comprobante-upload" 
                        type="file" 
                        class="hidden" 
                        accept="image/*"
                        :required="evento.opciones.adjuntoRequerido ?? false "
                        :multiple="evento.opciones.permitirMultiplesAdjuntos ?? false"
                        @change="manejarArchivo"
                      />
                    </label>
                  </div>
                </div>

                <!-- Preview de la imagen -->
                <div v-if="formulario.comprobante && formulario.comprobante.length" class="relative space-y-2">
                  <div v-for="(f, i) in formulario.comprobante" :key="i" class="p-2 border rounded-lg bg-white flex items-center gap-3">
                    <img :src="previews[i]" alt="Preview del comprobante" class="w-20 h-20 object-cover rounded" />
                    <div class="flex-1 text-sm text-gray-700">{{ f.name }} <div class="text-xs text-gray-500">{{ (f.size/1024/1024).toFixed(2) }} MB</div></div>
                    <button type="button" @click="eliminarArchivo(i)" class="bg-red-500 text-white rounded px-2 py-1 text-xs">Eliminar</button>
                  </div>
                </div>

                <!-- OCR deshabilitado: ingresar monto manualmente -->
                <div class="bg-green-50 p-4 rounded-lg" v-if="evento.opciones.adjuntoRequerido || formulario.comprobante && formulario.comprobante.length">
                  <h4 class="font-semibold text-green-800 mb-2">
                    <!-- <i class="fas fa-robot mr-2"></i> -->
                    Información del comprobante
                  </h4>
                  <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm items-start">
                    <div>
                      <label class="block text-green-700 font-medium">Monto (USD):</label>
                      <input required type="number" step="0.01" min="0" v-model="formulario.monto" class="mt-1 block w-40 px-3 py-2 border rounded text-gray-800 placeholder-gray-400" />
                      <p class="text-xs text-gray-600 mt-1">Ingresa el monto pagado manualmente.</p>
                    </div>
                    <!-- <div v-if="datosExtraidos.fecha">
                      <label class="block text-green-700 font-medium">Fecha:</label>
                      <span class="block p-2 rounded border bg-green-100 border-green-300  text-gray-800">
                        {{ datosExtraidos.fecha }}
                      </span>
                    </div>
                    <div v-if="datosExtraidos.confirmacion">
                      <label class="block text-green-700 font-medium">Confirmación:</label>
                      <span class="block p-2 rounded border bg-green-100 border-green-300  text-gray-800">
                        {{ datosExtraidos.confirmacion }}
                      </span>
                    </div> -->
                  </div>

                  <!-- Estado de validación -->
                  <div class="mt-4 p-3 rounded-lg" :class="pagoValido ? 'bg-green-100 border border-green-300' : 'bg-yellow-100 border border-yellow-300'">
                    <div class="flex items-center">
                      <i :class="['mr-2', pagoValido ? 'fas fa-check-circle text-green-500' : 'fas fa-exclamation-triangle text-yellow-500']"></i>
                      <span :class="pagoValido ? 'text-green-700' : 'text-yellow-700'">
                        {{ pagoValido ? 'Pago verificado correctamente' : 'Verifica que el monto sea correcto' }}
                      </span>
                    </div>
                  </div>
                </div>

                <!-- Error en OCR -->
                <div v-if="errorOCR" class="bg-red-50 p-4 rounded-lg">
                  <div class="flex items-center">
                    <i class="fas fa-exclamation-triangle text-red-500 mr-2"></i>
                    <span class="text-red-700">{{ errorOCR }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Botones -->
            <div class="flex gap-4 pt-6">
              <button 
                type="button"
                @click="$router.go(-1)"
                class="flex-1 px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-semibold"
              >
                <i class="fas fa-arrow-left mr-2"></i>
                Volver
              </button>
              <button 
                type="submit"
                :disabled="procesando || ((evento && evento.opciones && evento.opciones.adjuntoRequerido) ? !(formulario.comprobante && formulario.comprobante.length) : false)"
                :class="[
                  'flex-1 px-6 py-3 rounded-lg font-semibold transition-colors',
                  (procesando || ((evento && evento.opciones && evento.opciones.adjuntoRequerido) ? !(formulario.comprobante && formulario.comprobante.length) : false)) 
                    ? 'bg-gray-400 cursor-not-allowed' 
                    : 'bg-blue-600 hover:bg-blue-700',
                  'text-white'
                ]"
              >
                <i :class="['mr-2', procesando ? 'fas fa-spinner fa-spin' : 'fas fa-paper-plane']"></i>
                {{ procesando ? 'Enviando...' : 'Confirmar Inscripción' }}
              </button>
            </div>
          </form>
        </div>
        <div v-else class="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
          <h3 class="text-lg font-semibold text-gray-800 mb-2">Inscripciones cerradas</h3>
          <p class="text-sm text-gray-700">Este evento no está activo para inscripciones en este momento.</p>
        </div>
      </div>

      <!-- Loading state -->
      <div v-else class="flex justify-center items-center py-16">
        <i class="fas fa-spinner fa-spin text-4xl text-blue-600"></i>
      </div>
    </div>

    <!-- Modal de éxito con QR -->
    <RegistrationSuccessModal 
      :show="showSuccessModal" 
      :registrationData="registrationResult || {}" 
      @close="showSuccessModal = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useEventosStore } from '../stores/eventos'
import { v4 as uuidv4 } from 'uuid'
import RegistrationSuccessModal from '../components/RegistrationSuccessModal.vue'
import { collection, query, where, getDocs, doc, getDoc } from 'firebase/firestore'
import { db } from '../firebase'

const route = useRoute()
const router = useRouter()
const eventosStore = useEventosStore()

const procesando = ref(false)
const procesandoOCR = ref(false)
const errorOCR = ref('')
const previewUrl = ref('')
const previews = ref([])
const showSuccessModal = ref(false)
const registrationResult = ref(null)

const formulario = ref({
  nombre: '',
  cedula: '',
  telefono: '',
  edad: '',
  correo: '',
  nota: '',
  monto:0,
  comprobante: []
})

const cedulaError = ref('')
const cedulaInput = ref(null)

const selectedTicketIndex = ref(null)
const ticketTypes = ref([])
const ticketQuantity = ref(1)

const datosExtraidos = ref({
  monto: '',
  fecha: '',
  confirmacion: ''
})

const iglesias = ref([])
const mentores = ref([])

const evento = computed(() => {
  return eventosStore.obtenerEventoPorId(route.params.id)
})

// Cuando el evento cambie, inicializar la selección de ticket si existen tipos
watch(evento, (ev) => {
  // Mantener una copia local de los tipos de ticket para evitar mutaciones directas
  ticketTypes.value = ev && ev.ticketTypes ? [...ev.ticketTypes] : []

  if (ev && ticketTypes.value.length > 0) {
    // seleccionar el primero por defecto si no hay selección
    if (selectedTicketIndex.value === null) selectedTicketIndex.value = 0
  } else {
    selectedTicketIndex.value = null
    ticketQuantity.value = 1
  }
})

const selectedTicket = computed(() => {
  if (!evento.value) return null
  const types = ticketTypes.value || []
  if (types.length === 0 || selectedTicketIndex.value === null) return null
  return types[selectedTicketIndex.value]
})

const selectedTicketPrice = computed(() => {
  const priceFromTicket = selectedTicket.value ? selectedTicket.value.precio : null
  const p = priceFromTicket ?? evento.value?.precio ?? 0
  const parsed = parseFloat(p)
  return isNaN(parsed) ? 0 : parsed
})

const totalPrice = computed(() => {
  const qty = Number(ticketQuantity.value) || 1
  return (selectedTicketPrice.value * qty).toFixed(2)
})

const pagoValido = computed(() => {
  if (!datosExtraidos.value.monto) return false
  return validarMonto(datosExtraidos.value.monto) && validarFecha(datosExtraidos.value.fecha)
})

const parseDateLocal = (fecha) => {
  if (!fecha) return new Date(NaN)
  if (fecha instanceof Date) return fecha
  if (typeof fecha === 'string') {
    if (fecha.includes('T') || fecha.includes(' ')) return new Date(fecha)
    const parts = fecha.split('-')
    if (parts.length === 3) {
      const y = Number(parts[0])
      const m = Number(parts[1]) - 1
      const d = Number(parts[2])
      return new Date(y, m, d)
    }
  }
  return new Date(fecha)
}

const formatearFecha = (fecha) => {
  return parseDateLocal(fecha).toLocaleDateString('es-ES', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const manejarArchivo = async (event) => {
  const files = Array.from(event.target.files || [])
  if (!files.length) return

  // Decide append vs replace based on event option
  const permitirMultiples = evento.value && evento.value.opciones ? !!evento.value.opciones.permitirMultiplesAdjuntos : false

  // If not allowing multiples, take only the first valid file and replace existing
  if (!permitirMultiples) {
    const archivo = files[0]
    if (!archivo) return
    if (!archivo.type.startsWith('image/')) {
      alert('Por favor selecciona una imagen válida')
      return
    }
    if (archivo.size > 5 * 1024 * 1024) {
      alert(`El archivo ${archivo.name} supera el límite de 5MB y fue omitido.`)
      return
    }

    // Replace existing single file
    formulario.value.comprobante = [archivo]
    previews.value = []
    const reader = new FileReader()
    reader.onload = (e) => {
      previews.value.push(e.target.result)
    }
    reader.readAsDataURL(archivo)
    return
  }

  // If multiple allowed, append valid files
  for (const archivo of files) {
    if (!archivo.type.startsWith('image/')) {
      alert('Por favor selecciona solo imágenes válidas')
      continue
    }
    if (archivo.size > 5 * 1024 * 1024) {
      alert(`El archivo ${archivo.name} supera el límite de 5MB y fue omitido.`)
      continue
    }
    formulario.value.comprobante.push(archivo)
    const reader = new FileReader()
    reader.onload = (e) => {
      previews.value.push(e.target.result)
    }
    reader.readAsDataURL(archivo)
  }
}

const eliminarArchivo = (index) => {
  if (typeof index === 'number') {
    formulario.value.comprobante.splice(index, 1)
    previews.value.splice(index, 1)
  } else {
    formulario.value.comprobante = []
    previews.value = []
  }
  datosExtraidos.value = { monto: '', fecha: '', confirmacion: '' }
  errorOCR.value = ''
}

/*
const procesarOCR = async (archivo) => {
  // OCR temporalmente deshabilitado; si necesitas reactivar, descomenta
  // procesandoOCR.value = true
  // errorOCR.value = ''
  // datosExtraidos.value = { monto: '', fecha: '', confirmacion: '' }
  // try {
  //   if (window.Tesseract) {
  //     const { data: { text } } = await window.Tesseract.recognize(archivo, 'spa', { logger: m => console.log(m) })
  //     extraerDatos(text)
  //   } else {
  //     await simularOCR()
  //   }
  // } catch (error) {
  //   console.error('Error en OCR:', error)
  //   errorOCR.value = 'Error al procesar la imagen.'
  // } finally {
  //   procesandoOCR.value = false
  // }
}
*/

/*
const simularOCR = async () => {
  // Simular delay de procesamiento (deshabilitado)
  await new Promise(resolve => setTimeout(resolve, 200))
  datosExtraidos.value = {
    monto: '',
    fecha: '',
    confirmacion: ''
  }
}
*/

/*
const extraerDatos = (texto) => {
  // Lógica OCR deshabilitada. Si se reactiva, parsear texto aquí y asignar a datosExtraidos
}
*/

const validarMonto = (monto) => {
  if (!monto || !evento.value) return false
  const montoNumerico = parseFloat(monto)
  const precioEsperado = selectedTicketPrice.value || parseFloat(evento.value.precio || 0)
  return Math.abs(montoNumerico - precioEsperado) < 0.01 // Tolerancia de 1 centavo
}

const validarFecha = (fecha) => {
  if (!fecha) return true // La fecha es opcional para validación
  
  // Verificar que la fecha sea reciente (últimos 7 días)
  const fechaPago = parseDateLocal(fecha)
  const fechaActual = new Date()
  const diferenciaDias = (fechaActual - fechaPago) / (1000 * 60 * 60 * 24)
  
  return diferenciaDias >= 0 && diferenciaDias <= 7
}

const enviarInscripcion = async () => {
  procesando.value = true

  try {
    // Si hay tipos de boletos, asegurar que se haya seleccionado uno
    if (ticketTypes.value && ticketTypes.value.length && selectedTicketIndex.value === null) {
      alert('Por favor selecciona un tipo de boleto antes de continuar.')
      procesando.value = false
      return
    }

    // Validar cantidad
    const qty = Number(ticketQuantity.value) || 0
    if (qty < 1) {
      alert('La cantidad debe ser al menos 1')
      procesando.value = false
      return
    }

    // Preparar datos para envío
    const formData = new FormData()
    formData.append('nombre', formulario.value.nombre)
    formData.append('cedula', formulario.value.cedula)
    formData.append('telefono', formulario.value.telefono)
    formData.append('edad', formulario.value.edad)
    // Attach comprobante files (if any)
    if (formulario.value.comprobante && formulario.value.comprobante.length) {
      formulario.value.comprobante.forEach((f, idx) => {
        formData.append('comprobante_' + idx, f)
      })
    }
    formData.append('datosOCR', JSON.stringify(datosExtraidos.value))
    formData.append('eventoId', evento.value.id)

    // incluir info de ticket seleccionado
    if (selectedTicket.value) {
      formData.append('ticketType', selectedTicket.value.nombre)
      formData.append('ticketPrice', selectedTicket.value.precio)
      formData.append('ticketQuantity', String(ticketQuantity.value))
      formData.append('totalPrice', String(totalPrice.value))
    } else {
      formData.append('ticketType', 'General')
      formData.append('ticketPrice', evento.value.precio || '')
      formData.append('ticketQuantity', String(ticketQuantity.value))
      formData.append('totalPrice', String(totalPrice.value))
    }

    // Calcular total numérico para guardar
    const numericTotal = parseFloat(totalPrice.value) || (selectedTicketPrice.value * qty)

    // Generar token único de registro
    const registrationToken = uuidv4()

    // Simular envío / espera
    await new Promise(resolve => setTimeout(resolve, 2000))

    // Preparar datos de registro (sin incluir el archivo directamente)
    const registrationData = {
      nombre: formulario.value.nombre,
      cedula: formulario.value.cedula,
      telefono: formulario.value.telefono,
      edad: formulario.value.edad,
      correo: formulario.value.correo || null,
      nota: formulario.value.nota || null,
      comprobante: formulario.value.comprobante && formulario.value.comprobante.length ? [...formulario.value.comprobante] : null, // Se pasará al store para ser subido
      iglesia: formulario.value.iglesia || null,
      mentor: formulario.value.mentor || null,
      monto: formulario.value.monto,
      ticketType: selectedTicket.value ? selectedTicket.value.nombre : 'General',
      ticketPrice: selectedTicket.value ? Number(selectedTicket.value.precio) : Number(evento.value.precio) || 0,
      ticketQuantity: qty,
      totalPrice: formulario.value.monto,
      fechaInscripcion: new Date().toISOString(),
      registrationToken: registrationToken,
      eventoId: evento.value.id,
      eventoTitulo: evento.value.titulo
    }

    // Normalizar cédula: trim y mayúsculas para evitar duplicados por formato
    const cedulaNormalizada = String(registrationData.cedula || '').trim().toUpperCase()
    registrationData.cedula = cedulaNormalizada

    // Verificar si ya existe una inscripción con la misma cédula para este evento
    try {
      const inscripcionesRef = collection(db, 'inscripciones')
      const q = query(inscripcionesRef, where('participante.cedula', '==', cedulaNormalizada), where('eventoId', '==', evento.value.id))
      const snapshot = await getDocs(q)
      if (!snapshot.empty) {
        cedulaError.value = 'Ya existe una inscripción con esa cédula para este evento.'
        await nextTick()
        if (cedulaInput.value && cedulaInput.value.scrollIntoView) {
          cedulaInput.value.scrollIntoView({ behavior: 'smooth', block: 'center' })
        }
        if (cedulaInput.value && cedulaInput.value.focus) cedulaInput.value.focus()
        procesando.value = false
        return
      }
    } catch (e) {
      console.error('Error comprobando duplicados:', e)
      cedulaError.value = 'No se pudo verificar si la cédula está registrada. Intenta nuevamente más tarde.'
      await nextTick()
      if (cedulaInput.value && cedulaInput.value.scrollIntoView) {
        cedulaInput.value.scrollIntoView({ behavior: 'smooth', block: 'center' })
      }
      if (cedulaInput.value && cedulaInput.value.focus) cedulaInput.value.focus()
      procesando.value = false
      return
    }

    // Agregar inscripción al store
    await eventosStore.inscribirParticipante(evento.value.id, registrationData)

    // Preparar datos para el modal
    registrationResult.value = {
      nombre: formulario.value.nombre,
      cedula: formulario.value.cedula,
      telefono: formulario.value.telefono,
      ticketType: registrationData.ticketType,
      ticketPrice: registrationData.ticketPrice,
      registrationToken: registrationToken,
      eventoId: evento.value.id,
      eventoTitulo: evento.value.titulo,
      monto: formulario.value.monto
    }

    // Mostrar modal de éxito
    showSuccessModal.value = true

    // Reset formulario y selección
    formulario.value = {
      nombre: '',
      cedula: '',
      telefono: '',
      edad: '',
      correo: '',
      nota: '',
      comprobante: []
    }
    previews.value = []
    cedulaError.value = ''
    previewUrl.value = ''
    datosExtraidos.value = { monto: '', fecha: '', confirmacion: '' }
    selectedTicketIndex.value = null
    ticketQuantity.value = 1

  } catch (error) {
    console.error('Error:', error)
    alert('Error al procesar la inscripción. Por favor, inténtalo nuevamente.')
  } finally {
    procesando.value = false
  }
}

onMounted(() => {
  console.log(route.params.id);

  // Cargar Tesseract.js para OCR (opcional)
  // OCR disabled: no cargamos Tesseract automáticamente
  // Cargar configuración de iglesias y mentores desde Firestore
  (async () => {
    try {
      const configRef = doc(db, 'configuracion', 'igelsias')
      const snap = await getDoc(configRef)
      if (snap.exists()) {
        const data = snap.data()
        // Esperamos arrays: data.iglesias y data.mentores
        iglesias.value = Array.isArray(data.nombre) ? data.nombre : []
        mentores.value = Array.isArray(data.mentores) ? data.mentores : []
      }
    } catch (e) {
      console.warn('No se pudo cargar configuracion de iglesias/mentores:', e)
    }
  })()
})
</script>