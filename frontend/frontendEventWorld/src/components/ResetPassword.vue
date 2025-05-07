<template>
    <div class="fond">
      <div class="login-container">
        <h1 class="title">Reset Password</h1>
        <p>Reset your password</p>
        <form @submit.prevent="handleReset" class="form-container">
          <!-- Identifiant -->
          <div class="form-group">
            <input
              v-model="identifier"
              type="text"
              id="identifier"
              placeholder="Email"
              required
            />
          </div>
  
          <!-- Boutons -->
          <div class="button-group">
            <button type="submit" class="btn-secondary">Reset</button>
            <button @click="goback" type="button" class="btn-primary">Back</button>
          </div>
          <p v-if="successMessage" style="color: green">{{ successMessage }}</p>
          <p v-if="errorMessage" style="color: red">{{ errorMessage }}</p>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import { useAuthStore } from '@/stores/authStore';
  import { requestPasswordReset } from '@/services/authService';
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'Login',
    data() {
      return {
        identifier: '', // email 
        errorMessage: null,
        successMessage: null,
      };
    },
    setup() {
      const authStore = useAuthStore();
      const router = useRouter();
      return { authStore, router };
    },
    methods: {
      async handleReset() {
      try {
        await requestPasswordReset(this.identifier);
        this.successMessage = "Lien envoyé.";
        this.errorMessage = null;
      } catch (err) {
        this.errorMessage = err.message || "Erreur.";
        this.successMessage = null;
      }
    },
    goback() {
      this.router.push('/FirstPage');
    },

      goback() {
        this.router.push('/FirstPage'); // Redirige vers la page d'accueil
      },
    },
  };
  </script>
  
  <style scoped>
  
  @import '@/assets/styles/Login.css';
  
  </style>