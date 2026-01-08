<template>
  <div class="min-h-screen bg-gray-50 py-12">
    <div class="container mx-auto px-4 pt-[100px]">
      <div class="max-w-2xl mx-auto">
        <!-- Header -->
        <div class="text-center mb-8 animate-fade-in-up">
          <div class="w-20 h-20 bg-white/10 backdrop-blur-sm rounded-full flex items-center justify-center mx-auto mb-4">
            <i class="fas fa-search text-white text-3xl"></i>
          </div>
          <h1 class="text-4xl font-bold text-indigo-600 mb-3">Verificar Inscripción</h1>
          <p class="text-gray-700 text-lg">Ingresa tu cédula para ver tus datos de registro</p>
        </div>

        <!-- Formulario de búsqueda -->
        <div class="bg-white rounded-2xl shadow-2xl p-8 mb-6 animate-fade-in-up" style="animation-delay: 0.1s">
          <form @submit.prevent="buscarInscripcion" class="space-y-6">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">
                <i class="fas fa-id-card mr-2 text-indigo-600"></i>
                Número de Cédula
              </label>
              <input 
                v-model="cedula"
                type="text" 
                required
                placeholder="Ej: 8-123-4567"
                class="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-800 placeholder-gray-400 transition-all"
              >
              <p class="text-xs text-gray-500 mt-2">Ingresa tu cédula con el formato que usaste al registrarte</p>
            </div>

            <div v-if="eventoId">
              <label class="block text-sm font-semibold text-gray-700 mb-2">
                <i class="fas fa-calendar mr-2 text-indigo-600"></i>
                Evento
              </label>
              <div class="px-4 py-3 bg-indigo-50 border-2 border-indigo-200 rounded-xl text-gray-800">
                {{ eventoTitulo || 'Evento seleccionado' }}
              </div>
            </div>

            <button 
              type="submit"
              :disabled="buscando || !cedula"
              :class="[
                'w-full py-4 rounded-xl font-bold text-white transition-all duration-300 shadow-lg',
                (buscando || !cedula)
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 hover:shadow-xl transform hover:scale-105'
              ]"
            >
              <i :class="['mr-2', buscando ? 'fas fa-spinner fa-spin' : 'fas fa-search']"></i>
              {{ buscando ? 'Buscando...' : 'Buscar Inscripción' }}
            </button>
          </form>
        </div>

        <!-- Resultados -->
        <div v-if="mostrarResultado" class="animate-fade-in-up">
          <!-- Inscripción encontrada -->
          <div v-if="inscripcionEncontrada" class="bg-white rounded-2xl shadow-2xl overflow-hidden">
            <!-- Header de éxito -->
            <div class="bg-gradient-to-r from-green-500 to-emerald-600 p-6 text-center">
              <div class="w-16 h-16 bg-white rounded-full flex items-center justify-center mx-auto mb-3">
                <i class="fas fa-check text-green-500 text-2xl"></i>
              </div>
              <h2 class="text-2xl font-bold text-white mb-1">¡Inscripción Encontrada!</h2>
              <p class="text-green-50">Tu registro está confirmado</p>
            </div>

            <div class="p-8 space-y-6">
              <!-- Código QR -->
              <div v-if="inscripcionEncontrada.registrationToken" class="flex flex-col items-center bg-gray-50 p-6 rounded-xl">
                <h3 class="text-lg font-semibold text-gray-800 mb-4">Tu Boleto Digital</h3>
                <div class="bg-white p-4 rounded-lg shadow-md">
                  <template v-if="qrImageUrl">
                    <img :src="qrImageUrl" alt="QR" class="max-w-full" />
                  </template>
                  <template v-else>
                    <canvas ref="qrCanvas" class="max-w-full"></canvas>
                  </template>
                </div>
                <div class="flex gap-3 mt-4">
                  <button 
                    @click="downloadQR"
                    class="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
                  >
                    <i class="fas fa-download mr-2"></i>Descargar QR
                  </button>
                  <button 
                    @click="mostrarFormularioPago = true"
                    class="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                  >
                    <i class="fas fa-plus-circle mr-2"></i>Hacer Otro Pago
                  </button>
                </div>
              </div>

              <!-- Formulario para otro pago -->
              <div v-if="mostrarFormularioPago" class="bg-blue-50 border-2 border-blue-200 p-6 rounded-xl relative">
                <!-- Overlay de bloqueo mientras se sube -->
                <div v-if="subiendoComprobante" class="absolute inset-0 bg-black bg-opacity-30 rounded-xl flex items-center justify-center z-10">
                  <div class="bg-white rounded-lg p-6 shadow-2xl text-center">
                    <i class="fas fa-spinner fa-spin text-blue-600 text-4xl mb-3"></i>
                    <p class="text-lg font-semibold text-gray-800">Subiendo comprobante...</p>
                    <p class="text-sm text-gray-600 mt-2">Por favor espera</p>
                  </div>
                </div>
                
                <div class="flex justify-between items-center mb-4">
                  <h3 class="text-lg font-semibold text-gray-800">
                    <i class="fas fa-receipt mr-2 text-blue-600"></i>
                    Adjuntar Nuevo Comprobante de Pago
                  </h3>
                  <button 
                    @click="cerrarFormularioPago"
                    :disabled="subiendoComprobante"
                    :class="[
                      'transition-colors',
                      subiendoComprobante ? 'text-gray-300 cursor-not-allowed' : 'text-gray-500 hover:text-gray-700'
                    ]"
                  >
                    <i class="fas fa-times text-xl"></i>
                  </button>
                </div>
                
                <div class="space-y-4">
                  <!-- Campo de monto -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">
                      <i class="fas fa-dollar-sign mr-2 text-green-600"></i>
                      Monto del nuevo pago *
                    </label>
                    <input 
                      v-model.number="montoNuevoPago"
                      type="number" 
                      step="0.01"
                      min="0"
                      required
                      :disabled="subiendoComprobante"
                      placeholder="Ej: 50.00"
                      class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-800 placeholder-gray-400 disabled:bg-gray-100 disabled:cursor-not-allowed"
                    />
                    <p class="text-xs text-gray-500 mt-1">Ingresa el monto del pago adicional</p>
                  </div>

                  <!-- Mostrar total acumulado -->
                  <div class="bg-gradient-to-r from-green-50 to-blue-50 p-4 rounded-lg border border-green-200">
                    <div class="flex justify-between items-center text-sm mb-2">
                      <span class="text-gray-600">Monto actual:</span>
                      <span class="font-semibold text-gray-800">${{ inscripcionEncontrada.totalPrice || 0 }}</span>
                    </div>
                    <div class="flex justify-between items-center text-sm mb-2">
                      <span class="text-gray-600">Nuevo pago:</span>
                      <span class="font-semibold text-blue-600">+${{ montoNuevoPago || 0 }}</span>
                    </div>
                    <div class="border-t border-green-300 pt-2 mt-2">
                      <div class="flex justify-between items-center">
                        <span class="text-gray-800 font-bold">Total acumulado:</span>
                        <span class="text-xl font-bold text-green-600">${{ calcularTotalAcumulado }}</span>
                      </div>
                    </div>
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">
                      <i class="fas fa-image mr-2 text-blue-600"></i>
                      Selecciona el comprobante de pago *
                    </label>
                    <input 
                      type="file" 
                      @change="handleNuevoComprobante"
                      accept="image/*"
                      :multiple="eventoId && (eventosStore.obtenerEventoPorId(eventoId) && eventosStore.obtenerEventoPorId(eventoId).opciones ? eventosStore.obtenerEventoPorId(eventoId).opciones.permitirMultiplesAdjuntos : false)"
                      :disabled="subiendoComprobante"
                      class="w-full px-4 py-2 text-gray-600 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
                    />
                  </div>

                  <!-- Vista previa de la imagen -->
                  <div v-if="previewNuevoComprobante" class="relative">
                    <img :src="previewNuevoComprobante" alt="Preview" class="w-full max-h-64 object-cover rounded-lg" />
                    <button
                      @click="eliminarPreviewComprobante"
                      :disabled="subiendoComprobante"
                      :class="[
                        'absolute top-2 right-2 rounded-full p-2 transition-colors',
                        subiendoComprobante 
                          ? 'bg-gray-400 cursor-not-allowed' 
                          : 'bg-red-500 text-white hover:bg-red-600'
                      ]"
                    >
                      <i class="fas fa-trash text-sm"></i>
                    </button>
                  </div>

                  <button
                    @click="subirNuevoComprobante"
                    :disabled="!nuevoComprobante || !montoNuevoPago || montoNuevoPago <= 0 || subiendoComprobante"
                    class="w-full py-3 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                  >
                    <i v-if="subiendoComprobante" class="fas fa-spinner fa-spin"></i>
                    <span>{{ subiendoComprobante ? 'Subiendo...' : 'Subir Comprobante' }}</span>
                  </button>

                  <p v-if="mensajeComprobante" class="text-sm text-center" :class="mensajeComprobante.tipo === 'success' ? 'text-green-600' : 'text-red-600'">
                    {{ mensajeComprobante.texto }}
                  </p>
                </div>
              </div>

              <!-- Información de la inscripción -->
              <div class="space-y-3">
                <h3 class="text-lg font-semibold text-gray-800 flex items-center">
                  <i class="fas fa-user mr-2 text-indigo-600"></i>
                  Datos de Registro
                </h3>
                <div class="bg-indigo-50 rounded-xl p-5 space-y-3 text-sm">
                  <div class="flex justify-between border-b border-indigo-100 pb-2">
                    <span class="text-gray-600 font-medium">Nombre:</span>
                    <span class="font-bold text-gray-800">{{ inscripcionEncontrada.nombre }}</span>
                  </div>
                  <div class="flex justify-between border-b border-indigo-100 pb-2">
                    <span class="text-gray-600 font-medium">Cédula:</span>
                    <span class="font-bold text-gray-800">{{ inscripcionEncontrada.cedula }}</span>
                  </div>
                  <div class="flex justify-between border-b border-indigo-100 pb-2">
                    <span class="text-gray-600 font-medium">WhatsApp:</span>
                    <span class="font-bold text-gray-800">{{ inscripcionEncontrada.telefono }}</span>
                  </div>
                  <div v-if="inscripcionEncontrada.ticketType" class="flex justify-between border-b border-indigo-100 pb-2">
                    <span class="text-gray-600 font-medium">Tipo de Boleto:</span>
                    <span class="font-bold text-gray-800">{{ inscripcionEncontrada.ticketType }}</span>
                  </div>
                  <div v-if="inscripcionEncontrada.ticketPrice" class="flex justify-between border-b border-indigo-100 pb-2">
                    <span class="text-gray-600 font-medium">Precio Unitario:</span>
                    <span class="font-bold text-gray-600">${{ inscripcionEncontrada.ticketPrice }}</span>
                  </div>
                  <div v-if="inscripcionEncontrada.totalPrice" class="flex justify-between border-b border-indigo-100 pb-2">
                    <span class="text-gray-600 font-medium">Total Pagado:</span>
                    <span class="font-bold text-green-600">${{ Number(inscripcionEncontrada.totalPrice).toFixed(2) }}</span>
                  </div>
                  <div v-if="inscripcionEncontrada.fechaInscripcion" class="flex justify-between">
                    <span class="text-gray-600 font-medium">Fecha de Registro:</span>
                    <span class="font-bold text-gray-800">{{ formatearFecha(inscripcionEncontrada.fechaInscripcion) }}</span>
                  </div>
                </div>
              </div>

              <!-- ID de registro -->
              <div v-if="inscripcionEncontrada.registrationToken" class="bg-gray-100 rounded-xl p-4">
                <p class="text-xs text-gray-600 text-center mb-1">ID de Registro</p>
                <p class="text-sm font-mono text-gray-800 text-center break-all">{{ inscripcionEncontrada.registrationToken }}</p>
              </div>

              <!-- Botón para buscar otra inscripción -->
              <button 
                @click="resetearBusqueda"
                class="w-full py-3 bg-gray-200 text-gray-800 rounded-xl font-semibold hover:bg-gray-300 transition-colors"
              >
                Buscar Otra Inscripción
              </button>
            </div>
          </div>

          <!-- No se encontró inscripción -->
          <div v-else class="bg-white rounded-2xl shadow-2xl p-8 text-center">
            <div class="w-20 h-20 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <i class="fas fa-exclamation-circle text-red-500 text-4xl"></i>
            </div>
            <h2 class="text-2xl font-bold text-gray-800 mb-3">No se encontró inscripción</h2>
            <p class="text-gray-600 mb-6">No hay registros con la cédula <strong>{{ cedula }}</strong>{{ eventoId ? ' para este evento' : '' }}.</p>
            <div class="space-y-3">
              <p class="text-sm text-gray-500">Verifica que:</p>
              <ul class="text-sm text-gray-600 space-y-2 text-left max-w-md mx-auto">
                <li class="flex items-start">
                  <i class="fas fa-check-circle text-green-500 mr-2 mt-1"></i>
                  <span>El número de cédula sea correcto</span>
                </li>
                <li class="flex items-start">
                  <i class="fas fa-check-circle text-green-500 mr-2 mt-1"></i>
                  <span>Hayas completado el proceso de inscripción</span>
                </li>
                <li class="flex items-start">
                  <i class="fas fa-check-circle text-green-500 mr-2 mt-1"></i>
                  <span>El formato de cédula sea el mismo que usaste al registrarte</span>
                </li>
              </ul>
            </div>
            <button 
              @click="resetearBusqueda"
              class="mt-6 px-8 py-3 bg-indigo-600 text-white rounded-xl font-semibold hover:bg-indigo-700 transition-colors"
            >
              Intentar de Nuevo
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useEventosStore } from '../stores/eventos'
import { collection, query, where, getDocs, doc, updateDoc, arrayUnion, increment } from 'firebase/firestore'
import { db, storage } from '../firebase'
import { ref as storageRef, uploadBytes, getDownloadURL } from 'firebase/storage'
import QRCode from 'qrcode'

