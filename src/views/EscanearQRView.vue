<template>
  <div class="min-h-screen bg-slate-900 text-slate-100 font-sans p-2 sm:p-4">
    <div class="max-w-6xl mx-auto space-y-2.5">

      <!-- Header Compacto -->
      <div class="flex items-center justify-between gap-2 pb-2 border-b border-slate-800">
        <div class="flex flex-wrap items-center gap-2 sm:gap-3">
          <h1 class="text-sm sm:text-base font-bold text-white flex items-center gap-1.5">
            <i class="fas fa-qrcode text-indigo-400"></i>
            <span>Escáner QR</span>
          </h1>

          <!-- Conteos Compactos (Solo Inscritos e Ingresados) -->
          <div v-if="tieneAccesoQR && !cargando" class="flex items-center gap-1.5 text-xs">
            <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-slate-800 border border-slate-700 text-slate-300 text-[11px]">
              <i class="fas fa-users text-indigo-400 text-[10px]"></i>
              <span class="text-slate-400">Inscritos:</span>
              <strong class="text-white">{{ metricas.total }}</strong>
            </span>
            <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-slate-800 border border-slate-700 text-emerald-400 text-[11px]">
              <i class="fas fa-door-open text-emerald-400 text-[10px]"></i>
              <span class="text-slate-400">Ingresados:</span>
              <strong class="text-emerald-300">{{ metricas.ingresados }}</strong>
            </span>
          </div>
        </div>

        <!-- Botones de Salida / Conteo -->
        <div class="flex items-center gap-1.5 shrink-0">
          <router-link
            to="/conteo"
            class="py-1 px-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium text-xs rounded-lg border border-slate-700 transition-all flex items-center gap-1 cursor-pointer"
            title="Ver conteo"
          >
            <i class="fas fa-chart-pie text-indigo-400 text-xs"></i>
            <span class="hidden sm:inline">Conteo</span>
          </router-link>
          <router-link
            to="/admin"
            class="py-1 px-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium text-xs rounded-lg border border-slate-700 transition-all flex items-center gap-1 cursor-pointer"
            title="Panel Admin"
          >
            <i class="fas fa-grip text-indigo-400 text-xs"></i>
            <span class="hidden sm:inline">Admin</span>
          </router-link>
        </div>
      </div>

      <!-- Estado si no tiene permisos -->
      <div v-if="!cargando && !tieneAccesoQR" class="bg-slate-800 p-8 rounded-xl border border-slate-700 text-center max-w-md mx-auto space-y-3">
        <div class="w-12 h-12 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 flex items-center justify-center text-2xl mx-auto">
          <i class="fas fa-lock"></i>
        </div>
        <h2 class="text-base font-bold text-white">Acceso Restringido</h2>
        <p class="text-xs text-slate-400 leading-relaxed">
          Esta función requiere rol de <strong>Escáner QR</strong> o <strong>Administrador</strong>.
        </p>
        <router-link
          to="/admin"
          class="inline-flex items-center gap-1.5 py-2 px-4 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-xs font-semibold transition-colors"
        >
          <i class="fas fa-arrow-left"></i>
          <span>Volver al Panel Principal</span>
        </router-link>
      </div>

      <template v-else-if="!cargando">
      <!-- Zona del Escáner y Cámara -->
      <div class="grid grid-cols-1 md:grid-cols-12 gap-2.5 sm:gap-3 items-start">
        
        <!-- Panel Izquierdo: Cámara / Escáner -->
        <div class="md:col-span-5 space-y-2">
          <div class="bg-slate-800/90 p-3 rounded-xl border border-slate-700 shadow-md">
            
            <div class="flex items-center justify-between mb-2">
              <span class="text-[11px] font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                <span class="w-2 h-2 rounded-full" :class="camaraActiva ? 'bg-emerald-500 animate-pulse' : 'bg-slate-500'"></span>
                {{ camaraActiva ? 'Cámara Activa' : 'Escáner Apagado' }}
              </span>

              <div class="flex items-center gap-1.5">
                <button
                  v-if="camaraActiva"
                  @click="detenerEscaner"
                  class="px-2.5 py-0.5 bg-rose-600/80 hover:bg-rose-600 text-white rounded-md text-xs font-semibold transition-colors cursor-pointer"
                >
                  <i class="fas fa-video-slash mr-1"></i> Apagar
                </button>
                <button
                  v-else
                  @click="iniciarEscaner"
                  class="px-2.5 py-0.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-md text-xs font-semibold transition-colors cursor-pointer"
                >
                  <i class="fas fa-camera mr-1"></i> Encender
                </button>
              </div>
            </div>

            <!-- Viewport del Escáner QR HTML5 -->
            <div class="relative bg-black rounded-lg overflow-hidden flex items-center justify-center border border-slate-700 min-h-[160px] sm:min-h-[190px]">
              <div id="qr-reader" class="w-full"></div>

              <div v-if="!camaraActiva" class="text-center p-3 sm:p-4 space-y-2">
                <div class="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center text-slate-500 mx-auto text-base">
                  <i class="fas fa-camera"></i>
                </div>
                <p class="text-[11px] text-slate-400 max-w-xs mx-auto">
                  Activa la cámara para enfocar el código QR del boleto.
                </p>
                <button
                  @click="iniciarEscaner"
                  class="py-1.5 px-3.5 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs rounded-lg shadow transition-all cursor-pointer inline-flex items-center gap-1.5"
                >
                  <i class="fas fa-play text-[10px]"></i>
                  <span>Activar Escáner</span>
                </button>
              </div>
            </div>

            <!-- Entrada Manual por Cédula o Token -->
            <div class="mt-2 pt-2 border-t border-slate-700/60">
              <form @submit.prevent="buscarManual" class="flex gap-1.5">
                <input
                  v-model="busquedaManual"
                  type="text"
                  placeholder="Cédula o token..."
                  class="flex-1 px-2.5 py-1.5 bg-slate-900 border border-slate-700 rounded-lg text-white text-xs placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                />
                <button
                  type="submit"
                  :disabled="!busquedaManual.trim() || buscando"
                  class="py-1.5 px-3 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-semibold text-xs rounded-lg transition-all flex items-center gap-1 cursor-pointer"
                >
                  <i :class="['fas text-xs', buscando ? 'fa-spinner fa-spin' : 'fa-search']"></i>
                  <span>Buscar</span>
                </button>
              </form>
            </div>

          </div>
        </div>

        <!-- Panel Derecho: Resultado de Validación -->
        <div class="md:col-span-7 space-y-2">
          
          <!-- Estado Inicial / Vacío -->
          <div v-if="!resultadoValidacion && !buscando" class="bg-slate-800/60 border border-dashed border-slate-700 rounded-xl p-4 sm:p-6 text-center text-slate-500">
            <i class="fas fa-ticket text-2xl sm:text-3xl mb-1.5 text-slate-600 block"></i>
            <h3 class="text-xs sm:text-sm font-bold text-slate-300">Esperando Escaneo</h3>
            <p class="text-[11px] text-slate-400 mt-0.5">
              Apunta la cámara al código QR para validar el boleto y el coffee break.
            </p>
          </div>

          <!-- Spinner al procesar -->
          <div v-if="buscando" class="bg-slate-800 p-4 rounded-xl border border-slate-700 text-center">
            <i class="fas fa-circle-notch fa-spin text-2xl text-indigo-500 mb-1.5 block mx-auto"></i>
            <p class="text-xs font-semibold text-slate-300">Validando boleto...</p>
          </div>

          <!-- Tarjeta de Boleto Encontrado -->
          <div v-if="resultadoValidacion" class="bg-slate-800 rounded-xl border border-slate-700 shadow-md overflow-hidden animate-fade-in-up">
            
            <!-- Banner de Estado -->
            <div
              :class="[
                'py-1.5 px-3 text-white text-center font-bold text-xs flex items-center justify-center gap-1.5',
                resultadoValidacion.estaPagado ? 'bg-gradient-to-r from-emerald-600 to-teal-600' : 'bg-gradient-to-r from-amber-600 to-orange-600'
              ]"
            >
              <i :class="['fas text-xs', resultadoValidacion.estaPagado ? 'fa-check-circle' : 'fa-clock']"></i>
              <span>{{ resultadoValidacion.estaPagado ? 'Boleto Válido y Pagado' : 'Pago Pendiente / Saldo por Cobrar' }}</span>
            </div>

            <!-- Alerta de Asistencia Previa (si ya ingresó) -->
            <div v-if="resultadoValidacion.asistenciaConfirmada" class="py-1 px-2.5 bg-amber-500/15 border-b border-amber-500/30 text-amber-300 text-[11px] flex items-center gap-1.5">
              <i class="fas fa-triangle-exclamation text-amber-400 text-xs shrink-0"></i>
              <span><strong>¡Ya ingresó!</strong> Hora: {{ formatearFecha(resultadoValidacion.fechaIngreso) }}</span>
            </div>

            <div class="p-3 space-y-2 text-xs">
              <!-- Nombre, Cédula y Monto -->
              <div class="flex items-start justify-between gap-2">
                <div>
                  <h2 class="text-sm sm:text-base font-bold text-white leading-tight">
                    {{ resultadoValidacion.nombre }}
                  </h2>
                  <div class="flex flex-wrap items-center gap-x-2 text-[11px] text-slate-400 mt-0.5">
                    <span><i class="fas fa-id-card mr-1 text-indigo-400"></i>{{ resultadoValidacion.cedula }}</span>
                    <span v-if="resultadoValidacion.telefono"><i class="fas fa-phone mr-1 text-indigo-400"></i>{{ resultadoValidacion.telefono }}</span>
                  </div>
                </div>
                <div class="text-right shrink-0">
                  <span class="font-bold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded text-xs block">
                    ${{ resultadoValidacion.totalPagado.toFixed(2) }}
                  </span>
                  <span v-if="!resultadoValidacion.estaPagado" class="text-[10px] text-amber-400 font-bold block mt-0.5">
                    Saldo: ${{ resultadoValidacion.saldoPendiente.toFixed(2) }}
                  </span>
                </div>
              </div>

              <!-- Fila Compacta de Iglesia, Mentor y Boleto -->
              <div class="grid grid-cols-2 sm:grid-cols-3 gap-1.5 bg-slate-900/80 rounded-lg p-2 text-[11px] border border-slate-700/60">
                <div>
                  <span class="text-slate-400 block text-[10px]">Iglesia</span>
                  <span class="font-medium text-slate-200 truncate block">{{ resultadoValidacion.iglesia || 'N/A' }}</span>
                </div>
                <div>
                  <span class="text-slate-400 block text-[10px]">Boleto</span>
                  <span class="font-medium text-indigo-300 truncate block">{{ resultadoValidacion.ticketType || 'Adulto full' }}</span>
                </div>
                <div v-if="resultadoValidacion.mentor" class="col-span-2 sm:col-span-1">
                  <span class="text-slate-400 block text-[10px]">Mentor</span>
                  <span class="font-medium text-slate-200 truncate block">{{ resultadoValidacion.mentor }}</span>
                </div>
              </div>

              <!-- Sección: Control de Coffee Break (2 Turnos) -->
              <div v-if="resultadoValidacion.incluyeCoffee" class="bg-slate-900/90 rounded-lg p-2 space-y-1.5 border border-slate-700/70">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-white text-[11px] uppercase tracking-wide flex items-center gap-1.5">
                    <i class="fas fa-mug-hot text-amber-400"></i>
                    Coffee Break
                  </span>
                  <span
                    :class="[
                      'px-2 py-0.2 rounded-full text-[10px] font-extrabold uppercase tracking-wider border',
                      (resultadoValidacion.coffee1Tomado && resultadoValidacion.coffee2Tomado)
                        ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30'
                        : (resultadoValidacion.coffee1Tomado || resultadoValidacion.coffee2Tomado)
                          ? 'bg-amber-500/20 text-amber-300 border-amber-500/30'
                          : 'bg-slate-800 text-slate-400 border-slate-700'
                    ]"
                  >
                    {{ totalCoffeesTomados }}/2 Tomados
                  </span>
                </div>

                <!-- Alerta si el boleto tiene saldo pendiente -->
                <div v-if="!resultadoValidacion.estaPagado" class="p-1.5 bg-amber-500/10 border border-amber-500/30 rounded text-amber-300 text-[10px] flex items-center gap-1.5">
                  <i class="fas fa-triangle-exclamation text-amber-400 shrink-0"></i>
                  <span>Pago pendiente. Se requiere saldo pagado para coffee.</span>
                </div>

                <!-- Feedback mensaje Coffee -->
                <div
                  v-if="mensajeCoffee"
                  :class="[
                    'p-1.5 rounded text-[11px] font-semibold flex items-center justify-between gap-1.5 transition-all',
                    mensajeCoffee.tipo === 'exito'
                      ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                      : mensajeCoffee.tipo === 'info'
                        ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'
                        : 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                  ]"
                >
                  <span class="truncate">{{ mensajeCoffee.texto }}</span>
                  <button @click="mensajeCoffee = null" class="text-xs opacity-70 hover:opacity-100 p-0.5 cursor-pointer">
                    <i class="fas fa-times"></i>
                  </button>
                </div>

                <!-- Turnos 1 y 2 en cuadrícula compacta -->
                <div class="grid grid-cols-2 gap-2">
                  <!-- Coffee 1 -->
                  <div
                    :class="[
                      'p-2 rounded-lg border flex flex-col justify-between gap-1.5',
                      resultadoValidacion.coffee1Tomado
                        ? 'bg-slate-800 border-emerald-500/40'
                        : 'bg-slate-800/60 border-slate-700'
                    ]"
                  >
                    <div class="flex items-center justify-between">
                      <span class="font-bold text-[11px] text-white flex items-center gap-1">
                        <i class="fas fa-mug-hot text-amber-400 text-[10px]"></i> C1
                      </span>
                      <span
                        :class="[
                          'px-1.5 py-0.2 rounded text-[9px] font-bold',
                          resultadoValidacion.coffee1Tomado
                            ? 'bg-emerald-500/20 text-emerald-300'
                            : 'bg-slate-700 text-slate-400'
                        ]"
                      >
                        {{ resultadoValidacion.coffee1Tomado ? 'Tomado' : 'Disp.' }}
                      </span>
                    </div>

                    <div v-if="resultadoValidacion.coffee1Tomado" class="text-[10px] flex items-center justify-between pt-1 border-t border-slate-700/60">
                      <span class="text-emerald-400 truncate max-w-[85px]">
                        {{ formatearFechaHora(resultadoValidacion.fechaCoffee1) }}
                      </span>
                      <button
                        type="button"
                        @click="deshacerCoffee(1)"
                        :disabled="procesandoCoffee === 1"
                        class="text-slate-400 hover:text-rose-400 underline cursor-pointer"
                      >
                        Deshacer
                      </button>
                    </div>
                    <div v-else class="pt-0.5">
                      <button
                        type="button"
                        @click="redimirCoffee(1)"
                        :disabled="!resultadoValidacion.estaPagado || procesandoCoffee === 1"
                        class="w-full py-1 px-2 bg-amber-600 hover:bg-amber-500 disabled:opacity-40 text-white font-bold text-[11px] rounded transition-all flex items-center justify-center gap-1 cursor-pointer"
                      >
                        <i :class="['fas text-[10px]', procesandoCoffee === 1 ? 'fa-spinner fa-spin' : 'fa-mug-hot']"></i>
                        <span>{{ procesandoCoffee === 1 ? '...' : 'Redimir C1' }}</span>
                      </button>
                    </div>
                  </div>

                  <!-- Coffee 2 -->
                  <div
                    :class="[
                      'p-2 rounded-lg border flex flex-col justify-between gap-1.5',
                      resultadoValidacion.coffee2Tomado
                        ? 'bg-slate-800 border-emerald-500/40'
                        : 'bg-slate-800/60 border-slate-700'
                    ]"
                  >
                    <div class="flex items-center justify-between">
                      <span class="font-bold text-[11px] text-white flex items-center gap-1">
                        <i class="fas fa-mug-saucer text-orange-400 text-[10px]"></i> C2
                      </span>
                      <span
                        :class="[
                          'px-1.5 py-0.2 rounded text-[9px] font-bold',
                          resultadoValidacion.coffee2Tomado
                            ? 'bg-emerald-500/20 text-emerald-300'
                            : 'bg-slate-700 text-slate-400'
                        ]"
                      >
                        {{ resultadoValidacion.coffee2Tomado ? 'Tomado' : 'Disp.' }}
                      </span>
                    </div>

                    <div v-if="resultadoValidacion.coffee2Tomado" class="text-[10px] flex items-center justify-between pt-1 border-t border-slate-700/60">
                      <span class="text-emerald-400 truncate max-w-[85px]">
                        {{ formatearFechaHora(resultadoValidacion.fechaCoffee2) }}
                      </span>
                      <button
                        type="button"
                        @click="deshacerCoffee(2)"
                        :disabled="procesandoCoffee === 2"
                        class="text-slate-400 hover:text-rose-400 underline cursor-pointer"
                      >
                        Deshacer
                      </button>
                    </div>
                    <div v-else class="pt-0.5">
                      <button
                        type="button"
                        @click="redimirCoffee(2)"
                        :disabled="!resultadoValidacion.estaPagado || procesandoCoffee === 2"
                        class="w-full py-1 px-2 bg-amber-600 hover:bg-amber-500 disabled:opacity-40 text-white font-bold text-[11px] rounded transition-all flex items-center justify-center gap-1 cursor-pointer"
                      >
                        <i :class="['fas text-[10px]', procesandoCoffee === 2 ? 'fa-spinner fa-spin' : 'fa-mug-saucer']"></i>
                        <span>{{ procesandoCoffee === 2 ? '...' : 'Redimir C2' }}</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Botones de Acción de Check-In -->
              <div class="pt-1 space-y-1.5">
                <button
                  v-if="!resultadoValidacion.asistenciaConfirmada"
                  type="button"
                  @click="confirmarCheckIn"
                  :disabled="procesandoCheckIn"
                  class="w-full py-2 bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white font-bold text-xs rounded-lg shadow transition-all flex items-center justify-center gap-1.5 cursor-pointer"
                >
                  <i :class="['fas', procesandoCheckIn ? 'fa-spinner fa-spin' : 'fa-door-open']"></i>
                  <span>{{ procesandoCheckIn ? 'Registrando...' : 'Confirmar Ingreso (Check-In)' }}</span>
                </button>

                <div v-else class="py-1.5 px-2 bg-emerald-500/10 border border-emerald-500/20 rounded-lg text-emerald-400 font-bold text-xs text-center flex items-center justify-center gap-1.5">
                  <i class="fas fa-check-double"></i>
                  <span>Ingreso Confirmado</span>
                </div>

                <button
                  type="button"
                  @click="resetearEscaneo"
                  class="w-full py-1.5 bg-slate-700 hover:bg-slate-600 text-slate-200 font-semibold text-xs rounded-lg border border-slate-600 transition-all flex items-center justify-center gap-1.5 cursor-pointer"
                >
                  <i class="fas fa-rotate-right text-indigo-400"></i>
                  <span>Escanear Siguiente Boleto</span>
                </button>
              </div>

            </div>

          </div>

          <!-- Alerta de No Encontrado -->
          <div v-if="errorNoEncontrado" class="bg-rose-900/30 border border-rose-700/60 p-3 rounded-xl text-center space-y-1.5">
            <i class="fas fa-circle-xmark text-rose-400 text-xl"></i>
            <h4 class="text-xs font-bold text-rose-200">Boleto no registrado</h4>
            <p class="text-[11px] text-rose-300">
              No se encontró ninguna inscripción con los datos escaneados.
            </p>
            <button
              @click="errorNoEncontrado = false"
              class="px-2.5 py-0.5 bg-rose-800 hover:bg-rose-700 text-white rounded text-xs font-semibold"
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
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { Html5Qrcode } from 'html5-qrcode'
import { db, auth } from '../firebase'
import { collection, query, where, getDocs, doc, updateDoc } from 'firebase/firestore'
import { useEventosStore } from '../stores/eventos'
import { obtenerRolesUsuario } from '../utils/authRoles'
import { inscripcionIncluyeCoffee } from '../utils/ticketUtils'

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
const procesandoCoffee = ref(0) // 0: libre, 1: procesando turno 1, 2: procesando turno 2
const mensajeCoffee = ref(null)

