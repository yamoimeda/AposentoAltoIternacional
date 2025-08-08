<script setup>
import NavBar from './components/NavBar.vue'
import FooterSection from './components/FooterSection.vue'
</script>

<template>

    <NavBar />
    <main class="flex-1">
      <router-view />
    </main>
    <FooterSection />
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');


/* Estilos globales modernos */
#app {
  font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background: rgb(238, 238, 238);
  min-height: 100dvh;
  min-width: 100%;
}

/* Scroll suave y moderno */
html {
  scroll-behavior: smooth;
}

body {
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}

/* Scrollbar moderno */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

::-webkit-scrollbar-thumb {
  background: var(--primary-gradient);
  border-radius: 20px;
  border: 2px solid transparent;
  background-clip: content-box;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--secondary-gradient);
  background-clip: content-box;
}

/* Transiciones suaves y modernas */
* {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Efectos de glassmorphism */
.glass-effect {
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.18);
  box-shadow: var(--shadow-large);
}

.glass-dark {
  background: rgba(0, 0, 0, 0.25);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Botones modernos con gradientes */
.btn-modern {
  background: var(--primary-gradient);
  border: none;
  border-radius: var(--border-radius);
  padding: 12px 24px;
  color: white;
  font-weight: 600;
  text-transform: none;
  letter-spacing: 0.5px;
  box-shadow: var(--shadow-medium);
  position: relative;
  overflow: hidden;
  cursor: pointer;
}

.btn-modern::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.btn-modern:hover::before {
  left: 100%;
}

.btn-modern:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-large);
}

.btn-secondary {
  background: var(--secondary-gradient);
}

.btn-success {
  background: var(--success-gradient);
}

/* Cards modernas */
.card-modern {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-radius: var(--border-radius-lg);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: var(--shadow-medium);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.card-modern:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-xl);
  border: 1px solid rgba(255, 255, 255, 0.4);
}

/* Inputs modernos */
.input-modern {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: var(--border-radius);
  padding: 12px 16px;
  font-family: inherit;
  font-size: 14px;
  transition: all 0.3s ease;
}

.input-modern:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  background: rgba(255, 255, 255, 0.95);
}

/* Animaciones modernas */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

/* Clases de utilidad para animaciones */
.animate-fade-in-up {
  animation: fadeInUp 0.6s ease-out;
}

.animate-fade-in-down {
  animation: fadeInDown 0.6s ease-out;
}

.animate-scale-in {
  animation: scaleIn 0.6s ease-out;
}

.animate-slide-in-left {
  animation: slideInLeft 0.6s ease-out;
}

.animate-slide-in-right {
  animation: slideInRight 0.6s ease-out;
}

.animate-pulse {
  animation: pulse 2s infinite;
}

.animate-float {
  animation: float 3s ease-in-out infinite;
}

/* Focus moderno para accesibilidad */
button:focus-visible,
input:focus-visible,
textarea:focus-visible,
select:focus-visible,
a:focus-visible {
  outline: 3px solid #667eea;
  outline-offset: 2px;
  border-radius: 8px;
}

/* Efectos de hover modernos */
.hover-lift {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.hover-lift:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-large);
}

.hover-glow {
  transition: box-shadow 0.3s ease;
}

.hover-glow:hover {
  box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
}

/* Responsive design mejorado */
@media (max-width: 768px) {
  :root {
    --border-radius: 12px;
    --border-radius-lg: 16px;
    --border-radius-xl: 20px;
  }
  
  .btn-modern {
    padding: 10px 20px;
    font-size: 14px;
  }
}

/* Efectos de parallax sutiles */
.parallax {
  background-attachment: fixed;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
}

/* Loading animation moderna */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-spinner {
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top: 3px solid #667eea;
  width: 24px;
  height: 24px;
  animation: spin 1s linear infinite;
}

/* Modo oscuro */
@media (prefers-color-scheme: dark) {
  
  
  .card-modern {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .input-modern {
    background: rgba(255, 255, 255, 0.1);
    border: 2px solid rgba(255, 255, 255, 0.2);
    color: white;
  }
  
  .input-modern::placeholder {
    color: rgba(255, 255, 255, 0.6);
  }
}
</style>

