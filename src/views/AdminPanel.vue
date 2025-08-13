<template>
  <div class="min-h-screen bg-gray-50 p-8">
    <div class="max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-8">
      <h2 class="text-2xl font-bold mb-6 text-center">Panel de Administración de Eventos</h2>
      <button @click="logout" class="btn-modern mb-6 w-full">Cerrar sesión</button>
      <form @submit.prevent="addEvent" class="mb-8">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <input v-model="newEvent.titulo" placeholder="Título" class="input-modern" required />
          <input v-model="newEvent.fecha" type="date" class="input-modern" required />
          <input v-model="newEvent.lugar" placeholder="Lugar" class="input-modern" required />
          <input v-model="newEvent.descripcion" placeholder="Descripción" class="input-modern" required />
        </div>
        <button type="submit" class="btn-modern w-full">Agregar Evento</button>
      </form>
      <div>
        <h3 class="text-xl font-semibold mb-4">Eventos</h3>
        <div v-if="loading" class="text-center py-4">Cargando eventos...</div>
        <div v-else>
          <div v-for="evento in eventos" :key="evento.id" class="bg-gray-100 rounded p-4 mb-4 flex justify-between items-center">
            <div>
              <div class="font-bold">{{ evento.titulo }}</div>
              <div class="text-sm text-gray-600">{{ evento.fecha }} | {{ evento.lugar }}</div>
              <div class="text-gray-700">{{ evento.descripcion }}</div>
            </div>
            <button @click="deleteEvent(evento.id)" class="btn-modern bg-red-500 hover:bg-red-600 ml-4">Eliminar</button>
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
