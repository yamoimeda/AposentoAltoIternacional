<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="show"
        @click.self="cerrar"
        class="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4 overflow-y-auto"
      >
        <div class="bg-white rounded-2xl shadow-2xl max-w-2xl w-full my-8 animate-fade-in-up overflow-hidden flex flex-col max-h-[90vh]">
          <!-- Header -->
          <div class="bg-gradient-to-r from-indigo-700 to-purple-700 p-6 flex-shrink-0 text-white">
            <div class="flex justify-between items-center">
              <div>
                <h2 class="text-xl font-bold flex items-center gap-2">
                  <i class="fas fa-church"></i>
                  Gestión de Iglesias y Mentores
                </h2>
                <p class="text-xs text-indigo-100 mt-1">
                  Administra las sedes e iglesias disponibles y la lista de mentores/líderes.
                </p>
              </div>
              <button
                @click="cerrar"
                :disabled="guardando"
                class="hover:bg-white/20 rounded-lg p-2 transition-colors disabled:opacity-50"
              >
                <i class="fas fa-times text-xl"></i>
              </button>
            </div>

            <!-- Tab Switcher -->
            <div class="flex gap-2 mt-5 border-b border-indigo-500/40 pb-1">
              <button
                @click="activeTab = 'iglesias'"
                :class="[
                  'px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2',
                  activeTab === 'iglesias'
                    ? 'bg-white text-indigo-700 shadow-md'
                    : 'text-indigo-100 hover:bg-white/10'
                ]"
              >
                <i class="fas fa-place-of-worship"></i>
                Iglesias / Sedes ({{ iglesias.length }})
              </button>
              <button
                @click="activeTab = 'mentores'"
                :class="[
                  'px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2',
                  activeTab === 'mentores'
                    ? 'bg-white text-indigo-700 shadow-md'
                    : 'text-indigo-100 hover:bg-white/10'
                ]"
              >
                <i class="fas fa-user-tie"></i>
                Mentores / Líderes ({{ mentores.length }})
              </button>
            </div>
          </div>

          <!-- Body -->
          <div class="p-6 overflow-y-auto flex-1 space-y-4">
            <!-- Loader al cargar -->
            <div v-if="cargando" class="py-12 text-center text-slate-400">
              <i class="fas fa-spinner fa-spin text-3xl text-indigo-600 mb-2"></i>
              <p class="text-xs font-medium">Cargando datos de configuración...</p>
            </div>

            <template v-else>
              <!-- TAB 1: IGLESIAS -->
              <div v-if="activeTab === 'iglesias'" class="space-y-4">
                <!-- Formulario agregar iglesia -->
                <form @submit.prevent="agregarIglesia" class="flex gap-2">
                  <input
                    v-model="nuevaIglesia"
                    type="text"
                    placeholder="Nombre de la nueva iglesia o sede..."
                    class="flex-1 px-3.5 py-2 border border-slate-300 rounded-xl text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-slate-800"
                  />
                  <button
                    type="submit"
                    :disabled="!nuevaIglesia.trim()"
                    class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-semibold shadow-sm transition-colors disabled:opacity-50 flex items-center gap-1.5 cursor-pointer"
                  >
                    <i class="fas fa-plus"></i> Agregar
                  </button>
                </form>

                <!-- Lista de iglesias -->
                <div class="border border-slate-200 rounded-xl divide-y divide-slate-100 bg-white">
                  <div
                    v-for="(iglesia, idx) in iglesias"
                    :key="idx"
                    class="p-3 flex items-center justify-between gap-2 hover:bg-slate-50 transition-colors"
                  >
                    <!-- Vista normal / Edición -->
                    <div v-if="editingIglesiaIdx === idx" class="flex items-center gap-2 flex-1">
                      <input
                        v-model="editingIglesiaText"
                        type="text"
                        class="flex-1 px-3 py-1 border border-indigo-400 rounded-lg text-xs text-slate-900 focus:outline-none"
                        @keyup.enter="guardarEdicionIglesia(idx)"
                        @keyup.esc="cancelarEdicionIglesia"
                      />
                      <button
                        @click="guardarEdicionIglesia(idx)"
                        class="p-1.5 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 text-xs"
                        title="Guardar"
                      >
                        <i class="fas fa-check"></i>
                      </button>
                      <button
                        @click="cancelarEdicionIglesia"
                        class="p-1.5 bg-slate-200 text-slate-700 rounded-lg hover:bg-slate-300 text-xs"
                        title="Cancelar"
                      >
                        <i class="fas fa-times"></i>
                      </button>
                    </div>

                    <div v-else class="flex items-center gap-2 text-xs font-semibold text-slate-800 flex-1">
                      <i class="fas fa-church text-indigo-500 text-xs"></i>
                      <span>{{ iglesia }}</span>
                    </div>

                    <div v-if="editingIglesiaIdx !== idx" class="flex items-center gap-1">
                      <button
                        @click="iniciarEdicionIglesia(idx, iglesia)"
                        class="p-1.5 text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors text-xs"
                        title="Editar"
                      >
                        <i class="fas fa-pen"></i>
                      </button>
                      <button
                        @click="eliminarIglesia(idx)"
                        class="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors text-xs"
                        title="Eliminar"
                      >
                        <i class="fas fa-trash"></i>
                      </button>
                    </div>
                  </div>

                  <div v-if="iglesias.length === 0" class="p-8 text-center text-xs text-slate-400">
                    No hay iglesias registradas. Agrega una arriba.
                  </div>
                </div>
              </div>

              <!-- TAB 2: MENTORES -->
              <div v-if="activeTab === 'mentores'" class="space-y-4">
                <!-- Formulario agregar mentor -->
                <form @submit.prevent="agregarMentor" class="flex gap-2">
                  <input
                    v-model="nuevoMentor"
                    type="text"
                    placeholder="Nombre del nuevo mentor/líder (ej: Juan Pérez - Pastor)..."
                    class="flex-1 px-3.5 py-2 border border-slate-300 rounded-xl text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-slate-800"
                  />
                  <button
                    type="submit"
                    :disabled="!nuevoMentor.trim()"
                    class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-semibold shadow-sm transition-colors disabled:opacity-50 flex items-center gap-1.5 cursor-pointer"
                  >
                    <i class="fas fa-plus"></i> Agregar
                  </button>
                </form>

                <!-- Lista de mentores -->
                <div class="border border-slate-200 rounded-xl divide-y divide-slate-100 bg-white">
                  <div
                    v-for="(mentor, idx) in mentores"
                    :key="idx"
                    class="p-3 flex items-center justify-between gap-2 hover:bg-slate-50 transition-colors"
                  >
                    <div v-if="editingMentorIdx === idx" class="flex items-center gap-2 flex-1">
                      <input
                        v-model="editingMentorText"
                        type="text"
                        class="flex-1 px-3 py-1 border border-indigo-400 rounded-lg text-xs text-slate-900 focus:outline-none"
                        @keyup.enter="guardarEdicionMentor(idx)"
                        @keyup.esc="cancelarEdicionMentor"
                      />
                      <button
                        @click="guardarEdicionMentor(idx)"
                        class="p-1.5 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 text-xs"
                        title="Guardar"
                      >
                        <i class="fas fa-check"></i>
                      </button>
                      <button
                        @click="cancelarEdicionMentor"
                        class="p-1.5 bg-slate-200 text-slate-700 rounded-lg hover:bg-slate-300 text-xs"
                        title="Cancelar"
                      >
                        <i class="fas fa-times"></i>
                      </button>
                    </div>

                    <div v-else class="flex items-center gap-2 text-xs font-semibold text-slate-800 flex-1">
                      <i class="fas fa-user-tie text-purple-500 text-xs"></i>
                      <span>{{ mentor }}</span>
                    </div>

                    <div v-if="editingMentorIdx !== idx" class="flex items-center gap-1">
                      <button
                        @click="iniciarEdicionMentor(idx, mentor)"
                        class="p-1.5 text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors text-xs"
                        title="Editar"
                      >
                        <i class="fas fa-pen"></i>
                      </button>
                      <button
                        @click="eliminarMentor(idx)"
                        class="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors text-xs"
                        title="Eliminar"
                      >
                        <i class="fas fa-trash"></i>
                      </button>
                    </div>
                  </div>

                  <div v-if="mentores.length === 0" class="p-8 text-center text-xs text-slate-400">
                    No hay mentores registrados. Agrega uno arriba.
                  </div>
                </div>
              </div>

              <!-- Mensaje de estado -->
              <div
                v-if="mensaje"
                :class="[
                  'p-3.5 rounded-xl text-xs font-semibold flex items-center gap-2',
                  mensaje.tipo === 'success' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-rose-50 text-rose-700 border border-rose-200'
                ]"
              >
                <i :class="['text-base', mensaje.tipo === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle']"></i>
                {{ mensaje.texto }}
              </div>
            </template>
          </div>

          <!-- Footer -->
          <div class="bg-slate-50 px-6 py-4 border-t border-slate-200 flex justify-between items-center flex-shrink-0">
            <span class="text-[11px] text-slate-400">Los cambios se aplicarán inmediatamente a nuevos registros.</span>
            <div class="flex gap-2">
              <button
                type="button"
                @click="cerrar"
                :disabled="guardando"
                class="px-4 py-2 border border-slate-300 text-slate-700 rounded-xl hover:bg-slate-100 font-semibold text-xs transition-colors disabled:opacity-50"
              >
                Cancelar
              </button>
              <button
                type="button"
                @click="guardarCambiosFirestore"
                :disabled="guardando || cargando"
                class="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl font-semibold text-xs shadow-md transition-colors disabled:opacity-50 flex items-center gap-2 cursor-pointer"
              >
                <i v-if="guardando" class="fas fa-spinner fa-spin"></i>
                <i v-else class="fas fa-save"></i>
                {{ guardando ? 'Guardando...' : 'Guardar Todo' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, watch } from 'vue'
import { db } from '../firebase'
import { doc, getDoc, setDoc } from 'firebase/firestore'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'saved'])

