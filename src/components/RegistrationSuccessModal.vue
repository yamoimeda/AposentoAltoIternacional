<template>
  <Transition name="modal-fade">
    <div v-if="show" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 py-4 px-3" @click.self="$emit('close')">
      <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full max-h-[96vh] overflow-y-auto no-scrollbar transform transition-all duration-300 animate-scale-in">
        <!-- Header compacto con icono al lado -->
        <div class="bg-gradient-to-r from-emerald-600 to-teal-600 px-4 py-3.5 rounded-t-2xl flex items-center justify-center gap-2.5 shadow-xs">
          <div class="w-7 h-7 bg-white/20 rounded-full flex items-center justify-center text-white shrink-0">
            <i class="fas fa-check text-white text-sm"></i>
          </div>
          <h2 class="text-base sm:text-lg font-bold text-white tracking-wide">¡Inscripción Exitosa!</h2>
        </div>

        <!-- Contenido principal -->
        <div class="p-4 sm:p-5 space-y-3.5">
          <!-- Código QR -->
          <div class="flex flex-col items-center bg-slate-50 p-3 rounded-xl border border-slate-100">
            <div class="bg-white p-2.5 rounded-lg shadow-xs flex justify-center border border-slate-100">
              <canvas ref="qrCanvas" class="w-36 h-36 sm:w-44 sm:h-44 max-w-full max-h-[30vh]"></canvas>
            </div>
            <p class="text-xs text-slate-500 mt-2 text-center font-medium">
              Presenta este código QR el día del evento
            </p>
          </div>

          <!-- Información del registro -->
          <div class="space-y-1.5">
            <div class="bg-blue-50/80 border border-blue-100 rounded-xl p-3 space-y-1.5 text-xs sm:text-sm">
              <div class="flex justify-between items-center">
                <span class="text-slate-600 font-medium">Nombre:</span>
                <span class="font-bold text-slate-900 text-right truncate ml-2">{{ registrationData.nombre }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-slate-600 font-medium">Cédula:</span>
                <span class="font-semibold text-slate-800 font-mono">{{ registrationData.cedula }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-slate-600 font-medium">WhatsApp:</span>
                <span class="font-semibold text-slate-800">{{ registrationData.telefono }}</span>
              </div>
              <div v-if="registrationData.ticketType" class="flex justify-between items-center border-t border-blue-200/70 pt-1.5 mt-1.5">
                <span class="text-slate-600 font-medium">Tipo de Boleto:</span>
                <span class="font-bold text-blue-900">{{ registrationData.ticketType }}</span>
              </div>
              <div v-if="registrationData.ticketPrice" class="flex justify-between items-center">
                <span class="text-slate-600 font-medium">Precio del Boleto:</span>
                <span class="font-bold text-emerald-700">${{ Number(registrationData.ticketPrice).toFixed(2) }}</span>
              </div>
              <div v-if="registrationData.ticketPrice || registrationData.monto" class="flex justify-between items-center">
                <span class="text-slate-600 font-medium">Monto Abonado:</span>
                <span class="font-bold text-emerald-700 bg-emerald-100/80 px-2 py-0.5 rounded">${{ Number(registrationData.monto || registrationData.totalPrice || registrationData.montoPagado || 0).toFixed(2) }}</span>
              </div>
            </div>
          </div>

          <!-- Botones de acción -->
          <div class="flex gap-2.5 pt-1">
            <button 
              @click="downloadQR"
              class="flex-1 py-2.5 px-3 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-bold text-xs sm:text-sm transition-all shadow-xs flex items-center justify-center gap-1.5 cursor-pointer"
            >
              <i class="fas fa-download"></i>
              Descargar QR
            </button>
            <button 
              @click="$emit('close')"
              class="flex-1 py-2.5 px-3 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl font-semibold text-xs sm:text-sm transition-all cursor-pointer"
            >
              Cerrar
            </button>
          </div>

          <!-- Mensaje adicional -->
          <div class="bg-amber-50 border border-amber-200/80 rounded-xl p-2.5 flex items-center gap-2 text-xs text-amber-800">
            <i class="fas fa-info-circle text-amber-600 shrink-0"></i>
            <p>Guarda tu código QR. Lo necesitarás para verificar tu entrada.</p>
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
      registrationToken: '',
      monto: ''
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

.no-scrollbar::-webkit-scrollbar {
    display: none;
}

/* Hide scrollbar for IE, Edge and Firefox */
.no-scrollbar {
    -ms-overflow-style: none;  /* IE and Edge */
    scrollbar-width: none;  /* Firefox */
}

</style>

