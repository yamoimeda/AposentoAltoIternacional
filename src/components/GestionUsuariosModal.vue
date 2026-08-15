<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="show"
        @click.self="cerrar"
        class="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4 overflow-y-auto"
      >
        <div class="bg-white rounded-2xl shadow-2xl max-w-4xl w-full my-8 animate-fade-in-up overflow-hidden flex flex-col max-h-[92vh]">
          <!-- Header Enterprise -->
          <div class="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 p-6 flex-shrink-0 text-white border-b border-indigo-900/50">
            <div class="flex justify-between items-center">
              <div>
                <h2 class="text-xl font-bold flex items-center gap-2.5">
                  <i class="fas fa-user-gear text-indigo-400"></i>
                  Gestión de Cuentas y Control de Acceso
                </h2>
                <p class="text-xs text-slate-300 mt-1">
                  Administra credenciales, envía invitaciones por correo y asigna perfiles de acceso.
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

            <!-- Header Tabs -->
            <div class="flex items-center justify-between mt-5">
              <div class="flex gap-2">
                <button
                  @click="activeTab = 'lista'"
                  :class="[
                    'px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2',
                    activeTab === 'lista'
                      ? 'bg-white text-slate-900 shadow-md'
                      : 'text-slate-300 hover:bg-white/10'
                  ]"
                >
                  <i class="fas fa-users-gear"></i>
                  Directorio de Usuarios ({{ usuarios.length }})
                </button>
                <button
                  @click="activeTab = 'crear'"
                  :class="[
                    'px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2',
                    activeTab === 'crear'
                      ? 'bg-white text-slate-900 shadow-md'
                      : 'text-slate-300 hover:bg-white/10'
                  ]"
                >
                  <i class="fas fa-user-plus"></i>
                  Nuevo Usuario
                </button>
              </div>

              <button
                @click="cargarUsuarios"
                :disabled="cargando"
                class="text-xs text-indigo-300 hover:text-white flex items-center gap-1.5 transition-colors font-medium"
                title="Refrescar lista desde Firestore"
              >
                <i :class="['fas fa-rotate', cargando ? 'fa-spin' : '']"></i> Sincronizar
              </button>
            </div>
          </div>

          <!-- Body -->
          <div class="p-6 overflow-y-auto flex-1 space-y-4 bg-slate-50/60">
            <!-- Loading state -->
            <div v-if="cargando" class="py-16 text-center text-slate-400">
              <i class="fas fa-circle-notch fa-spin text-4xl text-indigo-600 mb-3 block mx-auto"></i>
              <p class="text-sm font-medium">Cargando directorio de cuentas y permisos...</p>
            </div>

            <template v-else>
              <!-- TAB 1: LISTA DE USUARIOS -->
              <div v-if="activeTab === 'lista'" class="space-y-4">
                <div class="border border-slate-200/90 rounded-2xl divide-y divide-slate-100 bg-white shadow-xs overflow-hidden">
                  <div
                    v-for="u in usuarios"
                    :key="u.id"
                    class="p-4 sm:p-5 flex flex-col md:flex-row md:items-center justify-between gap-4 hover:bg-slate-50/80 transition-colors"
                  >
                    <!-- Usuario Info -->
                    <div class="flex items-start gap-3.5 flex-1 min-w-0">
                      <div class="w-11 h-11 rounded-2xl bg-indigo-50 border border-indigo-100 flex items-center justify-center text-indigo-600 text-base font-bold shrink-0 mt-0.5 shadow-xs">
                        <i class="fas fa-user-shield"></i>
                      </div>

                      <div class="flex-1 min-w-0">
                        <div class="flex items-center gap-2 flex-wrap mb-1">
                          <p class="font-bold text-slate-900 text-sm truncate">
                            {{ u.nombre || u.correo || u.email || 'Usuario' }}
                          </p>
                          <span
                            :class="[
                              'text-[11px] font-semibold px-2.5 py-0.5 rounded-full border flex items-center gap-1',
                              obtenerPerfilUsuario(u.roles).badgeClass
                            ]"
                          >
                            <i :class="obtenerPerfilUsuario(u.roles).icon"></i>
                            {{ obtenerPerfilUsuario(u.roles).nombre }}
                          </span>
                        </div>

                        <p class="text-xs text-slate-600 font-mono flex items-center gap-1.5 mb-2.5">
                          <i class="fas fa-envelope text-slate-400 text-[11px]"></i>
                          <span>{{ u.email || u.correo }}</span>
                        </p>

                        <!-- Permisos Badges Limpios -->
                        <div class="flex items-center gap-1.5 flex-wrap">
                          <span
                            v-for="perm in todosLosPermisos"
                            :key="perm.key"
                            :class="[
                              'text-[10px] font-semibold px-2 py-0.5 rounded-md border flex items-center gap-1 transition-all',
                              tienePermiso(u, perm.key)
                                ? 'bg-indigo-50 text-indigo-700 border-indigo-200'
                                : 'bg-slate-50 text-slate-400 border-slate-200/80 opacity-40'
                            ]"
                          >
                            <i :class="[perm.icon, 'text-[10px]']"></i>
                            {{ perm.label }}
                          </span>
                        </div>
                      </div>
                    </div>

                    <!-- Controles de Edición de Permisos y Acciones -->
                    <div class="flex items-center gap-2 self-end md:self-center shrink-0">
                      <!-- Editar Permisos -->
                      <button
                        @click="abrirEditarPermisos(u)"
                        class="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200 rounded-xl text-xs font-semibold transition-colors flex items-center gap-1.5 cursor-pointer"
                        title="Modificar permisos y perfil de acceso"
                      >
                        <i class="fas fa-sliders text-indigo-600 text-xs"></i>
                        <span>Ajustar Permisos</span>
                      </button>

                      <!-- Enviar reset de clave -->
                      <button
                        @click="enviarResetPassword(u.email || u.correo)"
                        class="px-3 py-1.5 bg-amber-50 hover:bg-amber-100 text-amber-800 border border-amber-200 rounded-xl text-xs font-semibold transition-colors flex items-center gap-1.5 cursor-pointer shadow-xs"
                        title="Enviar correo de restablecimiento de contraseña en español"
                      >
                        <i class="fas fa-paper-plane text-xs text-amber-600"></i>
                        <span>Restablecer Contraseña</span>
                      </button>

                      <!-- Eliminar de Firestore -->
                      <button
                        @click="eliminarUsuario(u)"
                        class="p-2 text-slate-400 hover:text-rose-600 hover:bg-rose-50 border border-transparent hover:border-rose-100 rounded-xl transition-colors text-xs"
                        title="Eliminar usuario del registro"
                      >
                        <i class="fas fa-trash-can"></i>
                      </button>
                    </div>
                  </div>

                  <div v-if="usuarios.length === 0" class="p-12 text-center text-xs text-slate-400">
                    No se encontraron usuarios en la colección. Haz clic en "Nuevo Usuario" para registrar uno.
                  </div>
                </div>
              </div>

              <!-- TAB 2: CREAR USUARIO -->
              <div v-if="activeTab === 'crear'" class="space-y-5">
                <form @submit.prevent="crearUsuario" class="space-y-6 bg-white p-6 border border-slate-200/90 rounded-2xl shadow-xs">
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label class="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">Nombre Completo</label>
                      <input
                        v-model="nuevoForm.nombre"
                        type="text"
                        placeholder="Ej: Ángela Biscomb"
                        class="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-800"
                      />
                    </div>

                    <div>
                      <label class="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">Correo Electrónico *</label>
                      <input
                        v-model="nuevoForm.correo"
                        type="email"
                        required
                        placeholder="ejemplo@gmail.com"
                        class="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-indigo-500 focus:bg-white text-slate-800"
                      />
                    </div>
                  </div>

                  <!-- Modo de Invitación / Contraseña -->
                  <div class="bg-slate-50 border border-slate-200 p-4 rounded-xl space-y-3">
                    <label class="flex items-start gap-3 cursor-pointer">
                      <input
                        type="checkbox"
                        v-model="nuevoForm.enviarInvitacionCorreo"
                        class="mt-1 w-4 h-4 text-indigo-600 rounded border-slate-300 focus:ring-indigo-500"
                      />
                      <div class="text-xs">
                        <span class="font-bold text-slate-900 block">Enviar correo de invitación personalizado (Recomendado)</span>
                        <span class="text-slate-500 leading-relaxed block mt-0.5">
                          El usuario recibirá un correo electrónico en español con un <strong>enlace seguro y código de único uso</strong> para activar su cuenta y crear su propia contraseña personal.
                        </span>
                      </div>
                    </label>

                    <div v-if="!nuevoForm.enviarInvitacionCorreo" class="pt-2 border-t border-slate-200">
                      <label class="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">Contraseña Manual Inicial *</label>
                      <input
                        v-model="nuevoForm.password"
                        type="password"
                        :required="!nuevoForm.enviarInvitacionCorreo"
                        minlength="6"
                        placeholder="Mínimo 6 caracteres"
                        class="w-full px-3.5 py-2.5 bg-white border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-indigo-500 text-slate-800"
                      />
                    </div>
                  </div>

                  <!-- Perfil de Acceso Predefinido -->
                  <div>
                    <label class="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-2">Perfil de Acceso Recomendado</label>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                      <div
                        v-for="preset in perfilesPredefinidos"
                        :key="preset.id"
                        @click="aplicarPerfilForm(preset)"
                        :class="[
                          'p-3.5 rounded-xl border cursor-pointer transition-all flex flex-col justify-between',
                          esPerfilSeleccionado(preset.roles, nuevoForm.roles)
                            ? 'bg-indigo-50/80 border-indigo-400 ring-2 ring-indigo-500/20 shadow-xs'
                            : 'bg-slate-50 border-slate-200 hover:bg-slate-100/80'
                        ]"
                      >
                        <div>
                          <div class="flex items-center justify-between mb-1">
                            <span class="font-bold text-xs text-slate-900 flex items-center gap-1.5">
                              <i :class="[preset.icon, 'text-indigo-600']"></i>
                              {{ preset.nombre }}
                            </span>
                            <i v-if="esPerfilSeleccionado(preset.roles, nuevoForm.roles)" class="fas fa-circle-check text-indigo-600 text-xs"></i>
                          </div>
                          <p class="text-[11px] text-slate-500 leading-snug">{{ preset.descripcion }}</p>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Matriz de Permisos Granular -->
                  <div>
                    <div class="flex items-center justify-between mb-2.5">
                      <label class="block text-xs font-semibold text-slate-700 uppercase tracking-wider">Matriz de Permisos Granular</label>
                      <span class="text-[11px] text-indigo-600 font-medium">Personalización avanzada</span>
                    </div>

                    <div class="space-y-2 border border-slate-200 rounded-xl p-3 bg-slate-50/50">
                      <div
                        v-for="perm in todosLosPermisos"
                        :key="perm.key"
                        @click="togglePermisoForm(perm.key)"
                        class="flex items-center justify-between p-2.5 rounded-lg bg-white border border-slate-200/80 hover:border-slate-300 cursor-pointer transition-all"
                      >
                        <div class="flex items-center gap-3">
                          <div :class="['w-8 h-8 rounded-lg flex items-center justify-center text-xs shrink-0', nuevoForm.roles.includes(perm.key) ? 'bg-indigo-100 text-indigo-700' : 'bg-slate-100 text-slate-400']">
                            <i :class="perm.icon"></i>
                          </div>
                          <div>
                            <p class="text-xs font-bold text-slate-800">{{ perm.labelCompleto }}</p>
                            <p class="text-[11px] text-slate-500">{{ perm.descripcion }}</p>
                          </div>
                        </div>

                        <!-- Switch Toggle -->
                        <div
                          :class="[
                            'w-10 h-5 rounded-full transition-colors relative flex items-center px-0.5',
                            nuevoForm.roles.includes(perm.key) ? 'bg-indigo-600' : 'bg-slate-300'
                          ]"
                        >
                          <div
                            :class="[
                              'w-4 h-4 rounded-full bg-white shadow-md transition-transform transform',
                              nuevoForm.roles.includes(perm.key) ? 'translate-x-5' : 'translate-x-0'
                            ]"
                          ></div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div class="bg-indigo-50/70 border border-indigo-100 p-3.5 rounded-xl text-xs text-indigo-900 flex items-center gap-2.5">
                    <i class="fas fa-envelope-circle-check text-indigo-600 text-lg flex-shrink-0"></i>
                    <span>
                      <strong>Correo en Español:</strong> El enlace de invitación y código único se enviará automáticamente en idioma español al correo registrado.
                    </span>
                  </div>

                  <div class="flex justify-end pt-2">
                    <button
                      type="submit"
                      :disabled="guardando"
                      class="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-semibold shadow-md transition-colors disabled:opacity-50 flex items-center gap-2 cursor-pointer"
                    >
                      <i v-if="guardando" class="fas fa-spinner fa-spin"></i>
                      <i v-else class="fas fa-paper-plane"></i>
                      {{ guardando ? 'Creando usuario y enviando correo...' : 'Crear Usuario y Enviar Invitación' }}
                    </button>
                  </div>
                </form>
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

          <!-- Modal Sub-Dialog: Ajustar Permisos de Usuario Existente -->
          <div
            v-if="usuarioEditando"
            class="fixed inset-0 bg-black/50 z-[60] flex items-center justify-center p-4"
            @click.self="usuarioEditando = null"
          >
            <div class="bg-white rounded-2xl shadow-2xl max-w-lg w-full p-6 space-y-4 animate-fade-in-up">
              <div class="flex justify-between items-center border-b pb-3">
                <h3 class="text-sm font-bold text-slate-900 flex items-center gap-2">
                  <i class="fas fa-sliders text-indigo-600"></i>
                  Ajustar Permisos para {{ usuarioEditando.nombre || usuarioEditando.email }}
                </h3>
                <button @click="usuarioEditando = null" class="text-slate-400 hover:text-slate-600">
                  <i class="fas fa-times"></i>
                </button>
              </div>

              <p class="text-xs text-slate-500">Selecciona un perfil predefinido o conmuta los permisos requeridos:</p>

              <!-- Perfiles Predefinidos en Sub-modal -->
              <div class="grid grid-cols-3 gap-2 mb-3">
                <button
                  v-for="preset in perfilesPredefinidos"
                  :key="preset.id"
                  @click="aplicarPerfilUsuario(usuarioEditando, preset)"
                  :class="[
                    'p-2 rounded-xl border text-center transition-all text-xs font-bold flex flex-col items-center gap-1',
                    esPerfilSeleccionado(preset.roles, usuarioEditando.roles)
                      ? 'bg-indigo-50 border-indigo-300 text-indigo-900'
                      : 'bg-slate-50 border-slate-200 text-slate-600 hover:bg-slate-100'
                  ]"
                >
                  <i :class="preset.icon"></i>
                  {{ preset.nombre }}
                </button>
              </div>

              <!-- Lista Switches -->
              <div class="space-y-2 border rounded-xl p-3 bg-slate-50/50 max-h-60 overflow-y-auto">
                <div
                  v-for="perm in todosLosPermisos"
                  :key="perm.key"
                  @click="togglePermisoUsuario(usuarioEditando, perm.key)"
                  class="flex items-center justify-between p-2 rounded-lg bg-white border border-slate-200 cursor-pointer"
                >
                  <span class="text-xs font-semibold text-slate-800 flex items-center gap-2">
                    <i :class="[perm.icon, 'text-indigo-600']"></i>
                    {{ perm.labelCompleto }}
                  </span>
                  <div
                    :class="[
                      'w-9 h-5 rounded-full transition-colors relative flex items-center px-0.5',
                      tienePermiso(usuarioEditando, perm.key) ? 'bg-indigo-600' : 'bg-slate-300'
                    ]"
                  >
                    <div
                      :class="[
                        'w-4 h-4 rounded-full bg-white shadow-md transition-transform transform',
                        tienePermiso(usuarioEditando, perm.key) ? 'translate-x-4' : 'translate-x-0'
                      ]"
                    ></div>
                  </div>
                </div>
              </div>

              <div class="flex justify-end pt-2">
                <button
                  @click="usuarioEditando = null"
                  class="px-5 py-2 bg-indigo-600 text-white font-semibold text-xs rounded-xl hover:bg-indigo-700 transition-colors"
                >
                  Guardar Permisos
                </button>
              </div>
            </div>
          </div>

          <!-- Footer -->
          <div class="bg-slate-50 px-6 py-4 border-t border-slate-200 flex justify-between items-center flex-shrink-0">
            <span class="text-[11px] text-slate-400">Los usuarios registrados podrán acceder en /admin-login.</span>
            <button
              type="button"
              @click="cerrar"
              class="px-4 py-2 border border-slate-300 text-slate-700 rounded-xl hover:bg-slate-100 font-semibold text-xs transition-colors"
            >
              Cerrar
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, watch } from 'vue'
import { db, auth } from '../firebase'
import { collection, getDocs, doc, setDoc, deleteDoc, updateDoc } from 'firebase/firestore'
import { sendPasswordResetEmail, createUserWithEmailAndPassword, getAuth } from 'firebase/auth'
import { initializeApp, getApps } from 'firebase/app'
import { v4 as uuidv4 } from 'uuid'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close'])

