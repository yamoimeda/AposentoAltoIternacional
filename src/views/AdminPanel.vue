<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900 py-12 pt-25">
    <!-- Efectos de fondo hero igual que InicioView -->
    <div class="absolute top-20 left-10 w-72 h-72 bg-gradient-to-r from-yellow-400 to-pink-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float"></div>
    <div class="absolute top-40 right-10 w-72 h-72 bg-gradient-to-r from-purple-400 to-blue-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float" style="animation-delay: 2s;"></div>
    <div class="absolute bottom-20 left-1/2 w-72 h-72 bg-gradient-to-r from-green-400 to-cyan-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float" style="animation-delay: 4s;"></div>
    <!-- Partículas flotantes -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute top-1/4 left-1/4 w-2 h-2 bg-white rounded-full opacity-60 animate-pulse"></div>
      <div class="absolute top-1/3 right-1/4 w-1 h-1 bg-yellow-300 rounded-full opacity-80 animate-pulse" style="animation-delay: 1s;"></div>
      <div class="absolute bottom-1/3 left-1/3 w-3 h-3 bg-pink-300 rounded-full opacity-40 animate-pulse" style="animation-delay: 2s;"></div>
      <div class="absolute top-2/3 right-1/3 w-2 h-2 bg-blue-300 rounded-full opacity-70 animate-pulse" style="animation-delay: 3s;"></div>
    </div>
    
    <!-- Header del panel -->
    <div class="container mx-auto px-4 relative z-10">
      <div class="text-center mb-12">
        <div class="w-20 h-20 bg-gradient-to-br from-purple-600 to-blue-400 rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg">
          <i class="fas fa-cogs text-white text-3xl"></i>
        </div>
        <h1 class="text-5xl font-black text-white mb-4">Panel de Administración</h1>
        <p class="text-xl text-blue-100 mb-6">Gestiona los eventos de la iglesia</p>
        <button @click="logout" class="py-2 px-6 rounded-lg bg-gradient-to-r from-red-500 to-pink-500 text-white font-semibold shadow-md hover:from-red-600 hover:to-pink-600 transition-all">
          <i class="fas fa-sign-out-alt mr-2"></i>Cerrar sesión
        </button>
      </div>


      <!-- Crear Nuevo Evento -->
      <div class="max-w-2xl mx-auto bg-white/80 backdrop-blur-lg rounded-3xl shadow-2xl p-8 border border-purple-200 relative z-10 mb-12">
        <div class="flex flex-col items-center mb-6">
          <div class="w-16 h-16 bg-gradient-to-br from-yellow-400 via-pink-500 to-purple-500 rounded-full flex items-center justify-center mb-2 shadow-lg">
            <i class="fas fa-plus text-white text-2xl"></i>
          </div>
          <h3 class="text-2xl font-bold text-purple-700 mb-2">Crear Nuevo Evento</h3>
          <p class="text-purple-400">Agrega un nuevo evento a la programación de la iglesia</p>
        </div>
        <form @submit.prevent="addEvent">
          <div class="space-y-4 mb-6">
            <input v-model="newEvent.titulo" placeholder="Título del evento" class="w-full px-4 py-3 rounded-lg border border-purple-200 focus:outline-none focus:ring-2 focus:ring-purple-400 text-gray-800 placeholder-gray-400" required />
            <input v-model="newEvent.fecha" type="date" class="w-full px-4 py-3 rounded-lg border border-purple-200 focus:outline-none focus:ring-2 focus:ring-purple-400 text-gray-800" required />
            <input v-model="newEvent.lugar" placeholder="Lugar del evento" class="w-full px-4 py-3 rounded-lg border border-purple-200 focus:outline-none focus:ring-2 focus:ring-purple-400 text-gray-800 placeholder-gray-400" required />
            <textarea v-model="newEvent.descripcion" placeholder="Descripción del evento" rows="3" class="w-full px-4 py-3 rounded-lg border border-purple-200 focus:outline-none focus:ring-2 focus:ring-purple-400 text-gray-800 placeholder-gray-400" required></textarea>
          </div>
          <button type="submit" class="w-full py-3 rounded-lg bg-gradient-to-r from-yellow-400 via-pink-500 to-purple-500 text-gray-900 font-bold shadow-md hover:from-yellow-500 hover:to-purple-600 transition-all">
            <i class="fas fa-plus mr-2"></i>Crear Evento
          </button>
        </form>
      </div>

      <!-- Lista de Eventos -->
      <div class="max-w-4xl mx-auto bg-white/80 backdrop-blur-lg rounded-3xl shadow-2xl p-8 border border-purple-200 relative z-10">
        <div class="flex flex-col items-center mb-6">
          <div class="w-16 h-16 bg-gradient-to-br from-blue-400 via-purple-500 to-cyan-400 rounded-full flex items-center justify-center mb-2 shadow-lg">
            <i class="fas fa-calendar-alt text-white text-2xl"></i>
          </div>
          <h3 class="text-2xl font-bold text-purple-700 mb-2">Eventos Creados</h3>
          <p class="text-purple-400">Consulta y gestiona todos los eventos existentes</p>
        </div>
        <div v-if="loading" class="text-center py-8 text-purple-400">
          <i class="fas fa-spinner fa-spin text-3xl mb-4"></i>
          <p>Cargando eventos...</p>
        </div>
        <div v-else-if="eventos.length === 0" class="text-center py-8 text-purple-400">
          <i class="fas fa-calendar-times text-3xl mb-4"></i>
          <p>No hay eventos creados</p>
        </div>
        <div v-else class="space-y-4">
          <div v-for="evento in eventos" :key="evento.id" class="bg-gradient-to-r from-purple-100 via-blue-100 to-pink-100 rounded-xl p-6 shadow-md">
            <div class="flex justify-between items-start">
              <div class="flex-1">
                <h4 class="font-bold text-xl text-purple-700 mb-2">{{ evento.titulo }}</h4>
                <div class="flex items-center text-purple-500 mb-2">
                  <i class="fas fa-calendar mr-2"></i>
                  <span>{{ evento.fecha }}</span>
                  <i class="fas fa-map-marker-alt ml-4 mr-2"></i>
                  <span>{{ evento.lugar }}</span>
                </div>
                <p class="text-gray-700">{{ evento.descripcion }}</p>
              </div>
              <button @click="deleteEvent(evento.id)" class="ml-4 px-4 py-2 rounded-lg bg-gradient-to-r from-red-500 to-pink-500 text-white font-semibold shadow hover:from-red-600 hover:to-pink-600 transition-all">
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
import { db, auth } from '../firebase'
import { collection, addDoc, getDocs, deleteDoc, doc, onSnapshot, query, orderBy } from 'firebase/firestore'
import { useRouter } from 'vue-router'
import { signOut } from 'firebase/auth'

const router = useRouter()
const eventos = ref([])
const loading = ref(true)
const newEvent = ref({ titulo: '', fecha: '', lugar: '', descripcion: '' })
const mostrarCrearEvento = ref(false)
const mostrarEventos = ref(false)

const fetchEventos = () => {
  const eventosRef = collection(db, 'eventos')
  const q = query(eventosRef, orderBy('fecha', 'desc'))
  onSnapshot(q, (snapshot) => {
    eventos.value = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }))
    loading.value = false
  })
}

const addEvent = async () => {
  if (!newEvent.value.titulo || !newEvent.value.fecha || !newEvent.value.lugar || !newEvent.value.descripcion) return
  await addDoc(collection(db, 'eventos'), { ...newEvent.value })
  newEvent.value = { titulo: '', fecha: '', lugar: '', descripcion: '' }
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