// Control de escaneo continuo para evitar rebotes
let ultimoCodigoEscaneado = ''
let ultimoTiempoEscaneo = 0

const metricas = ref({
  total: 0,
  ingresados: 0,
  coffee1: 0,
  coffee2: 0
})

const totalCoffeesTomados = computed(() => {
  if (!resultadoValidacion.value) return 0
  let count = 0
  if (resultadoValidacion.value.coffee1Tomado) count++
  if (resultadoValidacion.value.coffee2Tomado) count++
  return count
})

// Feedback auditivo sutil con Web Audio API (útil para eventos ruidosos)
const reproducirSonidoExito = () => {
  try {
    const ctx = new (window.AudioContext || window.webkitAudioContext)()
    const osc = ctx.createOscillator()
    const gain = ctx.createGain()
    osc.connect(gain)
    gain.connect(ctx.destination)
    osc.type = 'sine'
    osc.frequency.setValueAtTime(587.33, ctx.currentTime) // Re5
    osc.frequency.setValueAtTime(880, ctx.currentTime + 0.08) // La5
    gain.gain.setValueAtTime(0.12, ctx.currentTime)
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.3)
    osc.start()
    osc.stop(ctx.currentTime + 0.3)
  } catch (e) {
    // Modo silencioso si el navegador no permite AudioContext
  }
}

