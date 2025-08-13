<template>
  <div class="min-h-screen flex items-center justify-center relative bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900">
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
    <form @submit.prevent="login" class="bg-white/80 backdrop-blur-lg p-8 rounded-2xl shadow-2xl w-full max-w-sm border border-purple-200">
      <div class="flex flex-col items-center mb-6">
        <div class="w-16 h-16 bg-gradient-to-br from-purple-600 to-blue-400 rounded-full flex items-center justify-center mb-2 shadow-lg">
          <i class="fas fa-user-shield text-white text-2xl"></i>
        </div>
        <h2 class="text-2xl font-bold text-purple-700">Acceso Administrador</h2>
        <p class="text-sm text-purple-400 mt-1">Solo personal autorizado</p>
      </div>
  <input v-model="email" type="email" placeholder="Email" class="w-full mb-4 px-4 py-2 rounded-lg border border-purple-200 focus:outline-none focus:ring-2 focus:ring-purple-400 text-sm text-gray-800 placeholder-gray-400" required />
  <input v-model="password" type="password" placeholder="Contraseña" class="w-full mb-6 px-4 py-2 rounded-lg border border-purple-200 focus:outline-none focus:ring-2 focus:ring-purple-400 text-sm text-gray-800 placeholder-gray-400" required />
  <button type="submit" class="w-full py-2 rounded-lg bg-gradient-to-r from-purple-600 to-blue-400 text-gray-100 font-semibold shadow-md hover:from-purple-700 hover:to-blue-500 transition-all">Iniciar sesión</button>
      <div v-if="error" class="text-red-500 mt-4 text-center">{{ error }}</div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { auth } from '../firebase'
import { signInWithEmailAndPassword } from 'firebase/auth'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

const login = async () => {
  error.value = ''
  try {
    await signInWithEmailAndPassword(auth, email.value, password.value)
    router.push('/admin')
  } catch (e) {
    error.value = 'Credenciales inválidas'
  }
}
</script>
