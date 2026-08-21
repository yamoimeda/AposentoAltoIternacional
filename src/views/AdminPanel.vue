<template>
  <div class="min-h-screen bg-slate-50/80 font-sans text-slate-800 pt-28 pb-16 px-4 sm:px-8">
    <div class="max-w-7xl mx-auto">
      <!-- Enterprise Page Header & Actions Bar -->
      <div class="mb-8 flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-200/80">
        <div>
          <div class="flex items-center gap-2 text-xs font-medium text-slate-500 mb-1.5">
            <router-link to="/" class="hover:text-indigo-600 transition-colors">Inicio</router-link>
            <span>/</span>
            <span class="text-slate-900 font-semibold">Panel de Administración</span>
          </div>
          <h1 class="text-2xl sm:text-3xl font-bold tracking-tight text-slate-900">
            Gestión de Eventos
          </h1>
          <p class="text-xs sm:text-sm text-slate-500 mt-1">
            Administra los eventos institucionales, tipos de entradas y registros de participantes.
          </p>
        </div>

        <div class="flex flex-wrap items-center gap-3">
          <router-link
            to="/conteo"
            class="py-2.5 px-4 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 font-semibold text-xs sm:text-sm rounded-xl shadow-xs transition-all flex items-center gap-2"
            title="Ver contadores compartibles sin tabla"
          >
            <i class="fas fa-chart-pie text-indigo-600"></i>
            <span>Conteo en Vivo</span>
          </router-link>

          <router-link
            to="/escanear-qr"
            class="py-2.5 px-4 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 font-semibold text-xs sm:text-sm rounded-xl shadow-xs transition-all flex items-center gap-2"
            title="Escanear boletos con cámara"
          >
            <i class="fas fa-qrcode text-indigo-600"></i>
            <span>Escanear QR</span>
          </router-link>

          <button
            @click="mostrarGestionUsuarios = true"
            class="py-2.5 px-4 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 font-semibold text-xs sm:text-sm rounded-xl shadow-xs transition-all flex items-center gap-2 cursor-pointer"
          >
            <i class="fas fa-users-gear text-indigo-600"></i>
            <span>Usuarios y Roles</span>
          </button>

          <button
            @click="mostrarConfigIglesias = true"
            class="py-2.5 px-4 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 font-semibold text-xs sm:text-sm rounded-xl shadow-xs transition-all flex items-center gap-2 cursor-pointer"
          >
            <i class="fas fa-church text-indigo-600"></i>
            <span>Iglesias y Mentores</span>
          </button>

          <button
            @click="abrirCrearEvento"
            class="py-2.5 px-5 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs sm:text-sm rounded-xl shadow-md shadow-indigo-600/20 transition-all flex items-center gap-2 cursor-pointer"
          >
            <i class="fas fa-plus-circle"></i>
            <span>Crear Nuevo Evento</span>
          </button>
        </div>
      </div>

      <!-- KPI Summary Cards -->
      <div class="mb-8">
        <!-- Combined Event Stats Card -->
        <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-xs flex items-center justify-between divide-x divide-slate-100 max-w-xl">
          <div class="flex items-center gap-3.5 pr-4 flex-1">
            <div class="w-11 h-11 rounded-xl bg-indigo-50 border border-indigo-100 flex items-center justify-center text-indigo-600 text-lg shrink-0">
              <i class="fas fa-calendar-check"></i>
            </div>
            <div>
              <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider block">Total Eventos</span>
              <span class="text-2xl font-bold text-slate-900">{{ eventos.length }}</span>
            </div>
          </div>

          <div class="flex items-center gap-3.5 pl-6 flex-1">
            <div class="w-11 h-11 rounded-xl bg-emerald-50 border border-emerald-100 flex items-center justify-center text-emerald-600 text-lg shrink-0">
              <i class="fas fa-clock"></i>
            </div>
            <div>
              <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider block">Próximos</span>
              <span class="text-2xl font-bold text-slate-900">{{ proximosCount }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal / EventForm Component -->
      <transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="opacity-0 scale-95"
        enter-to-class="opacity-100 scale-100"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="opacity-100 scale-100"
        leave-to-class="opacity-0 scale-95"
      >
        <EventForm
          v-if="mostrarCrearEvento"
          :initialEvent="editingEvent"
          @save="onFormSave"
          @close="closeForm"
        />
      </transition>

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

      <!-- Search Toolbar & List Header -->
      <div class="bg-white p-4 sm:p-5 rounded-2xl border border-slate-200/80 shadow-xs mb-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div class="relative w-full sm:w-80">
          <i class="fas fa-search absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-sm"></i>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Buscar por título o lugar..."
            class="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:bg-white focus:border-indigo-600 transition-all text-slate-800 placeholder-slate-400"
          />
        </div>

        <div class="text-xs text-slate-500 font-medium self-end sm:self-center">
          Mostrando <span class="font-bold text-slate-800">{{ filteredEventos.length }}</span> de {{ eventos.length }} eventos
        </div>
      </div>

      <!-- Events List Grid -->
      <div>
        <!-- Loading State -->
        <div v-if="loading" class="bg-white rounded-2xl border border-slate-200 p-12 text-center text-slate-400 shadow-xs">
          <i class="fas fa-circle-notch fa-spin text-3xl text-indigo-600 mb-3 block mx-auto"></i>
          <p class="text-sm font-medium">Cargando catálogo de eventos desde la nube...</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="filteredEventos.length === 0" class="bg-white rounded-2xl border border-slate-200 p-12 text-center shadow-xs">
          <div class="w-16 h-16 rounded-2xl bg-indigo-50 border border-indigo-100 flex items-center justify-center text-indigo-600 text-2xl mx-auto mb-4">
            <i class="fas fa-calendar-xmark"></i>
          </div>
          <h3 class="text-lg font-bold text-slate-900 mb-1">No se encontraron eventos</h3>
          <p class="text-xs sm:text-sm text-slate-500 max-w-sm mx-auto mb-6">
            {{ searchQuery ? 'No hay resultados que coincidan con la búsqueda.' : 'Aún no se han creado eventos en la plataforma.' }}
          </p>
          <button
            @click="abrirCrearEvento"
            class="py-2.5 px-5 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs sm:text-sm rounded-xl shadow-md transition-all inline-flex items-center gap-2 cursor-pointer"
          >
            <i class="fas fa-plus"></i>
            <span>Crear primer evento</span>
          </button>
        </div>

        <!-- Grid of Events -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="evento in filteredEventos"
            :key="evento.id"
            class="bg-white rounded-2xl border border-slate-200/90 shadow-xs hover:shadow-md hover:border-slate-300 transition-all duration-200 flex flex-col overflow-hidden group"
          >
            <!-- Banner Image Preview -->
            <div class="relative h-44 w-full bg-slate-900 overflow-hidden">
              <img
                v-if="evento.bannerUrl || evento.imagen"
                :src="evento.bannerUrl || evento.imagen"
                :alt="evento.titulo"
                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
              />
              <div v-else class="w-full h-full bg-gradient-to-br from-indigo-900 via-slate-900 to-indigo-950 flex items-center justify-center">
                <i class="fas fa-church text-indigo-400/40 text-4xl"></i>
              </div>

              <!-- Top Status Pills -->
              <div class="absolute top-3 left-3 right-3 flex items-center justify-between pointer-events-none">
                <span class="px-2.5 py-1 rounded-lg text-xs font-bold bg-white/90 backdrop-blur-md text-slate-800 shadow-xs border border-white/40">
                  <i class="fas fa-calendar-day text-indigo-600 mr-1"></i>
                  {{ formatearFecha(evento.fecha) }}
                </span>

                <span
                  :class="[
                    'px-2.5 py-1 rounded-lg text-xs font-bold backdrop-blur-md shadow-xs border',
                    evento.esGratis || evento.precio === 0
                      ? 'bg-emerald-500/90 text-white border-emerald-400/40'
                      : 'bg-indigo-600/90 text-white border-indigo-500/40'
                  ]"
                >
                  {{ evento.esGratis || evento.precio === 0 ? 'Gratuito' : `$${evento.precio}` }}
                </span>
              </div>
            </div>

            <!-- Card Content Body -->
            <div class="p-5 flex-1 flex flex-col justify-between">
              <div>
                <h3 class="font-bold text-lg text-slate-900 mb-2 leading-snug group-hover:text-indigo-600 transition-colors line-clamp-2">
                  {{ evento.titulo }}
                </h3>

                <div class="space-y-1.5 text-xs text-slate-500 mb-3">
                  <div class="flex items-center gap-2">
                    <i class="fas fa-clock text-indigo-500 shrink-0 w-4"></i>
                    <span>{{ evento.hora || 'Hora por confirmar' }}</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <i class="fas fa-location-dot text-indigo-500 shrink-0 w-4"></i>
                    <span class="truncate">{{ evento.lugar || 'Lugar por confirmar' }}</span>
                  </div>
                </div>

                <p v-if="evento.descripcion" class="text-xs text-slate-600 line-clamp-3 leading-relaxed mb-4">
                  {{ evento.descripcion }}
                </p>

                <!-- Trazabilidad de Auditoría en la Tarjeta -->
                <div v-if="evento.editadoPor || evento.creadoPor" class="text-[10px] text-slate-400 flex items-center gap-1.5 truncate mb-3 bg-slate-50 border border-slate-100 px-2 py-1 rounded-md">
                  <i class="fas fa-user-pen text-slate-400 text-[10px]"></i>
                  <span class="truncate">
                    {{ evento.editadoPor ? 'Últ. edición:' : 'Creado por:' }}
                    <b class="text-slate-700 font-medium">{{ evento.editadoPor || evento.creadoPor }}</b>
                  </span>
                </div>
              </div>

              <!-- Action Toolbar -->
              <div class="pt-4 border-t border-slate-100 flex flex-col gap-2">
                <button
                  @click="verInscripcionesEvento(evento.id)"
                  class="w-full py-2 px-3 rounded-xl bg-indigo-50 hover:bg-indigo-100 text-indigo-700 text-xs font-semibold border border-indigo-100 transition-colors flex items-center justify-center gap-1.5 cursor-pointer"
                >
                  <i class="fas fa-users-viewfinder"></i>
                  <span>Ver Inscripciones de este Evento</span>
                </button>

                <div class="flex gap-2">
                  <button
                    @click="editEvent(evento)"
                    class="flex-1 py-2 px-3 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold transition-colors flex items-center justify-center gap-1.5 cursor-pointer"
                  >
                    <i class="fas fa-pen-to-square text-slate-500"></i>
                    <span>Editar</span>
                  </button>

                  <button
                    @click="confirmDelete(evento)"
                    class="py-2 px-3 rounded-xl bg-rose-50 hover:bg-rose-100 text-rose-600 text-xs font-semibold border border-rose-100 transition-colors flex items-center justify-center gap-1.5 cursor-pointer"
                    title="Eliminar Evento"
                  >
                    <i class="fas fa-trash-can"></i>
                  </button>
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
import { ref, computed, onMounted } from 'vue'
import { db, auth, storage } from '../firebase'
import { collection, addDoc, deleteDoc, doc, onSnapshot, query, orderBy, updateDoc } from 'firebase/firestore'
import { ref as storageRef, uploadBytes, getDownloadURL, deleteObject } from 'firebase/storage'
import { useRouter } from 'vue-router'
import { signOut } from 'firebase/auth'
import { v4 as uuidv4 } from 'uuid'
import EventForm from '../components/EventForm.vue'
import ConfiguracionIglesiasModal from '../components/ConfiguracionIglesiasModal.vue'
import GestionUsuariosModal from '../components/GestionUsuariosModal.vue'

