<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-8">
    <div class="container mx-auto px-4 pt-[100px]">
      <!-- Header -->
      <div class="bg-white rounded-2xl shadow-xl p-6 mb-6">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <h1 class="text-3xl font-bold text-gray-800 flex items-center gap-3">
              <i class="fas fa-users-cog text-indigo-600"></i>
              Gestión de Inscripciones
            </h1>
            <p class="text-gray-600 mt-1">Administra todas las inscripciones a eventos</p>
          </div>
          <div class="flex items-center gap-3">
            <div class="bg-indigo-100 px-4 py-2 rounded-lg">
              <span class="text-sm text-indigo-600 font-semibold">
                Total: {{ inscripcionesFiltradas.length }}
              </span>
            </div>
            <button
              @click="cargarInscripciones"
              :disabled="cargando"
              class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors disabled:bg-gray-400 flex items-center gap-2"
            >
              <i :class="['fas', cargando ? 'fa-spinner fa-spin' : 'fa-sync-alt']"></i>
              Actualizar
            </button>
          </div>
        </div>
      </div>

      <!-- Filtros y Búsqueda -->
      <div class="bg-white rounded-2xl shadow-xl p-6 mb-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <!-- Búsqueda -->
          <div class="md:col-span-2">
            <label class="block text-sm font-semibold text-gray-700 mb-2">
              <i class="fas fa-search mr-2"></i>
              Buscar por nombre, cédula o teléfono
            </label>
            <input
              v-model="filtros.busqueda"
              type="text"
              placeholder="Ej: Juan Pérez, 8-123-4567..."
              class="w-full px-4 py-2 border-2 text-gray-700 border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          <!-- Filtro por Evento -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">
              <i class="fas fa-calendar mr-2"></i>
              Filtrar por Evento
            </label>
            <div class="flex gap-2">
              <select
                v-model="filtros.eventoId"
                class="flex-1 px-4 py-2 border-2 text-gray-700 border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              >
                <option value="">Todos los eventos</option>
                <option v-for="evento in eventos" :key="evento.id" :value="evento.id">
                  {{ evento.titulo }}
                </option>
              </select>
              <button
                v-if="filtros.eventoId"
                @click="limpiarFiltroEvento"
                class="px-3 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
                title="Limpiar filtro"
              >
                <i class="fas fa-times"></i>
              </button>
            </div>
          </div>
        </div>

        <!-- Alerta de filtro activo -->
        <div v-if="filtros.eventoId" class="mt-4 bg-blue-50 border-l-4 border-blue-500 p-4 rounded flex justify-between items-center">
          <div class="flex items-center gap-2">
            <i class="fas fa-filter text-blue-600"></i>
            <p class="text-sm text-blue-800">
              <strong>Filtrando por evento:</strong> {{ obtenerNombreEvento(filtros.eventoId) }}
            </p>
          </div>
          <button
            @click="limpiarFiltroEvento"
            class="text-blue-600 hover:text-blue-800 font-semibold text-sm"
          >
            Ver todos
          </button>
        </div>

        <!-- Estadísticas rápidas -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
          <div class="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
            <p class="text-sm text-gray-600">Total Inscripciones</p>
            <p class="text-2xl font-bold text-blue-600">{{ todasInscripciones.length }}</p>
          </div>
          <!-- <div class="bg-green-50 border-l-4 border-green-500 p-4 rounded">
            <p class="text-sm text-gray-600">Eventos Activos</p>
            <p class="text-2xl font-bold text-green-600">{{ eventos.length }}</p>
          </div> -->
          <div class="bg-purple-50 border-l-4 border-purple-500 p-4 rounded">
            <p class="text-sm text-gray-600">Filtradas</p>
            <p class="text-2xl font-bold text-purple-600">{{ inscripcionesFiltradas.length }}</p>
          </div>
          <div class="bg-orange-50 border-l-4 border-orange-500 p-4 rounded">
            <p class="text-sm text-gray-600">Ingresos Total</p>
            <p class="text-2xl font-bold text-orange-600">${{ calcularIngresoTotal }}</p>
          </div>
        </div>
      </div>

      <!-- Tabla de Inscripciones -->
      <div class="bg-white rounded-2xl shadow-xl overflow-hidden">
        <!-- Loading State -->
        <div v-if="cargando" class="flex items-center justify-center py-20">
          <div class="text-center">
            <i class="fas fa-spinner fa-spin text-5xl text-indigo-600 mb-4"></i>
            <p class="text-gray-600">Cargando inscripciones...</p>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="inscripcionesPaginadas.length === 0" class="text-center py-20">
          <i class="fas fa-inbox text-6xl text-gray-300 mb-4"></i>
          <p class="text-gray-600 text-lg mb-2">No se encontraron inscripciones</p>
          <p class="text-gray-500 text-sm">Ajusta los filtros o verifica que haya inscripciones registradas</p>
        </div>

        <!-- Tabla -->
        <div v-else class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gradient-to-r from-indigo-600 to-purple-600 text-white">
              <tr>
                <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider">Participante</th>
                <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider">Evento</th>
                <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider">Ticket</th>
                <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider">Monto</th>
                <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider">Fecha</th>
                <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider">Comprobante</th>
                <th class="px-4 py-3 text-center text-xs font-semibold uppercase tracking-wider">Acciones</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              <tr
                v-for="inscripcion in inscripcionesPaginadas"
                :key="inscripcion.id"
                class="hover:bg-gray-50 transition-colors"
              >
                <!-- Participante -->
                <td class="px-4 py-4">
                  <div>
                    <p class="font-semibold text-gray-800">{{ inscripcion.participante?.nombre || 'N/A' }}</p>
                    <p class="text-sm text-gray-600">
                      <i class="fas fa-id-card mr-1"></i>{{ inscripcion.participante?.cedula || 'N/A' }}
                    </p>
                    <p class="text-sm text-gray-600">
                      <i class="fas fa-phone mr-1"></i>{{ inscripcion.participante?.telefono || 'N/A' }}
                    </p>
                  </div>
                </td>

                <!-- Evento -->
                <td class="px-4 py-4">
                  <span class="inline-block px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">
                    {{ obtenerNombreEvento(inscripcion.eventoId) }}
                  </span>
                </td>

                <!-- Ticket -->
                <td class="px-4 py-4">
                  <p class="text-sm text-gray-800">{{ inscripcion.participante?.ticketType || 'N/A' }}</p>
                  <p class="text-xs text-gray-500">Cant: {{ inscripcion.participante?.ticketQuantity || 1 }}</p>
                </td>

                <!-- Monto -->
                <td class="px-4 py-4">
                  <span class="font-bold text-green-600">
                    ${{ Number(inscripcion.participante?.totalPrice || 0).toFixed(2) }}
                  </span>
                </td>

                <!-- Fecha -->
                <td class="px-4 py-4">
                  <p class="text-sm text-gray-600">{{ formatearFecha(inscripcion.fechaInscripcion) }}</p>
                </td>

                <!-- Comprobante -->
                <td class="px-4 py-4">
                  <FileViewer
                    v-if="inscripcion.participante?.comprobanteUrl"
                    :file-url="inscripcion.participante.comprobanteUrl"
                    :titulo="`Comprobante de ${inscripcion.participante.nombre}`"
                  />
                  <span v-else class="text-xs text-gray-400">Sin comprobante</span>
                  
                  <!-- Comprobantes adicionales -->
                  <div v-if="inscripcion.comprobantesAdicionales?.length" class="mt-2">
                    <p class="text-xs text-gray-500 mb-1">Adicionales ({{ inscripcion.comprobantesAdicionales.length }}):</p>
                    <div class="flex flex-wrap gap-1">
                      <FileViewer
                        v-for="(comp, idx) in inscripcion.comprobantesAdicionales"
                        :key="idx"
                        :file-url="comp.url"
                        :titulo="`Comprobante adicional #${idx + 1}`"
                      />
                    </div>
                  </div>
                </td>

                <!-- Acciones -->
                <td class="px-4 py-4">
                  <div class="flex items-center justify-center gap-2">
                    <button
                      @click="abrirModalEdicion(inscripcion)"
                      class="px-3 py-1.5 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors text-sm"
                      title="Editar"
                    >
                      <i class="fas fa-edit"></i>
                    </button>
                    <button
                      @click="confirmarEliminar(inscripcion)"
                      class="px-3 py-1.5 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors text-sm"
                      title="Eliminar"
                    >
                      <i class="fas fa-trash"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Paginación -->
        <div v-if="!cargando && inscripcionesFiltradas.length > 0" class="bg-gray-50 px-6 py-4 flex flex-col sm:flex-row justify-between items-center gap-4">
          <div class="text-sm text-gray-600">
            Mostrando {{ ((paginaActual - 1) * itemsPorPagina) + 1 }} - {{ Math.min(paginaActual * itemsPorPagina, inscripcionesFiltradas.length) }} 
            de {{ inscripcionesFiltradas.length }} inscripciones
          </div>
          <div class="flex gap-2">
            <button
              @click="paginaActual--"
              :disabled="paginaActual === 1"
              class="px-4 py-2 bg-white border-2 border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <i class="fas fa-chevron-left"></i>
            </button>
            <span class="px-4 py-2 bg-indigo-600 text-white rounded-lg font-semibold">
              {{ paginaActual }} / {{ totalPaginas }}
            </span>
            <button
              @click="paginaActual++"
              :disabled="paginaActual === totalPaginas"
              class="px-4 py-2 bg-white border-2 border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <i class="fas fa-chevron-right"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Edición -->
    <EditInscripcionModal
      :show="mostrarModalEdicion"
      :inscripcion="inscripcionSeleccionada"
      :evento-titulo="obtenerNombreEvento(inscripcionSeleccionada?.eventoId)"
      @close="cerrarModalEdicion"
      @save="guardarCambios"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useEventosStore } from '../stores/eventos'
