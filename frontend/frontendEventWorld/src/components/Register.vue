<template>
  <div class="fond">
    <!-- Conteneur principal -->

  <div class="register-container">
     
    <div class="container-logo"><img src="@/assets/styles/logo.png" alt="Logo" class="logo" /></div>

    <div class="container-title">
      <h1 class="title">Register for free</h1>
      <!-- <button @click="goback" class="back-button">←</button> -->
    </div>
    <form @submit.prevent="handleRegister" class="form-container">

      <!-- Nom d'utilisateur -->
      <div class="form-group">
        <label for="username">Nom utilisateur</label>
        <input v-model="user.username" type="text" id="username" placeholder="Nom utilisateur" required />
      </div>

      <div class="form-group">
        <label for="company_name">Raison Sociale</label>
        <input v-model="profil.company_name" type="text" id="company_name" />
      </div>

      <div class="form-group">
        <label for="company_number">N° Entreprise</label>
        <input v-model="profil.company_number" type="text" id="company_number" />
      </div>

      <!-- Ligne 2 -->
      <div class="form-group">
        <label for="email">Email</label>
        <input v-model="user.email" type="email" id="email" required />
      </div>

      <div class="form-group">
        <label for="civility">Civilité</label>
        <!-- <input v-model="profil.civility" type="text" id="civility" /> -->
        <select v-model="user.civility" id="civility" required>
          <option>Monsieur</option>
          <option>Madame</option>
          <option>Licone</option>
          <option>Chaise</option>
          <option>Mite en pullover</option>
          <option>Hélicoptère de combat</option>
          <option>Autre</option>
        </select>
      </div>

      <div class="form-group">
        <label for="name_contact">Nom du contact</label>
        <input v-model="profil.name_contact" type="text" id="name_contact" required @input="validateTextOnly"/>
      </div>

      <div class="form-group">
        <label for="address">Adresse</label>
        <input v-model="profil.address" type="text" id="address" />
      </div>

      <!-- Ligne 5 -->
      <!-- <div></div> case vide pour l’alignement -->
      <div class="form-group">
        <label for="postal_code">Code postal</label>
        <input v-model="profil.postal_code" type="text" id="postal_code" required @input="validateNumber" />
      </div>

      <div class="form-group">
        <label for="city">Ville</label>
        <input v-model="profil.city" type="text" id="city" required @input="validateTextOnly"/>
      </div>

      <!-- Ligne 3 -->
      <div class="form-group">
        <label for="password">Mot de passe</label>
        <input v-model="user.password" type="password" id="password" required />
      </div>

      <div class="form-group">
        <label for="surname_contact">Prénom du contact</label>
        <input v-model="profil.surname_contact" type="text" id="surname_contact" required @input="validateTextOnly"/>
      </div>

      <div class="form-group">
        <label for="mobile_phone">Téléphone mobile</label>
        <input v-model="profil.mobile_phone" type="tel" id="mobile_phone" placeholder="Téléphone mobile" required @input="validateNumber"/>
      </div>

      <!-- Ligne 4 -->
      <div class="form-group">
        <label for="role">Type de compte</label>
        <select v-model="user.role" id="role" required>
          <option value="organisateur">Organisateur</option>
          <option value="association">Association</option>
          <option value="etudiant">Étudiant</option>
          <option value="autre">Autre</option>
        </select>
      </div>

      <div class="form-group">
        <label for="landline_phone">Téléphone fixe</label>
        <input v-model="profil.landline_phone" type="tel" id="landline_phone" placeholder="Téléphone fixe" required @input="validateNumber"/>
      </div>

      <!-- Boutons -->
      <div class="form-buttons">
        <button type="submit" class="btn-primary">Sign up</button>
        <button @click="goback" type="button" class="btn-secondary">Back</button>
      </div>
      </form>

      <p class="terms">
              By signing up, you agree to Photo's <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a>.
            </p>

              <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
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
        this.$router.push('/login'); // Redirige après succès
      } catch (error) {
        this.errorMessage = "Erreur d'inscription. Vérifiez vos informations.";
      }
    },
    goback(){
      this.router.push('/firstPage'); // Redirige vers la page d'accueil
    }
  },
};

</script>

<style scoped>
 @import "@/assets/styles/Register.css";
</style>