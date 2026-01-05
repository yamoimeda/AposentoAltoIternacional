<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-900 to-purple-900 py-12 pt-25">
    <!-- Efectos de fondo hero igual que InicioView -->
  <div class="absolute top-20 left-10 w-72 h-72 bg-gray-200 rounded-full mix-blend-multiply filter blur-3xl opacity-10 animate-float"></div>
  <div class="absolute top-40 right-10 w-72 h-72 bg-gray-200 rounded-full mix-blend-multiply filter blur-3xl opacity-10 animate-float" style="animation-delay: 2s;"></div>
  <div class="absolute bottom-20 left-1/2 w-72 h-72 bg-gray-200 rounded-full mix-blend-multiply filter blur-3xl opacity-10 animate-float" style="animation-delay: 4s;"></div>
    <!-- Partículas flotantes -->
    <div class="absolute inset-0 overflow-hidden">
  <div class="absolute top-1/4 left-1/4 w-2 h-2 bg-white rounded-full opacity-60 animate-pulse"></div>
  <div class="absolute top-1/3 right-1/4 w-1 h-1 bg-gray-200 rounded-full opacity-80 animate-pulse" style="animation-delay: 1s;"></div>
  <div class="absolute bottom-1/3 left-1/3 w-3 h-3 bg-gray-200 rounded-full opacity-40 animate-pulse" style="animation-delay: 2s;"></div>
  <div class="absolute top-2/3 right-1/3 w-2 h-2 bg-blue-100 rounded-full opacity-70 animate-pulse" style="animation-delay: 3s;"></div>
    </div>
    
    <!-- Header del panel -->
    <div class=" mx-auto px-4 relative z-10">
  <div class="text-center mb-12">
        <!-- <div class="w-20 h-20 bg-gradient-to-br from-purple-600 to-blue-400 rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg">
          <i class="fas fa-cogs text-white text-3xl"></i>
        </div> -->
        <h1 class="text-5xl font-black text-white mb-4">Panel de Administración</h1>
        <p class="text-xl text-gray-200 mb-6">Gestiona los eventos de la iglesia</p>
        <div class="flex gap-4 justify-center">
          <button @click="mostrarCrearEvento = true" class="py-2 px-6 rounded-lg bg-blue-600 text-white font-semibold shadow-md hover:bg-blue-700 transition-all flex items-center gap-2">
            <i class="fas fa-plus-circle"></i>
            Crear Nuevo Evento
          </button>
          <!-- <button @click="irAInscripciones" class="py-2 px-6 rounded-lg bg-purple-600 text-white font-semibold shadow-md hover:bg-purple-700 transition-all flex items-center gap-2">
            <i class="fas fa-users-cog"></i>
            Gestionar Inscripciones
          </button> -->
        </div>
      </div>


      <!-- Crear Nuevo Evento -->
      <!-- <div class="max-w-2xl mx-auto bg-white/80 backdrop-blur-lg rounded-3xl shadow-2xl p-8 border border-purple-200 relative z-10 mb-12"> -->
      <EventForm v-if="mostrarCrearEvento" :initialEvent="editingEvent" @save="onFormSave" @close="closeForm" />

      <!-- Lista de Eventos -->
      <div class="mx-auto bg-white rounded-3xl shadow-md p-8 border border-gray-200 relative z-10">
        <div class="flex flex-col mb-6">
          <!-- <div class="w-16 h-16 bg-gradient-to-br from-blue-400 via-purple-500 to-cyan-400 rounded-full flex items-center justify-center mb-2 shadow-lg">
            <i class="fas fa-calendar-alt text-white text-2xl"></i>
          </div> -->
          <h3 class="text-2xl font-bold text-gray-800 mb-2">Eventos Creados</h3>
        </div>
        
        <div v-if="loading" class="text-center py-8 text-gray-500">
          <i class="fas fa-spinner fa-spin text-3xl mb-4"></i>
          <p>Cargando eventos...</p>
        </div>
        
        <div v-else-if="eventos.length === 0" class="text-center py-8 text-gray-500">
          <i class="fas fa-calendar-times text-3xl mb-4"></i>
          <p>No hay eventos creados</p>
        </div>
        
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          <div v-for="evento in eventos" 
               :key="evento.id" 
               class="bg-white rounded-xl p-4 shadow-sm flex flex-col border border-gray-100">
            <div class="flex-1">
              <h4 class="font-bold text-lg text-gray-800 mb-2 line-clamp-2">{{ evento.titulo }}</h4>
              <div class="flex flex-col text-sm text-purple-500 mb-2 space-y-1">
                <div class="flex items-center">
                  <i class="fas fa-calendar mr-2"></i>
                  <span class="truncate">{{ evento.fecha }}</span>
                </div>
                <div class="flex items-center">
                  <i class="fas fa-map-marker-alt mr-2"></i>
                  <span class="truncate">{{ evento.lugar }}</span>
                </div>
              </div>
              <p class="text-gray-700 text-sm line-clamp-3">{{ evento.descripcion }}</p>
            </div>
            <div class="flex flex-col gap-2 mt-4">
              <button @click="verInscripcionesEvento(evento.id)" 
                      class="w-full px-4 py-2 rounded-lg bg-green-600 text-white text-sm font-semibold shadow hover:bg-green-700 transition-all">
                <i class="fas fa-users mr-1"></i>Ver Inscripciones
              </button>
              <div class="flex gap-2">
                <button @click="editEvent(evento)" 
                        class="flex-1 px-4 py-2 rounded-lg bg-blue-600 text-white text-sm font-semibold shadow hover:bg-blue-700 transition-all">
                  <i class="fas fa-edit mr-1"></i>Editar
                </button>
                <button @click="confirmDelete(evento)" 
                        class="flex-1 px-4 py-2 rounded-lg bg-gray-200 text-gray-800 text-sm font-semibold shadow hover:bg-gray-300 transition-all">
                  <i class="fas fa-trash mr-1"></i>Eliminar
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { db, auth, storage } from '../firebase'
import { collection, addDoc, getDocs, deleteDoc, doc, onSnapshot, query, orderBy, updateDoc } from 'firebase/firestore'
import { ref as storageRef, uploadBytes, getDownloadURL, deleteObject } from 'firebase/storage'
import { useRouter } from 'vue-router'
import { signOut } from 'firebase/auth'
import { v4 as uuidv4 } from 'uuid'
import EventForm from '../components/EventForm.vue'