import { auth } from '../firebase'
import FileViewer from '../components/FileViewer.vue'
import EditInscripcionModal from '../components/EditInscripcionModal.vue'

const router = useRouter()
const route = useRoute()
const eventosStore = useEventosStore()

const todasInscripciones = ref([])
const eventos = ref([])
const cargando = ref(false)
const paginaActual = ref(1)
const itemsPorPagina = ref(10)
const mostrarModalEdicion = ref(false)
const inscripcionSeleccionada = ref(null)

const filtros = ref({
  busqueda: '',
  eventoId: ''
})

// Verificar autenticación
onMounted(async () => {
  const unsubscribe = auth.onAuthStateChanged(user => {
    unsubscribe()
    if (!user) {
      router.push('/admin-login')
    } else {
      // Si viene un eventoId en la query, aplicar el filtro
      if (route.query.eventoId) {
        filtros.value.eventoId = route.query.eventoId
      }
      cargarDatos()
    }
  })
})

const cargarDatos = async () => {
  await eventosStore.cargarEventos()
  eventos.value = eventosStore.eventos
  await cargarInscripciones()
}

const cargarInscripciones = async () => {
  cargando.value = true
  try {
    todasInscripciones.value = await eventosStore.obtenerTodasInscripciones()
  } catch (error) {
    console.error('Error cargando inscripciones:', error)
  } finally {
    cargando.value = false
  }
}

