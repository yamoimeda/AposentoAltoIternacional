<template>
  <div class="min-h-screen bg-slate-900 text-slate-100 font-sans pt-24 pb-16 px-4 sm:px-8">
    <div class="max-w-6xl mx-auto space-y-8">
      
      <!-- Header Superior -->
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-800">
        <div>
          <div class="flex items-center gap-2 text-xs font-semibold text-indigo-400 uppercase tracking-widest mb-1.5">
            <i class="fas fa-chart-pie"></i>
            <span>Estadísticas y Conteo en Vivo</span>
          </div>
          <h1 class="text-2xl sm:text-4xl font-extrabold text-white tracking-tight flex items-center gap-3">
            <span>{{ eventoActual ? eventoActual.titulo : 'Conteo General de Eventos' }}</span>
          </h1>
          <p class="text-xs sm:text-sm text-slate-400 mt-1">
            Resumen cuantitativo de participación, iglesias y recaudación en tiempo real.
          </p>
        </div>

        <!-- Botones de Acción -->
        <div class="flex flex-wrap items-center gap-3">
          <button
            @click="copiarEnlace"
            class="py-2.5 px-4 bg-indigo-600/90 hover:bg-indigo-600 text-white font-semibold text-xs sm:text-sm rounded-xl shadow-lg shadow-indigo-600/20 transition-all flex items-center gap-2 cursor-pointer"
          >
            <i :class="['fas', copiado ? 'fa-check text-emerald-300' : 'fa-share-nodes']"></i>
            <span>{{ copiado ? '¡Enlace Copiado!' : 'Compartir Conteo' }}</span>
          </button>

          <router-link
            to="/escanear-qr"
            class="py-2.5 px-4 bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-xs sm:text-sm rounded-xl border border-slate-700 transition-all flex items-center gap-2"
          >
            <i class="fas fa-qrcode text-indigo-400"></i>
            <span>Escanear QR</span>
          </router-link>

          <button
            @click="cargarDatos"
            :disabled="cargando"
            class="p-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl border border-slate-700 transition-all flex items-center justify-center cursor-pointer"
            title="Recargar datos"
          >
            <i :class="['fas', cargando ? 'fa-spinner fa-spin' : 'fa-rotate']"></i>
          </button>
        </div>
      </div>

      <!-- Selector de Evento si hay varios -->
      <div v-if="eventos.length > 1" class="bg-slate-800/80 backdrop-blur-md p-4 rounded-2xl border border-slate-700/80 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div class="flex items-center gap-2 text-xs text-slate-300 font-medium w-full sm:w-auto">
          <i class="fas fa-filter text-indigo-400"></i>
          <span>Filtrar por evento:</span>
        </div>
        <select
          v-model="eventoSeleccionadoId"
          class="w-full sm:w-80 px-3.5 py-2 bg-slate-900 border border-slate-700 rounded-xl text-white text-xs font-semibold focus:outline-none focus:border-indigo-500 transition-all"
        >
          <option value="">-- Ver todos los eventos --</option>
          <option v-for="ev in eventos" :key="ev.id" :value="ev.id">
            {{ ev.titulo }} ({{ ev.fecha }})
          </option>
        </select>
      </div>

      <!-- Spinner de Carga -->
      <div v-if="cargando" class="text-center py-20">
        <i class="fas fa-circle-notch fa-spin text-4xl text-indigo-500 mb-3 block mx-auto"></i>
        <p class="text-sm font-medium text-slate-400">Sincronizando contadores en vivo...</p>
      </div>

      <div v-else class="space-y-8">
        
        <!-- Tarjetas Principales de Conteo (KPIs) -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <!-- Total Inscritos -->
          <div class="bg-gradient-to-br from-slate-800 to-slate-800/60 p-6 rounded-2xl border border-slate-700/80 shadow-lg relative overflow-hidden">
            <div class="absolute -right-4 -bottom-4 w-24 h-24 bg-indigo-500/10 rounded-full blur-xl pointer-events-none"></div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Total Inscritos</span>
              <div class="w-10 h-10 rounded-xl bg-indigo-500/20 text-indigo-400 flex items-center justify-center text-lg">
                <i class="fas fa-users"></i>
              </div>
            </div>
            <div class="text-4xl font-extrabold text-white mb-1">
              {{ metricas.totalInscritos }}
            </div>
            <span class="text-xs text-slate-400">Personas confirmadas</span>
          </div>

          <!-- Total Recaudado -->
          <div class="bg-gradient-to-br from-slate-800 to-slate-800/60 p-6 rounded-2xl border border-slate-700/80 shadow-lg relative overflow-hidden">
            <div class="absolute -right-4 -bottom-4 w-24 h-24 bg-emerald-500/10 rounded-full blur-xl pointer-events-none"></div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-bold uppercase tracking-wider text-emerald-400">Total Recaudado</span>
              <div class="w-10 h-10 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-lg">
                <i class="fas fa-dollar-sign"></i>
              </div>
            </div>
            <div class="text-4xl font-extrabold text-emerald-400 mb-1">
              ${{ metricas.totalRecaudado.toFixed(2) }}
            </div>
            <span class="text-xs text-slate-400">Pagos recibidos y validados</span>
          </div>

          <!-- Total Esperado / Saldo -->
          <div class="bg-gradient-to-br from-slate-800 to-slate-800/60 p-6 rounded-2xl border border-slate-700/80 shadow-lg relative overflow-hidden">
            <div class="absolute -right-4 -bottom-4 w-24 h-24 bg-amber-500/10 rounded-full blur-xl pointer-events-none"></div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-bold uppercase tracking-wider text-amber-400">Total Esperado</span>
              <div class="w-10 h-10 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center text-lg">
                <i class="fas fa-calculator"></i>
              </div>
            </div>
            <div class="text-4xl font-extrabold text-amber-400 mb-1">
              ${{ metricas.totalEsperado.toFixed(2) }}
            </div>
            <span class="text-xs text-slate-400">
              Saldo pendiente: <b class="text-slate-200">${{ Math.max(0, metricas.totalEsperado - metricas.totalRecaudado).toFixed(2) }}</b>
            </span>
          </div>

          <!-- Asistentes Ingresados (Check-in) -->
          <div class="bg-gradient-to-br from-slate-800 to-slate-800/60 p-6 rounded-2xl border border-slate-700/80 shadow-lg relative overflow-hidden">
            <div class="absolute -right-4 -bottom-4 w-24 h-24 bg-purple-500/10 rounded-full blur-xl pointer-events-none"></div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-bold uppercase tracking-wider text-purple-400">En Puerta / Check-in</span>
              <div class="w-10 h-10 rounded-xl bg-purple-500/20 text-purple-400 flex items-center justify-center text-lg">
                <i class="fas fa-door-open"></i>
              </div>
            </div>
            <div class="text-4xl font-extrabold text-purple-300 mb-1">
              {{ metricas.totalIngresados }}
            </div>
            <span class="text-xs text-slate-400">
              {{ metricas.totalInscritos > 0 ? ((metricas.totalIngresados / metricas.totalInscritos) * 100).toFixed(1) + '% de asistencia' : 'Sin ingresos' }}
            </span>
          </div>
        </div>

        <!-- Meta de Cupos y Progreso (si el evento tiene cupos definidos) -->
        <div v-if="cupoMaximo > 0" class="bg-slate-800 p-6 rounded-2xl border border-slate-700 shadow-md space-y-3">
          <div class="flex justify-between items-center text-sm font-semibold">
            <span class="text-slate-300 flex items-center gap-2">
              <i class="fas fa-bullseye text-indigo-400"></i>
              Meta de Cupos Ocupados
            </span>
            <span class="text-white font-bold">{{ metricas.totalInscritos }} / {{ cupoMaximo }} ({{ porcentajeCupos }}%)</span>
          </div>
          <div class="w-full bg-slate-900 rounded-full h-4 overflow-hidden border border-slate-700">
            <div
              class="bg-gradient-to-r from-indigo-500 via-purple-500 to-emerald-500 h-full rounded-full transition-all duration-500"
              :style="{ width: Math.min(100, porcentajeCupos) + '%' }"
            ></div>
          </div>
        </div>

        <!-- Sección de Desgloses: Iglesias, Boletos y Mentores -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          
          <!-- Conteo por Iglesia -->
          <div class="bg-slate-800/90 p-6 rounded-2xl border border-slate-700/80 shadow-md">
            <h3 class="text-base font-bold text-white mb-4 flex items-center gap-2">
              <i class="fas fa-church text-indigo-400"></i>
              <span>Participación por Iglesia</span>
              <span class="ml-auto text-xs bg-indigo-500/20 text-indigo-300 px-2.5 py-0.5 rounded-full">
                {{ desglosePorIglesia.length }} iglesias
              </span>
            </h3>

            <div v-if="desglosePorIglesia.length === 0" class="text-xs text-slate-400 italic text-center py-6">
              Aún no hay inscripciones registradas.
            </div>

            <div v-else class="space-y-3.5 max-h-[380px] overflow-y-auto pr-1">
              <div
                v-for="item in desglosePorIglesia"
                :key="item.nombre"
                class="bg-slate-900/80 p-3.5 rounded-xl border border-slate-700/50 flex flex-col gap-2"
              >
                <div class="flex items-center justify-between text-xs sm:text-sm">
                  <span class="font-bold text-slate-200 truncate">{{ item.nombre }}</span>
                  <span class="font-extrabold text-indigo-400 bg-indigo-500/10 border border-indigo-500/20 px-2.5 py-0.5 rounded-lg">
                    {{ item.cantidad }} inscrito{{ item.cantidad !== 1 ? 's' : '' }}
                  </span>
                </div>
                <div class="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                  <div
                    class="bg-indigo-500 h-full rounded-full transition-all duration-300"
                    :style="{ width: ((item.cantidad / metricas.totalInscritos) * 100) + '%' }"
                  ></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Conteo por Tipo de Boleto y Mentores -->
          <div class="space-y-6">
            <!-- Tipos de Boleto -->
            <div class="bg-slate-800/90 p-6 rounded-2xl border border-slate-700/80 shadow-md">
              <h3 class="text-base font-bold text-white mb-4 flex items-center gap-2">
                <i class="fas fa-ticket text-indigo-400"></i>
                <span>Desglose por Tipo de Boleto</span>
              </h3>

              <div v-if="desglosePorBoleto.length === 0" class="text-xs text-slate-400 italic text-center py-4">
                Sin datos de boletos aún.
              </div>

              <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div
                  v-for="b in desglosePorBoleto"
                  :key="b.nombre"
                  class="bg-slate-900/80 p-3.5 rounded-xl border border-slate-700/50 flex items-center justify-between"
                >
                  <div class="overflow-hidden">
                    <span class="text-xs font-semibold text-slate-300 block truncate">{{ b.nombre }}</span>
                    <span class="text-[10px] text-slate-500">{{ ((b.cantidad / metricas.totalInscritos) * 100).toFixed(0) }}% del total</span>
                  </div>
                  <span class="text-lg font-bold text-white bg-slate-800 px-3 py-1 rounded-lg border border-slate-700">
                    {{ b.cantidad }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Conteo por Mentor / Líder -->
            <div class="bg-slate-800/90 p-6 rounded-2xl border border-slate-700/80 shadow-md">
              <h3 class="text-base font-bold text-white mb-4 flex items-center gap-2">
                <i class="fas fa-user-tie text-indigo-400"></i>
                <span>Inscritos por Mentor</span>
                <span class="ml-auto text-xs bg-purple-500/20 text-purple-300 px-2.5 py-0.5 rounded-full">
                  {{ desglosePorMentor.length }} mentores
                </span>
              </h3>

              <div v-if="desglosePorMentor.length === 0" class="text-xs text-slate-400 italic text-center py-4">
                No hay mentores especificados.
              </div>

              <div v-else class="space-y-2 max-h-48 overflow-y-auto pr-1">
                <div
                  v-for="m in desglosePorMentor"
                  :key="m.nombre"
                  class="bg-slate-900/80 px-3.5 py-2 rounded-xl border border-slate-700/50 flex items-center justify-between text-xs"
                >
                  <span class="font-medium text-slate-200 truncate">{{ m.nombre }}</span>
                  <span class="font-bold text-purple-400 bg-purple-500/10 px-2 py-0.5 rounded-md">
                    {{ m.cantidad }}
                  </span>
                </div>
              </div>
            </div>

          </div>

        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useEventosStore } from '../stores/eventos'

