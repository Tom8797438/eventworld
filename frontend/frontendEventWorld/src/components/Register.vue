<template>
  <div class="register-container">
        <h1 class="title">Inscription</h1>
        <form @submit.prevent="handleRegister" class="form-grid">

<!-- Titre au-dessus des colonnes 2 et 3 -->
<h2 class="section-title">Informations Entreprise</h2>

<!-- Ligne 1 -->
<div class="form-group">
  <label for="username">Nom d'utilisateur</label>
  <input v-model="user.username" type="text" id="username" required />
</div>

<div class="form-group">
  <label for="company_name">Nom de l'entreprise</label>
  <input v-model="profil.company_name" type="text" id="company_name" />
</div>

<div class="form-group">
  <label for="company_number">Numéro de l'entreprise</label>
  <input v-model="profil.company_number" type="text" id="company_number" />
</div>

<!-- Ligne 2 -->
<div class="form-group">
  <label for="email">Email</label>
  <input v-model="user.email" type="email" id="email" required />
</div>

<div class="form-group">
  <label for="civility">Civilité</label>
  <input v-model="profil.civility" type="text" id="civility" />
</div>

<div class="form-group">
  <label for="name_contact">Nom du contact</label>
  <input v-model="profil.name_contact" type="text" id="name_contact" />
</div>

<!-- Ligne 3 -->
<div class="form-group">
  <label for="password">Mot de passe</label>
  <input v-model="user.password" type="password" id="password" required />
</div>

<div class="form-group">
  <label for="surname_contact">Prénom du contact</label>
  <input v-model="profil.surname_contact" type="text" id="surname_contact" />
</div>

<div class="form-group">
  <label for="mobile_phone">Téléphone mobile</label>
  <input v-model="profil.mobile_phone" type="text" id="mobile_phone" />
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
  <input v-model="profil.landline_phone" type="text" id="landline_phone" />
</div>

<div class="form-group">
  <label for="address">Adresse</label>
  <input v-model="profil.address" type="text" id="address" />
</div>

<!-- Ligne 5 -->
<div></div> <!-- case vide pour l’alignement -->
<div class="form-group">
  <label for="postal_code">Code postal</label>
  <input v-model="profil.postal_code" type="text" id="postal_code" />
</div>

<div class="form-group">
  <label for="city">Ville</label>
  <input v-model="profil.city" type="text" id="city" />
</div>

<!-- Boutons -->
<div class="form-buttons">
  <button type="submit">S'inscrire</button>
  <button @click="goback" type="button">Retour</button>
</div>
</form>



        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import { registerUser } from '@/services/authService';
import { useRouter } from 'vue-router';

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
  setup() {
    const router = useRouter();
    return { router };
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
      this.router.push('/login');
    }
  },
};

</script>

<style scoped>
@import '@/assets/styles/Authentification.css';
.register-container{
  background: linear-gradient(135deg, #6f45e285, #88d3ceab);
  border-radius: 18px;
  padding: 1rem;
  margin: 0 auto;
  border: none;
  box-shadow: none;
  /* display:block; Éviter un comportement inline par défaut */
  max-width: 1000px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.title{
  color:white;
}

.section-title {
  grid-column: 2 / 4;
  font-size: 1.5rem;
  color: white;
  margin-bottom: 1rem;
  display: none;
  
}

.form-group {
  display: flex;
  flex-direction: column;
  color: white;
}

input,
select {
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.form-buttons {
  grid-column: 1 / 4;
  display: flex;
  justify-content: flex-start;
  gap: 1rem;
  margin-top: 2rem;
}


</style>