const route = useRoute()
const eventosStore = useEventosStore()

const cedula = ref('')
const eventoId = ref(null)
const eventoTitulo = ref('')
const buscando = ref(false)
const mostrarResultado = ref(false)
const inscripcionEncontrada = ref(null)
const qrCanvas = ref(null)
const qrImageUrl = ref(null)
const mostrarFormularioPago = ref(false)
const nuevoComprobante = ref(null)
const previewNuevoComprobante = ref(null)
const subiendoComprobante = ref(false)
const mensajeComprobante = ref(null)
const montoNuevoPago = ref(0)

// Computed para calcular el total acumulado
const calcularTotalAcumulado = computed(() => {
  const montoActual = inscripcionEncontrada.value?.totalPrice || 0
  const nuevoMonto = montoNuevoPago.value || 0
  return (Number(montoActual) + Number(nuevoMonto)).toFixed(2)
})

onMounted(async () => {
  // Cargar eventos primero (si la función está disponible)
  if (typeof eventosStore.cargarEventos === 'function') {
    await eventosStore.cargarEventos()
  } else {
    console.warn('eventosStore.cargarEventos is not available')
  }
  
  // Si viene de un evento específico, obtener el ID
  eventoId.value = route.params.eventoId || route.query.eventoId || null
  
  if (eventoId.value) {
      const evento = eventosStore.obtenerEventoPorId(eventoId.value)
    if (evento) {
      eventoTitulo.value = evento.titulo
    }
  }
})

