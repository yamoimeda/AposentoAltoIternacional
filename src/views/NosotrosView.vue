<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Hero Section -->
    <section class="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-20 ">
      <div class="container mx-auto px-4 text-center pt-[80px]">
        <h1 class="text-4xl md:text-5xl font-bold mb-6">
          <i class="fas fa-church mr-3"></i>
          Nuestra Historia
        </h1>
        <p class="text-xl text-blue-100 max-w-3xl mx-auto">
          Conoce la historia, visión y valores que nos definen como comunidad de fe
        </p>
      </div>
    </section>

    <!-- Historia -->
    <section class="py-16 bg-white">
      <div class="container mx-auto px-4">
        <div class="max-w-4xl mx-auto">
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 class="text-3xl font-bold text-gray-800 mb-6">
                <i class="fas fa-history text-blue-600 mr-3"></i>
                Nuestra Historia
              </h2>
              <p class="text-gray-600 mb-4 text-lg leading-relaxed">
                Aposento Alto Internacional nació en 1995 como una pequeña congregación con el sueño 
                de crear un espacio donde las personas pudieran experimentar el amor transformador de Dios.
              </p>
              <p class="text-gray-600 mb-4 text-lg leading-relaxed">
                A lo largo de más de 25 años, hemos crecido no solo en número, sino en propósito y 
                compromiso con nuestra comunidad. Lo que comenzó con 20 personas reunidas en una sala, 
                hoy es una iglesia vibrante que impacta vidas en toda la región.
              </p>
              <p class="text-gray-600 text-lg leading-relaxed">
                Nuestro nombre "Aposento Alto" viene del lugar donde los discípulos se reunían para 
                orar y esperar la promesa del Espíritu Santo, simbolizando nuestro deseo de ser 
                un lugar de encuentro con Dios.
              </p>
            </div>
            <div>
              <img 
                src="https://images.unsplash.com/photo-1438032005730-c779502df39b?w=600&h=400&fit=crop" 
                alt="Historia de la iglesia"
                class="rounded-lg shadow-lg w-full"
              >
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Misión, Visión y Valores -->
    <section class="py-16 bg-gray-100">
      <div class="container mx-auto px-4">
        <div class="text-center mb-12">
          <h2 class="text-4xl font-bold text-gray-800 mb-4">
            <i class="fas fa-compass text-purple-600 mr-3"></i>
            Misión, Visión y Valores
          </h2>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <!-- Misión -->
          <div class="bg-white p-8 rounded-lg shadow-lg">
            <div class="text-center mb-6">
              <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <i class="fas fa-bullseye text-2xl text-blue-600"></i>
              </div>
              <h3 class="text-2xl font-bold text-gray-800">Misión</h3>
            </div>
            <p class="text-gray-600 text-center leading-relaxed">
              Conectar a las personas con Dios, edificar una comunidad de fe sólida y 
              transformar vidas a través del amor de Cristo, sirviendo con excelencia 
              a nuestra comunidad local y más allá.
            </p>
          </div>

          <!-- Visión -->
          <div class="bg-white p-8 rounded-lg shadow-lg">
            <div class="text-center mb-6">
              <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <i class="fas fa-eye text-2xl text-green-600"></i>
              </div>
              <h3 class="text-2xl font-bold text-gray-800">Visión</h3>
            </div>
            <p class="text-gray-600 text-center leading-relaxed">
              Ser una iglesia de influencia que forme discípulos comprometidos, 
              que impacte positivamente a las familias y sea un referente de esperanza 
              y transformación en nuestra región.
            </p>
          </div>

          <!-- Valores -->
          <div class="bg-white p-8 rounded-lg shadow-lg">
            <div class="text-center mb-6">
              <div class="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <i class="fas fa-heart text-2xl text-yellow-600"></i>
              </div>
              <h3 class="text-2xl font-bold text-gray-800">Valores</h3>
            </div>
            <ul class="text-gray-600 space-y-2">
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-2"></i>
                <span>Amor incondicional</span>
              </li>
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-2"></i>
                <span>Integridad y honestidad</span>
              </li>
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-2"></i>
                <span>Excelencia en el servicio</span>
              </li>
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-2"></i>
                <span>Comunidad y familia</span>
              </li>
              <li class="flex items-center">
                <i class="fas fa-check text-green-500 mr-2"></i>
                <span>Transformación personal</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- Liderazgo -->
    <section class="py-16 bg-white">
      <div class="container mx-auto px-4">
        <div class="text-center mb-12">
          <h2 class="text-4xl font-bold text-gray-800 mb-4">
            <i class="fas fa-users text-blue-600 mr-3"></i>
            Nuestro Liderazgo
          </h2>
          <p class="text-xl text-gray-600">Conoce a los pastores y líderes que sirven en nuestra iglesia</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
          <!-- Pastor Principal -->
          <div class="bg-gray-50 rounded-lg overflow-hidden shadow-lg">
            <img 
              src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=300&h=300&fit=crop&crop=face" 
              alt="Pastor Principal"
              class="w-full h-64 object-cover"
            >
            <div class="p-6">
              <h3 class="text-xl font-bold text-gray-800 mb-2">Pastor Carlos Mendoza</h3>
              <p class="text-blue-600 font-semibold mb-3">Pastor Principal</p>
              <p class="text-gray-600 text-sm">
                Con más de 20 años de ministerio, el Pastor Carlos lidera con pasión y sabiduría, 
                guiando a la congregación en crecimiento espiritual y comunitario.
              </p>
            </div>
          </div>

          <!-- Pastora Asociada -->
          <div class="bg-gray-50 rounded-lg overflow-hidden shadow-lg">
            <img 
              src="https://images.unsplash.com/photo-1494790108755-2616b612b740?w=300&h=300&fit=crop&crop=face" 
              alt="Pastora Asociada"
              class="w-full h-64 object-cover"
            >
            <div class="p-6">
              <h3 class="text-xl font-bold text-gray-800 mb-2">Pastora María González</h3>
              <p class="text-purple-600 font-semibold mb-3">Pastora Asociada</p>
              <p class="text-gray-600 text-sm">
                Especializada en ministerio familiar y de mujeres, la Pastora María trae 
                una perspectiva única de cuidado pastoral y enseñanza bíblica.
              </p>
            </div>
          </div>

          <!-- Pastor de Jóvenes -->
          <div class="bg-gray-50 rounded-lg overflow-hidden shadow-lg">
            <img 
              src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=300&fit=crop&crop=face" 
              alt="Pastor de Jóvenes"
              class="w-full h-64 object-cover"
            >
            <div class="p-6">
              <h3 class="text-xl font-bold text-gray-800 mb-2">Pastor David Ruiz</h3>
              <p class="text-green-600 font-semibold mb-3">Pastor de Jóvenes</p>
              <p class="text-gray-600 text-sm">
                Dinámico y apasionado por la nueva generación, el Pastor David desarrolla 
                programas innovadores para el crecimiento espiritual de los jóvenes.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Estadísticas -->
    <section class="py-16 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
      <div class="container mx-auto px-4">
        <div class="text-center mb-12">
          <h2 class="text-4xl font-bold mb-4">
            <i class="fas fa-chart-line mr-3"></i>
            Nuestro Impacto
          </h2>
          <p class="text-xl text-blue-100">Números que reflejan el crecimiento de nuestra comunidad</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div class="text-center">
            <div class="text-4xl font-bold mb-2">500+</div>
            <div class="text-blue-200">Miembros Activos</div>
          </div>
          <div class="text-center">
            <div class="text-4xl font-bold mb-2">25+</div>
            <div class="text-blue-200">Años de Ministerio</div>
          </div>
          <div class="text-center">
            <div class="text-4xl font-bold mb-2">50+</div>
            <div class="text-blue-200">Ministerios y Grupos</div>
          </div>
          <div class="text-center">
            <div class="text-4xl font-bold mb-2">1000+</div>
            <div class="text-blue-200">Vidas Transformadas</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Llamado a la acción -->
    <section class="py-16 bg-gray-100">
      <div class="container mx-auto px-4 text-center">
        <h2 class="text-4xl font-bold text-gray-800 mb-4">¿Te gustaría ser parte?</h2>
        <p class="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Te invitamos a conocer más sobre cómo puedes involucrarte en nuestra comunidad 
          y crecer en tu caminar con Dios
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <router-link 
            to="/eventos" 
            class="bg-blue-600 text-white px-8 py-4 rounded-lg hover:bg-blue-700 transition-colors font-semibold"
          >
            <i class="fas fa-calendar-alt mr-2"></i>
            Ver Próximos Eventos
          </router-link>
          <router-link 
            to="/contacto" 
            class="border-2 border-blue-600 text-blue-600 px-8 py-4 rounded-lg hover:bg-blue-50 transition-colors font-semibold"
          >
            <i class="fas fa-envelope mr-2"></i>
            Contáctanos
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
// Esta página es principalmente estática, no requiere lógica compleja
</script>
