<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-indigo-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white p-8 rounded-lg shadow-lg">
      <div class="text-center">
        <h1 class="text-3xl font-bold text-purple-800">Reset Password</h1>
        <p class="text-gray-600">Reset your password</p>
      </div>
      <form @submit.prevent="handleReset" class="space-y-6">
        <!-- Email -->
        <div>
          <input
            v-model="identifier"
            type="text"
            id="identifier"
            placeholder="Email"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          />
        </div>

        <!-- Boutons -->
        <div class="flex space-x-4">
          <button
            type="submit"
            class="flex-1 bg-gray-800 text-white py-2 px-4 rounded-md hover:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-colors duration-200"
          >
            Reset
          </button>
          <button
            @click="goback"
            type="button"
            class="flex-1 bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200"
          >
            Back
          </button>
        </div>

        <!-- Messages -->
        <p v-if="successMessage" class="text-center text-green-600 text-sm">{{ successMessage }}</p>
        <p v-if="errorMessage" class="text-center text-red-600 text-sm">{{ errorMessage }}</p>
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
 