// Watcher: si los eventos se cargan después del montaje, actualizar el título
watch(
  () => eventosStore.eventos,
  (newList) => {
    if (eventoId.value) {
      const evento = eventosStore.obtenerEventoPorId(eventoId.value)
      if (evento) eventoTitulo.value = evento.titulo
    }
  },
  { immediate: true, deep: true }
)

// Watcher: si el route params cambia (por ejemplo refresco o navegación), actualizar eventoId y título
watch(
  () => route.params.eventoId,
  (newId) => {
    eventoId.value = newId || route.query.eventoId || null
    if (eventoId.value) {
      const evento = eventosStore.obtenerEventoPorId(eventoId.value)
      if (evento) eventoTitulo.value = evento.titulo
    } else {
      eventoTitulo.value = ''
    }
  },
  { immediate: true }
)

const buscarInscripcion = async () => {
  if (!cedula.value) return
  
  buscando.value = true
  mostrarResultado.value = false
  inscripcionEncontrada.value = null

  try {
    // Buscar en Firestore
    const inscripcionesRef = collection(db, 'inscripciones')
    let q

    if (eventoId.value) {
      // Buscar por cédula y evento específico
      q = query(
        inscripcionesRef,
        where('participante.cedula', '==', cedula.value.trim()),
        where('eventoId', '==', eventoId.value)
      )
    } else {
      // Buscar solo por cédula (todos los eventos)
      q = query(
        inscripcionesRef,
        where('participante.cedula', '==', cedula.value.trim())
      )
    }

    const querySnapshot = await getDocs(q)
    
    if (!querySnapshot.empty) {
      // Tomar la primera inscripción encontrada
      const doc = querySnapshot.docs[0]
      const data = doc.data()
      inscripcionEncontrada.value = {
        id: doc.id,
        ...data.participante,
        eventoId: data.eventoId,
        fechaInscripcion: data.fechaInscripcion
      }

      // Generar QR si hay token
      if (inscripcionEncontrada.value.registrationToken) {
        await nextTick()
        await generateQR()
      }
    }
  } catch (error) {
    console.error('Error buscando inscripción:', error)
  } finally {
    buscando.value = false
    mostrarResultado.value = true
  }
}

