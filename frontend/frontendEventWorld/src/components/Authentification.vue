<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-indigo-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white p-8 rounded-lg shadow-lg">
      <div class="text-center">
        <h1 class="text-3xl font-bold text-purple-800">Connexion</h1>
      </div>
      <form @submit.prevent="login" class="space-y-6">
        <div>
          <label for="identifier" class="block text-sm font-medium text-gray-700">Email ou Nom d'utilisateur</label>
          <input
            v-model="identifier"
            type="text"
            id="identifier"
            placeholder="Email ou Nom d'utilisateur"
            required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          />
        </div>
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">Mot de passe</label>
          <input
            v-model="password"
            type="password"
            id="password"
            required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          />
        </div>
        <button
          type="submit"
          class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200"
        >
          Se connecter
        </button>
      </form>
      <p v-if="error" class="text-center text-red-600 text-sm">{{ error }}</p>
    </div>
  </div>
</template>
  
<script>
import { useAuthStore } from '@/stores/authStore';

export default {
  name: 'Login',
  data() {
    return {
      identifier: '',
      password: '',
    };
  },
  computed: {
    error() {
      const authStore = useAuthStore();
      return authStore.error;
    },
  },
  methods: {
    async login() {
      const authStore = useAuthStore();
      await authStore.login(this.identifier, this.password);
      if (!authStore.error) {
        this.$router.push('/menu'); 
      }
    },
  },
};
</script>
