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
        <h1 class="text-5xl font-black text-blue-700 mb-4">Panel de Administración</h1>
        <p class="text-xl text-gray-200 mb-6">Gestiona los eventos de la iglesia</p>
        <button @click="mostrarCrearEvento = true" class="py-2 px-6 rounded-lg bg-blue-600 text-white font-semibold shadow-md hover:bg-blue-700 transition-all">
          Crear Nuevo Evento
        </button>
      </div>


      <!-- Crear Nuevo Evento -->
      <!-- <div class="max-w-2xl mx-auto bg-white/80 backdrop-blur-lg rounded-3xl shadow-2xl p-8 border border-purple-200 relative z-10 mb-12"> -->
  <div v-if="mostrarCrearEvento" class="fixed inset-0 bg-black/50 bg-opacity-50 flex items-start sm:items-center justify-center z-50 py-12 px-4">
  <div class="bg-white rounded-3xl shadow-md p-6 w-full max-w-lg border border-gray-200 max-h-[80vh] overflow-y-auto">
          <div class="flex justify-between items-center mb-6">
            <h3 class="text-2xl font-bold text-gray-800">
              {{ editingEvent ? 'Editar Evento' : 'Crear Nuevo Evento' }}
            </h3>
            <button @click="closeForm" class="text-gray-500 hover:text-red-500 text-2xl">
              <i class="fas fa-times"></i>
            </button>
          </div>
          <form @submit.prevent="addEvent">
            <div class="space-y-4 mb-6">
              <input v-model="newEvent.titulo" placeholder="Título del evento" class="w-full px-4 py-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-200 text-gray-800 placeholder-gray-400" required />
              <input v-model="newEvent.fecha" type="date" class="w-full px-4 py-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-200 text-gray-800" required />
              <input v-model="newEvent.lugar" placeholder="Lugar del evento" class="w-full px-4 py-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-200 text-gray-800 placeholder-gray-400" required />
              <textarea v-model="newEvent.descripcion" placeholder="Descripción del evento" rows="3" class="w-full px-4 py-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-200 text-gray-800 placeholder-gray-400"></textarea>

              <!-- Precio base obligatorio -->
              <div>
                <label class="block text-sm font-medium text-gray-800">Precio base (USD)</label>
                <input v-model="newEvent.precio" type="number" step="0.01" min="0" required class="w-full px-4 py-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-200 text-gray-800 placeholder-gray-400" />
              </div>

              <!-- Tipos de boletos -->
              <div class="mt-4 border-t pt-4">
                <h4 class="text-md font-semibold text-gray-800 mb-2">Tipos de boletos (opcional)</h4>
                <div class="flex gap-2">
                  <input v-model="newTicket.nombre" placeholder="Nombre (ej: General)" class="flex-1 px-3 py-2 rounded-lg border border-gray-300 text-gray-800 placeholder-gray-400" />
                  <input v-model="newTicket.precio" type="number" step="0.01" min="0" placeholder="Precio" class="w-28 px-3 py-2 rounded-lg border border-gray-300 text-gray-800 placeholder-gray-400" />
                  <button type="button" @click="addTicketType" class="px-4 py-2 rounded-lg bg-blue-600 text-white">Añadir</button>
                </div>

                <div v-if="newEvent.ticketTypes.length" class="mt-3 space-y-2">
                  <div v-for="(t,i) in newEvent.ticketTypes" :key="i" class="flex items-center justify-between bg-white p-2 rounded border border-gray-100">
                    <div class="text-sm text-gray-800 placeholder-gray-400">
                      <strong>{{ t.nombre }}</strong> — ${{ t.precio }}
                    </div>
                    <button type="button" @click="removeTicketType(i)" class="text-red-600">Eliminar</button>
                  </div>
                </div>
              </div>
              
              <!-- Nuevo campo para forma de pago (texto largo) -->
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-800">Forma de pago / Instrucciones</label>
                <textarea v-model="newEvent.formaPago" rows="4" placeholder="Describe cómo se puede pagar (ej: datos de transferencia, instrucciones para pago presencial, link de pago, etc.)" class="w-full px-4 py-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-200 text-gray-800"></textarea>
              </div>

              <!-- Campo esFuturo -->
              <div class="flex items-center gap-3 mt-2">
                <input id="esFuturo" type="checkbox" v-model="newEvent.esFuturo" class="w-4 h-4" />
                <label for="esFuturo" class="text-sm text-gray-700">Evento activo / Futuro</label>
              </div>

              <!-- Nuevo campo para imagen -->
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-800">Banner del evento</label>
                <input 
                  type="file" 
                  @change="handleImageUpload" 
                  accept="image/*"
                  class="w-full px-4 py-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-200 text-gray-800"
                  :required=false
                />
              </div>
            </div>
            <button type="submit" 
                    class="w-full py-3 rounded-lg bg-blue-600 text-white font-bold shadow-md hover:bg-blue-700 transition-all">
              <i :class="editingEvent ? 'fas fa-save' : 'fas fa-plus'" class="mr-2"></i>
              {{ editingEvent ? 'Guardar Cambios' : 'Crear Evento' }}
            </button>
          </form>
        </div>
      </div>

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
            <div class="flex gap-2 mt-4">
              <button @click="editEvent(evento)" 
                      class="flex-1 px-4 py-2 rounded-lg bg-blue-600 text-white text-sm font-semibold shadow hover:bg-blue-700 transition-all">
                <i class="fas fa-edit mr-1"></i>Editar
              </button>
              <button @click="deleteEvent(evento.id)" 
                      class="flex-1 px-4 py-2 rounded-lg bg-gray-200 text-gray-800 text-sm font-semibold shadow hover:bg-gray-300 transition-all">
                <i class="fas fa-trash mr-1"></i>Eliminar
              </button>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { db, auth, storage } from '../firebase' // Agregar storage
