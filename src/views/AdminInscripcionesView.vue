<template>
  <div class="min-h-screen bg-slate-50/80 font-sans text-slate-800 pt-20 md:pt-28 pb-16 px-4 sm:px-8">
    <div class="max-w-7xl mx-auto">
      <!-- Enterprise Page Header & Actions -->
      <div class="mb-8 flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-200/80">
        <div>
          <div class="flex items-center gap-2 text-xs font-medium text-slate-500 mb-1.5">
            <router-link to="/" class="hover:text-indigo-600 transition-colors">Inicio</router-link>
            <span>/</span>
            <router-link to="/admin" class="hover:text-indigo-600 transition-colors">Panel Admin</router-link>
            <span>/</span>
            <span class="text-slate-900 font-semibold">Inscripciones</span>
          </div>
          <h1 class="text-2xl sm:text-3xl font-bold tracking-tight text-slate-900 flex items-center gap-3">
            <span>Inscripciones</span>
            <span v-if="eventoActual" class="text-xs font-bold bg-indigo-50 border border-indigo-200 text-indigo-700 px-3 py-1 rounded-lg">
              {{ eventoActual.titulo }}
            </span>
          </h1>
          <p class="text-xs sm:text-sm text-slate-500 mt-1">
            Visualización y gestión de participantes registrados por evento.
          </p>
        </div>

        <div class="flex flex-wrap items-center gap-3">
          <button
            @click="mostrarGestionUsuarios = true"
            class="py-2.5 px-4 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 font-semibold text-xs sm:text-sm rounded-xl shadow-xs transition-all flex items-center gap-2 cursor-pointer"
          >
            <i class="fas fa-users-gear text-indigo-600"></i>
            <span>Usuarios</span>
          </button>

          <button
            @click="mostrarConfigIglesias = true"
            class="py-2.5 px-4 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 font-semibold text-xs sm:text-sm rounded-xl shadow-xs transition-all flex items-center gap-2 cursor-pointer"
          >
            <i class="fas fa-church text-indigo-600"></i>
            <span>Iglesias / Mentores</span>
          </button>

          <router-link
            to="/admin"
            class="py-2.5 px-4 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 font-semibold text-xs sm:text-sm rounded-xl shadow-xs transition-all flex items-center gap-2"
          >
            <i class="fas fa-arrow-left text-slate-400"></i>
            <span>Volver al Panel Admin</span>
          </router-link>

          <button
            @click="exportarCSV"
            :disabled="inscripcionesFiltradas.length === 0"
            class="py-2.5 px-4 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs sm:text-sm rounded-xl shadow-md shadow-emerald-600/20 transition-all flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
            title="Exportar archivo CSV"
          >
            <i class="fas fa-file-csv"></i>
            <span>Exportar CSV</span>
          </button>

          <button
            @click="cargarInscripciones"
            :disabled="cargando"
            class="py-2.5 px-3.5 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs sm:text-sm rounded-xl shadow-md transition-all flex items-center gap-1.5 disabled:opacity-50 cursor-pointer"
            title="Actualizar datos"
          >
            <i :class="['fas', cargando ? 'fa-spinner fa-spin' : 'fa-rotate']"></i>
          </button>
        </div>
      </div>

      <!-- Controls & Filter Toolbar -->
      <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-xs mb-8">
        <div class="grid grid-cols-1 md:grid-cols-12 gap-4 items-center">
          <!-- Event Selector Dropdown / Evento fijo cuando viene de un evento específico -->
          <div class="md:col-span-6">
            <label class="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
              <i class="fas fa-calendar-day text-indigo-600 mr-1.5"></i>
              Evento
            </label>

            <!-- Modo bloqueado: viene de un evento específico -->
            <div v-if="eventoFijado" class="flex items-center gap-3 px-3.5 py-2.5 bg-indigo-50 border-2 border-indigo-200 rounded-xl">
              <i class="fas fa-lock text-indigo-400 text-xs flex-shrink-0"></i>
              <span class="text-indigo-800 font-semibold text-sm truncate">{{ eventoActual?.titulo || 'Cargando...' }}</span>
              <router-link
                to="/admin"
                class="ml-auto text-xs text-indigo-500 hover:text-indigo-700 whitespace-nowrap flex items-center gap-1 transition-colors"
                title="Ver todos los eventos"
              >
                <i class="fas fa-th-list"></i> Ver todos
              </router-link>
            </div>

            <!-- Modo libre: selector general -->
            <select
              v-else
              v-model="filtros.eventoId"
              class="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-slate-900 text-sm font-medium focus:outline-none focus:bg-white focus:border-indigo-600 focus:ring-2 focus:ring-indigo-600/15 transition-all"
            >
              <option value="">-- Todos los eventos --</option>
              <option v-for="evento in eventos" :key="evento.id" :value="evento.id">
                {{ evento.titulo }} ({{ evento.fecha }})
              </option>
            </select>
          </div>

          <!-- Participant Search Input -->
          <div class="md:col-span-6">
            <label class="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
              <i class="fas fa-magnifying-glass text-indigo-600 mr-1.5"></i>
              Buscar Participante
            </label>

            <div class="relative">
              <input
                v-model="filtros.busqueda"
                type="text"
                placeholder="Nombre, cédula o teléfono..."
                class="w-full pl-3.5 pr-8 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-slate-900 placeholder-slate-400 text-sm focus:outline-none focus:bg-white focus:border-indigo-600 focus:ring-2 focus:ring-indigo-600/15 transition-all"
              />
              <button
                v-if="filtros.busqueda"
                @click="filtros.busqueda = ''"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
              >
                <i class="fas fa-times text-xs"></i>
              </button>
            </div>
          </div>
        </div>

        <!-- KPI Metrics Summary Bar -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6 pt-5 border-t border-slate-100">
          <div class="bg-slate-50 p-3.5 rounded-xl border border-slate-100">
            <span class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">Inscritos</span>
            <span class="text-xl font-bold text-slate-900">{{ inscripcionesFiltradas.length }}</span>
          </div>

          <div class="bg-indigo-50/60 p-3.5 rounded-xl border border-indigo-100">
            <span class="text-[11px] font-semibold text-indigo-400 uppercase tracking-wider block">Total Recaudado</span>
            <span class="text-xl font-bold text-indigo-700">${{ calcularIngresoTotal }}</span>
          </div>

          <div class="bg-amber-50/60 p-3.5 rounded-xl border border-amber-100">
            <span class="text-[11px] font-semibold text-amber-500 uppercase tracking-wider block">Total Esperado</span>
            <span class="text-xl font-bold text-amber-700">${{ calcularTotalEsperado }}</span>
          </div>

          <div class="bg-slate-50 p-3.5 rounded-xl border border-slate-100 flex items-center justify-between">
            <div>
              <span class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">Página</span>
              <span class="text-sm font-bold text-slate-800">{{ paginaActual }} de {{ totalPaginas || 1 }}</span>
            </div>
            <div class="flex gap-1">
              <button
                @click="paginaActual--"
                :disabled="paginaActual === 1"
                class="w-7 h-7 rounded-lg bg-white border border-slate-200 text-slate-600 hover:bg-slate-100 disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center text-xs"
              >
                <i class="fas fa-chevron-left"></i>
              </button>
              <button
                @click="paginaActual++"
                :disabled="paginaActual >= totalPaginas"
                class="w-7 h-7 rounded-lg bg-white border border-slate-200 text-slate-600 hover:bg-slate-100 disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center text-xs"
              >
                <i class="fas fa-chevron-right"></i>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Registrations Data Table Container -->
      <div class="bg-white rounded-2xl border border-slate-200/90 shadow-xs overflow-hidden">
        <!-- Loading State -->
        <div v-if="cargando" class="flex items-center justify-center py-20 text-slate-400">
          <div class="text-center">
            <i class="fas fa-circle-notch fa-spin text-3xl text-indigo-600 mb-3 block mx-auto"></i>
            <p class="text-sm font-medium">Cargando inscripciones...</p>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="inscripcionesPaginadas.length === 0" class="text-center py-16 px-4">
          <div class="w-14 h-14 rounded-2xl bg-indigo-50 border border-indigo-100 flex items-center justify-center text-indigo-600 text-2xl mx-auto mb-3">
            <i class="fas fa-users-slash"></i>
          </div>
          <h3 class="text-base font-bold text-slate-900 mb-1">No hay inscripciones registradas</h3>
          <p class="text-xs text-slate-500 max-w-sm mx-auto">
            {{ filtros.busqueda || filtros.eventoId ? 'No se encontraron resultados para los filtros seleccionados.' : 'Aún no hay participantes inscritos en este evento.' }}
          </p>
        </div>

        <!-- ── DATOS: un v-else que contiene ambos layouts ── -->
        <div v-else>

          <!-- VISTA MÓVIL: tarjetas apiladas (< md) -->
          <div class="md:hidden divide-y divide-slate-100">
            <div
              v-for="inscripcion in inscripcionesPaginadas"
              :key="inscripcion.id + '-card'"
              class="p-4 hover:bg-slate-50/70 transition-colors"
            >
              <!-- Cabecera de la tarjeta: nombre + monto -->
              <div class="flex items-start justify-between gap-3 mb-3">
                <div>
                  <p class="font-bold text-slate-900 text-sm leading-tight">
                    {{ inscripcion.participante?.nombre || 'N/A' }}
                  </p>
                  <p v-if="inscripcion.participante?.cedula" class="text-[11px] text-slate-500 mt-0.5">
                    <i class="fas fa-id-card mr-1 text-slate-400"></i>{{ inscripcion.participante.cedula }}
                  </p>
                </div>
                <span class="flex-shrink-0 font-bold text-emerald-700 bg-emerald-50 border border-emerald-200 rounded-lg px-2.5 py-1 text-sm">
                  ${{ Number(inscripcion.participante?.totalPrice || 0).toFixed(2) }}
                </span>
              </div>

              <!-- Grid de datos secundarios -->
              <div class="grid grid-cols-2 gap-x-4 gap-y-1.5 text-[11px] mb-3">
                <div v-if="inscripcion.participante?.telefono">
                  <span class="text-slate-400 font-semibold uppercase tracking-wide">WhatsApp</span>
                  <p class="text-slate-700"><i class="fas fa-phone mr-1 text-slate-400"></i>{{ inscripcion.participante.telefono }}</p>
                </div>
                <div v-if="inscripcion.participante?.correo">
                  <span class="text-slate-400 font-semibold uppercase tracking-wide">Correo</span>
                  <p class="text-slate-700 truncate">{{ inscripcion.participante.correo }}</p>
                </div>
                <div v-if="!eventoFijado">
                  <span class="text-slate-400 font-semibold uppercase tracking-wide">Evento</span>
                  <p class="text-slate-700">{{ obtenerNombreEvento(inscripcion.eventoId) }}</p>
                </div>
                <div v-if="inscripcion.participante?.iglesia">
                  <span class="text-slate-400 font-semibold uppercase tracking-wide">Iglesia</span>
                  <p class="text-slate-700">{{ inscripcion.participante.iglesia }}</p>
                </div>
                <div v-if="inscripcion.participante?.mentor">
                  <span class="text-slate-400 font-semibold uppercase tracking-wide">Mentor</span>
                  <p class="text-slate-700">{{ inscripcion.participante.mentor }}</p>
                </div>
                <div>
                  <span class="text-slate-400 font-semibold uppercase tracking-wide">Boleto</span>
                  <p class="text-slate-700">{{ inscripcion.participante?.ticketType || 'General' }}</p>
                </div>
                <div>
                  <span class="text-slate-400 font-semibold uppercase tracking-wide">Fecha</span>
                  <p class="text-slate-700">{{ formatearFecha(inscripcion.fechaInscripcion) }}</p>
                  <div v-if="obtenerEditor(inscripcion)" class="mt-1 text-[10px] text-indigo-700 bg-indigo-50 border border-indigo-100 rounded px-1.5 py-0.5 inline-flex items-center gap-1 font-medium" :title="'Editado por ' + obtenerEditor(inscripcion)">
                    <i class="fas fa-user-pen text-[9px]"></i>
                    <span class="truncate max-w-[130px]">{{ obtenerEditor(inscripcion) }}</span>
                  </div>
                </div>
              </div>

              <!-- Fila de acciones -->
              <div class="flex items-center gap-2 pt-2 border-t border-slate-100">
                <FileViewer
                  v-if="obtenerArchivos(inscripcion).length > 0"
                  :files="obtenerArchivos(inscripcion)"
                />
                <span v-else class="text-slate-400 text-[11px] italic flex-1">Sin adjunto</span>
                <div class="flex items-center gap-1.5 ml-auto">
                  <button
                    @click="abrirModalEdicion(inscripcion)"
                    class="p-2 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 transition-colors"
                    title="Editar"
                  >
                    <i class="fas fa-pen-to-square text-sm"></i>
                  </button>
                  <button
                    @click="confirmarEliminarInscripcion(inscripcion)"
                    class="p-2 rounded-lg bg-rose-50 hover:bg-rose-100 text-rose-600 border border-rose-100 transition-colors"
                    title="Eliminar"
                  >
                    <i class="fas fa-trash-can text-sm"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- VISTA ESCRITORIO: tabla (md+) -->
          <div class="hidden md:block overflow-x-auto">
            <table class="w-full text-left border-collapse">
              <thead class="bg-slate-900 text-slate-200 text-[11px] font-semibold uppercase tracking-wider">
                <tr>
                  <th class="px-5 py-3.5">Participante</th>
                  <th class="px-5 py-3.5">Evento</th>
                  <th class="px-5 py-3.5">Iglesia / Mentor</th>
                  <th class="px-5 py-3.5">Boleto / Cant.</th>
                  <th class="px-5 py-3.5">Monto Total</th>
                  <th class="px-5 py-3.5">Fecha Registro</th>
                  <th class="px-5 py-3.5">Comprobante</th>
                  <th class="px-5 py-3.5 text-center">Acciones</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 text-xs text-slate-700">
                <tr
                  v-for="inscripcion in inscripcionesPaginadas"
                  :key="inscripcion.id"
                  class="hover:bg-slate-50/80 transition-colors"
                >
                  <!-- Participante -->
                  <td class="px-5 py-4">
                    <div class="font-bold text-slate-900 text-sm mb-0.5">
                      {{ inscripcion.participante?.nombre || 'N/A' }}
                    </div>
                    <div class="text-slate-500 space-y-0.5 text-[11px]">
                      <div v-if="inscripcion.participante?.cedula">
                        <i class="fas fa-id-card text-slate-400 mr-1"></i>{{ inscripcion.participante?.cedula }}
                      </div>
                      <div v-if="inscripcion.participante?.telefono">
                        <i class="fas fa-phone text-slate-400 mr-1"></i>{{ inscripcion.participante?.telefono }}
                      </div>
                      <div v-if="inscripcion.participante?.correo">
                        <i class="fas fa-envelope text-slate-400 mr-1"></i>{{ inscripcion.participante?.correo }}
                      </div>
                    </div>
                  </td>

                  <!-- Evento -->
                  <td class="px-5 py-4">
                    <span class="font-semibold text-slate-800 block">
                      {{ obtenerNombreEvento(inscripcion.eventoId) }}
                    </span>
                  </td>

                  <!-- Iglesia / Mentor -->
                  <td class="px-5 py-4">
                    <div class="space-y-0.5">
                      <div class="font-medium text-slate-800">
                        {{ inscripcion.participante?.iglesia || 'N/A' }}
                      </div>
                      <div v-if="inscripcion.participante?.mentor" class="text-[11px] text-slate-500">
                        <span class="font-semibold text-slate-400">Mentor:</span> {{ inscripcion.participante?.mentor }}
                      </div>
                    </div>
                  </td>

                  <!-- Boleto / Cant. -->
                  <td class="px-5 py-4">
                    <div class="font-semibold text-slate-800">
                      {{ inscripcion.participante?.ticketType || 'General' }}
                    </div>
                    <div class="text-[11px] text-slate-500">
                      Cant: {{ inscripcion.participante?.ticketQuantity || 1 }}
                    </div>
                  </td>

                  <!-- Monto Total -->
                  <td class="px-5 py-4">
                    <span class="font-bold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-lg border border-emerald-200">
                      ${{ Number(inscripcion.participante?.totalPrice || 0).toFixed(2) }}
                    </span>
                  </td>

                  <!-- Fecha Registro & Auditoría -->
                  <td class="px-5 py-4 text-slate-500">
                    <div class="text-xs text-slate-700">
                      {{ formatearFecha(inscripcion.fechaInscripcion) }}
                    </div>
                    <div
                      v-if="obtenerEditor(inscripcion)"
                      class="mt-1 text-[10px] text-indigo-700 bg-indigo-50 border border-indigo-100 rounded px-1.5 py-0.5 inline-flex items-center gap-1 font-medium"
                      :title="'Última edición por ' + obtenerEditor(inscripcion)"
                    >
                      <i class="fas fa-user-pen text-[9px]"></i>
                      <span class="truncate max-w-[120px]">{{ obtenerEditor(inscripcion) }}</span>
                    </div>
                  </td>

                  <!-- Comprobante / Adjuntos -->
                  <td class="px-5 py-4">
                    <FileViewer
                      v-if="obtenerArchivos(inscripcion).length > 0"
                      :files="obtenerArchivos(inscripcion)"
                    />
                    <span v-else class="text-slate-400 text-[11px] italic">Sin adjunto</span>
                  </td>

                  <!-- Acciones -->
                  <td class="px-5 py-4 text-center">
                    <div class="inline-flex items-center gap-1.5">
                      <button
                        @click="abrirModalEdicion(inscripcion)"
                        class="p-2 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 transition-colors cursor-pointer"
                        title="Editar inscripción"
                      >
                        <i class="fas fa-pen-to-square"></i>
                      </button>
                      <button
                        @click="confirmarEliminarInscripcion(inscripcion)"
                        class="p-2 rounded-lg bg-rose-50 hover:bg-rose-100 text-rose-600 border border-rose-100 transition-colors cursor-pointer"
                        title="Eliminar inscripción"
                      >
                        <i class="fas fa-trash-can"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

        </div><!-- /v-else -->

        <!-- ── PAGINACIÓN INFERIOR ── -->
        <div
          v-if="!cargando && inscripcionesFiltradas.length > 0 && totalPaginas > 1"
          class="flex items-center justify-between px-5 py-4 border-t border-slate-100 bg-white"
        >
          <span class="text-xs text-slate-500">
            Página <span class="font-bold text-slate-800">{{ paginaActual }}</span> de <span class="font-bold text-slate-800">{{ totalPaginas }}</span>
            &nbsp;·&nbsp; {{ inscripcionesFiltradas.length }} inscrito{{ inscripcionesFiltradas.length !== 1 ? 's' : '' }}
          </span>

          <div class="flex items-center gap-1.5">
            <button
              @click="paginaActual = 1"
              :disabled="paginaActual === 1"
              class="w-8 h-8 rounded-lg border border-slate-200 bg-white text-slate-500 hover:bg-slate-50 disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-center text-xs transition-colors"
              title="Primera página"
            >
              <i class="fas fa-angles-left"></i>
            </button>
            <button
              @click="paginaActual--"
              :disabled="paginaActual === 1"
              class="w-8 h-8 rounded-lg border border-slate-200 bg-white text-slate-500 hover:bg-slate-50 disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-center text-xs transition-colors"
              title="Página anterior"
            >
              <i class="fas fa-chevron-left"></i>
            </button>

            <!-- Números de página (máx 5 visibles) -->
            <template v-for="n in totalPaginas" :key="n">
              <button
                v-if="n === 1 || n === totalPaginas || Math.abs(n - paginaActual) <= 1"
                @click="paginaActual = n"
                class="w-8 h-8 rounded-lg border text-xs font-semibold transition-colors"
                :class="n === paginaActual
                  ? 'bg-indigo-600 border-indigo-600 text-white shadow-sm'
                  : 'border-slate-200 bg-white text-slate-600 hover:bg-slate-50'"
              >{{ n }}</button>
              <span
                v-else-if="n === paginaActual - 2 || n === paginaActual + 2"
                class="text-slate-400 text-xs px-0.5"
              >…</span>
            </template>

            <button
              @click="paginaActual++"
              :disabled="paginaActual >= totalPaginas"
              class="w-8 h-8 rounded-lg border border-slate-200 bg-white text-slate-500 hover:bg-slate-50 disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-center text-xs transition-colors"
              title="Página siguiente"
            >
              <i class="fas fa-chevron-right"></i>
            </button>
            <button
              @click="paginaActual = totalPaginas"
              :disabled="paginaActual >= totalPaginas"
              class="w-8 h-8 rounded-lg border border-slate-200 bg-white text-slate-500 hover:bg-slate-50 disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-center text-xs transition-colors"
              title="Última página"
            >
              <i class="fas fa-angles-right"></i>
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
      :evento-opciones="obtenerOpcionesEvento(inscripcionSeleccionada?.eventoId)"
      @close="cerrarModalEdicion"
      @save="guardarCambios"
    />

    <!-- Modal de Gestión de Iglesias y Mentores -->
    <ConfiguracionIglesiasModal
      :show="mostrarConfigIglesias"
      @close="mostrarConfigIglesias = false"
    />

    <!-- Modal de Gestión de Usuarios y Roles -->
    <GestionUsuariosModal
      :show="mostrarGestionUsuarios"
      @close="mostrarGestionUsuarios = false"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useEventosStore } from '../stores/eventos'