const router = useRouter()
const eventos = ref([])
const loading = ref(true)
const searchQuery = ref('')
const mostrarCrearEvento = ref(false)
const mostrarConfigIglesias = ref(false)
const mostrarGestionUsuarios = ref(false)
const editingEvent = ref(null)
const selectedImage = ref(null)

const userEmail = computed(() => {
  return auth.currentUser ? auth.currentUser.email : 'Administrador'
})

const proximosCount = computed(() => {
  const hoy = new Date().toISOString().split('T')[0]
  return eventos.value.filter(e => e.fecha >= hoy).length
})

const filteredEventos = computed(() => {
  if (!searchQuery.value.trim()) return eventos.value
  const q = searchQuery.value.toLowerCase()
  return eventos.value.filter(e =>
    (e.titulo && e.titulo.toLowerCase().includes(q)) ||
    (e.lugar && e.lugar.toLowerCase().includes(q)) ||
    (e.descripcion && e.descripcion.toLowerCase().includes(q))
  )
})

const formatearFecha = (fecha) => {
  if (!fecha) return 'Fecha TBD'
  try {
    const parts = fecha.split('-')
    if (parts.length === 3) {
      const d = new Date(parts[0], parts[1] - 1, parts[2])
      return d.toLocaleDateString('es-ES', { month: 'short', day: 'numeric', year: 'numeric' })
    }
    return fecha
  } catch (e) {
    return fecha
  }
}

