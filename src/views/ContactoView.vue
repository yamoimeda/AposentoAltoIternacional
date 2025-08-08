<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Hero Section -->
    <section class="bg-gradient-to-r from-green-600 to-blue-600 text-white py-20">
      <div class="container mx-auto px-4 text-center">
        <h1 class="text-4xl md:text-5xl font-bold mb-6">
          <i class="fas fa-phone-alt mr-3"></i>
          Contáctanos
        </h1>
        <p class="text-xl text-green-100 max-w-3xl mx-auto">
          Estamos aquí para escucharte, orar contigo y ayudarte en lo que necesites
        </p>
      </div>
    </section>

    <!-- Información de Contacto y Formulario -->
    <section class="py-16">
      <div class="container mx-auto px-4">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <!-- Información de Contacto -->
          <div>
            <h2 class="text-3xl font-bold text-gray-800 mb-8">
              <i class="fas fa-info-circle text-blue-600 mr-3"></i>
              Información de Contacto
            </h2>

            <div class="space-y-6">
              <!-- Ubicación -->
              <div class="bg-white p-6 rounded-lg shadow-md">
                <div class="flex items-start">
                  <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mr-4">
                    <i class="fas fa-map-marker-alt text-blue-600"></i>
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold text-gray-800 mb-2">Dirección</h3>
                    <p class="text-gray-600">
                      Avenida Principal 123<br>
                      Colonia Centro<br>
                      Ciudad, Estado 12345<br>
                      País
                    </p>
                  </div>
                </div>
              </div>

              <!-- Teléfonos -->
              <div class="bg-white p-6 rounded-lg shadow-md">
                <div class="flex items-start">
                  <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mr-4">
                    <i class="fas fa-phone text-green-600"></i>
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold text-gray-800 mb-2">Teléfonos</h3>
                    <p class="text-gray-600">
                      Oficina Principal: <a href="tel:+15551234567" class="text-blue-600 hover:underline">+1 (555) 123-4567</a><br>
                      Pastor Principal: <a href="tel:+15551234568" class="text-blue-600 hover:underline">+1 (555) 123-4568</a><br>
                      Emergencias: <a href="tel:+15551234569" class="text-blue-600 hover:underline">+1 (555) 123-4569</a>
                    </p>
                  </div>
                </div>
              </div>

              <!-- Email -->
              <div class="bg-white p-6 rounded-lg shadow-md">
                <div class="flex items-start">
                  <div class="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mr-4">
                    <i class="fas fa-envelope text-purple-600"></i>
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold text-gray-800 mb-2">Correos Electrónicos</h3>
                    <p class="text-gray-600">
                      General: <a href="mailto:info@aposentoalto.org" class="text-blue-600 hover:underline">info@aposentoalto.org</a><br>
                      Pastor: <a href="mailto:pastor@aposentoalto.org" class="text-blue-600 hover:underline">pastor@aposentoalto.org</a><br>
                      Eventos: <a href="mailto:eventos@aposentoalto.org" class="text-blue-600 hover:underline">eventos@aposentoalto.org</a>
                    </p>
                  </div>
                </div>
              </div>

              <!-- Horarios -->
              <div class="bg-white p-6 rounded-lg shadow-md">
                <div class="flex items-start">
                  <div class="w-12 h-12 bg-yellow-100 rounded-full flex items-center justify-center mr-4">
                    <i class="fas fa-clock text-yellow-600"></i>
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold text-gray-800 mb-2">Horarios de Servicio</h3>
                    <div class="text-gray-600 space-y-1">
                      <p><strong>Domingo:</strong> 10:00 AM - Culto Principal</p>
                      <p><strong>Miércoles:</strong> 7:00 PM - Estudio Bíblico</p>
                      <p><strong>Viernes:</strong> 7:00 PM - Servicio de Jóvenes</p>
                      <p><strong>Sábado:</strong> 10:00 AM - Ministerio de Niños</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Formulario de Contacto -->
          <div>
            <div class="bg-white p-8 rounded-lg shadow-lg">
              <h2 class="text-3xl font-bold text-gray-800 mb-6">
                <i class="fas fa-paper-plane text-green-600 mr-3"></i>
                Envíanos un Mensaje
              </h2>

              <form @submit.prevent="enviarMensaje" class="space-y-6">
                <!-- Tipo de Consulta -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Tipo de Consulta *
                  </label>
                  <select 
                    v-model="formulario.tipo"
                    required
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  >
                    <option value="">Selecciona una opción</option>
                    <option value="informacion">Información General</option>
                    <option value="oracion">Petición de Oración</option>
                    <option value="consejeria">Consejería Pastoral</option>
                    <option value="eventos">Eventos y Actividades</option>
                    <option value="voluntariado">Voluntariado</option>
                    <option value="donaciones">Donaciones y Ofrendas</option>
                    <option value="otro">Otro</option>
                  </select>
                </div>

                <!-- Información Personal -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">
                      Nombre Completo *
                    </label>
                    <input 
                      v-model="formulario.nombre"
                      type="text" 
                      required
                      class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      placeholder="Tu nombre completo"
                    >
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">
                      Correo Electrónico *
                    </label>
                    <input 
                      v-model="formulario.email"
                      type="email" 
                      required
                      class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      placeholder="tu@email.com"
                    >
                  </div>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Teléfono
                  </label>
                  <input 
                    v-model="formulario.telefono"
                    type="tel"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    placeholder="+1 234 567 8900"
                  >
                </div>

                <!-- Mensaje -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Mensaje *
                  </label>
                  <textarea 
                    v-model="formulario.mensaje"
                    rows="6"
                    required
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    placeholder="Comparte tu mensaje, petición de oración, o cualquier consulta que tengas..."
                  ></textarea>
                </div>

                <!-- Método de Respuesta Preferido -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    ¿Cómo prefieres que te contactemos?
                  </label>
                  <div class="flex flex-wrap gap-4">
                    <label class="flex items-center">
                      <input 
                        v-model="formulario.contactoPreferido"
                        type="radio" 
                        value="email"
                        class="mr-2"
                      >
                      <span>Correo Electrónico</span>
                    </label>
                    <label class="flex items-center">
                      <input 
                        v-model="formulario.contactoPreferido"
                        type="radio" 
                        value="telefono"
                        class="mr-2"
                      >
                      <span>Teléfono</span>
                    </label>
                    <label class="flex items-center">
                      <input 
                        v-model="formulario.contactoPreferido"
                        type="radio" 
                        value="cualquiera"
                        class="mr-2"
                      >
                      <span>Cualquiera</span>
                    </label>
                  </div>
                </div>

                <!-- Urgencia -->
                <div v-if="formulario.tipo === 'oracion' || formulario.tipo === 'consejeria'">
                  <label class="flex items-start">
                    <input 
                      v-model="formulario.urgente"
                      type="checkbox"
                      class="mt-1 mr-3"
                    >
                    <span class="text-sm text-gray-700">
                      Esto es urgente - necesito una respuesta rápida
                    </span>
                  </label>
                </div>

                <!-- Privacidad -->
                <div>
                  <label class="flex items-start">
                    <input 
                      v-model="formulario.aceptaPrivacidad"
                      type="checkbox" 
                      required
                      class="mt-1 mr-3"
                    >
                    <span class="text-sm text-gray-700">
                      Acepto la <a href="#" class="text-green-600 hover:underline">política de privacidad</a> 
                      y autorizo el uso de mis datos para responder a mi consulta. *
                    </span>
                  </label>
                </div>

                <!-- Botón de Envío -->
                <button 
                  type="submit"
                  :disabled="procesando"
                  :class="['w-full py-3 px-6 rounded-lg font-semibold transition-colors',
                           procesando ? 'bg-gray-400 cursor-not-allowed' : 'bg-green-600 hover:bg-green-700',
                           'text-white']"
                >
                  <i :class="['mr-2', procesando ? 'fas fa-spinner fa-spin' : 'fas fa-paper-plane']"></i>
                  {{ procesando ? 'Enviando...' : 'Enviar Mensaje' }}
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Mapa y Ubicación -->
    <section class="py-16 bg-gray-100">
      <div class="container mx-auto px-4">
        <div class="text-center mb-12">
          <h2 class="text-4xl font-bold text-gray-800 mb-4">
            <i class="fas fa-map text-blue-600 mr-3"></i>
            Nuestra Ubicación
          </h2>
          <p class="text-xl text-gray-600">Ven y visítanos, te esperamos con los brazos abiertos</p>
        </div>

        <div class="bg-white rounded-lg shadow-lg overflow-hidden">
          <div class="grid grid-cols-1 lg:grid-cols-2">
            <!-- Mapa Placeholder -->
            <div class="h-96 bg-gray-300 flex items-center justify-center">
              <div class="text-center text-gray-600">
                <i class="fas fa-map-marked-alt text-6xl mb-4"></i>
                <p class="text-lg">Mapa Interactivo</p>
                <p class="text-sm">Aquí iría integrado Google Maps o similar</p>
              </div>
            </div>

            <!-- Información de Transporte -->
            <div class="p-8">
              <h3 class="text-2xl font-bold text-gray-800 mb-6">Cómo Llegar</h3>
              
              <div class="space-y-6">
                <div>
                  <h4 class="font-semibold text-gray-800 mb-2 flex items-center">
                    <i class="fas fa-car text-blue-600 mr-2"></i>
                    En Automóvil
                  </h4>
                  <p class="text-gray-600 text-sm">
                    Desde el centro de la ciudad, toma la Avenida Principal hacia el norte. 
                    Tenemos estacionamiento gratuito disponible.
                  </p>
                </div>

                <div>
                  <h4 class="font-semibold text-gray-800 mb-2 flex items-center">
                    <i class="fas fa-bus text-green-600 mr-2"></i>
                    Transporte Público
                  </h4>
                  <p class="text-gray-600 text-sm">
                    Rutas 15, 22 y 38 con parada en "Iglesia Aposento Alto". 
                    También puedes tomar el metro línea azul, estación "Centro".
                  </p>
                </div>

                <div>
                  <h4 class="font-semibold text-gray-800 mb-2 flex items-center">
                    <i class="fas fa-walking text-purple-600 mr-2"></i>
                    Puntos de Referencia
                  </h4>
                  <p class="text-gray-600 text-sm">
                    Frente al Parque Central, a dos cuadras del Hospital Regional 
                    y al lado de la Escuela Primaria San José.
                  </p>
                </div>

                <div class="bg-blue-50 p-4 rounded-lg">
                  <h4 class="font-semibold text-blue-800 mb-2 flex items-center">
                    <i class="fas fa-info-circle text-blue-600 mr-2"></i>
                    Información Adicional
                  </h4>
                  <ul class="text-blue-700 text-sm space-y-1">
                    <li>• Estacionamiento gratuito disponible</li>
                    <li>• Acceso para personas con discapacidad</li>
                    <li>• Área de juegos para niños</li>
                    <li>• Cafetería y librería cristiana</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Llamado a la Acción -->
    <section class="py-16 bg-gradient-to-r from-green-600 to-blue-600 text-white">
      <div class="container mx-auto px-4 text-center">
        <h2 class="text-4xl font-bold mb-4">¿Te gustaría visitarnos?</h2>
        <p class="text-xl text-green-100 mb-8 max-w-2xl mx-auto">
          Nuestras puertas están siempre abiertas. Ven como eres, te recibiremos con amor
        </p>
        <router-link 
          to="/eventos" 
          class="bg-white text-green-600 px-8 py-4 rounded-lg hover:bg-green-50 transition-colors font-semibold inline-block"
        >
          <i class="fas fa-calendar-alt mr-2"></i>
          Ver Próximos Eventos
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const procesando = ref(false)

const formulario = ref({
  tipo: '',
  nombre: '',
  email: '',
  telefono: '',
  mensaje: '',
  contactoPreferido: 'email',
  urgente: false,
  aceptaPrivacidad: false
})

const enviarMensaje = async () => {
  procesando.value = true
  
  try {
    // Simular envío del mensaje
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // En una aplicación real, aquí se enviaría el mensaje a un servidor
    console.log('Mensaje enviado:', formulario.value)
    
    // Mostrar mensaje de éxito
    alert('¡Mensaje enviado exitosamente! Te contactaremos pronto.')
    
    // Resetear formulario
    formulario.value = {
      tipo: '',
      nombre: '',
      email: '',
      telefono: '',
      mensaje: '',
      contactoPreferido: 'email',
      urgente: false,
      aceptaPrivacidad: false
    }
    
  } catch (error) {
    alert('Error al enviar el mensaje. Por favor, inténtalo nuevamente.')
  } finally {
    procesando.value = false
  }
}
</script>
