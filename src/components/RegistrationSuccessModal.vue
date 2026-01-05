<template>
  <Transition name="modal-fade">
    <div v-if="show" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click.self="$emit('close')">
      <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full transform transition-all duration-300 animate-scale-in">
        <!-- Header con animación de éxito -->
        <div class="bg-gradient-to-r from-green-500 to-emerald-600 p-6 rounded-t-2xl text-center relative overflow-hidden">
          <!-- Confeti animado de fondo -->
          <div class="absolute inset-0 opacity-20">
            <div class="absolute top-0 left-1/4 w-2 h-2 bg-white rounded-full animate-confetti"></div>
            <div class="absolute top-0 left-1/2 w-2 h-2 bg-white rounded-full animate-confetti" style="animation-delay: 0.2s;"></div>
            <div class="absolute top-0 left-3/4 w-2 h-2 bg-white rounded-full animate-confetti" style="animation-delay: 0.4s;"></div>
          </div>
          
          <div class="relative z-10">
            <div class="w-20 h-20 bg-white rounded-full flex items-center justify-center mx-auto mb-4 animate-bounce-in">
              <i class="fas fa-check text-green-500 text-4xl"></i>
            </div>
            <h2 class="text-2xl font-bold text-white mb-2">¡Inscripción Exitosa!</h2>
            <p class="text-green-50">Tu registro ha sido confirmado</p>
          </div>
        </div>

        <!-- Contenido principal -->
        <div class="p-6 space-y-6">
          <!-- Código QR -->
          <div class="flex flex-col items-center bg-gray-50 p-6 rounded-xl">
            <h3 class="text-lg font-semibold text-gray-800 mb-4">Tu Boleto Digital</h3>
            <div class="bg-white p-4 rounded-lg shadow-md">
              <canvas ref="qrCanvas" class="max-w-full"></canvas>
            </div>
            <p class="text-sm text-gray-600 mt-4 text-center">
              Guarda este código QR para presentarlo el día del evento
            </p>
          </div>

          <!-- Información del cliente -->
          <div class="space-y-3">
            <h3 class="text-lg font-semibold text-gray-800 flex items-center">
              <i class="fas fa-user mr-2 text-blue-600"></i>
              Información del Registro
            </h3>
            <div class="bg-blue-50 rounded-lg p-4 space-y-2 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-600">Nombre:</span>
                <span class="font-semibold text-gray-800">{{ registrationData.nombre }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Cédula:</span>
                <span class="font-semibold text-gray-800">{{ registrationData.cedula }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">WhatsApp:</span>
                <span class="font-semibold text-gray-800">{{ registrationData.telefono }}</span>
              </div>
              <div v-if="registrationData.ticketType" class="flex justify-between border-t border-blue-200 pt-2 mt-2">
                <span class="text-gray-600">Tipo de Boleto:</span>
                <span class="font-semibold text-gray-800">{{ registrationData.ticketType }}</span>
              </div>
              <div v-if="registrationData.ticketPrice" class="flex justify-between">
                <span class="text-gray-600">Precio:</span>
                <span class="font-semibold text-green-600">${{ registrationData.ticketPrice }}</span>
              </div>
            </div>
          </div>

          <!-- ID de registro -->
          <div class="bg-gray-100 rounded-lg p-3">
            <p class="text-xs text-gray-600 text-center">ID de Registro</p>
            <p class="text-sm font-mono text-gray-800 text-center break-all">{{ registrationData.registrationToken }}</p>
          </div>

          <!-- Botones de acción -->
          <div class="flex gap-3">
            <button 
              @click="downloadQR"
              class="flex-1 px-4 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors flex items-center justify-center gap-2"
            >
              <i class="fas fa-download"></i>
              Descargar QR
            </button>
            <button 
              @click="$emit('close')"
              class="flex-1 px-4 py-3 bg-gray-200 text-gray-800 rounded-lg font-semibold hover:bg-gray-300 transition-colors"
            >
              Cerrar
            </button>
          </div>

          <!-- Mensaje adicional -->
          <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4 flex items-start gap-3">
            <i class="fas fa-info-circle text-yellow-600 mt-1"></i>
            <div class="text-sm text-yellow-800">
              <p class="font-semibold mb-1">Importante:</p>
              <p>Conserva este código QR. Lo necesitarás para verificar tu entrada el día del evento.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, watch, onMounted, nextTick } from 'vue'
import QRCode from 'qrcode'

const props = defineProps({
  show: { type: Boolean, required: true },
  registrationData: {
    type: Object,
    required: true,
    default: () => ({
      nombre: '',
      cedula: '',
      telefono: '',
      ticketType: '',
      ticketPrice: '',
      registrationToken: ''
    })
  }
})

const emit = defineEmits(['close'])

const qrCanvas = ref(null)

const generateQR = async () => {
  if (!qrCanvas.value || !props.registrationData.registrationToken) return
  
  try {
    // Crear objeto con datos para el QR
    const qrData = {
      token: props.registrationData.registrationToken,
      nombre: props.registrationData.nombre,
      cedula: props.registrationData.cedula,
      ticketType: props.registrationData.ticketType,
      eventoId: props.registrationData.eventoId
    }
    
    await QRCode.toCanvas(qrCanvas.value, JSON.stringify(qrData), {
      width: 200,
      margin: 2,
      color: {
        dark: '#1f2937',
        light: '#ffffff'
      }
    })
  } catch (error) {
    console.error('Error generando QR:', error)
  }
}

const downloadQR = () => {
  if (!qrCanvas.value) return
  
  const link = document.createElement('a')
  link.download = `boleto-${props.registrationData.registrationToken}.png`
  link.href = qrCanvas.value.toDataURL()
  link.click()
}

watch(() => props.show, async (newVal) => {
  if (newVal) {
    await nextTick()
    generateQR()
  }
})

onMounted(() => {
  if (props.show) {
    generateQR()
  }
})
</script>

<style scoped>
/* Animaciones de entrada */
.modal-fade-enter-active {
  transition: opacity 0.3s ease;
}

.modal-fade-leave-active {
  transition: opacity 0.2s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

@keyframes scale-in {
  0% {
    transform: scale(0.9);
    opacity: 0;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.animate-scale-in {
  animation: scale-in 0.3s ease-out;
}

@keyframes bounce-in {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}

.animate-bounce-in {
  animation: bounce-in 0.6s ease-out;
}

@keyframes confetti {
  0% {
    transform: translateY(0) rotate(0deg);
    opacity: 1;
  }
  100% {
    transform: translateY(200px) rotate(360deg);
    opacity: 0;
  }
}

.animate-confetti {
  animation: confetti 2s ease-out infinite;
}
</style>
