<template>
  <div class="login-container">
    <h1 class="title">Connexion</h1>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="identifier" class="title">Email ou Nom d'utilisateur</label>
        <input
          v-model="identifier"
          type="text"
          id="identifier"
          placeholder="Email ou Nom d'utilisateur"
          required
        />
      </div>
      <div class="form-group">
        <label for="password" class="title">Mot de passe</label>
        <input
          v-model="password"
          type="password"
          id="password"
          required
        />
      </div>
      <button type="submit">Se connecter</button>
    </form>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    <div class="register-button">
      <button @click="redirection">Inscription</button>
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
      identifier: '', // email ou un nom d'utilisateur
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
          this.router.push('/menu'); // Redirection
        } else {
          this.errorMessage = "Identifiants incorrects.";
        }
      } catch (error) {
        this.errorMessage = "Échec de la connexion. Vérifiez vos identifiants.";
      }
    },
  
    redirection(){
      this.router.push('/register');
    }
  },
};
</script>

<style scoped>
@import '@/assets/styles/Authentification.css';
</style>
