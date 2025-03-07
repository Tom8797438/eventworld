import axios from "axios";
import Cookies from "js-cookie";

// Création d'une instance Axios avec la base URL de l'API
const api = axios.create({
  baseURL: "http://localhost:8000/api/",
  headers: { "Content-Type": "application/json" },
});

// Fonction pour se connecter
export async function login(username, password) {
  try {
    const response = await api.post("token/", {
      username,
      password,
    });
    
    const { access, refresh } = response.data;

    // Stocker les tokens dans les cookies
    Cookies.set("authToken", access, { sameSite: "strict" }); // Pour HTTP
    // Cookies.set("authToken", access, { secure: true, sameSite: "strict" }); // Pour HTTPS

    // Configurer Axios avec le token
    api.defaults.headers.common["Authorization"] = `Bearer ${access}`;

    return { access, refresh };
  } catch (error) {
    console.error("Erreur d'authentification :", error.response?.data || error.message);
    throw error;
  }
}

// Fonction pour rafraîchir le token
export async function refreshToken() {
  try {
    const refresh = Cookies.get("refreshToken");
    if (!refresh) throw new Error("Aucun token de rafraîchissement disponible.");

    const response = await api.post("token/refresh/", { refresh });
    const { access } = response.data;

    Cookies.set("authToken", access, { sameSite: "strict" });
    // Cookies.set à adapter pour le HTTPS

    // Met à jour l'Authorization d'Axios
    api.defaults.headers.common["Authorization"] = `Bearer ${access}`;

    return access;
  } catch (error) {
    console.error("Erreur lors du rafraîchissement du token :", error.response?.data || error.message);
    throw error;
  }
}

// Fonction pour se déconnecter
export function logout(router) {
  Cookies.remove("authToken");
  Cookies.remove("refreshToken");
  delete api.defaults.headers.common["Authorization"];

  if (router) {
    router.push("/login").catch(err => {
      if (err.name !== "NavigationDuplicated") {
        console.error(err);
      }
    });
  }
}

// Fonction pour récupérer l'utilisateur connecté
export async function getUser() {
  try {
    const token = Cookies.get("authToken");
    if (!token) throw new Error("Aucun token trouvé");

    // Ajouter le token dans les headers
    api.defaults.headers.common["Authorization"] = `Bearer ${token}`;

    // Appel API pour récupérer les infos utilisateur
    const response = await api.get("user/");
    return response.data;
  } catch (error) {
    console.warn("Erreur lors de la récupération de l'utilisateur :", error);
    return null; // Retourne null en cas d'échec
  }
}

export default api;