const route = useRoute()
const eventosStore = useEventosStore()

const cargando = ref(true)
const copiado = ref(false)
const eventos = ref([])
const inscripciones = ref([])
const eventoSeleccionadoId = ref('')

const eventoActual = computed(() => {
  if (!eventoSeleccionadoId.value) return null
  return eventos.value.find(e => e.id === eventoSeleccionadoId.value) || null
})

const cupoMaximo = computed(() => {
  if (eventoActual.value && eventoActual.value.cupos) {
    return Number(eventoActual.value.cupos)
  }
  return 0
})

const porcentajeCupos = computed(() => {
  if (!cupoMaximo.value) return 0
  return Math.round((metricas.value.totalInscritos / cupoMaximo.value) * 100)
})

const inscripcionesFiltradas = computed(() => {
  if (!eventoSeleccionadoId.value) return inscripciones.value
  return inscripciones.value.filter(i => i.eventoId === eventoSeleccionadoId.value)
})

const obtenerMontoInscripcion = (ins) => {
  if (!ins) return 0
  const p = ins.participante || ins || {}
  const candidatos = [p.montoPagado, p.monto, p.totalPrice, ins.montoPagado, ins.monto, ins.totalPrice]
  for (const c of candidatos) {
    if (c !== undefined && c !== null && c !== '') {
      const n = Number(c)
      if (!isNaN(n) && n > 0) return n
    }
  }
  const tPrice = Number(p.ticketPrice || 0)
  const tQty = Number(p.ticketQuantity || 1)
  if (tPrice > 0) return tPrice * tQty
  return 0
}