const router = useRouter()
const eventos = ref([])
const loading = ref(true)
// form state moved to EventForm component
const mostrarCrearEvento = ref(false)
const mostrarEventos = ref(false)
const editingEvent = ref(null)
const selectedImage = ref(null) // used temporarily when saving from child

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
  const eventosRef = collection(db, 'eventos')
  const q = query(eventosRef, orderBy('fecha', 'desc'))
  onSnapshot(q, (snapshot) => {
    eventos.value = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }))
    loading.value = false
  })
}

// image handling is done in EventForm and passed up on save

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
    // Create a reference from the URL and delete
    const fileRef = storageRef(storage, url)
    // Note: storageRef(storage, url) expects a path, not a full URL. Try extracting path if needed.
    // If url is a full download URL, attempt to extract the path after '/o/' and decode it.
    if (url.startsWith('http')) {
      try {
        const decoded = decodeURIComponent(url.split('/o/')[1].split('?')[0])
        const path = decoded
        const r = storageRef(storage, path)
        await deleteObject(r)
        return
      } catch (e) {
        // fallback below
      }
    }
    await deleteObject(fileRef)
  } catch (e) {
    console.warn('Could not delete previous banner:', e)
  }
}

// Handler called when EventForm emits save
const onFormSave = async ({ eventData, imageFile }) => {
  // basic validation
  if (!eventData.titulo || !eventData.fecha || !eventData.lugar) return

  try {
    if (editingEvent.value) {
      const eventRef = doc(db, 'eventos', editingEvent.value.id)
      let updateData = { ...eventData }

      if (imageFile) {
        // delete previous banner if exists
        if (editingEvent.value.bannerUrl) {
          await deleteStorageFileByUrl(editingEvent.value.bannerUrl)
        }
        const bannerUrl = await uploadImage(editingEvent.value.eventId, imageFile)
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
        createdAt: new Date().toISOString()
      })
    }
    closeForm()
    return true
  } catch (error) {
    console.error('Error:', error)
    return false
  }
}

const editEvent = (evento) => {
  // Pass the selected event object to the EventForm via the `editingEvent` prop
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

// Ask for confirmation and delete event + banner if confirmed
const confirmDelete = async (evento) => {
  const confirmed = window.confirm(`¿Seguro que deseas eliminar el evento "${evento.titulo}"? Esta acción no se puede deshacer.`)
  if (!confirmed) return

  // Attempt to delete banner from storage if present
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
