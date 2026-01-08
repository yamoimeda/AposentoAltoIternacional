import { defineStore } from 'pinia'
import { ref } from 'vue'
import { db, storage } from '../firebase'
import { collection, addDoc, getDocs, doc, updateDoc, deleteDoc, onSnapshot, query, orderBy } from 'firebase/firestore'
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

  // Cargar eventos desde Firestore en tiempo real
  const cargarEventos = () => {
    const eventosRef = collection(db, 'eventos')
    const q = query(eventosRef, orderBy('fecha', 'desc'))
    onSnapshot(q, (snapshot) => {
      eventos.value = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }))
      loading.value = false
      
    })
  }

  const obtenerEventoPorId = (id) => {
    return eventos.value.find(evento => evento.id === id || evento.id === parseInt(id))
  }

  // Inscribir participante en Firestore (colección inscripciones)
  const inscribirParticipante = async (eventoId, datosParticipante) => {
    // Si el participante adjuntó un archivo 'comprobante', súbelo a Storage
    try {
      // soportar uno o varios archivos en datosParticipante.comprobante (array de File)
      if (datosParticipante && datosParticipante.comprobante && Array.isArray(datosParticipante.comprobante) && typeof File !== 'undefined') {
        const urls = []
        for (const file of datosParticipante.comprobante) {
          if (!(file instanceof File)) continue
          const path = `inscripciones/${eventoId}/${Date.now()}_${file.name}`
          const sRef = storageRef(storage, path)
          try {
            await uploadBytes(sRef, file)
            const url = await getDownloadURL(sRef)
            urls.push(url)
          } catch (uploadError) {
            console.error('Error subiendo archivo:', file.name, uploadError)
          }
        }
        if (urls.length) {
          datosParticipante.comprobantesUrls = urls
        }
        delete datosParticipante.comprobante
      } else if (datosParticipante && datosParticipante.comprobante && typeof File !== 'undefined' && datosParticipante.comprobante instanceof File) {
        const file = datosParticipante.comprobante
        const path = `inscripciones/${eventoId}/${Date.now()}_${file.name}`
        const sRef = storageRef(storage, path)
        await uploadBytes(sRef, file)
        const url = await getDownloadURL(sRef)
        // Guardar la URL en lugar del objeto File
        datosParticipante.comprobanteUrl = url
        delete datosParticipante.comprobante
      }
    } catch (uploadError) {
      console.error('Error subiendo comprobante a Storage:', uploadError)
      // continuar sin la URL si falla la subida
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
    return inscripcion
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
    const snapshot = await getDocs(inscripcionesRef)
    return snapshot.docs
      .map(doc => ({ id: doc.id, ...doc.data() }))
      .filter(insc => insc.eventoId === eventoId)
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
    await updateDoc(inscripcionRef, datosActualizados)
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