const abrirCrearEvento = () => {
  editingEvent.value = null
  mostrarCrearEvento.value = true
}

const irAInscripciones = () => {
  router.push('/admin/inscripciones')
}

const verInscripcionesEvento = (eventoId) => {
  router.push({
    path: '/admin/inscripciones',
    query: { eventoId }
  })
}

const fetchEventos = () => {
  try {
    const eventosRef = collection(db, 'eventos')
    const q = query(eventosRef, orderBy('fecha', 'desc'))
    onSnapshot(q, (snapshot) => {
      eventos.value = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }))
      loading.value = false
    }, (err) => {
      console.warn('Snapshot listener notice:', err)
      loading.value = false
    })
  } catch (e) {
    console.error('Error fetching eventos:', e)
    loading.value = false
  }
}

const uploadImage = async (eventId, file) => {
  if (!file) return null
  const imageRef = storageRef(storage, `eventos/${eventId}/banner.jpg`)
  await uploadBytes(imageRef, file)
  const imageUrl = await getDownloadURL(imageRef)
  return imageUrl
}

const deleteStorageFileByUrl = async (url) => {
  if (!url) return
  try {
    if (url.startsWith('http')) {
      const decoded = decodeURIComponent(url.split('/o/')[1].split('?')[0])
      const r = storageRef(storage, decoded)
      await deleteObject(r)
      return
    }
    const fileRef = storageRef(storage, url)
    await deleteObject(fileRef)
  } catch (e) {
    console.warn('Could not delete banner file:', e)
  }
}

