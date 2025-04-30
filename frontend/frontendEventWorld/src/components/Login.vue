<template>
  <div class="fond">
    <div class="login-container">
      <h1 class="title">Log in</h1>
      <form @submit.prevent="handleLogin" class="form-container">
        <!-- Identifiant -->
        <div class="form-group">
          <input
            v-model="identifier"
            type="text"
            id="identifier"
            placeholder="Email or Username"
            required
          />
        </div>

        <!-- Mot de passe -->
        <div class="form-group">
          <input
            v-model="password"
            type="password"
            id="password"
            placeholder="Password"
            required
          />
        </div>

        <!-- Boutons -->
        <div class="button-group">
          <button type="submit" class="btn-secondary">Log in</button>
          <button @click="goback" type="button" class="btn-primary">Back</button>
        </div>

        <!-- Lien pour mot de passe oublié -->
        <p class="forgot-password" @click="forgotPassword">Forgotten password</p>
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
      alert('Redirect to password recovery page (to be implemented).');
    },
    goback() {
      this.router.push('/FirstPage'); // Redirige vers la page d'accueil
    },
  },
};
</script>

<style scoped>
/* Fond */
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

/* Conteneur principal */
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 50vh;
  width: 25vw;
  padding: 18px;
  background: linear-gradient(180deg, #f0f4ff, #d6e4ff); /* Dégradé bleu clair */
  text-align: center;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Ombre légère */
}

/* Titre */
.title {
  font-size: 2rem;
  text-transform: uppercase;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}

/* Formulaire */
.form-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
  width: 100%;
  max-width: 400px;
}

.form-group {
  display: flex;
  flex-direction: column;
  text-align: left;
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

/* Boutons */
.button-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.btn-primary {
  padding: 12px;
  font-size: 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background-color: #000;
  color: #fff;
  text-transform: uppercase;
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
  text-transform: uppercase;
}

.btn-secondary:hover {
  background-color: #0056b3;
}

/* Lien pour mot de passe oublié */
.forgot-password {
  margin-top: 10px;
  font-size: 0.9rem;
  color: #007bff;
  cursor: pointer;
}

.forgot-password:hover {
  text-decoration: underline;
}

/* Responsive */
@media (max-width: 768px) {
  .login-container {
    padding: 16px;
    width: 80vw;

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

  .forgot-password {
    font-size: 0.8rem;
  }
}
</style>