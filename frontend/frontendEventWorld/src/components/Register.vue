<template>
  <div class="register-container">
    <h1 class="title">Inscription</h1>
    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label for="username">Nom d'utilisateur</label>
        <input v-model="user.username" type="text" id="username" required />
      </div>

      <div class="form-group">
        <label for="email">Email</label>
        <input v-model="user.email" type="email" id="email" required />
      </div>

      <div class="form-group">
        <label for="password">Mot de passe</label>
        <input v-model="user.password" type="password" id="password" required />
      </div>

      <div class="form-group">
        <label for="role">Type de compte</label>
        <select v-model="user.role" id="role" required>
          <option value="organisateur">Organisateur</option>
          <option value="association">Association</option>
          <option value="etudiant">Étudiant</option>
          <option value="autre">Autre</option>
        </select>
      </div>

      <hr />

      <h2>Informations Entreprise (facultatif)</h2>

      <div class="form-group">
        <label for="company_name">Nom de l'entreprise</label>
        <input v-model="profil.company_name" type="text" id="company_name" />
      </div>

      <div class="form-group">
        <label for="company_number">Numéro de l'entreprise</label>
        <input v-model="profil.company_number" type="text" id="company_number" />
      </div>

      <div class="form-group">
        <label for="email">Email</label>
        <input v-model="profil.email" type="email" id="email" required />
      </div>

      <div class="form-group">
        <label for="civility">Civilité</label>
        <input v-model="profil.civility" type="text" id="civility" required />
      </div>

      <div class="form-group">
        <label for="name_contact">Nom du contact</label>
        <input v-model="profil.name_contact" type="text" id="name_contact" required />
      </div>

      <div class="form-group">
        <label for="surname_contact">Prénom du contact</label>
        <input v-model="profil.surname_contact" type="text" id="surname_contact" required />
      </div>

      <div class="form-group">
        <label for="mobile_phone">Téléphone mobile</label>
        <input v-model="profil.mobile_phone" type="text" id="mobile_phone" />
      </div>

      <div class="form-group">
        <label for="landline_phone">Téléphone fixe</label>
        <input v-model="profil.landline_phone" type="text" id="landline_phone" />
      </div>

      <div class="form-group">
        <label for="address">Adresse</label>
        <input v-model="profil.address" type="text" id="address" />
      </div>

      <div class="form-group">
        <label for="postal_code">postal_code</label>
        <input v-model="profil.postal_code" type="text" id="postal_code" />
      </div>

      <div class="form-group">
        <label for="city">Ville</label>
        <input v-model="profil.city" type="text" id="city" />
      </div>

      <button type="submit">S'inscrire</button>
    </form>

    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import { registerUser } from '@/services/authService';

export default {
  name: 'Register',
  data() {
    return {
      user: {
        username: '',
        email: '',
        password: '',
        role: 'organisateur',
      },
      profil: {
        company_name: '',
        company_number: '',
        name_contact: '',
        surname_contact: '',
        mobile_phone: '',
        address: '',
        city: '',
      },
      errorMessage: null,
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
  },
};
</script>

<style scoped>
/* @import '@/assets/styles/Authentification.css'; */
</style>
