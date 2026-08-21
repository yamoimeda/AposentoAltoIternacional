<template>
  <div class="min-h-screen bg-slate-900 text-slate-100 font-sans pt-24 pb-16 px-4 sm:px-8">
    <div class="max-w-4xl mx-auto space-y-6">

      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div>
          <div class="flex items-center gap-2 text-xs font-semibold text-indigo-400 uppercase tracking-widest mb-1">
            <i class="fas fa-qrcode"></i>
            <span>Control de Entrada y Asistencia</span>
          </div>
          <h1 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Escáner QR de Boletos
          </h1>
          <p class="text-xs sm:text-sm text-slate-400 mt-0.5">
            Valida los boletos digitales en la puerta y registra la asistencia en tiempo real.
          </p>
        </div>

        <div class="flex items-center gap-2">
          <router-link
            to="/conteo"
            class="py-2 px-3.5 bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-xs rounded-xl border border-slate-700 transition-all flex items-center gap-2"
          >
            <i class="fas fa-chart-pie text-indigo-400"></i>
            <span>Ver Conteo</span>
          </router-link>

          <router-link
            to="/admin"
            class="py-2 px-3.5 bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-xs rounded-xl border border-slate-700 transition-all flex items-center gap-2"
          >
            <i class="fas fa-grip text-indigo-400"></i>
            <span>Panel Admin</span>
          </router-link>
        </div>
      </div>

      <!-- Estado si no tiene permisos -->
      <div v-if="!cargando && !tieneAccesoQR" class="bg-slate-800 p-12 rounded-2xl border border-slate-700 text-center max-w-lg mx-auto space-y-4">
        <div class="w-16 h-16 rounded-2xl bg-rose-500/10 border border-rose-500/20 text-rose-400 flex items-center justify-center text-3xl mx-auto">
          <i class="fas fa-lock"></i>
        </div>
        <h2 class="text-xl font-bold text-white">Acceso Restringido</h2>
        <p class="text-xs text-slate-400 leading-relaxed">
          Esta función de escaneo y control de puerta requiere rol de <strong>Escáner QR</strong> o <strong>Administrador</strong>.
        </p>
        <router-link
          to="/admin"
          class="inline-flex items-center gap-2 py-2.5 px-5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-semibold transition-colors"
        >
          <i class="fas fa-arrow-left"></i>
          <span>Volver al Panel Principal</span>
        </router-link>
      </div>

      <template v-else-if="!cargando">
        <!-- Barra de Resumen en Vivo -->
        <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
          <div class="bg-slate-800/90 p-3.5 rounded-xl border border-slate-700 flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center text-lg">
              <i class="fas fa-users"></i>
            </div>
            <div>
              <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">Total Inscritos</span>
              <span class="text-xl font-extrabold text-white">{{ metricas.total }}</span>
            </div>
          </div>

          <div class="bg-slate-800/90 p-3.5 rounded-xl border border-slate-700 flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-lg">
              <i class="fas fa-circle-check"></i>
            </div>
            <div>
              <span class="text-[10px] font-bold uppercase tracking-wider text-emerald-400 block">Ingresados</span>
              <span class="text-xl font-extrabold text-emerald-400">{{ metricas.ingresados }}</span>
            </div>
          </div>

          <div class="col-span-2 sm:col-span-1 bg-slate-800/90 p-3.5 rounded-xl border border-slate-700 flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-amber-500/20 text-amber-400 flex items-center justify-center text-lg">
              <i class="fas fa-clock"></i>
            </div>
            <div>
              <span class="text-[10px] font-bold uppercase tracking-wider text-amber-400 block">Faltan por Ingresar</span>
              <span class="text-xl font-extrabold text-amber-400">{{ Math.max(0, metricas.total - metricas.ingresados) }}</span>
            </div>
          </div>
        </div>

      <!-- Zona del Escáner y Cámara -->
      <div class="grid grid-cols-1 md:grid-cols-12 gap-6">
        
        <!-- Panel Izquierdo: Cámara / Escáner -->
        <div class="md:col-span-7 space-y-4">
          <div class="bg-slate-800/90 p-4 rounded-2xl border border-slate-700 shadow-xl overflow-hidden">
            
            <div class="flex items-center justify-between mb-3">
              <span class="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full" :class="camaraActiva ? 'bg-emerald-500 animate-pulse' : 'bg-slate-500'"></span>
                {{ camaraActiva ? 'Cámara Activa (Enfoca el QR)' : 'Escáner Desactivado' }}
              </span>

              <div class="flex items-center gap-2">
                <button
                  v-if="camaraActiva"
                  @click="detenerEscaner"
                  class="px-3 py-1 bg-rose-600/80 hover:bg-rose-600 text-white rounded-lg text-xs font-semibold transition-colors cursor-pointer"
                >
                  <i class="fas fa-video-slash mr-1"></i> Apagar
                </button>
                <button
                  v-else
                  @click="iniciarEscaner"
                  class="px-3 py-1 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-xs font-semibold transition-colors cursor-pointer"
                >
                  <i class="fas fa-camera mr-1"></i> Encender Cámara
                </button>
              </div>
            </div>

            <!-- Viewport del Escáner QR HTML5 -->
            <div class="relative bg-black rounded-xl overflow-hidden min-h-[260px] flex items-center justify-center border border-slate-700">
              <div id="qr-reader" class="w-full"></div>

              <div v-if="!camaraActiva" class="text-center p-6 space-y-3">
                <div class="w-16 h-16 rounded-full bg-slate-800 flex items-center justify-center text-slate-500 mx-auto text-2xl">
                  <i class="fas fa-camera"></i>
                </div>
                <p class="text-xs text-slate-400 max-w-xs mx-auto">
                  Presiona el botón para activar la cámara de tu celular o computadora y escanear el boleto.
                </p>
                <button
                  @click="iniciarEscaner"
                  class="py-2.5 px-5 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs rounded-xl shadow-md transition-all cursor-pointer inline-flex items-center gap-2"
                >
                  <i class="fas fa-play"></i>
                  <span>Activar Escáner</span>
                </button>
              </div>
            </div>

            <!-- Entrada Manual por Cédula o Token -->
            <div class="mt-4 pt-4 border-t border-slate-700/60">
              <label class="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
                O buscar manualmente por Cédula o Token:
              </label>
              <form @submit.prevent="buscarManual" class="flex gap-2">
                <input
                  v-model="busquedaManual"
                  type="text"
                  placeholder="Ej: 8-123-4567 o token..."
                  class="flex-1 px-3.5 py-2 bg-slate-900 border border-slate-700 rounded-xl text-white text-xs placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                />
                <button
                  type="submit"
                  :disabled="!busquedaManual.trim() || buscando"
                  class="py-2 px-4 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-semibold text-xs rounded-xl transition-all flex items-center gap-1.5 cursor-pointer"
                >
                  <i :class="['fas', buscando ? 'fa-spinner fa-spin' : 'fa-search']"></i>
                  <span>Buscar</span>
                </button>
              </form>
            </div>

          </div>
        </div>

        <!-- Panel Derecho: Resultado de Validación -->
        <div class="md:col-span-5 space-y-4">
          
          <!-- Estado Inicial / Vacío -->
          <div v-if="!resultadoValidacion && !buscando" class="bg-slate-800/60 border border-dashed border-slate-700 rounded-2xl p-8 text-center text-slate-500">
            <i class="fas fa-ticket text-4xl mb-3 text-slate-600 block"></i>
            <h3 class="text-sm font-bold text-slate-300 mb-1">Esperando Escaneo</h3>
            <p class="text-xs text-slate-400">
              Apunta la cámara al código QR del participante para validar su boleto y estado de pago.
            </p>
          </div>

          <!-- Spinner al procesar -->
          <div v-if="buscando" class="bg-slate-800 p-8 rounded-2xl border border-slate-700 text-center">
            <i class="fas fa-circle-notch fa-spin text-3xl text-indigo-500 mb-2 block mx-auto"></i>
            <p class="text-xs font-semibold text-slate-300">Validando boleto con la base de datos...</p>
          </div>

          <!-- Tarjeta de Boleto Encontrado -->
          <div v-if="resultadoValidacion" class="bg-slate-800 rounded-2xl border border-slate-700 shadow-xl overflow-hidden animate-fade-in-up">
            
            <!-- Banner de Estado -->
            <div
              :class="[
                'p-4 text-white text-center font-bold text-sm flex items-center justify-center gap-2',
                resultadoValidacion.estaPagado ? 'bg-gradient-to-r from-emerald-600 to-teal-600' : 'bg-gradient-to-r from-amber-600 to-orange-600'
              ]"
            >
              <i :class="['fas text-lg', resultadoValidacion.estaPagado ? 'fa-check-circle' : 'fa-clock']"></i>
              <span>{{ resultadoValidacion.estaPagado ? 'Boleto Válido y Pagado' : 'Pago Pendiente / Saldo por Cobrar' }}</span>
            </div>

            <!-- Alerta de Asistencia Previa (si ya ingresó) -->
            <div v-if="resultadoValidacion.asistenciaConfirmada" class="p-3 bg-amber-500/10 border-b border-amber-500/20 text-amber-300 text-xs flex items-center gap-2">
              <i class="fas fa-triangle-exclamation text-amber-400 text-base shrink-0"></i>
              <div>
                <b>¡Este boleto ya fue ingresado previamente!</b>
                <span class="block text-[11px] text-amber-400/80">
                  Hora de ingreso: {{ formatearFecha(resultadoValidacion.fechaIngreso) }}
                </span>
              </div>
            </div>

            <div class="p-5 space-y-4 text-xs">
              <!-- Nombre y Cédula -->
              <div>
                <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400">Participante</span>
                <h2 class="text-lg font-bold text-white leading-tight mt-0.5">
                  {{ resultadoValidacion.nombre }}
                </h2>
                <div class="flex items-center gap-3 text-slate-400 mt-1">
                  <span><i class="fas fa-id-card mr-1 text-indigo-400"></i>{{ resultadoValidacion.cedula }}</span>
                  <span v-if="resultadoValidacion.telefono"><i class="fas fa-phone mr-1 text-indigo-400"></i>{{ resultadoValidacion.telefono }}</span>
                </div>
              </div>

              <!-- Detalles de Iglesia, Mentor y Boleto -->
              <div class="bg-slate-900/80 rounded-xl p-3.5 space-y-2 border border-slate-700/60">
                <div class="flex justify-between">
                  <span class="text-slate-400">Iglesia:</span>
                  <span class="font-semibold text-slate-200">{{ resultadoValidacion.iglesia || 'N/A' }}</span>
                </div>
                <div v-if="resultadoValidacion.mentor" class="flex justify-between">
                  <span class="text-slate-400">Mentor:</span>
                  <span class="font-semibold text-slate-200">{{ resultadoValidacion.mentor }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-slate-400">Tipo de Boleto:</span>
                  <span class="font-semibold text-indigo-300">{{ resultadoValidacion.ticketType || 'Adulto full' }}</span>
                </div>
                <div class="flex justify-between pt-1.5 border-t border-slate-800">
                  <span class="text-slate-400">Total Pagado:</span>
                  <span class="font-bold text-emerald-400">${{ resultadoValidacion.totalPagado.toFixed(2) }}</span>
                </div>
                <div v-if="!resultadoValidacion.estaPagado" class="flex justify-between">
                  <span class="text-amber-400 font-bold">Saldo Pendiente:</span>
                  <span class="font-bold text-amber-400">${{ resultadoValidacion.saldoPendiente.toFixed(2) }}</span>
                </div>
              </div>

              <!-- Botones de Acción de Check-In -->
              <div class="pt-2">
                <button
                  v-if="!resultadoValidacion.asistenciaConfirmada"
                  @click="confirmarCheckIn"
                  :disabled="procesandoCheckIn"
                  class="w-full py-3 bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white font-bold text-sm rounded-xl shadow-lg shadow-emerald-600/20 transition-all flex items-center justify-center gap-2 cursor-pointer"
                >
                  <i :class="['fas', procesandoCheckIn ? 'fa-spinner fa-spin' : 'fa-door-open']"></i>
                  <span>{{ procesandoCheckIn ? 'Registrando...' : 'Confirmar Ingreso (Check-In)' }}</span>
                </button>

                <div v-else class="space-y-2">
                  <div class="p-2.5 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-400 font-bold text-center flex items-center justify-center gap-2">
                    <i class="fas fa-check-double"></i>
                    <span>Ingreso Registrado con Éxito</span>
                  </div>
                  <button
                    @click="resetearEscaneo"
                    class="w-full py-2 bg-slate-700 hover:bg-slate-600 text-slate-200 font-semibold rounded-xl transition-colors cursor-pointer"
                  >
                    Escanear Siguiente Boleto
                  </button>
                </div>
              </div>

            </div>

          </div>

          <!-- Alerta de No Encontrado -->
          <div v-if="errorNoEncontrado" class="bg-rose-900/30 border border-rose-700/60 p-4 rounded-2xl text-center space-y-2">
            <i class="fas fa-circle-xmark text-rose-400 text-2xl"></i>
            <h4 class="text-sm font-bold text-rose-200">Boleto no registrado</h4>
            <p class="text-xs text-rose-300">
              No se encontró ninguna inscripción con los datos escaneados.
            </p>
            <button
              @click="errorNoEncontrado = false"
              class="px-3 py-1 bg-rose-800 hover:bg-rose-700 text-white rounded-lg text-xs font-semibold"
            >
              Intentar de nuevo
            </button>
          </div>

        </div>

      </div>
      </template>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { Html5Qrcode } from 'html5-qrcode'
import { db, auth } from '../firebase'
import { collection, query, where, getDocs, doc, updateDoc } from 'firebase/firestore'
import { useEventosStore } from '../stores/eventos'
import { obtenerRolesUsuario } from '../utils/authRoles'

const router = useRouter()
const eventosStore = useEventosStore()

const cargando = ref(true)
const tieneAccesoQR = ref(false)
let html5QrCode = null
const camaraActiva = ref(false)
const buscando = ref(false)
const busquedaManual = ref('')
const resultadoValidacion = ref(null)
const errorNoEncontrado = ref(false)
const procesandoCheckIn = ref(false)

const metricas = ref({
  total: 0,
  ingresados: 0
})

const cargarMetricas = async () => {
  try {
    const list = await eventosStore.obtenerTodasInscripciones()
    metricas.value.total = list.length
    metricas.value.ingresados = list.filter(i => i.asistenciaConfirmada || i.participante?.asistenciaConfirmada || i.checkIn).length
  } catch (e) {
    console.error('Error metricas:', e)
  }
}

const iniciarEscaner = async () => {
  try {
    if (!html5QrCode) {
      html5QrCode = new Html5Qrcode('qr-reader')
    }

    const config = {
      fps: 10,
      qrbox: { width: 220, height: 220 },
      aspectRatio: 1.0
    }

    await html5QrCode.start(
      { facingMode: 'environment' },
      config,
      onScanSuccess,
      onScanFailure
    )
    camaraActiva.value = true
    errorNoEncontrado.value = false
  } catch (err) {
    console.error('Error al iniciar la cámara:', err)
    alert('No se pudo acceder a la cámara. Asegúrate de otorgar permisos de cámara en tu navegador.')
    camaraActiva.value = false
  }
}

const detenerEscaner = async () => {
  if (html5QrCode && camaraActiva.value) {
    try {
      await html5QrCode.stop()
      camaraActiva.value = false
    } catch (e) {
      console.warn('Error deteniendo scanner:', e)
    }
  }
}

const onScanSuccess = async (decodedText) => {
  if (buscando.value) return
  await procesarCodigo(decodedText)
}

const onScanFailure = (error) => {
  // Ignorar frames sin código QR
}

const procesarCodigo = async (rawCode) => {
  buscando.value = true
  resultadoValidacion.value = null
  errorNoEncontrado.value = false

  try {
    let token = ''
    let cedula = ''

    // Si el QR contiene JSON codificado
    try {
      const parsed = JSON.parse(rawCode)
      token = parsed.token || parsed.registrationToken || ''
      cedula = parsed.cedula || ''
    } catch (e) {
      // Es una cadena de texto simple (cédula o token)
      token = rawCode.trim()
      cedula = rawCode.trim()
    }

    const inscripcionesRef = collection(db, 'inscripciones')
    let docSnap = null

    // 1. Buscar por registrationToken
    if (token) {
      const qToken = query(inscripcionesRef, where('participante.registrationToken', '==', token))
      const snapToken = await getDocs(qToken)
      if (!snapToken.empty) {
        docSnap = snapToken.docs[0]
      }
    }

    // 2. Buscar por cédula
    if (!docSnap && cedula) {
      const qCedula = query(inscripcionesRef, where('participante.cedula', '==', cedula.toUpperCase()))
      const snapCedula = await getDocs(qCedula)
      if (!snapCedula.empty) {
        docSnap = snapCedula.docs[0]
      }
    }

    if (docSnap) {
      const data = docSnap.data()
      const p = data.participante || {}

      const candidatos = [p.montoPagado, p.monto, p.totalPrice, data.montoPagado, data.monto, data.totalPrice]
      let totalPagado = 0
      for (const c of candidatos) {
        if (c !== undefined && c !== null && c !== '') {
          const num = Number(c)
          if (!isNaN(num) && num > 0) {
            totalPagado = num
            break
          }
        }
      }

      const ticketCost = Number(p.ticketPrice || 0)
      const saldoPendiente = Math.max(0, ticketCost - totalPagado)
      const estaPagado = ticketCost === 0 ? true : (totalPagado >= (ticketCost - 0.01))

      resultadoValidacion.value = {
        id: docSnap.id,
        nombre: p.nombre || 'N/A',
        cedula: p.cedula || 'N/A',
        telefono: p.telefono || '',
        iglesia: p.iglesia || '',
        mentor: p.mentor || '',
        ticketType: p.ticketType || 'Adulto full',
        ticketPrice: ticketCost,
        totalPagado: totalPagado,
        saldoPendiente: saldoPendiente,
        estaPagado: estaPagado,
        asistenciaConfirmada: !!(data.asistenciaConfirmada || p.asistenciaConfirmada || data.checkIn),
        fechaIngreso: data.fechaIngreso || p.fechaIngreso || null
      }
    } else {
      errorNoEncontrado.value = true
    }
  } catch (err) {
    console.error('Error buscando boleto:', err)
    errorNoEncontrado.value = true
  } finally {
    buscando.value = false
  }
}

const buscarManual = async () => {
  if (!busquedaManual.value.trim()) return
  await procesarCodigo(busquedaManual.value.trim())
}

const confirmarCheckIn = async () => {
  if (!resultadoValidacion.value) return
  procesandoCheckIn.value = true

  try {
    const ahora = new Date().toISOString()
    const usuarioEmail = auth.currentUser?.email || 'Control Puerta'
    const docRef = doc(db, 'inscripciones', resultadoValidacion.value.id)

    await updateDoc(docRef, {
      asistenciaConfirmada: true,
      checkIn: true,
      fechaIngreso: ahora,
      ingresadoPor: usuarioEmail
    })

    resultadoValidacion.value.asistenciaConfirmada = true
    resultadoValidacion.value.fechaIngreso = ahora
    metricas.value.ingresados++
  } catch (e) {
    console.error('Error al registrar check-in:', e)
    alert('No se pudo registrar el ingreso en la base de datos.')
  } finally {
    procesandoCheckIn.value = false
  }
}

const resetearEscaneo = () => {
  resultadoValidacion.value = null
  busquedaManual.value = ''
  errorNoEncontrado.value = false
}

const formatearFecha = (str) => {
  if (!str) return ''
  try {
    const d = new Date(str)
    return d.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
  } catch (e) {
    return str
  }
}

onMounted(async () => {
  auth.onAuthStateChanged(async (user) => {
    if (!user) {
      router.push('/admin-login')
      return
    }
    const roles = await obtenerRolesUsuario(user)
    if (!roles.includes('qr') && !roles.includes('admin')) {
      tieneAccesoQR.value = false
      cargando.value = false
    } else {
      tieneAccesoQR.value = true
      await cargarMetricas()
      cargando.value = false
    }
  })
})

onUnmounted(() => {
  detenerEscaner()
})
</script>
