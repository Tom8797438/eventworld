<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-indigo-100 flex items-center justify-center sm:px-4 lg:px-6">
    <div class="max-w-2xl w-full space-y-8 bg-gradient-to-br from-blue-100 via-purple-50 to-purple-200 p-8 rounded-lg shadow-lg">
      <!-- Logo -->
      <div class="flex justify-center">
        <img src="@/assets/styles/pictures/logo.png" alt="Logo" class="h-28 w-auto " />
      </div>

      <!-- Titre -->
      <div class="text-center">
        <h1 class="text-3xl font-bold text-purple-800">Register for free</h1>
      </div>

      <!-- Formulaire -->
      <form @submit.prevent="handleRegister" class="space-y-6">
        <!-- Grille pour les champs -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Nom d'utilisateur -->
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700">Nom utilisateur</label>
            <input
              v-model="user.username"
              type="text"
              id="username"
              placeholder="Nom utilisateur"
              required
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>

          <!-- Raison Sociale -->
          <div>
            <label for="company_name" class="block text-sm font-medium text-gray-700">Raison Sociale</label>
            <input
              v-model="profil.company_name"
              type="text"
              id="company_name"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>

          <!-- N° Entreprise -->
          <div>
            <label for="company_number" class="block text-sm font-medium text-gray-700">N° Entreprise</label>
            <input
              v-model="profil.company_number"
              type="text"
              id="company_number"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>

          <!-- Email -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
            <input
              v-model="user.email"
              type="email"
              id="email"
              required
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>

          <!-- Civilité -->
          <div>
            <label for="civility" class="block text-sm font-medium text-gray-700">Civilité</label>
            <select
              v-model="user.civility"
              id="civility"
              required
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            >
              <option>Monsieur</option>
              <option>Madame</option>
              <option>Licone</option>
              <option>Chaise</option>
              <option>Mite en pullover</option>
              <option>Hélicoptère de combat</option>
              <option>Autre</option>
            </select>
          </div>

          <!-- Nom du contact -->
          <div>
            <label for="name_contact" class="block text-sm font-medium text-gray-700">Nom du contact</label>
            <input
              v-model="profil.name_contact"
              type="text"
              id="name_contact"
              required
              @input="validateTextOnly"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>

          <!-- Adresse -->
          <div>
            <label for="address" class="block text-sm font-medium text-gray-700">Adresse</label>
            <input
              v-model="profil.address"
              type="text"
              id="address"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>

          <!-- Code postal -->
          <div>
            <label for="postal_code" class="block text-sm font-medium text-gray-700">Code postal</label>
            <input
              v-model="profil.postal_code"
              type="text"
              id="postal_code"
              required
              @input="validateNumber"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>

          <!-- Ville -->
          <div>
            <label for="city" class="block text-sm font-medium text-gray-700">Ville</label>
            <input
              v-model="profil.city"
              type="text"
              id="city"
              required
              @input="validateTextOnly"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>

          <!-- Mot de passe -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">Mot de passe</label>
            <input
              v-model="user.password"
              type="password"
              id="password"
              required
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>

          <!-- Prénom du contact -->
          <div>
            <label for="surname_contact" class="block text-sm font-medium text-gray-700">Prénom du contact</label>
            <input
              v-model="profil.surname_contact"
              type="text"
              id="surname_contact"
              required
              @input="validateTextOnly"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>

          <!-- Téléphone mobile -->
          <div>
            <label for="mobile_phone" class="block text-sm font-medium text-gray-700">Téléphone mobile</label>
            <input
              v-model="profil.mobile_phone"
              type="tel"
              id="mobile_phone"
              placeholder="Téléphone mobile"
              required
              @input="validateNumber"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>

          <!-- Type de compte -->
          <div>
            <label for="role" class="block text-sm font-medium text-gray-700">Type de compte</label>
            <select
              v-model="user.role"
              id="role"
              required
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            >
              <option value="organisateur">Organisateur</option>
              <option value="association">Association</option>
              <option value="etudiant">Étudiant</option>
              <option value="autre">Autre</option>
            </select>
          </div>

          <!-- Téléphone fixe -->
          <div>
            <label for="landline_phone" class="block text-sm font-medium text-gray-700">Téléphone fixe</label>
            <input
              v-model="profil.landline_phone"
              type="tel"
              id="landline_phone"
              placeholder="Téléphone fixe"
              required
              @input="validateNumber"
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>
        </div>

        <!-- Boutons -->
        <div class="flex space-x-4">
          <button
            type="submit"
            class="flex-1 bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200"
          >
            Sign up
          </button>
          <button
            @click="goback"
            type="button"
            class="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-colors duration-200"
          >
            Back
          </button>
        </div>
      </form>

      <!-- Termes -->
      <p class="text-center text-sm text-gray-600">
        By signing up, you agree to Photo's <a href="#" class="text-indigo-600 hover:text-indigo-500">Terms of Service</a> and <a href="#" class="text-indigo-600 hover:text-indigo-500">Privacy Policy</a>.
      </p>

      <!-- Erreur -->
      <p v-if="errorMessage" class="text-center text-red-600 text-sm">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
import { registerUser } from '@/services/authService';
import { useRouter } from 'vue-router';
import { validateNumber, validateTextOnly,isValidEmail } from '@/utils/validators';

export default {
  name: 'Register',
  data() {
    return {
      user: {
        username: '',
        email: '',
        password: '',
        role: 'organisateur',
        civility:'',
      },
      profil: {
        company_name: '',
        company_number: '',
        name_contact: '',
        surname_contact: '',
        mobile_phone: '',
        address: '',
        city: '',
        postal_code: '',
        landline_phone: '',
        civility: '',
      },
      errorMessage: null,
    };
  },
  setup() {
    const router = useRouter();
    return { 
      router,
      validateNumber,
      validateTextOnly,
      isValidEmail,
     };
  },
  methods: {
    async handleRegister() {
      try {
        await registerUser({ user: this.user, profil: this.profil });
        this.$router.push('/login'); 
      } catch (error) {
        this.errorMessage = "Erreur d'inscription. Vérifiez vos informations.";
      }
    },
    goback(){
      this.router.push('/firstPage'); 
    }
  },
};

</script>

