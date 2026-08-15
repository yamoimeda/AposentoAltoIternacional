# Sistema de Diseño & Guía Estética — El Aposento Alto Internacional

## 1. Filosofía de Diseño (Enterprise & Modern Light)
- **Claridad y Función Primaria**: Interfaz limpia, ágil y sin elementos decorativos excesivos ni héroes redundantes cuando existen barras de navegación fijas.
- **Jerarquía Visual y Tipografía**: Estructura de encabezados claros, espacios de aire (*whitespace*) equilibrados y jerarquía basada en la escala Slate/Indigo.
- **Aislamiento por Contexto y Trazabilidad Contable**: Los datos financieros e inscripciones se mantienen inmutables (*snapshots*) y aislados por cada evento (`eventoId`), protegiendo la integridad histórica de recibos y auditorías.
- **Microinteracciones y Feedback en Tiempo Real**: Componentes adaptables con animaciones fluidas, estados de carga (*spinners*), alertas contextuales de error/éxito y transiciones al pasar el cursor (*hover*).
- **Accesibilidad y Conexión Segura**: Indicadores visuales de estados de seguridad, contraste adecuado y estados de foco visibles.

---

## 2. Paleta de Colores & Tokens Visuales
- **Fondos**:
  - Superficie principal: `bg-slate-50` / `bg-slate-50/80`
  - Tarjetas y Contenedores: `bg-white`
  - Encabezados de Modal y Acentos Institucionales: `bg-slate-900 text-white` / `bg-indigo-950`
- **Bordes & Sombras**:
  - Bordes sutiles: `border-slate-100` / `border-slate-200`
  - Sombras suaves: `shadow-sm`, `shadow-md`, `shadow-xl shadow-slate-200/60`
  - Líneas decorativas superiores: `bg-gradient-to-r from-indigo-500 via-purple-500 to-indigo-600`
- **Botones & Acentos**:
  - Primario: `bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800 text-white`
  - Secundario / Retorno: `bg-white border border-slate-200 hover:bg-indigo-50/50 hover:border-indigo-200`
  - Éxito / Cifrado: `text-emerald-600`, `bg-emerald-50 text-emerald-700 border-emerald-200`
  - Archivado / Advertencia: `bg-amber-50 text-amber-700 border-amber-200`
  - Alertas / Errores / Eliminar: `bg-rose-50 border-rose-200 text-rose-800`

---

## 3. Patrones de Componentes & Arquitectura Reutilizable

### A. Botón y Enlace de Navegación de Retorno (`Back Navigation`)
```html
<router-link
  to="/admin"
  class="inline-flex items-center gap-2 text-xs font-semibold text-slate-500 hover:text-indigo-600 transition-colors group"
>
  <div class="w-7 h-7 rounded-lg bg-white border border-slate-200 flex items-center justify-center shadow-xs group-hover:border-indigo-200 group-hover:bg-indigo-50/50 transition-all">
    <i class="fas fa-arrow-left text-[11px] group-hover:-translate-x-0.5 transition-transform"></i>
  </div>
  <span>Volver al Panel Admin</span>
</router-link>
```

### B. Encabezado de Página y Barra de Acciones (`Enterprise Page Header`)
```html
<div class="mb-8 flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-200/80">
  <div>
    <div class="flex items-center gap-2 text-xs font-medium text-slate-500 mb-1.5">
      <router-link to="/" class="hover:text-indigo-600 transition-colors">Inicio</router-link>
      <span>/</span>
      <router-link to="/admin" class="hover:text-indigo-600 transition-colors">Panel Admin</router-link>
      <span>/</span>
      <span class="text-slate-900 font-semibold">Inscripciones</span>
    </div>
    <h1 class="text-2xl sm:text-3xl font-bold tracking-tight text-slate-900 flex items-center gap-3">
      <span>Inscripciones</span>
      <span class="text-xs font-bold bg-indigo-50 border border-indigo-200 text-indigo-700 px-3 py-1 rounded-lg">
        Conferencia 2026
      </span>
    </h1>
    <p class="text-xs sm:text-sm text-slate-500 mt-1">
      Visualización y gestión de participantes registrados por evento.
    </p>
  </div>
  <div class="flex flex-wrap items-center gap-3">
    <!-- Botones de Acción Primaria -->
  </div>
</div>
```

### C. Modal con Encabezado Sticky Ajustado a Borde Superior (`Top-Flush Dark Sticky Modal Header`)
```html
<div class="fixed inset-0 bg-slate-950/60 backdrop-blur-xs flex items-center justify-center z-50 p-3 sm:p-6 overflow-y-auto">
  <div class="bg-white rounded-2xl shadow-2xl w-full max-w-xl border border-slate-200 my-auto max-h-[90vh] overflow-y-auto relative p-0">
    <!-- Sticky Header Top-Flush Dark -->
    <div class="sticky top-0 z-20 bg-slate-900 text-white px-5 sm:px-6 py-4 rounded-t-2xl flex justify-between items-center shadow-md">
      <h3 class="text-lg sm:text-xl font-bold text-white tracking-tight flex items-center gap-2.5">
        <i class="fas fa-pen-to-square text-indigo-400"></i>
        <span>Editar Evento</span>
      </h3>
      <button type="button" @click="close" class="w-8 h-8 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white flex items-center justify-center transition-colors cursor-pointer">
        <i class="fas fa-times text-base"></i>
      </button>
    </div>
    <div class="p-5 sm:p-6">
      <!-- Cuerpo del Formulario -->
    </div>
  </div>
</div>
```