import { auth } from '../firebase'
import FileViewer from '../components/FileViewer.vue'
import EditInscripcionModal from '../components/EditInscripcionModal.vue'
import ConfiguracionIglesiasModal from '../components/ConfiguracionIglesiasModal.vue'
import GestionUsuariosModal from '../components/GestionUsuariosModal.vue'

const router = useRouter()
const route = useRoute()
const eventosStore = useEventosStore()

const mostrarConfigIglesias = ref(false)
const mostrarGestionUsuarios = ref(false)

const todasInscripciones = ref([])
const eventos = ref([])
const cargando = ref(false)
const paginaActual = ref(1)
const itemsPorPagina = ref(15)
const mostrarModalEdicion = ref(false)
const inscripcionSeleccionada = ref(null)

const filtros = ref({
  busqueda: '',
  eventoId: ''
})

// true cuando la página fue abierta desde el botón de un evento específico
const eventoFijado = computed(() => !!route.query.eventoId)

const eventoActual = computed(() => {
  if (!filtros.value.eventoId) return null
  return eventos.value.find(e => e.id === filtros.value.eventoId)
})

// Sincronizar filtros.eventoId con la URL para sobrevivir al refresh
watch(
  () => route.query.eventoId,
  (nuevoId) => {
    filtros.value.eventoId = nuevoId || ''
  },
  { immediate: true }
)

