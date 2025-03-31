// chaque store doit être équipé de l'import des api : par exemple
//import { recherche_produits } from "@/utils/api_utils";
// ...export async function recherche_produits(entreprise_id = null) {...
// model d'appel pour éviter la redondance dans les stores
// ...allProducts.value = await recherche_produits(selectedFournisseurId); // Appel à la fonction API...


import { defineStore } from "pinia";
import api from "@/services/axiosInstance";
import Cookies from "js-cookie";

export const useAuthStore = defineStore("authStore", {
  state: () => ({
    user: null,
    token: Cookies.get("authToken") || null,
    error: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    isNotStudent: (state) => state.user?.role !== "etudiant", // utilisateur ≠ étudiant
    //isStudent: (state) => state.user?.role === 'etudiant',
  },

  actions: {
    async loginUser(username, password) {
      try {
        const response = await api.post("token/", { username, password });
        const { access, refresh } = response.data;

        Cookies.set("authToken", access);
        Cookies.set("refreshToken", refresh);
        this.token = access;

        // Met à jour les headers Axios automatiquement
        api.defaults.headers.common["Authorization"] = `Bearer ${access}`;

  // 🔄 Recharge les données utilisateur
  const userResponse = await api.get("user/");
  this.user = userResponse.data;

  // ✅ On vide les anciens événements (optionnel)
  const eventStore = useEventStore();
  
  eventStore.events = [];
   // ✅ Recharge les événements de ce user
   await eventStore.fetchEvents();

        this.error = null;
      } catch (err) {
        this.error = "Échec de la connexion. Vérifiez vos identifiants.";
      }
    },

    async logoutUser(router) {
      Cookies.remove("authToken");
      Cookies.remove("refreshToken");
      this.token = null;
      this.user = null;
      delete api.defaults.headers.common["Authorization"];
      if (router) router.push("/login");
    },

    async autoLogin() {
      try {
        const response = await api.get("user/");
        this.user = response.data;
      } catch (err) {
        this.logoutUser();
      }
    },
  },
});