const obtenerPrecioEsperadoInscripcion = (ins) => {
  if (!ins) return 0
  const p = ins.participante || {}
  const ev = eventos.value.find(e => e.id === ins.eventoId || String(e.id) === String(ins.eventoId))
  if (ev) {
    const list = ev.ticketTypes || ev.tickets || []
    if (list.length > 0) {
      const t = list.find(tick => 
        (p.ticketTypeId && String(tick.id) === String(p.ticketTypeId)) ||
        (p.ticketType && tick.nombre?.trim().toLowerCase() === p.ticketType?.trim().toLowerCase())
      )
      if (t && !isNaN(Number(t.precio)) && Number(t.precio) > 0) return Number(t.precio)
      const primerConPrecio = list.find(tick => Number(tick.precio) > 0)
      if (primerConPrecio) return Number(primerConPrecio.precio)
    }
    if (ev.precio && !isNaN(Number(ev.precio)) && Number(ev.precio) > 0) return Number(ev.precio)
  }
  return Number(p.ticketPrice) || 0
}

const metricas = computed(() => {
  const lista = inscripcionesFiltradas.value
  let totalRecaudado = 0
  let totalEsperado = 0
  let totalIngresados = 0

  lista.forEach(ins => {
    totalRecaudado += obtenerMontoInscripcion(ins)
    const precio = obtenerPrecioEsperadoInscripcion(ins)
    const cant = Number(ins.participante?.ticketQuantity || 1)
    totalEsperado += (precio * cant)

    // Check-in
    if (ins.asistenciaConfirmada || ins.participante?.asistenciaConfirmada || ins.checkIn) {
      totalIngresados++
    }
  })

  return {
    totalInscritos: lista.length,
    totalRecaudado,
    totalEsperado,
    totalIngresados
  }
})