const reproducirSonidoAlerta = () => {
  try {
    const ctx = new (window.AudioContext || window.webkitAudioContext)()
    const osc = ctx.createOscillator()
    const gain = ctx.createGain()
    osc.connect(gain)
    gain.connect(ctx.destination)
    osc.type = 'sawtooth'
    osc.frequency.setValueAtTime(220, ctx.currentTime)
    gain.gain.setValueAtTime(0.15, ctx.currentTime)
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.25)
    osc.start()
    osc.stop(ctx.currentTime + 0.25)
  } catch (e) {
    // Silencioso
  }
}

const cargarMetricas = async () => {
  try {
    if (!eventosStore.eventos || eventosStore.eventos.length === 0) {
      if (typeof eventosStore.cargarEventos === 'function') {
        await eventosStore.cargarEventos()
      }
    }
    const list = await eventosStore.obtenerTodasInscripciones()
    metricas.value.total = list.length
    metricas.value.ingresados = list.filter(i => i.asistenciaConfirmada || i.participante?.asistenciaConfirmada || i.checkIn).length
    metricas.value.coffee1 = list.filter(i => i.coffee1Tomado || i.coffeeBreak1 || i.participante?.coffee1Tomado || i.participante?.coffeeBreak1).length
    metricas.value.coffee2 = list.filter(i => i.coffee2Tomado || i.coffeeBreak2 || i.participante?.coffee2Tomado || i.participante?.coffeeBreak2).length
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
  const ahora = Date.now()
  if (buscando.value) return

  // Si ya tenemos un resultado visible y es el mismo código escaneado hace menos de 3.5 segundos, ignorar
  if (resultadoValidacion.value && decodedText === ultimoCodigoEscaneado && (ahora - ultimoTiempoEscaneo) < 3500) {
    return
  }

  ultimoCodigoEscaneado = decodedText
  ultimoTiempoEscaneo = ahora
  await procesarCodigo(decodedText)
}

const onScanFailure = (error) => {
  // Ignorar frames sin código QR
}

const procesarCodigo = async (rawCode) => {
  buscando.value = true
  resultadoValidacion.value = null
  errorNoEncontrado.value = false
  mensajeCoffee.value = null

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

      // Extraer estados de turnos de coffee break
      const coffee1Tomado = !!(data.coffee1Tomado ?? data.coffeeBreak1 ?? p.coffee1Tomado ?? p.coffeeBreak1)
      const fechaCoffee1 = data.fechaCoffee1 || data.fechaCoffeeBreak1 || p.fechaCoffee1 || null
      const coffee1Por = data.coffee1Por || p.coffee1Por || null

      const coffee2Tomado = !!(data.coffee2Tomado ?? data.coffeeBreak2 ?? p.coffee2Tomado ?? p.coffeeBreak2)
      const fechaCoffee2 = data.fechaCoffee2 || data.fechaCoffeeBreak2 || p.fechaCoffee2 || null
      const coffee2Por = data.coffee2Por || p.coffee2Por || null

      const incluyeCoffee = inscripcionIncluyeCoffee(data, eventosStore.eventos)

      resultadoValidacion.value = {
        id: docSnap.id,
        nombre: p.nombre || 'N/A',
        cedula: p.cedula || 'N/A',
        telefono: p.telefono || '',
        iglesia: p.iglesia || '',
        mentor: p.mentor || '',
        ticketType: p.ticketType || 'Adulto full',
        ticketPrice: ticketCost,
        incluyeCoffee,
        totalPagado: totalPagado,
        saldoPendiente: saldoPendiente,
        estaPagado: estaPagado,
        asistenciaConfirmada: !!(data.asistenciaConfirmada || p.asistenciaConfirmada || data.checkIn),
        fechaIngreso: data.fechaIngreso || p.fechaIngreso || null,
        coffee1Tomado,
        fechaCoffee1,
        coffee1Por,
        coffee2Tomado,
        fechaCoffee2,
        coffee2Por
      }

      reproducirSonidoExito()
    } else {
      errorNoEncontrado.value = true
      reproducirSonidoAlerta()
    }
  } catch (err) {
    console.error('Error buscando boleto:', err)
    errorNoEncontrado.value = true
    reproducirSonidoAlerta()
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
    reproducirSonidoExito()
  } catch (e) {
    console.error('Error al registrar check-in:', e)
    reproducirSonidoAlerta()
    alert('No se pudo registrar el ingreso en la base de datos.')
  } finally {
    procesandoCheckIn.value = false
  }
}