const activeTab = ref('lista')
const cargando = ref(false)
const guardando = ref(false)
const mensaje = ref(null)
const usuarioEditando = ref(null)

const usuarios = ref([])

const todosLosPermisos = [
  { key: 'admin', label: 'Admin', labelCompleto: 'Administración General', icon: 'fas fa-crown', descripcion: 'Acceso total a configuración, finanzas y usuarios.' },
  { key: 'crear', label: 'Crear', labelCompleto: 'Crear Eventos y Registros', icon: 'fas fa-plus-circle', descripcion: 'Alta de eventos y registros manuales.' },
  { key: 'editar', label: 'Editar', labelCompleto: 'Editar Registros', icon: 'fas fa-pen-to-square', descripcion: 'Modificación de datos de inscritos y pagos.' },
  { key: 'ver', label: 'Ver', labelCompleto: 'Ver Informes y Listas', icon: 'fas fa-eye', descripcion: 'Consulta de tablas, reportes y exportación CSV.' },
  { key: 'qr', label: 'Escáner QR', labelCompleto: 'Validación de Boletos QR', icon: 'fas fa-qrcode', descripcion: 'Escaneo y verificación de entradas en puerta.' }
]

const perfilesPredefinidos = [
  {
    id: 'superadmin',
    nombre: 'SuperAdmin',
    icon: 'fas fa-crown',
    badgeClass: 'bg-purple-50 text-purple-700 border-purple-200',
    descripcion: 'Acceso completo e ilimitado.',
    roles: ['admin', 'crear', 'editar', 'ver', 'qr']
  },
  {
    id: 'editor',
    nombre: 'Editor / Gestor',
    icon: 'fas fa-pen-to-square',
    badgeClass: 'bg-indigo-50 text-indigo-700 border-indigo-200',
    descripcion: 'Crear y modificar inscripciones y eventos.',
    roles: ['crear', 'editar', 'ver']
  },
  {
    id: 'verificador',
    nombre: 'Verificador QR',
    icon: 'fas fa-qrcode',
    badgeClass: 'bg-emerald-50 text-emerald-700 border-emerald-200',
    descripcion: 'Consulta de listas y escaneo en la puerta.',
    roles: ['ver', 'qr']
  }
]