const obtenerNombreEvento = (eventoId) => {
  const ev = eventos.value.find(e => e.id === eventoId)
  return ev ? ev.titulo : 'Evento'
}

const obtenerOpcionesEvento = (eventoId) => {
  const ev = eventos.value.find(e => e.id === eventoId)
  return ev ? ev.opciones : null
}

// Recibe la inscripción completa para poder leer tanto participante como comprobantesAdicionales (raíz)
const obtenerArchivos = (inscripcion) => {
  if (!inscripcion) return []
  const urls = []

  // Comprobantes del registro inicial (dentro de participante)
  const p = inscripcion.participante || inscripcion // retrocompatibilidad
  if (Array.isArray(p.comprobantesUrls)) {
    urls.push(...p.comprobantesUrls)
  } else if (p.comprobanteUrl) {
    urls.push(p.comprobanteUrl)
  }

  // Comprobantes adicionales agregados vía "Hacer Otro Pago" (raíz del documento)
  const adicionales = inscripcion.comprobantesAdicionales || []
  for (const ca of adicionales) {
    if (ca.url) urls.push(ca.url)
  }

  return urls
}

const formatearFecha = (fecha) => {
  if (!fecha) return 'N/A'
  try {
    const d = new Date(fecha)
    return d.toLocaleDateString('es-ES', { month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit' })
  } catch (e) {
    return fecha
  }
}

const calcularIngresoTotal = computed(() => {
  return inscripcionesFiltradas.value.reduce((acc, ins) => {
    const price = Number(ins.participante?.totalPrice || 0)
    return acc + price
  }, 0).toFixed(2)
})

// Suma de ticketPrice × ticketQuantity: lo que DEBERÍA haberse cobrado según el boleto seleccionado
const calcularTotalEsperado = computed(() => {
  return inscripcionesFiltradas.value.reduce((acc, ins) => {
    const precio = Number(ins.participante?.ticketPrice || 0)
    const cantidad = Number(ins.participante?.ticketQuantity || 1)
    return acc + precio * cantidad
  }, 0).toFixed(2)
})

onMounted(async () => {
  const unsubscribe = auth.onAuthStateChanged(user => {
    unsubscribe()
    if (!user) {
      router.push('/admin-login')
    } else {
      cargarDatos()
    }
  })
})

const cargarDatos = async () => {
  if (typeof eventosStore.cargarEventos === 'function') {
    await eventosStore.cargarEventos()
  }
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

const inscripcionesFiltradas = computed(() => {
  let resultado = [...todasInscripciones.value]

  if (filtros.value.eventoId) {
    resultado = resultado.filter(ins => ins.eventoId === filtros.value.eventoId)
  }

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

const totalPaginas = computed(() => {
  return Math.ceil(inscripcionesFiltradas.value.length / itemsPorPagina.value) || 1
})

const inscripcionesPaginadas = computed(() => {
  const inicio = (paginaActual.value - 1) * itemsPorPagina.value
  return inscripcionesFiltradas.value.slice(inicio, inicio + itemsPorPagina.value)
})

const obtenerEditor = (inscripcion) => {
  if (!inscripcion) return null
  return inscripcion.editadoPor || inscripcion.participante?.editadoPor || inscripcion.ultimaModificacion?.por || null
}

const abrirModalEdicion = (inscripcion) => {
  inscripcionSeleccionada.value = { ...inscripcion }
  mostrarModalEdicion.value = true
}

const cerrarModalEdicion = () => {
  mostrarModalEdicion.value = false
  inscripcionSeleccionada.value = null
}

// Resetear a página 1 cuando cambia el filtro de búsqueda o evento
watch([() => filtros.value.busqueda, () => filtros.value.eventoId], () => {
  paginaActual.value = 1
})

const guardarCambios = async (datosActualizados) => {
  try {
    const id = inscripcionSeleccionada.value.id
    await eventosStore.actualizarInscripcion(id, datosActualizados)

    // Actualización local optimista para evitar recargar 270+ registros
    const idx = todasInscripciones.value.findIndex(item => item.id === id)
    if (idx !== -1) {
      todasInscripciones.value[idx] = {
        ...todasInscripciones.value[idx],
        ...datosActualizados,
        participante: {
          ...todasInscripciones.value[idx].participante,
          ...(datosActualizados.participante || {})
        }
      }
    }
    cerrarModalEdicion()
  } catch (e) {
    console.error('Error actualizando inscripción:', e)
    alert('❌ Ocurrió un error al guardar los cambios en la base de datos.')
  }
}

const confirmarEliminarInscripcion = async (inscripcion) => {
  const nombre = inscripcion.participante?.nombre || 'este participante'
  const confirmed = window.confirm(`¿Estás seguro de que deseas eliminar permanentemente la inscripción de "${nombre}"?\n\nEsta acción no se puede deshacer.`)
  if (!confirmed) return

  try {
    await eventosStore.eliminarInscripcion(inscripcion.id)
    // Eliminación local optimista
    todasInscripciones.value = todasInscripciones.value.filter(i => i.id !== inscripcion.id)
  } catch (e) {
    console.error('Error eliminando inscripción:', e)
    alert('❌ Ocurrió un error al intentar eliminar la inscripción.')
  }
}

const escapeCsv = (val) => {
  if (val === undefined || val === null) return ''
  const str = String(val)
  if (str.includes(',') || str.includes('"') || str.includes('\n')) {
    return '"' + str.replace(/"/g, '""') + '"'
  }
  return str
}

const exportarCSV = () => {
  if (inscripcionesFiltradas.value.length === 0) return
  const headers = [
    'Evento',
    'ID Registro',
    'Nombre',
    'Cédula',
    'Teléfono',
    'Correo',
    'Edad',
    'Iglesia',
    'Mentor',
    'Boleto',
    'Cantidad',
    'Precio Unitario ($)',
    'Monto Total ($)',
    'Monto Pagado Inicial ($)',
    'Comprobantes Adjuntos',
    'Fecha Registro'
  ]
  const rows = [headers.join(',')]

  inscripcionesFiltradas.value.forEach(ins => {
    const p = ins.participante || {}
    const archs = obtenerArchivos(ins)
    const r = [
      obtenerNombreEvento(ins.eventoId),
      p.registrationToken || ins.id || '',
      p.nombre || '',
      p.cedula || '',
      p.telefono || '',
      p.correo || '',
      p.edad !== undefined && p.edad !== null ? p.edad : '',
      p.iglesia || '',
      p.mentor || '',
      p.ticketType || 'General',
      p.ticketQuantity || 1,
      Number(p.ticketPrice || 0).toFixed(2),
      Number(p.totalPrice || 0).toFixed(2),
      Number(p.montoPagado || p.monto || 0).toFixed(2),
      archs.length,
      formatearFecha(ins.fechaInscripcion)
    ]
    rows.push(r.map(escapeCsv).join(','))
  })

  const csvContent = '\uFEFF' + rows.join('\r\n') // BOM UTF-8 para Excel
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url

  const nombreEvento = eventoActual.value ? eventoActual.value.titulo.toLowerCase().replace(/\s+/g, '_') : 'eventos'
  a.download = `inscripciones_${nombreEvento}_${new Date().toISOString().slice(0,10)}.csv`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}
</script>
