import { defineStore } from 'pinia'
import { ref } from 'vue'
import { db, storage } from '../firebase'
import { collection, addDoc, getDocs, doc, updateDoc, deleteDoc, onSnapshot, query, where, orderBy } from 'firebase/firestore'
import { ref as storageRef, uploadBytes, getDownloadURL } from 'firebase/storage'


export const useEventosStore = defineStore('eventos', () => {
  const eventos = ref([])
  const inscripciones = ref([])
  const loading = ref(true)

  // Eliminar campos `undefined` recursivamente para que Firestore no rechace el documento
  const sanitize = (value) => {
    if (value === null) return null
    if (Array.isArray(value)) return value.map(sanitize)
    if (typeof value === 'object') {
      const out = {}
      Object.keys(value).forEach((k) => {
        const v = value[k]
        if (v === undefined) return
        // Skip functions and symbols
        if (typeof v === 'function' || typeof v === 'symbol') return
        out[k] = sanitize(v)
      })
      return out
    }
    return value
  }

  const mockEventos = [
    {
      id: '1',
      titulo: 'Conferencia Internacional de Fe 2026',
      subtitulo: 'Desatando el Poder de Dios',
      descripcion: 'Únete a nosotros en tres días de avivamiento, enseñanza de la Palabra y adoración junto a invitados especiales internacionales.',
      fecha: '2026-09-20',
      hora: '19:00',
      lugar: 'Auditorio Principal - El Aposento Alto',
      imagen: 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=1200&q=80',
      bannerUrl: 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=1200&q=80',
      precio: 0,
      esGratis: true,
      cupos: 500,
      inscritos: 120
    },
    {
      id: '2',
      titulo: 'Congreso de Jóvenes: Generación Radical',
      subtitulo: 'Levantándonos en Verdad y Poder',
      descripcion: 'Un encuentro transformador para la juventud con música en vivo, talleres interactivos y conferencias impactantes.',
      fecha: '2026-10-15',
      hora: '18:30',
      lugar: 'Centro de Convenciones El Aposento Alto',
      imagen: 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?auto=format&fit=crop&w=1200&q=80',
      bannerUrl: 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?auto=format&fit=crop&w=1200&q=80',
      precio: 15,
      esGratis: false,
      cupos: 300,
      inscritos: 85
    },
    {
      id: '3',
      titulo: 'Noche de Gloriosa Adoración y Milagros',
      subtitulo: 'Presencia Divina',
      descripcion: 'Una velada dedicada a la ministración del Espíritu Santo, sanidades y alabanza ininterrumpida.',
      fecha: '2026-11-05',
      hora: '20:00',
      lugar: 'Templo Central',
      imagen: 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=1200&q=80',
      bannerUrl: 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=1200&q=80',
      precio: 0,
      esGratis: true,
      cupos: 400,
      inscritos: 210
    }
  ]

  // Cargar eventos desde Firestore en tiempo real (con fallback a mock data)
  const cargarEventos = () => {
    try {
      const eventosRef = collection(db, 'eventos')
      const q = query(eventosRef, orderBy('fecha', 'desc'))
      onSnapshot(q, (snapshot) => {
        const loaded = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }))
        eventos.value = loaded.length > 0 ? loaded : mockEventos
        loading.value = false
      }, (error) => {
        console.warn('Firestore onSnapshot notice:', error.message)
        if (eventos.value.length === 0) {
          eventos.value = mockEventos
        }
        loading.value = false
      })
    } catch (err) {
      console.warn('Error connecting to Firestore:', err)
      if (eventos.value.length === 0) {
        eventos.value = mockEventos
      }
      loading.value = false
    }
  }

  const obtenerEventoPorId = (id) => {
    return eventos.value.find(evento => evento.id === id || evento.id === parseInt(id))
  }

  const inscribirParticipante = async (eventoId, datosParticipante) => {
    // Si el participante adjuntó un archivo 'comprobante', súbelo a Storage
    let uploadWarning = false
    try {
      // soportar uno o varios archivos en datosParticipante.comprobante (array de File)
      if (datosParticipante && datosParticipante.comprobante && Array.isArray(datosParticipante.comprobante) && typeof File !== 'undefined') {
        const archivosOriginales = datosParticipante.comprobante.filter(f => f instanceof File)
        const urls = []
        for (const file of archivosOriginales) {
          const path = `inscripciones/${eventoId}/${Date.now()}_${file.name}`
          const sRef = storageRef(storage, path)
          try {
            await uploadBytes(sRef, file)
            const url = await getDownloadURL(sRef)
            urls.push(url)
          } catch (uploadError) {
            console.error('Error subiendo archivo:', file.name, uploadError)
            uploadWarning = true // marcar fallo para notificar al usuario
          }
        }
        if (urls.length) {
          datosParticipante.comprobantesUrls = urls
        }
        // Si había archivos pero no se subió ninguno, es fallo total
        if (archivosOriginales.length > 0 && urls.length === 0) {
          uploadWarning = true
        }
        delete datosParticipante.comprobante
      } else if (datosParticipante && datosParticipante.comprobante && typeof File !== 'undefined' && datosParticipante.comprobante instanceof File) {
        const file = datosParticipante.comprobante
        const path = `inscripciones/${eventoId}/${Date.now()}_${file.name}`
        const sRef = storageRef(storage, path)
        try {
          await uploadBytes(sRef, file)
          const url = await getDownloadURL(sRef)
          datosParticipante.comprobanteUrl = url
        } catch (uploadError) {
          console.error('Error subiendo comprobante a Storage:', uploadError)
          uploadWarning = true
        }
        delete datosParticipante.comprobante
      }
    } catch (uploadError) {
      console.error('Error subiendo comprobante a Storage:', uploadError)
      uploadWarning = true
    }

    // Sanitize participant data to remove undefined fields (Firestore rejects undefined)
    const participanteSanitizado = datosParticipante ? sanitize(datosParticipante) : datosParticipante

    const inscripcion = {
      eventoId,
      participante: participanteSanitizado,
      fechaInscripcion: new Date().toISOString()
    }

    console.log('Guardando inscripcion:', inscripcion)
    await addDoc(collection(db, 'inscripciones'), inscripcion)
    inscripciones.value.push(inscripcion)
    return { ...inscripcion, uploadWarning }
  }

  // Agregar evento a Firestore
  const agregarEvento = async (nuevoEvento) => {
    const docRef = await addDoc(collection(db, 'eventos'), {
      ...nuevoEvento,
      inscritos: 0
    })
    return docRef.id
  }

  // Actualizar evento en Firestore
  const actualizarEvento = async (id, datosActualizados) => {
    const eventoRef = doc(db, 'eventos', id)
    await updateDoc(eventoRef, datosActualizados)
  }

  // Eliminar evento de Firestore
  const eliminarEvento = async (id) => {
    const eventoRef = doc(db, 'eventos', id)
    await deleteDoc(eventoRef)
  }

  // Obtener inscripciones por evento desde Firestore
  const obtenerInscripcionesPorEvento = async (eventoId) => {
    const inscripcionesRef = collection(db, 'inscripciones')
    const q = query(inscripcionesRef, where('eventoId', '==', eventoId))
    const snapshot = await getDocs(q)
    return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }))
  }

  // Obtener todas las inscripciones (con paginación opcional)
  const obtenerTodasInscripciones = async () => {
    const inscripcionesRef = collection(db, 'inscripciones')
    const q = query(inscripcionesRef, orderBy('fechaInscripcion', 'desc'))
    const snapshot = await getDocs(q)
    return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }))
  }

  // Actualizar inscripción
  const actualizarInscripcion = async (id, datosActualizados) => {
    const inscripcionRef = doc(db, 'inscripciones', id)
    const sanitizado = datosActualizados ? sanitize(datosActualizados) : datosActualizados
    await updateDoc(inscripcionRef, sanitizado)
  }

  // Eliminar inscripción
  const eliminarInscripcion = async (id) => {
    const inscripcionRef = doc(db, 'inscripciones', id)
    await deleteDoc(inscripcionRef)
  }

  return {
    eventos,
    inscripciones,
    loading,
    cargarEventos,
    obtenerEventoPorId,
    inscribirParticipante,
    agregarEvento,
    actualizarEvento,
    eliminarEvento,
    obtenerInscripcionesPorEvento,
    obtenerTodasInscripciones,
    actualizarInscripcion,
    eliminarInscripcion
  }
})
