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
        <input v-model="profil.name_contact" type="text" id="name_contact" />
      </div>

      <div class="form-group">
        <label for="address">Adresse</label>
        <input v-model="profil.address" type="text" id="address" />
      </div>

      <!-- Ligne 5 -->
      <!-- <div></div> case vide pour l’alignement -->
      <div class="form-group">
        <label for="postal_code">Code postal</label>
        <input v-model="profil.postal_code" type="text" id="postal_code" />
      </div>

      <div class="form-group">
        <label for="city">Ville</label>
        <input v-model="profil.city" type="text" id="city" />
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
        <input v-model="profil.mobile_phone" type="tel" id="mobile_phone" placeholder="Téléphone mobile"/>
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
        <input v-model="profil.landline_phone" type="tel" id="landline_phone" placeholder="Téléphone fixe"/>
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
      this.router.push('/firstPage'); // Redirige vers la page d'accueil
    }
  },
};

</script>

<style scoped>
  .fond {
    background-image: linear-gradient(rgba(255, 255, 255, 0.4), rgba(255, 255, 255, 0.2)), url('@/assets/styles/fond.png'); 
    background-size: cover; /* L'image couvre tout l'écran */
    background-position: center; /* Centre l'image */
    background-repeat: no-repeat; 
    width: 100vw; 
    height: 100vh;
    display: flex; /* Permet de centrer le contenu */
    justify-content: center;
    align-items: center;
}

.container-logo{
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

/* Conteneur principal @import '@/assets/styles/Authentification.css'; */
.register-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 40%;
  max-height: 98%;
  padding: 22px;
  background: linear-gradient(180deg, #f0f4ff, #d6e4ff); /* Dégradé bleu clair */
  text-align: center;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Ombre légère */
}

/* Bouton retour */
.back-button {
  align-self: flex-start;
  margin-bottom: 10px;
  font-size: 1.5rem;
  background: none;
  border: none;
  cursor: pointer;
  transition: scale(1);
  transition: transform 0.3s ease; 
}

.back-button:hover {
  transform: scale(1.2);
}

/* Titre */
.title {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;

}

/* Logo */
.logo {
  width: 100px;
  height: auto;
  margin-bottom: 20px;
}

/* Formulaire */
.form-container {
  display: grid;
  grid-template-columns: 1fr;
  gap: 15px;
  width: 100%;
}

.form-group {
  display: flex;
  flex-direction: column;
  text-align: left;
  width: 100%;
}

label {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 5px;
}

input {
  padding: 12px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 100%;
  box-sizing: border-box;
}

input::placeholder {
  color: #aaa;
}

/* Bouton d'inscription */
.btn-primary {
  padding: 12px;
  font-size: 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background-color: #000;
  color: #fff;
  /* text-transform: uppercase; */
}

.btn-primary:hover {
  background-color: #333;
}

/* Politique de confidentialité */
.terms {
  margin-top: 10px;
  font-size: 0.8rem;
  color: #666;
}

.terms a {
  color: #007bff;
  text-decoration: none;
}

.terms a:hover {
  text-decoration: underline;
}

/* Responsive */
@media (min-width: 768px) {
  .form-container {
    grid-template-columns: 1fr 1fr; /* 2 colonnes sur desktop */
  }
}

.form-group {
  display: flex;
  flex-direction: column;
  text-align: left;
}

label {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 5px;
}

input,
select {
  padding: 12px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 100%;
  box-sizing: border-box;
}

input::placeholder {
  color: #aaa;
}

/* Boutons */
.form-buttons {
  grid-column: span 2; /* Les boutons occupent toute la largeur sur desktop */
  display: flex;
  gap: 10px;
  justify-content: center;
}

.btn-primary {
  padding: 12px;
  font-size: 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background-color: #000;
  color: #fff;
}

.btn-primary:hover {
  background-color: #333;
}

.btn-secondary {
  padding: 12px;
  font-size: 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background-color: #007bff;
  color: #fff;
}

.btn-secondary:hover {
  background-color: #0056b3;
}

/* Politique de confidentialité */
.terms {
  margin-top: 10px;
  font-size: 0.8rem;
  color: #666;
}

.terms a {
  color: #007bff;
  text-decoration: none;
}

.terms a:hover {
  text-decoration: underline;
}

/* Responsive */
@media (max-width: 768px) {
  .register-container {
    padding: 15px;
    max-width: 95%;
  }

  .title {
    font-size: 1.5rem;
  }

  input {
    font-size: 0.9rem;
    padding: 10px;
  }

  .btn-primary,
  .btn-secondary {
    font-size: 0.9rem;
    padding: 10px;
  }

  .terms {
    font-size: 0.7rem;
  }
}
</style>