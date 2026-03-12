/**
 * Skillify – Firebase Configuration
 * ====================================
 * SETUP INSTRUCTIONS (takes ~5 minutes):
 *
 * 1. Go to https://console.firebase.google.com/
 * 2. Click "Add project" → name it "skillify" → Continue
 * 3. Go to Authentication → Get Started → Enable "Email/Password" + "Google"
 * 4. Go to Project Settings (⚙️) → Your apps → click "</>" Web icon
 * 5. Register app (any name) → Copy the config below and paste it here
 *
 * Until you do this, the site runs in DEMO MODE (localStorage-based)
 */

const firebaseConfig = {
    apiKey: "AIzaSyDql21rjQQlNxLaRwVyxcEalUSHyCLhziE",
    authDomain: "killify-5028e.firebaseapp.com",
    projectId: "killify-5028e",
    storageBucket: "killify-5028e.firebasestorage.app",
    messagingSenderId: "786948386994",
    appId: "1:786948386994:web:059e1bbf0a06e64fa859ab",
    measurementId: "G-32BHX1N6W4"
};

// Detect demo mode
const IS_DEMO = firebaseConfig.apiKey === "YOUR_API_KEY";

let firebaseApp = null;
let firebaseAuth = null;
let firebaseDB = null;

if (!IS_DEMO) {
  // Real Firebase
  firebaseApp = firebase.initializeApp(firebaseConfig);
  firebaseAuth = firebase.auth();
} else {
  console.warn("🔵 Skillify running in DEMO MODE – Fill in firebase-config.js to enable real auth");
}

const BACKEND_URL = "http://localhost:5000/api";
