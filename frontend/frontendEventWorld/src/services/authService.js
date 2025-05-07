//Connection du Frontend Vue.js à l’API Django

import axios from 'axios';

const AUTH_API_URL = 'http://127.0.0.1:8000/api/token/';
const API_URL = 'http://127.0.0.1:8000/api/'; 

export async function login(username, password) {
    return await axios.post(AUTH_API_URL, { username, password,}, {
        withCredentials: true  // 🍪 Très important pour envoyer/recevoir les cookies
      });
    }

// Rafraîchissement du token (si tu en fais un jour, via cookie sécurisé)
export async function refreshToken() {
    return await axios.post(`${AUTH_API_URL}refresh/`, {}, {
      withCredentials: true
    });
  }

// Déconnexion
export async function logout() {
    // Optionnel : faire un appel backend pour effacer le cookie si besoin
    return await axios.post(`${API_URL}logout/`, {}, {
      withCredentials: true
    });
  }

// Inscription de l'utilisateur
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

// Reset password
export async function requestPasswordReset(email) {
  try {
    console.log("Demande de réinitialisation du mot de passe pour l'email :", email);
    const response = await axios.post(
      `${API_URL}reset-password/`,
      { email },
      {
        withCredentials: true, // ✅ très important ici
        headers: { "Content-Type": "application/json" }
      }
    );
    console.log("Réponse du backend:", response.data);
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la demande de réinitialisation du mot de passe :", error.response?.data || error.message);
    throw error;
  }
}