const activeTab = ref('iglesias')
const cargando = ref(false)
const guardando = ref(false)
const mensaje = ref(null)

const iglesias = ref([])
const mentores = ref([])

const nuevaIglesia = ref('')
const nuevoMentor = ref('')

const editingIglesiaIdx = ref(null)
const editingIglesiaText = ref('')

const editingMentorIdx = ref(null)
const editingMentorText = ref('')

watch(() => props.show, (val) => {
  if (val) {
    cargarConfiguracion()
  }
})

const cargarConfiguracion = async () => {
  cargando.value = true
  mensaje.value = null
  try {
    let snap = await getDoc(doc(db, 'configuracion', 'iglesias'))
    if (!snap.exists()) {
      snap = await getDoc(doc(db, 'configuracion', 'igelsias'))
    }
    if (snap.exists()) {
      const data = snap.data()
      iglesias.value = [...(data.iglesias || data.nombre || [])]
      mentores.value = [...(data.mentores || [])]
    } else {
      // Valores por defecto
      iglesias.value = ['Panamá', 'Colón', 'Penonomé', 'Barraza', 'Pedregal', 'Arraiján', 'Chilibre', 'Invitado', 'Sede Cañitas', 'Sede San Miguelito']
      mentores.value = ['Wendy Brathwaite - Profeta', 'Ramses Álvarez - Pastor', 'Sin mentor']
    }
  } catch (e) {
    console.error('Error cargando configuración de iglesias:', e)
    mensaje.value = { tipo: 'error', texto: 'No se pudo cargar la configuración de Firestore.' }
  } finally {
    cargando.value = false
  }
}