const desglosePorIglesia = computed(() => {
  const mapa = {}
  inscripcionesFiltradas.value.forEach(ins => {
    const ig = ins.participante?.iglesia?.trim() || 'No especificada'
    mapa[ig] = (mapa[ig] || 0) + 1
  })

  return Object.keys(mapa)
    .map(nombre => ({ nombre, cantidad: mapa[nombre] }))
    .sort((a, b) => b.cantidad - a.cantidad)
})

const desglosePorBoleto = computed(() => {
  const mapa = {}
  inscripcionesFiltradas.value.forEach(ins => {
    const t = ins.participante?.ticketType?.trim() || 'Adulto full'
    mapa[t] = (mapa[t] || 0) + 1
  })

  return Object.keys(mapa)
    .map(nombre => ({ nombre, cantidad: mapa[nombre] }))
    .sort((a, b) => b.cantidad - a.cantidad)
})

const desglosePorMentor = computed(() => {
  const mapa = {}
  inscripcionesFiltradas.value.forEach(ins => {
    const m = ins.participante?.mentor?.trim() || 'Sin mentor'
    mapa[m] = (mapa[m] || 0) + 1
  })

  return Object.keys(mapa)
    .map(nombre => ({ nombre, cantidad: mapa[nombre] }))
    .sort((a, b) => b.cantidad - a.cantidad)
})

const cargarDatos = async () => {
  cargando.value = true
  try {
    if (typeof eventosStore.cargarEventos === 'function') {
      await eventosStore.cargarEventos()
    }
    eventos.value = eventosStore.eventos || []
    inscripciones.value = await eventosStore.obtenerTodasInscripciones()
  } catch (error) {
    console.error('Error cargando conteo:', error)
  } finally {
    cargando.value = false
  }
}

const copiarEnlace = () => {
  const url = window.location.href
  navigator.clipboard.writeText(url).then(() => {
    copiado.value = true
    setTimeout(() => { copiado.value = false }, 3000)
  })
}

watch(
  () => route.params.eventoId || route.query.eventoId,
  (evId) => {
    if (evId) {
      eventoSeleccionadoId.value = evId
    }
  },
  { immediate: true }
)

onMounted(async () => {
  await cargarDatos()
  if (route.params.eventoId || route.query.eventoId) {
    eventoSeleccionadoId.value = route.params.eventoId || route.query.eventoId
  }
})
</script>
