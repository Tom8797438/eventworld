<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-indigo-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white p-8 rounded-lg shadow-lg">
      <div class="text-center">
        <h1 class="text-3xl font-bold text-purple-800">Nouveau mot de passe</h1>
      </div>
      <form @submit.prevent="submitNewPassword" class="space-y-6">
        <!-- Nouveau mot de passe -->
        <div>
          <input
            v-model="password"
            type="password"
            placeholder="Nouveau mot de passe"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          />
        </div>

        <!-- Confirmation -->
        <div>
          <input
            v-model="confirmPassword"
            type="password"
            placeholder="Confirmez le mot de passe"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          />
        </div>

        <!-- Bouton -->
        <button
          type="submit"
          class="w-full bg-gray-800 text-white py-2 px-4 rounded-md hover:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-colors duration-200"
        >
          Réinitialiser
        </button>

        <!-- Messages -->
        <p v-if="successMessage" class="text-center text-green-600 text-sm">{{ successMessage }}</p>
        <p v-if="errorMessage" class="text-center text-red-600 text-sm">{{ errorMessage }}</p>
      </form>
    </div>
  </div>
</template>
  
  <script>
  import { useRoute, useRouter } from 'vue-router';
  import { resetPasswordConfirm } from '@/services/authService';
  
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
        await resetPasswordConfirm(
            this.route.params.uid,
            this.route.params.token,
            this.password,
            );
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