### D. Organización de Boletos: Secciones Activos vs Archivados (`Ticket Archiving Pattern`)
```html
<!-- Sección Boletos Activos -->
<div v-if="boletosActivos.length" class="space-y-2 mb-4">
  <div class="text-xs font-bold text-slate-700 uppercase tracking-wider mb-1 flex items-center gap-1.5">
    <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
    <span>Boletos Activos ({{ boletosActivos.length }})</span>
  </div>
  <div v-for="t in boletosActivos" :key="t.id" class="flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs text-sm">
    <div class="flex-1 min-w-0">
      <div class="font-bold text-slate-900 truncate">{{ t.nombre }}</div>
      <div class="text-xs font-semibold text-indigo-600 mt-0.5">${{ t.precio }} USD</div>
    </div>
    <div class="flex items-center gap-2 self-end sm:self-center shrink-0">
      <button type="button" @click="archivar(t.id)" class="text-xs font-semibold px-3 py-1.5 rounded-lg bg-amber-50 text-amber-700 border border-amber-200">Archivar</button>
      <button type="button" @click="eliminar(t.id)" class="text-xs font-semibold px-3 py-1.5 rounded-lg bg-rose-50 text-rose-600 border border-rose-100">Eliminar</button>
    </div>
  </div>
</div>

<!-- Sección Boletos Archivados -->
<div v-if="boletosArchivados.length" class="space-y-2 pt-3 border-t border-slate-100">
  <div class="text-xs font-bold text-amber-700 uppercase tracking-wider mb-1 flex items-center gap-1.5">
    <i class="fas fa-box-archive text-amber-600 text-xs"></i>
    <span>Boletos Archivados ({{ boletosArchivados.length }})</span>
  </div>
  <div v-for="t in boletosArchivados" :key="t.id" class="flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 bg-slate-50/80 p-3.5 rounded-xl border border-amber-200/60 text-sm">
    <div class="flex-1 min-w-0">
      <div class="font-bold text-slate-700 truncate opacity-75">{{ t.nombre }}</div>
      <div class="text-xs font-semibold text-slate-500 mt-0.5">${{ t.precio }} USD</div>
    </div>
    <div class="flex items-center gap-2 self-end sm:self-center shrink-0">
      <button type="button" @click="reactivar(t.id)" class="text-xs font-semibold px-3 py-1.5 rounded-lg bg-emerald-50 text-emerald-700 border border-emerald-200">Reactivar</button>
      <button type="button" @click="eliminar(t.id)" class="text-xs font-semibold px-3 py-1.5 rounded-lg bg-rose-50 text-rose-600 border border-rose-100">Eliminar</button>
    </div>
  </div>
</div>
```

### E. Diálogo de Sincronización Masiva en Lote (`Client-side Batch Sync Pattern`)
```html
<div v-if="mostrarModalActualizarPasadas" class="fixed inset-0 bg-slate-950/70 backdrop-blur-xs flex items-center justify-center z-[60] p-4">
  <div class="bg-white rounded-2xl p-6 w-full max-w-md shadow-2xl border border-slate-200">
    <div class="w-12 h-12 rounded-2xl bg-amber-50 border border-amber-200 text-amber-600 flex items-center justify-center text-xl mb-4">
      <i class="fas fa-triangle-exclamation"></i>
    </div>
    <h3 class="text-lg font-bold text-slate-900 mb-2">Inscripciones Existentes Detectadas</h3>
    <p class="text-xs text-slate-600 leading-relaxed mb-3">
      Se encontraron <strong class="text-indigo-600 font-bold">{{ conteo }} inscripciones</strong> registradas previamente.
    </p>
    <div class="flex flex-col gap-2">
      <button type="button" @click="confirmar(true)" class="w-full py-2.5 px-4 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs rounded-xl shadow-md">
        Sí, actualizar inscripciones registradas
      </button>
      <button type="button" @click="confirmar(false)" class="w-full py-2.5 px-4 bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs rounded-xl">
        Mantener precio histórico (Recomendado)
      </button>
    </div>
  </div>
</div>
```

### F. Tarjetas de Métricas KPI Combinadas (`Combined KPI Stat Card`)
```html
<div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-xs flex items-center justify-between divide-x divide-slate-100 max-w-xl">
  <div class="flex items-center gap-3.5 pr-4 flex-1">
    <div class="w-11 h-11 rounded-xl bg-indigo-50 border border-indigo-100 flex items-center justify-center text-indigo-600 text-lg shrink-0">
      <i class="fas fa-calendar-check"></i>
    </div>
    <div>
      <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider block">Total Eventos</span>
      <span class="text-2xl font-bold text-slate-900">12</span>
    </div>
  </div>

  <div class="flex items-center gap-3.5 pl-6 flex-1">
    <div class="w-11 h-11 rounded-xl bg-emerald-50 border border-emerald-100 flex items-center justify-center text-emerald-600 text-lg shrink-0">
      <i class="fas fa-clock"></i>
    </div>
    <div>
      <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider block">Próximos</span>
      <span class="text-2xl font-bold text-slate-900">5</span>
    </div>
  </div>
</div>
```

---

## 4. Evolución del Sistema
Este documento sirve como la guía maestra de arquitectura visual y lógica para actualizar y mantener la coherencia en toda la plataforma El Aposento Alto Internacional.