// Filtrado inteligente
const inscripcionesFiltradas = computed(() => {
  let resultado = [...todasInscripciones.value]

  // Filtro por evento
  if (filtros.value.eventoId) {
    resultado = resultado.filter(ins => ins.eventoId === filtros.value.eventoId)
  }

  // Filtro por búsqueda (nombre, cédula, teléfono)
  if (filtros.value.busqueda) {
    const busqueda = filtros.value.busqueda.toLowerCase()
    resultado = resultado.filter(ins => {
      const nombre = ins.participante?.nombre?.toLowerCase() || ''
      const cedula = ins.participante?.cedula?.toLowerCase() || ''
      const telefono = ins.participante?.telefono?.toLowerCase() || ''
      return nombre.includes(busqueda) || cedula.includes(busqueda) || telefono.includes(busqueda)
    })
  }

  return resultado
})

// Paginación
const totalPaginas = computed(() => {
  return Math.ceil(inscripcionesFiltradas.value.length / itemsPorPagina.value)
})

const inscripcionesPaginadas = computed(() => {
  const inicio = (paginaActual.value - 1) * itemsPorPagina.value
  const fin = inicio + itemsPorPagina.value
  return inscripcionesFiltradas.value.slice(inicio, fin)
})

// Calcular ingreso total
const calcularIngresoTotal = computed(() => {
  const total = inscripcionesFiltradas.value.reduce((sum, ins) => {
    return sum + (Number(ins.participante?.totalPrice) || 0)
  }, 0)
  return total.toFixed(2)
})

const obtenerNombreEvento = (eventoId) => {
  const evento = eventos.value.find(e => e.id === eventoId)
  return evento ? evento.titulo : 'Evento desconocido'
}

const formatearFecha = (fechaISO) => {
  if (!fechaISO) return 'N/A'
  return new Date(fechaISO).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const abrirModalEdicion = (inscripcion) => {
  console.log('AdminInscripcionesView: abriendo modal con inscripcion:', inscripcion)
  inscripcionSeleccionada.value = { ...inscripcion } // Crear copia para forzar reactividad
  mostrarModalEdicion.value = true
}

const cerrarModalEdicion = () => {
  mostrarModalEdicion.value = false
  inscripcionSeleccionada.value = null
}

const guardarCambios = async (datos) => {
  try {
    await eventosStore.actualizarInscripcion(datos.id, {
      participante: datos.participante
    })
    
    // Actualizar la lista local
    const index = todasInscripciones.value.findIndex(ins => ins.id === datos.id)
    if (index !== -1) {
      todasInscripciones.value[index].participante = datos.participante
    }
  } catch (error) {
    console.error('Error guardando cambios:', error)
    throw error
  }
}

const limpiarFiltroEvento = () => {
  filtros.value.eventoId = ''
  // También limpiar el query param de la URL
  router.push({ path: '/admin/inscripciones', query: {} })
}

const confirmarEliminar = async (inscripcion) => {
  if (confirm(`¿Estás seguro de eliminar la inscripción de ${inscripcion.participante?.nombre}?`)) {
    try {
      await eventosStore.eliminarInscripcion(inscripcion.id)
      todasInscripciones.value = todasInscripciones.value.filter(ins => ins.id !== inscripcion.id)
    } catch (error) {
      console.error('Error eliminando inscripción:', error)
      alert('Error al eliminar la inscripción')
    }
  }
}
</script>

<style scoped>
/* Estilos adicionales si es necesario */
</style>
