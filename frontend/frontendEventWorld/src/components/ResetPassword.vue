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
  console.log('handleReset called with identifier:', this.identifier);

  try {
    const response = await fetch("http://127.0.0.1:8000/api/reset-password/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ email: this.identifier }),
    });

    const data = await response.json();
    console.log("Réponse brute:", response.status, data);

    if (response.ok) {
      this.successMessage = "Lien envoyé.";
      // this.router.push('/reset-password-confirm'); Redirection vers la page de confirmation
    } else {
      this.errorMessage = data?.error || "Erreur.";
      this.successMessage = null;
    }
  } catch (err) {
    console.error("Erreur réseau:", err);
    this.errorMessage = "Erreur réseau.";
    this.successMessage = null;
  }
},

    
      // async handleReset() {
    //   try {
    //     console.log('handleReset called with identifier:', this.identifier);
    //     await this.authStore.requestPasswordResetStore(this.identifier);
    //     this.successMessage = 'Un lien de réinitialisation vous a été envoyé.';
    //     this.errorMessage = null;
    //   } catch (error) {
    //     this.errorMessage = "Adresse e-mail inconnue ou erreur serveur.";
    //     this.successMessage = null;
    //     // Toast (optionnel avec alert simple ici)
    //     alert(this.successMessage);

    //     // Redirection 3 secondes après
    //     setTimeout(() => {
    //       this.router.push('/FirstPage');
    //     }, 3000);
    //   }
    // },
      goback() {
        this.router.push('/FirstPage'); // Redirige vers la page d'accueil
      },
    },
  };
  </script>
  
  <style scoped>
  
  @import '@/assets/styles/Login.css';
  
  </style>