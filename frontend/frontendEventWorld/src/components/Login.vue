<template>
  <div class="fond">
    <div class="login-container">
      <h1 class="title">Log in</h1>
      <form @submit.prevent="handleLogin" class="form-container">
        <!-- Identifiant -->
        <div class="form-group">
          <input
            v-model="identifier"
            type="text"
            id="identifier"
            placeholder="Email or Username"
            required
          />
        </div>

        <!-- Mot de passe -->
        <div class="form-group">
          <input
            v-model="password"
            type="password"
            id="password"
            placeholder="Password"
            required
            autocomplete="current-password"
          />
        </div>

        <!-- Boutons -->
        <div class="button-group">
          <button type="submit" class="btn-secondary">Log in</button>
          <button @click="goback" type="button" class="btn-primary">Back</button>
        </div>

        <!-- Lien pour mot de passe oublié -->
        <p class="forgot-password" @click="forgotPassword">Forgotten password</p>
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
      identifier: '', // email ou nom d'utilisateur
      password: '',
      errorMessage: null,
    };
  },
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();
    return { authStore, router };
  },
  methods: {
    async handleLogin() {
      try {
        await this.authStore.loginUser(this.identifier, this.password);
        if (this.authStore.isAuthenticated) {
          this.router.push('/menu'); // Redirection après connexion réussie
        } else {
          this.errorMessage = 'Incorrect credentials.';
        }
      } catch (error) {
        this.errorMessage = 'Login failed. Please check your credentials.';
      }
    },
    forgotPassword() {
      this.router.push('/ResetPassword'); // Redirige vers la page de réinitialisation du mot de passe
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