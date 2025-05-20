import axios from "axios";
// import { error } from "cypress/types/jquery";
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
    Cookies.set("authToken", response.data.access, { secure: true, sameSite: "Strict", expires: 1,});

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

// reset-password/
export async function resetPassword(email) {
  try {
    const response = await api.post("reset-password/", { email });
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la demande de réinitialisation du mot de passe :", error.response?.data || error.message);
    throw error;
  }
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
    //console.log("Données envoyées:", eventData);
    const response = await api.post("events/", eventData, {
      headers: {
        'Content-Type': 'multipart/form-data', // Indique que les données incluent un fichier
      },
  });
    return response.data;
  } catch (error) {
    console.error("Erreur création d'événement :", error.response?.data || error.message);
    throw error;
  }
}
//******
// élément à supprimer
// {
//   headers: {
//     'Content-Type': 'multipart/form-data',
//   },
// });        ne pas oublier de laisser )
//*******

// Modifier un événement
export async function updateEvent(eventId, updatedData) {
  try{
    const response = await api.put(`events/${eventId}/`, updatedData, {
      headers: {
        'Content-Type': 'multipart/form-data', // Indique que les données incluent un fichier
      },
  });
    return response.data;
  } catch (error) {
    console.error("Erreur modification d'événement :", error.response?.data || error.message);
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

// ===========================
// ✅ PARTIE SCAN TICKET
// ===========================

// Vérifier le QR Code auprès du backend
export async function checkTicketStatus(qr_code) {
  try {
    const response = await api.post("scan_ticket/", qr_code);
    console.log("api_utils.js checkTicketStatus: ",qr_code)
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la vérification du ticket :", error.response?.data || error.message);
    throw error;
  }
}

// ===========================
// ✅ PARTIE INVITATION
// ===========================

export async function generateInvitation(eventId, email = null) {
  try {
    // Construire le payload en incluant l'event_id et, optionnellement, l'email.
    const payload = { event_id: eventId };
    if (email) {
      payload.email = email;
    }
    // Appel à l'API pour créer l'invitation
    const response = await api.post("invitation/", payload);
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la génération de l'invitation :", error.response?.data || error.message);
    throw error;
  }
}

// ✅ Récupération de l’invitation via son ID
export async function fetchInvitationById(invitationId) {
  try {
    const response = await api.get(`invitation/${invitationId}/`);
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la récupération de l'invitation :", error.response?.data || error.message);
    throw error;
  }
}

export async function fetchInvitationByEventId(eventId) {
  try {
    const response = await api.get(`invitation/by-event/?event_id=${eventId}`);
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la récupération de l'invitation via event_id :", error.response?.data || error.message);
    throw error;
  }
}

// ===========================
// ✅ PARTIE GESTION DES UTILISATEURS TEMPORAIRES
// ===========================

  export async function createEventWithTempUsers(formData) {
    try {
      console.log("Données dans api_utils.js createEventWithTempUsers :", formData);
      const response = await api.post('event/create-with-temp-users/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      console.log("Données dans api_utils.js createEventWithTempUsers :", formData);
      return response.data;
    } catch (error) {
      console.error("Erreur lors de la création de l'utilisateur temporaire :", error.response?.data || error.message);
      throw error;
    }
  }

  export async function fetchTemporaryScanners(eventId) {
    try {
      const response = await api.get(`event/${eventId}/temporary-scanners/`);
      console.log("Données dans api_utils.js loadTemporaryScanners :", response.data);
      return response.data;
    } catch (error) {
      console.error("Erreur loadTemporaryScanners:", error.response?.data || error.message);
      throw error;
    }
  }

  export async function updateTemporaryScanner(scannerId, payload) {
    try {
      const response = await api.put(`temporary-scanner/${scannerId}/`, payload);
      return response.data;
    } catch (error) {
      console.error("Erreur updateTemporaryScanner:", error.response?.data || error.message);
      throw error;
    }
  }

  export async function deleteTemporaryScanner(scannerId) {
    try {
      const response = await api.delete(`temporary-scanner/${scannerId}/`);
      return response.data;
    } catch (error) {
      console.error("Erreur deleteTemporaryScanner:", error.response?.data || error.message);
      throw error;
    }
  }
