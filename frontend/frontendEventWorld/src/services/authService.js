//Connection du Frontend Vue.js à l’API Django

import axios from 'axios';

const AUTH_API_URL = 'http://127.0.0.1:8000/api/token/';
const API_URL = 'http://127.0.0.1:8000/api/'; 

export async function login(username, password) {
    return await axios.post(AUTH_API_URL, { username, password,}, {
        withCredentials: true  // 🍪 Très important pour envoyer/recevoir les cookies
      });
    }

// export async function refreshToken() {
//     const response = await axios.post(`${AUTH_API_URL}refresh/`, {
//         refresh: localStorage.getItem('refresh_token'),
//     });
//     localStorage.setItem('access_token', response.data.access);
// }

// Rafraîchissement du token (si tu en fais un jour, via cookie sécurisé)
export async function refreshToken() {
    return await axios.post(`${AUTH_API_URL}refresh/`, {}, {
      withCredentials: true
    });
  }

// export function logout() {
//     localStorage.removeItem('access_token');
//     localStorage.removeItem('refresh_token');
// }

// Déconnexion
export async function logout() {
    // ❌ On ne touche plus au localStorage
    // ✅ Optionnel : tu peux faire un appel backend pour effacer le cookie si besoin
    return await axios.post(`${API_URL}logout/`, {}, {
      withCredentials: true
    });
  }

export async function registerUser(userData) {
    try {
        console.log("donnée envoyée: ", JSON.stringify(userData, null, 2));
        const response = await axios.post(`${API_URL}register/`, userData, {
            headers: { "Content-Type": "application/json" },
        });
        console.log("réponse de api: ", response.data)
        return response.data;
    } catch (error) {
      console.error("Erreur d'inscription :", error.response?.data || error.message);
      throw error;
    }
} 