// Redimir turno de coffee (1 o 2)
const redimirCoffee = async (turno) => {
  if (!resultadoValidacion.value) return
  if (!resultadoValidacion.value.estaPagado) {
    reproducirSonidoAlerta()
    mensajeCoffee.value = {
      tipo: 'error',
      texto: 'No se puede redimir coffee: el boleto aún tiene saldo pendiente.'
    }
    return
  }

  const yaTomado = turno === 1 ? resultadoValidacion.value.coffee1Tomado : resultadoValidacion.value.coffee2Tomado
  if (yaTomado) {
    reproducirSonidoAlerta()
    mensajeCoffee.value = {
      tipo: 'info',
      texto: `El Coffee ${turno} ya fue entregado previamente a este participante.`
    }
    return
  }

  procesandoCoffee.value = turno
  try {
    const ahora = new Date().toISOString()
    const usuarioEmail = auth.currentUser?.email || 'Control QR'
    const docRef = doc(db, 'inscripciones', resultadoValidacion.value.id)

    if (turno === 1) {
      await updateDoc(docRef, {
        coffee1Tomado: true,
        coffeeBreak1: true,
        fechaCoffee1: ahora,
        coffee1Por: usuarioEmail
      })
      resultadoValidacion.value.coffee1Tomado = true
      resultadoValidacion.value.fechaCoffee1 = ahora
      resultadoValidacion.value.coffee1Por = usuarioEmail
      metricas.value.coffee1++
    } else if (turno === 2) {
      await updateDoc(docRef, {
        coffee2Tomado: true,
        coffeeBreak2: true,
        fechaCoffee2: ahora,
        coffee2Por: usuarioEmail
      })
      resultadoValidacion.value.coffee2Tomado = true
      resultadoValidacion.value.fechaCoffee2 = ahora
      resultadoValidacion.value.coffee2Por = usuarioEmail
      metricas.value.coffee2++
    }

    reproducirSonidoExito()
    mensajeCoffee.value = {
      tipo: 'exito',
      texto: `¡Coffee ${turno} registrado y entregado a ${resultadoValidacion.value.nombre}!`
    }
  } catch (err) {
    console.error(`Error al registrar coffee ${turno}:`, err)
    reproducirSonidoAlerta()
    mensajeCoffee.value = {
      tipo: 'error',
      texto: `Error al registrar entrega de Coffee ${turno}. Intenta nuevamente.`
    }
  } finally {
    procesandoCoffee.value = 0
  }
}

