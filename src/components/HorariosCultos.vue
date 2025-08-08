<template>
   <!-- Servicios y Ministerios modernos -->
     <!-- Información de Contacto Rápida moderna -->
    <section class="py-16 bg-gradient-to-br from-gray-900 to-black text-white">
      <div class="container mx-auto px-4">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
          <div class="animate-fade-in-up" style="animation-delay: 0.1s">
            <div class="w-16 h-16 bg-gradient-to-br from-red-500 to-pink-600 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-xl">
              <i class="fas fa-map-marker-alt text-2xl text-white"></i>
            </div>
            <h3 class="text-xl font-bold mb-4">Ubicación</h3>
            <p class="text-gray-300 leading-relaxed">Calle 6ta, Pueblo Nuevo<br>Panamá, Ciudad de Panamá</p>
          </div>
          
          <div class="animate-fade-in-up" style="animation-delay: 0.2s">
            <div class="w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-xl">
              <i class="fas fa-clock text-2xl text-white"></i>
            </div>
            <h3 class="text-xl font-bold mb-4">Horarios de Culto</h3>
            <p class="text-gray-300 leading-relaxed">Domingos: 11:00 AM<br>Miércoles: 7:00 PM
            <br>Viernes: 7:00 PM</p>
          </div>
          
          <div class="animate-fade-in-up" style="animation-delay: 0.3s">
            <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-xl">
              <i class="fas fa-phone text-2xl text-white"></i>
            </div>
            <h3 class="text-xl font-bold mb-4">Contacto</h3>
            <p class="text-gray-300 leading-relaxed">+507 000-000<br>info@aposentoalto.org</p>
          </div>
        </div>
      </div>
    </section>
</template>

<script setup>

</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Pausar auto-play al hacer hover */
.container:hover {
  /* El auto-play se puede pausar con JavaScript en el futuro */
}
</style>