// ---- IGLESIAS ----
const agregarIglesia = () => {
  const val = nuevaIglesia.value.trim()
  if (!val) return
  if (iglesias.value.includes(val)) {
    alert('Esta iglesia ya está en la lista.')
    return
  }
  iglesias.value.push(val)
  nuevaIglesia.value = ''
}

const iniciarEdicionIglesia = (idx, text) => {
  editingIglesiaIdx.value = idx
  editingIglesiaText.value = text
}

const guardarEdicionIglesia = (idx) => {
  const val = editingIglesiaText.value.trim()
  if (val) {
    iglesias.value[idx] = val
  }
  cancelarEdicionIglesia()
}

const cancelarEdicionIglesia = () => {
  editingIglesiaIdx.value = null
  editingIglesiaText.value = ''
}

const eliminarIglesia = (idx) => {
  iglesias.value.splice(idx, 1)
}

// ---- MENTORES ----
const agregarMentor = () => {
  const val = nuevoMentor.value.trim()
  if (!val) return
  if (mentores.value.includes(val)) {
    alert('Este mentor ya está en la lista.')
    return
  }
  mentores.value.push(val)
  nuevoMentor.value = ''
}

const iniciarEdicionMentor = (idx, text) => {
  editingMentorIdx.value = idx
  editingMentorText.value = text
}

const guardarEdicionMentor = (idx) => {
  const val = editingMentorText.value.trim()
  if (val) {
    mentores.value[idx] = val
  }
  cancelarEdicionMentor()
}

const cancelarEdicionMentor = () => {
  editingMentorIdx.value = null
  editingMentorText.value = ''
}

const eliminarMentor = (idx) => {
  mentores.value.splice(idx, 1)
}

// ---- GUARDAR TODO ----
const guardarCambiosFirestore = async () => {
  guardando.value = true
  mensaje.value = null
  try {
    const payload = {
      nombre: iglesias.value,
      iglesias: iglesias.value,
      mentores: mentores.value,
      updatedAt: new Date().toISOString()
    }

    // Guardar en ambas claves para garantizar retrocompatibilidad absoluta
    await setDoc(doc(db, 'configuracion', 'iglesias'), payload)
    await setDoc(doc(db, 'configuracion', 'igelsias'), payload)

    mensaje.value = { tipo: 'success', texto: '¡Configuración guardada exitosamente!' }
    emit('saved')

    setTimeout(() => {
      cerrar()
    }, 1200)
  } catch (e) {
    console.error('Error guardando configuración:', e)
    mensaje.value = { tipo: 'error', texto: 'Error al guardar la configuración en Firestore.' }
  } finally {
    guardando.value = false
  }
}

const cerrar = () => {
  if (!guardando.value) {
    mensaje.value = null
    emit('close')
  }
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.25s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-fade-in-up {
  animation: fade-in-up 0.3s ease-out;
}
</style>
