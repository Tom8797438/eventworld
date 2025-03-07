// chaque store doit être équipé de l'import des api : par exemple
//import { recherche_produits } from "@/utils/api_utils";
// ...export async function recherche_produits(entreprise_id = null) {...
// model d'appel pour éviter la redondance dans les stores
// ...allProducts.value = await recherche_produits(selectedFournisseurId); // Appel à la fonction API...


import { defineStore } from "pinia";
import { login, logout } from "@/utils/api_utils";
import Cookies from "js-cookie";

export const useAuthStore = defineStore("authStore", {
  state: () => ({
    user: null,
    token: Cookies.get("authToken") || null,
    error: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    async loginUser(username, password) {
      try {
        const { access } = await login(username, password);
        this.token = access;
        this.error = null;
      } catch (err) {
        this.error = "Échec de la connexion. Vérifiez vos identifiants.";
      }
    },

    logoutUser(router) {
      logout(router);
      this.token = null;
      this.user = null;
    },

    async autoLogin() {
      try {
        const user = await getUser();
        if (user) {
          this.user = user;
          this.token = Cookies.get("authToken"); // Vérifier si le token est bien récupéré
        } else {
          this.logoutUser(); // Déconnexion si le token est invalide
        }
      } catch (err) {
        console.warn("Auto-login échoué", err);
      }
    },
  },
});