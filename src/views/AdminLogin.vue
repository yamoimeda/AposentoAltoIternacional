<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <form @submit.prevent="login" class="bg-white p-8 rounded-lg shadow-lg w-full max-w-sm">
      <h2 class="text-2xl font-bold mb-6 text-center">Admin Login</h2>
      <input v-model="email" type="email" placeholder="Email" class="input-modern w-full mb-4" required />
      <input v-model="password" type="password" placeholder="Password" class="input-modern w-full mb-6" required />
      <button type="submit" class="btn-modern w-full">Ingresar</button>
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