const nuevoForm = ref({
  nombre: '',
  correo: '',
  password: '',
  enviarInvitacionCorreo: true,
  roles: ['admin', 'crear', 'editar', 'ver', 'qr']
})

watch(() => props.show, (val) => {
  if (val) {
    cargarUsuarios()
  }
})

const cargarUsuarios = async () => {
  cargando.value = true
  mensaje.value = null
  try {
    const snap = await getDocs(collection(db, 'users'))
    let docsList = snap.docs.map(d => ({ id: d.id, ...d.data() }))

    try {
      const snapUsuarios = await getDocs(collection(db, 'usuarios'))
      snapUsuarios.docs.forEach(d => {
        const data = d.data()
        const existe = docsList.find(u => u.id === d.id || u.email === data.email || u.correo === data.correo)
        if (!existe) {
          docsList.push({ id: d.id, ...data })
        }
      })
    } catch (err) {}

    usuarios.value = docsList
  } catch (e) {
    console.error('Error cargando usuarios:', e)
    mensaje.value = { tipo: 'error', texto: 'No se pudo cargar el directorio de usuarios.' }
  } finally {
    cargando.value = false
  }
}

const tienePermiso = (usuario, permKey) => {
  if (!usuario || !usuario.roles || !Array.isArray(usuario.roles)) return false
  return usuario.roles.includes(permKey)
}

