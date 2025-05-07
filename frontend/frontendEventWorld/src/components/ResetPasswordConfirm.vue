<template>
    <div class="fond">
      <div class="login-container">
        <h1 class="title">Nouveau mot de passe</h1>
        <form @submit.prevent="submitNewPassword" class="form-container">
          <div class="form-group">
            <input
              v-model="password"
              type="password"
              placeholder="Nouveau mot de passe"
              required
            />
          </div>
          <div class="form-group">
            <input
              v-model="confirmPassword"
              type="password"
              placeholder="Confirmez le mot de passe"
              required
            />
          </div>
  
          <div class="button-group">
            <button type="submit" class="btn-secondary">Réinitialiser</button>
          </div>
          <p v-if="successMessage" style="color: green">{{ successMessage }}</p>
          <p v-if="errorMessage" style="color: red">{{ errorMessage }}</p>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import { useRoute, useRouter } from 'vue-router';
  import axios from 'axios';
  
  export default {
    data() {
      return {
        password: '',
        confirmPassword: '',
        successMessage: null,
        errorMessage: null,
      };
    },
    setup() {
      const route = useRoute();
      const router = useRouter();
      return { route, router };
    },
    methods: {
      async submitNewPassword() {
        if (this.password !== this.confirmPassword) {
          this.errorMessage = "Les mots de passe ne correspondent pas.";
          return;
        }
  
        try {
          const { uid, token } = this.route.params;
          const response = await axios.post('http://127.0.0.1:8000/api/reset-password-confirm/', {
            uid,
            token,
            password: this.password,
          });
          console.log("Réponse brute:", response);
          this.successMessage = "Mot de passe réinitialisé avec succès.";
          this.errorMessage = null;
  
          setTimeout(() => {
            this.router.push('/Login');
          }, 2000);
        } catch (err) {
          this.errorMessage = "Erreur : lien invalide ou expiré.";
          this.successMessage = null;
        }
      },
    },
  };
  </script>
  
  <style scoped>
  @import '@/assets/styles/Login.css';
  </style>
  