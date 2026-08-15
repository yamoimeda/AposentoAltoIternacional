import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
import { getStorage } from 'firebase/storage'

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || "AIzaSyCW-1YmJC0BgObJTk0eJ7PJdAtTI_rz2X4",
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || "el-aposento-alto.firebaseapp.com",
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || "el-aposento-alto",
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || "el-aposento-alto.firebasestorage.app",
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || "906915946572",
  appId: import.meta.env.VITE_FIREBASE_APP_ID || "1:906915946572:web:075b1f160d073d5ae554e9",
  measurementId: import.meta.env.VITE_FIREBASE_MEASUREMENT_ID || ""
};

let app;
try {
  app = initializeApp(firebaseConfig);
} catch (e) {
  console.warn("Firebase initialization warning:", e);
  app = initializeApp({ apiKey: "demo-key", projectId: "el-aposento-alto" });
}

export const storage = getStorage(app);
export const auth = getAuth(app);
auth.languageCode = 'es';
export const db = getFirestore(app);