// Deshacer entrega de coffee (en caso de error accidental)
const deshacerCoffee = async (turno) => {
  if (!resultadoValidacion.value) return
  if (!confirm(`¿Estás seguro de desmarcar la entrega de Coffee ${turno} para este boleto?`)) return

  procesandoCoffee.value = turno
  try {
    const docRef = doc(db, 'inscripciones', resultadoValidacion.value.id)

    if (turno === 1) {
      await updateDoc(docRef, {
        coffee1Tomado: false,
        coffeeBreak1: false,
        fechaCoffee1: null,
        coffee1Por: null
      })
      resultadoValidacion.value.coffee1Tomado = false
      resultadoValidacion.value.fechaCoffee1 = null
      resultadoValidacion.value.coffee1Por = null
      metricas.value.coffee1 = Math.max(0, metricas.value.coffee1 - 1)
    } else if (turno === 2) {
      await updateDoc(docRef, {
        coffee2Tomado: false,
        coffeeBreak2: false,
        fechaCoffee2: null,
        coffee2Por: null
      })
      resultadoValidacion.value.coffee2Tomado = false
      resultadoValidacion.value.fechaCoffee2 = null
      resultadoValidacion.value.coffee2Por = null
      metricas.value.coffee2 = Math.max(0, metricas.value.coffee2 - 1)
    }

    mensajeCoffee.value = {
      tipo: 'info',
      texto: `Se canceló la marca de entrega de Coffee ${turno}.`
    }
  } catch (err) {
    console.error(`Error al deshacer coffee ${turno}:`, err)
    mensajeCoffee.value = {
      tipo: 'error',
      texto: `Error al deshacer entrega de Coffee ${turno}.`
    }
  } finally {
    procesandoCoffee.value = 0
  }
}

const resetearEscaneo = () => {
  resultadoValidacion.value = null
  busquedaManual.value = ''
  errorNoEncontrado.value = false
  mensajeCoffee.value = null
  ultimoCodigoEscaneado = ''
  ultimoTiempoEscaneo = 0
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

const formatearFechaHora = (str) => {
  if (!str) return ''
  try {
    const d = new Date(str)
    const hoy = new Date()
    const esMismoDia = d.getDate() === hoy.getDate() &&
                       d.getMonth() === hoy.getMonth() &&
                       d.getFullYear() === hoy.getFullYear()
    const hora = d.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
    return esMismoDia ? hora : `${d.toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit' })} ${hora}`
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
