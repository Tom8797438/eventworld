import axios from "axios";
import Cookies from "js-cookie";

const API_URL = "http://localhost:8000/api/";

// ✅ Création d'une instance Axios avec configuration sécurisée
const api = axios.create({
  baseURL: API_URL,
  headers: { "Content-Type": "application/json" },
});

// ✅ Ajoute automatiquement le token aux requêtes si disponible
api.interceptors.request.use(
  (config) => {
    const token = Cookies.get("authToken");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// ===========================
// ✅ PARTIE AUTHENTIFICATION
// ===========================

// Fonction de connexion
export async function login(username, password) {
  try {
    const response = await api.post("token/", { username, password });
    const { access, refresh } = response.data;

    // Stockage sécurisé des tokens
    Cookies.set("authToken", access, { secure: true, sameSite: "Strict" });
    Cookies.set("refreshToken", refresh, { secure: true, sameSite: "Strict" });

    return response.data;
  } catch (error) {
    console.error("Erreur de connexion :", error.response?.data || error.message);
    throw error;
  }
}

// Rafraîchir le token
export async function refreshToken() {
  try {
    const refresh = Cookies.get("refreshToken");
    if (!refresh) throw new Error("Aucun token de rafraîchissement disponible.");

    const response = await api.post("token/refresh/", { refresh });
    Cookies.set("authToken", response.data.access, { secure: true, sameSite: "Strict" });

    return response.data.access;
  } catch (error) {
    console.error("Erreur lors du rafraîchissement du token :", error.response?.data || error.message);
    throw error;
  }
}

// Déconnexion
export function logout(router) {
  Cookies.remove("authToken");
  Cookies.remove("refreshToken");
  delete api.defaults.headers.common["Authorization"];

  if (router) router.push("/login").catch(err => console.error(err));
}

// ===========================
// ✅ PARTIE ÉVÉNEMENTS
// ===========================

// Récupérer tous les événements
export async function fetchEvents() {
  try {
    const response = await api.get("events/");
    return response.data;
  } catch (error) {
    console.error("Erreur récupération des événements :", error.response?.data || error.message);
    throw error;
  }
}

// Créer un nouvel événement
export async function createEvent(eventData) {
  try {
    console.log("Données envoyées:", eventData);
    const response = await api.post("events/", eventData);
    return response.data;
  } catch (error) {
    console.error("Erreur création d'événement :", error.response?.data || error.message);
    throw error;
  }
}

// Supprimer un événement
export async function deleteEvent(Id) {
  try {
    const response = await api.delete(`events/${Id}/`);
    return response.data;
  } catch (error) {
    console.error("Erreur suppression d'événement :", error.response?.data || error.message);
    throw error;
  }
}

// ===========================
// ✅ PARTIE TICKETS
// ===========================

// Fonction pour acheter des billets
export async function purchaseTickets(Id, tickets) {
  try {
    const response = await api.post("tickets/", {
      id: Id,
      tickets: tickets
    });

    return response.data;
  } catch (error) {
    console.error("Erreur lors de l'achat des billets :", error.response?.data || error.message);
    throw error;
  }
}
export default api;
