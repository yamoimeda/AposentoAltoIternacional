import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useEventosStore = defineStore('eventos', () => {
  const eventos = ref([])
  const inscripciones = ref([])

  // Datos de ejemplo para la demostración
  const eventosEjemplo = [
    {
      id: 1,
      titulo: 'Koinonia 2025 | EMUNAH',
      descripcion: 'Únete a nosotros en un tiempo especial de alabanza y adoración al Señor. Ven y experimenta la presencia de Dios en nuestro santuario.',
      fecha: '2025-08-10',
      hora: '10:00 AM',
      ubicacion: 'Templo Principal',
      imagen: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500&h=300&fit=crop',
      cupos: 200,
      inscritos: 45,
      categoria: 'culto',
      esFuturo: true
    },
    {
      id: 2,
      titulo: 'Retiro de Jóvenes "Generación de Fuego"',
      descripcion: 'Un fin de semana transformador para jóvenes de 13 a 25 años. Actividades, talleres, adoración y mucha diversión en un ambiente cristiano.',
      fecha: '2025-08-15',
      hora: '7:00 PM',
      ubicacion: 'Centro de Retiros "Monte Hermón"',
      imagen: 'https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=500&h=300&fit=crop',
      cupos: 80,
      inscritos: 62,
      categoria: 'retiro',
      esFuturo: true
    },
    {
      id: 3,
      titulo: 'Conferencia "Matrimonios Sólidos"',
      descripción: 'Fortalece tu matrimonio con principios bíblicos. Conferencia dirigida a parejas casadas con talleres prácticos y dinámicas.',
      fecha: '2025-08-20',
      hora: '6:00 PM',
      ubicacion: 'Salón de Usos Múltiples',
      imagen: 'https://images.unsplash.com/photo-1469371670807-013ccf25f16a?w=500&h=300&fit=crop',
      cupos: 50,
      inscritos: 28,
      categoria: 'conferencia',
      esFuturo: true
    },
    {
      id: 4,
      titulo: 'Escuela Bíblica de Verano para Niños',
      descripcion: 'Una semana llena de diversión, juegos, manualidades y enseñanzas bíblicas para niños de 4 a 12 años.',
      fecha: '2025-08-25',
      hora: '9:00 AM',
      ubicacion: 'Aulas de Educación Cristiana',
      imagen: 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=500&h=300&fit=crop',
      cupos: 60,
      inscritos: 42,
      categoria: 'educacion',
      esFuturo: true
    },
    {
      id: 5,
      titulo: 'Noche de Oración y Ayuno',
      descripcion: 'Una noche especial dedicada a la oración intercesora y búsqueda de la presencia de Dios. Incluye tiempo de ayuno comunitario.',
      fecha: '2025-07-28',
      hora: '8:00 PM',
      ubicacion: 'Santuario Principal',
      imagen: 'https://images.unsplash.com/photo-1519491050282-cf00c82424b4?w=500&h=300&fit=crop',
      cupos: null,
      inscritos: 0,
      categoria: 'oracion',
      esFuturo: false
    },
    {
      id: 6,
      titulo: 'Evangelismo en el Parque Central',
      descripcion: 'Salida evangelística para compartir el amor de Cristo en nuestra comunidad. Incluye distribución de folletos y testimonios.',
      fecha: '2025-07-20',
      hora: '4:00 PM',
      ubicacion: 'Parque Central de la Ciudad',
      imagen: 'https://images.unsplash.com/photo-1544027993-37dbfe43562a?w=500&h=300&fit=crop',
      cupos: 30,
      inscritos: 25,
      categoria: 'evangelismo',
      esFuturo: false
    }
  ]

  const cargarEventos = () => {
    // En una aplicación real, esto vendría de una API
    eventos.value = eventosEjemplo.map(evento => ({
      ...evento,
      esFuturo: new Date(evento.fecha) >= new Date()
    }))
  }

  const obtenerEventoPorId = (id) => {
    return eventos.value.find(evento => evento.id === parseInt(id))
  }

  const inscribirParticipante = (eventoId, datosParticipante) => {
    const evento = eventos.value.find(e => e.id === eventoId)
    if (evento && (!evento.cupos || evento.inscritos < evento.cupos)) {
      evento.inscritos++
      
      const inscripcion = {
        id: Date.now(),
        eventoId: eventoId,
        participante: datosParticipante,
        fechaInscripcion: new Date().toISOString()
      }
      
      inscripciones.value.push(inscripcion)
      
      // Guardar en localStorage para persistencia
      localStorage.setItem('inscripciones', JSON.stringify(inscripciones.value))
      localStorage.setItem('eventos', JSON.stringify(eventos.value))
      
      return inscripcion
    }
    throw new Error('No se pudo completar la inscripción')
  }

  const agregarEvento = (nuevoEvento) => {
    const evento = {
      ...nuevoEvento,
      id: Math.max(...eventos.value.map(e => e.id)) + 1,
      inscritos: 0,
      esFuturo: new Date(nuevoEvento.fecha) >= new Date()
    }
    eventos.value.push(evento)
    localStorage.setItem('eventos', JSON.stringify(eventos.value))
    return evento
  }

  const actualizarEvento = (id, datosActualizados) => {
    const index = eventos.value.findIndex(e => e.id === id)
    if (index !== -1) {
      eventos.value[index] = {
        ...eventos.value[index],
        ...datosActualizados,
        esFuturo: new Date(datosActualizados.fecha || eventos.value[index].fecha) >= new Date()
      }
      localStorage.setItem('eventos', JSON.stringify(eventos.value))
      return eventos.value[index]
    }
    throw new Error('Evento no encontrado')
  }

  const eliminarEvento = (id) => {
    const index = eventos.value.findIndex(e => e.id === id)
    if (index !== -1) {
      eventos.value.splice(index, 1)
      localStorage.setItem('eventos', JSON.stringify(eventos.value))
      return true
    }
    return false
  }

  const obtenerInscripcionesPorEvento = (eventoId) => {
    return inscripciones.value.filter(inscripcion => inscripcion.eventoId === eventoId)
  }

  const cargarDatosLocalStorage = () => {
    const eventosGuardados = localStorage.getItem('eventos')
    const inscripcionesGuardadas = localStorage.getItem('inscripciones')
    
    if (eventosGuardados) {
      eventos.value = JSON.parse(eventosGuardados)
    } else {
      cargarEventos()
    }
    
    if (inscripcionesGuardadas) {
      inscripciones.value = JSON.parse(inscripcionesGuardadas)
    }
  }

  return {
    eventos,
    inscripciones,
    cargarEventos,
    obtenerEventoPorId,
    inscribirParticipante,
    agregarEvento,
    actualizarEvento,
    eliminarEvento,
    obtenerInscripcionesPorEvento,
    cargarDatosLocalStorage
  }
})