const obtenerPerfilUsuario = (rolesArr) => {
  if (!Array.isArray(rolesArr)) return { nombre: 'Personalizado', icon: 'fas fa-user-gear', badgeClass: 'bg-slate-100 text-slate-700 border-slate-200' }
  const r = [...rolesArr].sort().join(',')
  for (const preset of perfilesPredefinidos) {
    if ([...preset.roles].sort().join(',') === r) {
      return preset
    }
  }
  if (rolesArr.includes('admin')) {
    return { nombre: 'Administrador', icon: 'fas fa-user-shield', badgeClass: 'bg-purple-50 text-purple-700 border-purple-200' }
  }
  return { nombre: 'Personalizado', icon: 'fas fa-user-gear', badgeClass: 'bg-slate-100 text-slate-700 border-slate-200' }
}

const esPerfilSeleccionado = (rolesPreset, rolesActuales) => {
  if (!Array.isArray(rolesActuales)) return false
  return [...rolesPreset].sort().join(',') === [...rolesActuales].sort().join(',')
}

const aplicarPerfilForm = (preset) => {
  nuevoForm.value.roles = [...preset.roles]
}

const togglePermisoForm = (permKey) => {
  if (nuevoForm.value.roles.includes(permKey)) {
    nuevoForm.value.roles = nuevoForm.value.roles.filter(r => r !== permKey)
  } else {
    nuevoForm.value.roles.push(permKey)
  }
}