import { collection, addDoc, getDocs, deleteDoc, doc, onSnapshot, query, orderBy, updateDoc } from 'firebase/firestore'// Importar updateDoc
import { ref as storageRef, uploadBytes, getDownloadURL } from 'firebase/storage' // Importar funciones de storage
import { useRouter } from 'vue-router'
import { signOut } from 'firebase/auth'
import { v4 as uuidv4 } from 'uuid' // Add this import at the top


const router = useRouter()
const eventos = ref([])
const loading = ref(true)
const newEvent = ref({ titulo: '', fecha: '', lugar: '', descripcion: '', formaPago: '', esFuturo: true, precio: '', ticketTypes: [] })
const newTicket = ref({ nombre: '', precio: '' })

const addTicketType = () => {
  if (!newTicket.value.nombre || newTicket.value.precio === '') return
  // ensure precio is a number string
  newEvent.value.ticketTypes.push({ nombre: newTicket.value.nombre, precio: parseFloat(newTicket.value.precio).toFixed(2) })
  newTicket.value = { nombre: '', precio: '' }
}

const removeTicketType = (index) => {
  newEvent.value.ticketTypes.splice(index, 1)
}
const mostrarCrearEvento = ref(false)
const mostrarEventos = ref(false)
const selectedImage = ref(null)
const editingEvent = ref(null)

const fetchEventos = () => {
  const eventosRef = collection(db, 'eventos')
  const q = query(eventosRef, orderBy('fecha', 'desc'))
  onSnapshot(q, (snapshot) => {
    eventos.value = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }))
    loading.value = false
  })
}

const handleImageUpload = (e) => {
  const file = e.target.files[0]
  if (file) {
    selectedImage.value = file
  }
}

const uploadImage = async (eventId) => {
  if (!selectedImage.value) return null
  
  const imageRef = storageRef(storage, `eventos/${eventId}/banner.jpg`)
  await uploadBytes(imageRef, selectedImage.value)
  const imageUrl = await getDownloadURL(imageRef)
  return imageUrl
}

const addEvent = async () => {
  // Validación: titulo, fecha y lugar siempre requeridos. descripcion y banner pueden ser opcionales en edición.
  if (!newEvent.value.titulo || !newEvent.value.fecha || !newEvent.value.lugar) return

  try {
    if (editingEvent.value) {
      // Si estamos editando, actualizar el documento existente
      const eventRef = doc(db, 'eventos', editingEvent.value.id)
      let updateData = { ...newEvent.value }

      // Si hay una nueva imagen, subirla
      if (selectedImage.value) {
        const bannerUrl = await uploadImage(editingEvent.value.eventId)
        updateData.bannerUrl = bannerUrl
      }

      await updateDoc(eventRef, updateData)
    } else {
      // Si estamos creando uno nuevo
      const eventId = uuidv4()
      const storagePath = `eventos/${eventId}/imagenes`
      const bannerUrl = selectedImage.value ? await uploadImage(eventId) : null

      await addDoc(collection(db, 'eventos'), {
        ...newEvent.value,
        eventId,
        storagePath,
        bannerUrl,
        createdAt: new Date().toISOString()
      })
    }

    closeForm()
  } catch (error) {
    console.error('Error:', error)
    // Aquí podrías agregar un manejo de errores más amigable
  }
}

const editEvent = (evento) => {
  editingEvent.value = evento
  newEvent.value = { 
    titulo: evento.titulo,
    fecha: evento.fecha,
    lugar: evento.lugar,
    descripcion: evento.descripcion,
    formaPago: evento.formaPago || '',
    esFuturo: evento.esFuturo !== undefined ? evento.esFuturo : true,
    precio: evento.precio || '',
    ticketTypes: evento.ticketTypes ? [...evento.ticketTypes] : []
  }
  mostrarCrearEvento.value = true
}

const closeForm = () => {
  newEvent.value = { titulo: '', fecha: '', lugar: '', descripcion: '', formaPago: '', esFuturo: true, precio: '', ticketTypes: [] }
  selectedImage.value = null
  editingEvent.value = null
  mostrarCrearEvento.value = false
}

const deleteEvent = async (id) => {
  await deleteDoc(doc(db, 'eventos', id))
}

const logout = async () => {
  await signOut(auth)
  router.push('/admin-login')
}

onMounted(() => {
  fetchEventos()
})
</script>
