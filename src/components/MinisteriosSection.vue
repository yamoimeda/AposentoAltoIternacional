<template>
   <!-- Servicios y Ministerios modernos -->
    <section class="py-24 relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900"></div>
      <div class="absolute inset-0">
        <div class="absolute top-20 left-20 w-64 h-64 bg-gradient-to-r from-yellow-400 to-orange-400 rounded-full mix-blend-multiply filter blur-3xl opacity-10 animate-float"></div>
        <div class="absolute bottom-20 right-20 w-64 h-64 bg-gradient-to-r from-pink-400 to-purple-400 rounded-full mix-blend-multiply filter blur-3xl opacity-10 animate-float" style="animation-delay: 3s;"></div>
      </div>
      
      <div class="relative container mx-auto px-4">
        <div class="text-center mb-16 animate-fade-in-up">
          <div class="inline-flex items-center bg-white/10 backdrop-blur-sm text-white px-6 py-3 rounded-full text-sm font-semibold mb-6 border border-white/20">
            
            Ministerios
          </div>
          <h2 class="text-5xl md:text-6xl font-black text-white mb-6">
            Espacios para
            <span class="bg-gradient-to-r from-yellow-400 to-pink-400 bg-clip-text text-transparent">
              Crecer y Servir
            </span>
          </h2>
          <p class="text-xl text-indigo-200 max-w-3xl mx-auto font-light">
            Encuentra tu lugar en nuestra comunidad y descubre cómo puedes hacer la diferencia
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div class="glass-effect p-8 rounded-3xl text-center hover-lift animate-fade-in-up group" style="animation-delay: 0.1s">
            <div class="w-20 h-20 bg-gradient-to-br from-blue-400 to-indigo-600 rounded-3xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300 shadow-xl">
              <i class="fas fa-pray text-3xl text-white"></i>
            </div>
            <h3 class="text-2xl font-bold text-white mb-4">Oración e Intercesión</h3>
            <p class="text-indigo-200 leading-relaxed">Únete a nuestro tiempo de oración comunitaria y experimenta el poder de la oración</p>
          </div>

          <div class="glass-effect p-8 rounded-3xl text-center hover-lift animate-fade-in-up group" style="animation-delay: 0.2s">
            <div class="w-20 h-20 bg-gradient-to-br from-green-400 to-emerald-600 rounded-3xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300 shadow-xl">
              <i class="fas fa-users text-3xl text-white"></i>
            </div>
            <h3 class="text-2xl font-bold text-white mb-4">Jóvenes</h3>
            <p class="text-indigo-200 leading-relaxed">Ministerio dinámico y vibrante diseñado especialmente para la nueva generación</p>
          </div>

          <div class="glass-effect p-8 rounded-3xl text-center hover-lift animate-fade-in-up group" style="animation-delay: 0.3s">
            <div class="w-20 h-20 bg-gradient-to-br from-yellow-400 to-orange-600 rounded-3xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300 shadow-xl">
              <i class="fas fa-child text-3xl text-white"></i>
            </div>
            <h3 class="text-2xl font-bold text-white mb-4">Niños</h3>
            <p class="text-indigo-200 leading-relaxed">Educación cristiana divertida y significativa para nuestros pequeños</p>
          </div>

          <div class="glass-effect p-8 rounded-3xl text-center hover-lift animate-fade-in-up group" style="animation-delay: 0.4s">
            <div class="w-20 h-20 bg-gradient-to-br from-purple-400 to-pink-600 rounded-3xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300 shadow-xl">
              <i class="fas fa-heart text-3xl text-white"></i>
            </div>
            <h3 class="text-2xl font-bold text-white mb-4">Matrimonios</h3>
            <p class="text-indigo-200 leading-relaxed">Fortaleciendo las relaciones familiares con principios bíblicos sólidos</p>
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