const abrirEditarPermisos = (u) => {
  usuarioEditando.value = u
}

const aplicarPerfilUsuario = async (u, preset) => {
  u.roles = [...preset.roles]
  await guardarRolesUsuario(u)
}

const togglePermisoUsuario = async (u, permKey) => {
  const rolesActuales = Array.isArray(u.roles) ? [...u.roles] : []
  let nuevosRoles = []
  if (rolesActuales.includes(permKey)) {
    nuevosRoles = rolesActuales.filter(r => r !== permKey)
  } else {
    nuevosRoles = [...rolesActuales, permKey]
  }

  u.roles = nuevosRoles
  await guardarRolesUsuario(u)
}

const guardarRolesUsuario = async (u) => {
  try {
    await updateDoc(doc(db, 'users', u.id), { roles: u.roles })
  } catch (e) {
    try {
      await setDoc(doc(db, 'users', u.id), { roles: u.roles }, { merge: true })
    } catch (e2) {
      console.error('Error actualizando permisos:', e2)
    }
  }
}

const crearUsuario = async () => {
  if (!nuevoForm.value.correo) return
  if (!nuevoForm.value.enviarInvitacionCorreo && !nuevoForm.value.password) return

  guardando.value = true
  mensaje.value = null

  try {
    const firebaseConfig = {
      apiKey: import.meta.env.VITE_FIREBASE_API_KEY || "AIzaSyCW-1YmJC0BgObJTk0eJ7PJdAtTI_rz2X4",
      authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || "el-aposento-alto.firebaseapp.com",
      projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || "el-aposento-alto",
      storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || "el-aposento-alto.firebasestorage.app",
      messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || "906915946572",
      appId: import.meta.env.VITE_FIREBASE_APP_ID || "1:906915946572:web:075b1f160d073d5ae554e9"
    }

    const secondaryAppName = 'SecondaryAuthAdminApp'
    let secondaryApp
    const existingApps = getApps()
    const found = existingApps.find(a => a.name === secondaryAppName)
    if (found) {
      secondaryApp = found
    } else {
      secondaryApp = initializeApp(firebaseConfig, secondaryAppName)
    }

    const secondaryAuth = getAuth(secondaryApp)
    secondaryAuth.languageCode = 'es'

    // Si se envía invitación por correo, generar contraseña aleatoria temporal
    const passwordFinal = nuevoForm.value.enviarInvitacionCorreo
      ? `Aposento_${uuidv4().slice(0, 8)}!`
      : nuevoForm.value.password

    const userCred = await createUserWithEmailAndPassword(
      secondaryAuth,
      nuevoForm.value.correo.trim(),
      passwordFinal
    )

    const uid = userCred.user.uid
    const userData = {
      email: nuevoForm.value.correo.trim().toLowerCase(),
      nombre: nuevoForm.value.nombre.trim() || undefined,
      roles: nuevoForm.value.roles.length > 0 ? nuevoForm.value.roles : ['admin', 'crear', 'editar', 'ver', 'qr'],
      createdAt: new Date().toISOString()
    }

    await setDoc(doc(db, 'users', uid), userData)

    await secondaryAuth.signOut()

    // Si está activado enviar invitación por correo:
    if (nuevoForm.value.enviarInvitacionCorreo) {
      auth.languageCode = 'es'
      const actionCodeSettings = {
        url: window.location.origin + '/admin-login',
        handleCodeInApp: false
      }
      await sendPasswordResetEmail(auth, nuevoForm.value.correo.trim(), actionCodeSettings)
      mensaje.value = {
        tipo: 'success',
        texto: `¡Usuario creado! Se envió un correo de bienvenida en español a ${nuevoForm.value.correo} con su enlace único de activación y retorno directo al portal.`
      }
    } else {
      mensaje.value = { tipo: 'success', texto: `¡Usuario ${nuevoForm.value.correo} creado exitosamente en Auth y Firestore!` }
    }

    nuevoForm.value = { nombre: '', correo: '', password: '', enviarInvitacionCorreo: true, roles: ['admin', 'crear', 'editar', 'ver', 'qr'] }
    activeTab.value = 'lista'
    await cargarUsuarios()
  } catch (e) {
    console.error('Error creando usuario:', e)
    if (e.code === 'auth/email-already-in-use') {
      mensaje.value = { tipo: 'error', texto: 'Este correo electrónico ya está registrado en Firebase Auth.' }
    } else if (e.code === 'auth/weak-password') {
      mensaje.value = { tipo: 'error', texto: 'La contraseña debe tener al menos 6 caracteres.' }
    } else {
      mensaje.value = { tipo: 'error', texto: `Error al crear usuario: ${e.message}` }
    }
  } finally {
    guardando.value = false
  }
}

