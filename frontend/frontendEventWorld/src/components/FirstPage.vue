<template>
    <div class="fond">
    <div class="first-page-container">
        <img src="@/assets/styles/Logo.png" alt="Event World Logo" class="logo" />
        <div class="button-group">
            <button @click="goToLogin" class="btn-primary">Log In</button>
            <button @click="goToRegister" class="btn-secondary">Register</button>
        </div>
        <footer class="footer"><a class="footer-title" href="">By Tom</a></footer>
    </div>    
    </div>
  </template>
  
  <script>
  export default {
    name: 'FirstPage',
    methods: {
      goToLogin() {
        this.$router.push('/login'); // Redirige vers la page de connexion
      },
      goToRegister() {
        this.$router.push('/register'); // Redirige vers la page d'inscription
      },
    },
  };
  </script>
  
  <style scoped>

@import '@/assets/styles/FirstPage.css';

  </style>