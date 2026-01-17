<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-indigo-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white p-8 rounded-lg shadow-lg">
      <div class="text-center">
        <h1 class="text-3xl font-bold text-purple-800">Log in</h1>
      </div>
      <form @submit.prevent="handleLogin" class="space-y-6">
        <!-- Identifiant -->
        <div>
          <input
            v-model="identifier"
            type="text"
            id="identifier"
            placeholder="Email or Username"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          />
        </div>

        <!-- Mot de passe -->
        <div>
          <input
            v-model="password"
            type="password"
            id="password"
            placeholder="Password"
            required
            autocomplete="current-password"
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          />
        </div>

        <!-- Boutons -->
        <div class="flex space-x-4">
          <button
            type="submit"
            class="flex-1 bg-gray-800 text-white py-2 px-4 rounded-md hover:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-colors duration-200"
          >
            Log in
          </button>
          <button
            @click="goback"
            type="button"
            class="flex-1 bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200"
          >
            Back
          </button>
        </div>

        <!-- Lien pour mot de passe oublié -->
        <p
          class="text-center text-sm text-blue-600 hover:text-blue-500 cursor-pointer transition-colors duration-200"
          @click="forgotPassword"
        >
          Forgotten password
        </p>
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

