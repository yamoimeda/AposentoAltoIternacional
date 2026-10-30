/**
 * Determina si el nombre de un boleto corresponde por defecto a un boleto "completo" o "full".
 * @param {string} nombre
 * @returns {boolean}
 */
export function esNombreBoletoFull(nombre) {
  const norm = String(nombre || '').trim().toLowerCase()
  return norm.includes('full') || norm.includes('completo')
}

/**
 * Determina si la configuración de un objeto boleto incluye Coffee Break (Coffee 1 y 2).
 * Respeta la propiedad booleana explícita `incluyeCoffee` si existe;
 * de lo contrario usa el fallback por nombre ('full' o 'completo').
 * @param {Object} ticket
 * @returns {boolean}
 */
export function ticketConfigIncluyeCoffee(ticket) {
  if (!ticket) return false
  if (typeof ticket.incluyeCoffee === 'boolean') {
    return ticket.incluyeCoffee
  }
  return esNombreBoletoFull(ticket.nombre)
}

/**
 * Determina si una inscripción (o participante) tiene derecho a Coffee Break (Coffee 1 y 2).
 * Prioriza la configuración actual del boleto en el evento (si se provee el evento o lista de eventos),
 * luego la propiedad `incluyeCoffee` guardada en la inscripción, y finalmente el fallback por nombre.
 * @param {Object} inscripcion - Objeto inscripción o participante aplanado
 * @param {Object|Array|null} eventoOEventos - Objeto evento o arreglo de eventos
 * @returns {boolean}
 */
export function inscripcionIncluyeCoffee(inscripcion, eventoOEventos = null) {
  if (!inscripcion) return false
  const p = inscripcion.participante || inscripcion
  const evId = inscripcion.eventoId || p.eventoId || null
  const ticketTypeId = p.ticketTypeId || inscripcion.ticketTypeId || null
  const ticketTypeName = (p.ticketType || inscripcion.ticketType || 'Adulto full').trim()

  // 1. Resolver el evento si se pasó el objeto o la lista de eventos
  let ev = null
  if (Array.isArray(eventoOEventos)) {
    if (evId) {
      ev = eventoOEventos.find(e => e && (e.id === evId || String(e.id) === String(evId))) || null
    }
  } else if (eventoOEventos && typeof eventoOEventos === 'object') {
    ev = eventoOEventos
  }

  // 2. Buscar en la lista de boletos del evento (priorizando coincidencia por nombre para respetar ediciones previas, luego por ticketTypeId)
  if (ev) {
    const list = ev.ticketTypes || ev.tickets || []
    if (Array.isArray(list) && list.length > 0) {
      const match =
        list.find(tick => ticketTypeName && tick.nombre && tick.nombre.trim().toLowerCase() === ticketTypeName.toLowerCase()) ||
        list.find(tick => ticketTypeId && tick.id && String(tick.id) === String(ticketTypeId))
      if (match) {
        return ticketConfigIncluyeCoffee(match)
      }
    }
  }

  // 3. Propiedad explícita guardada en participante o inscripción
  if (typeof p.incluyeCoffee === 'boolean') {
    return p.incluyeCoffee
  }
  if (typeof inscripcion.incluyeCoffee === 'boolean') {
    return inscripcion.incluyeCoffee
  }

  // 4. Fallback por nombre del boleto ('full' o 'completo')
  return esNombreBoletoFull(ticketTypeName)
}