const generateQR = async () => {
  if (!inscripcionEncontrada.value || !inscripcionEncontrada.value.registrationToken) return

  const qrData = {
    token: inscripcionEncontrada.value.registrationToken,
    nombre: inscripcionEncontrada.value.nombre,
    cedula: inscripcionEncontrada.value.cedula,
    ticketType: inscripcionEncontrada.value.ticketType,
    eventoId: inscripcionEncontrada.value.eventoId
  }

  // Reset previous QR image
  qrImageUrl.value = null

  // Try rendering to canvas first (faster in DOM). If it fails, fall back to DataURL.
  try {
    if (qrCanvas.value) {
      await QRCode.toCanvas(qrCanvas.value, JSON.stringify(qrData), {
        width: 200,
        margin: 2,
        color: { dark: '#1f2937', light: '#ffffff' }
      })
      return
    }
  } catch (error) {
    console.warn('toCanvas no funcionó, usando fallback toDataURL:', error)
  }

  // Fallback: generate an image DataURL and display as <img>
  try {
    const dataUrl = await QRCode.toDataURL(JSON.stringify(qrData), {
      width: 200,
      margin: 2,
      color: { dark: '#1f2937', light: '#ffffff' }
    })
    qrImageUrl.value = dataUrl
  } catch (err) {
    console.error('Error generando QR toDataURL:', err)
  }
}

