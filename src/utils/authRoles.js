import { db } from '../firebase'
import { getDoc, doc, getDocs, collection, query, where } from 'firebase/firestore'

export const obtenerRolesUsuario = async (user) => {
  if (!user) return []
  try {
    const docRef = doc(db, 'users', user.uid)
    const snap = await getDoc(docRef)
    if (snap.exists() && Array.isArray(snap.data().roles)) {
      return snap.data().roles
    }

    if (user.email) {
      const emailLower = user.email.toLowerCase().trim()
      const q = query(collection(db, 'users'), where('email', '==', emailLower))
      const snapEmail = await getDocs(q)
      if (!snapEmail.empty && Array.isArray(snapEmail.docs[0].data().roles)) {
        return snapEmail.docs[0].data().roles
      }

      // Buscar por campo 'correo' en 'users'
      const qCorreo = query(collection(db, 'users'), where('correo', '==', emailLower))
      const snapCorreo = await getDocs(qCorreo)
      if (!snapCorreo.empty && Array.isArray(snapCorreo.docs[0].data().roles)) {
        return snapCorreo.docs[0].data().roles
      }

      // Buscar en colección legacy 'usuarios'
      try {
        const qLegacy = query(collection(db, 'usuarios'), where('correo', '==', emailLower))
        const snapLegacy = await getDocs(qLegacy)
        if (!snapLegacy.empty && Array.isArray(snapLegacy.docs[0].data().roles)) {
          return snapLegacy.docs[0].data().roles
        }
      } catch (errLegacy) {}
    }

    // Default para superadmin / primer usuario sin roles explícitos
    return ['admin', 'crear', 'editar', 'ver', 'qr']
  } catch (e) {
    console.warn('Error resolviendo roles:', e)
    return ['admin', 'crear', 'editar', 'ver', 'qr']
  }
}