const enviarResetPassword = async (email) => {
  if (!email) return
  try {
    // Configurar idioma español y URL de retorno a la web
    auth.languageCode = 'es'
    const actionCodeSettings = {
      url: window.location.origin + '/admin-login',
      handleCodeInApp: false
    }
    await sendPasswordResetEmail(auth, email, actionCodeSettings)
    alert(`✉️ Se ha enviado un correo electrónico en español para restablecer la contraseña a:\n\n${email}\n\nEl usuario recibirá un enlace único para cambiar su contraseña y al terminar será redirigido automáticamente a la web.`)
  } catch (e) {
    console.error('Error enviando reset de clave:', e)
    alert(`❌ No se pudo enviar el correo de restablecimiento: ${e.message}`)
  }
}

const eliminarUsuario = async (u) => {
  const confirmed = window.confirm(`¿Seguro que deseas eliminar el usuario "${u.email || u.nombre}" del registro de Firestore?`)
  if (!confirmed) return
  try {
    await deleteDoc(doc(db, 'users', u.id))
    usuarios.value = usuarios.value.filter(item => item.id !== u.id)
  } catch (e) {
    console.error('Error eliminando usuario:', e)
    alert('No se pudo eliminar el usuario.')
  }
}

const cerrar = () => {
  if (!guardando.value) {
    mensaje.value = null
    usuarioEditando.value = null
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
