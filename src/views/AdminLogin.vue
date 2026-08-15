<template>
  <div class="min-h-screen w-full bg-slate-50/80 font-sans text-slate-800 flex flex-col justify-between pt-24 pb-12 px-4 sm:px-6">
    <div class="w-full max-w-md mx-auto my-auto">
      <!-- Volver Link Above Card -->
      <div class="mb-6 flex items-center justify-between">
        <router-link
          to="/"
          class="inline-flex items-center gap-2 text-xs font-semibold text-slate-500 hover:text-indigo-600 transition-colors group"
        >
          <div class="w-7 h-7 rounded-lg bg-white border border-slate-200 flex items-center justify-center shadow-xs group-hover:border-indigo-200 group-hover:bg-indigo-50/50 transition-all">
            <i class="fas fa-arrow-left text-[11px] group-hover:-translate-x-0.5 transition-transform"></i>
          </div>
          <span>Volver al inicio</span>
        </router-link>

        <span class="text-[11px] font-medium text-slate-400 uppercase tracking-wider bg-slate-100 px-2.5 py-1 rounded-md">
          Portal Admin
        </span>
      </div>

      <!-- Main Login Card Container -->
      <div class="bg-white rounded-2xl shadow-xl shadow-slate-200/60 border border-slate-100 p-8 sm:p-10 relative overflow-hidden">
        <!-- Top Subtle Indigo Decorative Border -->
        <div class="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-indigo-500 via-purple-500 to-indigo-600"></div>

        <!-- Card Header -->
        <div class="text-center mb-8">
          <div class="w-14 h-14 rounded-2xl bg-indigo-50 border border-indigo-100 flex items-center justify-center mx-auto mb-4 text-indigo-600 shadow-sm">
            <i class="fas fa-user-shield text-2xl"></i>
          </div>
          <h1 class="text-2xl font-bold tracking-tight text-slate-900">
            Acceso Administrador
          </h1>
          <p class="text-xs sm:text-sm text-slate-500 mt-1.5">
            Ingresa tus credenciales para gestionar el sistema
          </p>
        </div>

        <!-- Error Alert Banner -->
        <transition
          enter-active-class="transition duration-200 ease-out"
          enter-from-class="transform -translate-y-2 opacity-0"
          enter-to-class="transform translate-y-0 opacity-100"
          leave-active-class="transition duration-150 ease-in"
          leave-from-class="transform translate-y-0 opacity-100"
          leave-to-class="transform -translate-y-2 opacity-0"
        >
          <div v-if="error" class="mb-6 p-3.5 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-start gap-3 shadow-xs">
            <i class="fas fa-circle-exclamation text-rose-500 text-sm mt-0.5 shrink-0"></i>
            <div class="flex-1 leading-snug">
              <span class="font-semibold block text-rose-900 mb-0.5">Error al iniciar sesión</span>
              <span>{{ error }}</span>
            </div>
            <button @click="error = ''" class="text-rose-400 hover:text-rose-600 transition-colors p-0.5">
              <i class="fas fa-times text-xs"></i>
            </button>
          </div>
        </transition>

        <!-- Form Fields -->
        <form @submit.prevent="login" class="space-y-5">
          <!-- Email Field -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
              Correo Electrónico
            </label>
            <div class="relative rounded-xl shadow-xs">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                <i class="fas fa-envelope text-sm"></i>
              </div>
              <input
                v-model="email"
                type="email"
                required
                autocomplete="email"
                placeholder="admin@aposentoalto.org"
                class="w-full pl-10 pr-4 py-2.5 bg-slate-50/60 border border-slate-200 rounded-xl text-slate-900 placeholder-slate-400 text-sm focus:outline-none focus:bg-white focus:border-indigo-600 focus:ring-2 focus:ring-indigo-600/15 transition-all duration-200"
                :disabled="loading"
              />
            </div>
          </div>

          <!-- Password Field -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
              Contraseña
            </label>
            <div class="relative rounded-xl shadow-xs">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                <i class="fas fa-lock text-sm"></i>
              </div>
              <input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                required
                autocomplete="current-password"
                placeholder="••••••••••••"
                class="w-full pl-10 pr-11 py-2.5 bg-slate-50/60 border border-slate-200 rounded-xl text-slate-900 placeholder-slate-400 text-sm focus:outline-none focus:bg-white focus:border-indigo-600 focus:ring-2 focus:ring-indigo-600/15 transition-all duration-200"
                :disabled="loading"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute inset-y-0 right-0 pr-3.5 flex items-center text-slate-400 hover:text-slate-600 transition-colors cursor-pointer"
                tabindex="-1"
              >
                <i :class="['fas', showPassword ? 'fa-eye-slash' : 'fa-eye', 'text-sm']"></i>
              </button>
            </div>
          </div>

          <!-- Forgot Password Link -->
          <div class="flex justify-end pt-1">
            <button
              type="button"
              @click="abrirModalReset"
              class="text-xs font-medium text-indigo-600 hover:text-indigo-700 transition-colors cursor-pointer"
            >
              ¿Olvidaste tu contraseña?
            </button>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full py-3 px-4 bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800 text-white font-semibold text-sm rounded-xl shadow-md shadow-indigo-600/20 hover:shadow-indigo-600/30 transition-all duration-200 flex items-center justify-center gap-2 disabled:opacity-60 disabled:cursor-not-allowed cursor-pointer mt-2"
          >
            <i v-if="loading" class="fas fa-circle-notch fa-spin text-sm"></i>
            <i v-else class="fas fa-right-to-bracket text-sm"></i>
            <span>{{ loading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}</span>
          </button>
        </form>

        <!-- Security Footer -->
        <div class="mt-8 pt-5 border-t border-slate-100 text-center">
          <p class="text-[11px] text-slate-400 flex items-center justify-center gap-1.5">
            <i class="fas fa-shield text-[10px] text-emerald-600"></i>
            <span>Conexión segura cifrada SSL</span>
          </p>
        </div>
      </div>
    </div>

    <!-- Modal Restablecer Contraseña -->
    <transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div v-if="mostrarModalReset" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs">
        <div class="bg-white rounded-2xl shadow-2xl border border-slate-100 max-w-md w-full p-6 sm:p-8 relative overflow-hidden">
          <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-indigo-500 to-indigo-600"></div>
          
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center">
                <i class="fas fa-key text-base"></i>
              </div>
              <h3 class="text-base font-bold text-slate-900">Restablecer Contraseña</h3>
            </div>
            <button @click="cerrarModalReset" class="text-slate-400 hover:text-slate-600 p-1 cursor-pointer">
              <i class="fas fa-times"></i>
            </button>
          </div>

          <p class="text-xs text-slate-500 mb-5 leading-relaxed">
            Ingresa tu correo electrónico registrado. Te enviaremos un enlace seguro para crear tu nueva contraseña y regresar a la web.
          </p>

          <!-- Feedback Alert -->
          <div v-if="resetMensaje.texto" :class="['mb-4 p-3 rounded-xl text-xs flex items-start gap-2.5', resetMensaje.tipo === 'success' ? 'bg-emerald-50 border border-emerald-200 text-emerald-800' : 'bg-rose-50 border border-rose-200 text-rose-800']">
            <i :class="['fas mt-0.5', resetMensaje.tipo === 'success' ? 'fa-circle-check text-emerald-600' : 'fa-circle-exclamation text-rose-500']"></i>
            <span class="leading-snug">{{ resetMensaje.texto }}</span>
          </div>

          <form @submit.prevent="enviarLinkRecuperacion" class="space-y-4">
            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1.5">Correo Electrónico</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                  <i class="fas fa-envelope text-sm"></i>
                </div>
                <input
                  v-model="resetEmail"
                  type="email"
                  required
                  placeholder="admin@aposentoalto.org"
                  class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-slate-900 text-sm focus:outline-none focus:bg-white focus:border-indigo-600 focus:ring-2 focus:ring-indigo-600/15"
                  :disabled="enviandoReset"
                />
              </div>
            </div>

            <div class="flex gap-2 pt-2">
              <button
                type="button"
                @click="cerrarModalReset"
                class="flex-1 py-2.5 px-4 rounded-xl border border-slate-200 text-slate-700 text-xs font-semibold hover:bg-slate-50 transition-colors cursor-pointer"
              >
                Cancelar
              </button>
              <button
                type="submit"
                :disabled="enviandoReset || !resetEmail"
                class="flex-1 py-2.5 px-4 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-semibold shadow-sm transition-colors flex items-center justify-center gap-2 disabled:opacity-60 cursor-pointer"
              >
                <i v-if="enviandoReset" class="fas fa-circle-notch fa-spin"></i>
                <span>{{ enviandoReset ? 'Enviando...' : 'Enviar enlace' }}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <!-- Page Footer Copyright -->
    <div class="text-center text-xs text-slate-400 mt-6">
      &copy; {{ new Date().getFullYear() }} Ministerio El Aposento Alto Internacional
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { auth } from '../firebase'
import { signInWithEmailAndPassword, sendPasswordResetEmail } from 'firebase/auth'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const showPassword = ref(false)
const router = useRouter()

// Estado para modal de recuperación de contraseña
const mostrarModalReset = ref(false)
const resetEmail = ref('')
const enviandoReset = ref(false)
const resetMensaje = ref({ tipo: '', texto: '' })

const abrirModalReset = () => {
  resetEmail.value = email.value || ''
  resetMensaje.value = { tipo: '', texto: '' }
  mostrarModalReset.value = true
}

const cerrarModalReset = () => {
  mostrarModalReset.value = false
  resetMensaje.value = { tipo: '', texto: '' }
}

const enviarLinkRecuperacion = async () => {
  if (!resetEmail.value) return
  enviandoReset.value = true
  resetMensaje.value = { tipo: '', texto: '' }
  
  try {
    auth.languageCode = 'es'
    await sendPasswordResetEmail(auth, resetEmail.value.trim())

    resetMensaje.value = {
      tipo: 'success',
      texto: `¡Enlace enviado a ${resetEmail.value}! Revisa tu bandeja de entrada o la carpeta de SPAM / No deseados.`
    }
  } catch (e) {
    console.error('Error enviando reset:', e)
    if (e.code === 'auth/user-not-found') {
      resetMensaje.value = { tipo: 'error', texto: 'No existe ninguna cuenta registrada con este correo.' }
    } else if (e.code === 'auth/invalid-email') {
      resetMensaje.value = { tipo: 'error', texto: 'Por favor ingresa un correo electrónico válido.' }
    } else if (e.code === 'auth/too-many-requests') {
      resetMensaje.value = { tipo: 'error', texto: 'Se han realizado demasiadas solicitudes seguidas. Firebase ha pausado temporalmente los envíos a este correo. Espera unos minutos.' }
    } else {
      resetMensaje.value = { tipo: 'error', texto: 'No se pudo enviar el correo. Intenta de nuevo en unos minutos.' }
    }
  } finally {
    enviandoReset.value = false
  }
}

const login = async () => {
  if (!email.value || !password.value) return
  error.value = ''
  loading.value = true
  try {
    await signInWithEmailAndPassword(auth, email.value, password.value)
    router.push('/admin')
  } catch (e) {
    console.error('Login error:', e)
    if (e.code === 'auth/invalid-credential' || e.code === 'auth/wrong-password' || e.code === 'auth/user-not-found') {
      error.value = 'El correo electrónico o la contraseña son incorrectos.'
    } else if (e.code === 'auth/too-many-requests') {
      error.value = 'Demasiados intentos fallidos. Por favor intente más tarde.'
    } else {
      error.value = 'No se pudo iniciar sesión. Verifique sus datos o su conexión.'
    }
  } finally {
    loading.value = false
  }
}
</script>
