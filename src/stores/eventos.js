import { defineStore } from 'pinia'
import { ref } from 'vue'
import { db, storage } from '../firebase'
import { collection, addDoc, getDocs, doc, updateDoc, deleteDoc, onSnapshot, query, orderBy } from 'firebase/firestore'
import { ref as storageRef, uploadBytes, getDownloadURL } from 'firebase/storage'


export const useEventosStore = defineStore('eventos', () => {
  const eventos = ref([])
  const inscripciones = ref([])
  const loading = ref(true)

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
      if (datosParticipante && datosParticipante.comprobante && typeof File !== 'undefined' && datosParticipante.comprobante instanceof File) {
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

    const inscripcion = {
      eventoId,
      participante: datosParticipante,
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
      .map(doc => doc.data())
      .filter(insc => insc.eventoId === eventoId)
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
    obtenerInscripcionesPorEvento
  }
})