const downloadQR = () => {
  const link = document.createElement('a')
  link.download = `boleto-${inscripcionEncontrada.value.registrationToken}.png`

  // Prefer qrImageUrl if available, otherwise use canvas dataURL
  if (qrImageUrl.value) {
    link.href = qrImageUrl.value
  } else if (qrCanvas.value) {
    try {
      link.href = qrCanvas.value.toDataURL()
    } catch (err) {
      console.error('No se pudo obtener dataURL desde canvas:', err)
      return
    }
  } else {
    return
  }

  link.click()
}

const resetearBusqueda = () => {
  cedula.value = ''
  mostrarResultado.value = false
  inscripcionEncontrada.value = null
  cerrarFormularioPago()
}

const handleNuevoComprobante = (event) => {
  const file = event.target.files[0]
  if (file) {
    nuevoComprobante.value = file
    
    // Crear preview
    const reader = new FileReader()
    reader.onload = (e) => {
      previewNuevoComprobante.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

const eliminarPreviewComprobante = () => {
  nuevoComprobante.value = null
  previewNuevoComprobante.value = null
  mensajeComprobante.value = null
}

const cerrarFormularioPago = () => {
  mostrarFormularioPago.value = false
  montoNuevoPago.value = 0
  eliminarPreviewComprobante()
}

const subirNuevoComprobante = async () => {
  if (!nuevoComprobante.value || !inscripcionEncontrada.value || !montoNuevoPago.value || montoNuevoPago.value <= 0) return
  
  subiendoComprobante.value = true
  mensajeComprobante.value = null

  try {
    // Subir imagen a Storage
    const timestamp = Date.now()
    const fileName = `${timestamp}_${nuevoComprobante.value.name}`
    const fileRef = storageRef(storage, `inscripciones/${inscripcionEncontrada.value.eventoId}/${fileName}`)
    
    await uploadBytes(fileRef, nuevoComprobante.value)
    const url = await getDownloadURL(fileRef)

    // Actualizar documento en Firestore
    const inscripcionRef = doc(db, 'inscripciones', inscripcionEncontrada.value.id)
    
    // Calcular el nuevo total
    const montoActual = inscripcionEncontrada.value.totalPrice || 0
    const nuevoTotal = Number(montoActual) + Number(montoNuevoPago.value)
    
    await updateDoc(inscripcionRef, {
      // Agregar comprobante adicional al array
      comprobantesAdicionales: arrayUnion({
        url: url,
        monto: Number(montoNuevoPago.value),
        fecha: new Date().toISOString()
      }),
      // Actualizar el total sumando el nuevo monto
      'participante.totalPrice': nuevoTotal
    })

    // Actualizar la información local para reflejar el cambio
    inscripcionEncontrada.value.totalPrice = nuevoTotal

    mensajeComprobante.value = {
      tipo: 'success',
      texto: `¡Comprobante subido exitosamente! Total actualizado: $${nuevoTotal.toFixed(2)}`
    }

    // Limpiar formulario después de 2 segundos
    setTimeout(() => {
      cerrarFormularioPago()
    }, 2000)

  } catch (error) {
    console.error('Error subiendo comprobante:', error)
    mensajeComprobante.value = {
      tipo: 'error',
      texto: 'Error al subir el comprobante. Intenta de nuevo.'
    }
  } finally {
    subiendoComprobante.value = false
  }
}

const formatearFecha = (fechaISO) => {
  if (!fechaISO) return ''
  return new Date(fechaISO).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
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
  animation: fade-in-up 0.6s ease-out;
}
</style>