const onFormSave = async ({ eventData, imageFile }) => {
  if (!eventData.titulo || !eventData.fecha || !eventData.lugar) return

  try {
    const ahora = new Date().toISOString()
    const usuarioActualEmail = auth.currentUser?.email || auth.currentUser?.displayName || 'Administrador'

    if (editingEvent.value) {
      const eventRef = doc(db, 'eventos', editingEvent.value.id)
      let updateData = {
        ...eventData,
        editadoPor: usuarioActualEmail,
        updatedAt: ahora,
        ultimaModificacion: {
          por: usuarioActualEmail,
          fecha: ahora
        }
      }

      if (imageFile) {
        if (editingEvent.value.bannerUrl) {
          await deleteStorageFileByUrl(editingEvent.value.bannerUrl)
        }
        const bannerUrl = await uploadImage(editingEvent.value.eventId || editingEvent.value.id, imageFile)
        updateData.bannerUrl = bannerUrl
      }

      await updateDoc(eventRef, updateData)
    } else {
      const eventId = uuidv4()
      const storagePath = `eventos/${eventId}/imagenes`
      const bannerUrl = imageFile ? await uploadImage(eventId, imageFile) : null

      await addDoc(collection(db, 'eventos'), {
        ...eventData,
        eventId,
        storagePath,
        bannerUrl,
        creadoPor: usuarioActualEmail,
        createdAt: ahora,
        ultimaModificacion: {
          por: usuarioActualEmail,
          fecha: ahora
        }
      })
    }
    closeForm()
    return true
  } catch (error) {
    console.error('Error saving event:', error)
    return false
  }
}

const editEvent = (evento) => {
  editingEvent.value = evento
  mostrarCrearEvento.value = true
}

const closeForm = () => {
  selectedImage.value = null
  editingEvent.value = null
  mostrarCrearEvento.value = false
}

const deleteEvent = async (id) => {
  try {
    await deleteDoc(doc(db, 'eventos', id))
  } catch (e) {
    console.error('Error deleting event:', e)
  }
}

const confirmDelete = async (evento) => {
  const confirmed = window.confirm(`¿Seguro que deseas eliminar el evento "${evento.titulo}"? Esta acción no se puede deshacer.`)
  if (!confirmed) return

  if (evento.bannerUrl) {
    try {
      await deleteStorageFileByUrl(evento.bannerUrl)
    } catch (e) {
      console.warn('No se pudo eliminar el banner del storage:', e)
    }
  }

  await deleteEvent(evento.id)
}

const logout = async () => {
  await signOut(auth)
  router.push('/admin-login')
}

onMounted(() => {
  fetchEventos()
})
</script>
