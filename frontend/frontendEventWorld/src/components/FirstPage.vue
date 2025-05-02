<template>
    <div class="fond">
    <div class="first-page-container">
        <img src="@/assets/styles/Logo.png" alt="Event World Logo" class="logo" />
        <!-- <h1 class="title">Event World</h1>
        <p class="subtitle">Pour un monde ensemble</p> -->
        <div class="button-group">
            <button @click="goToLogin" class="btn-primary">Log In</button>
            <button @click="goToRegister" class="btn-secondary">Register</button>
        </div>
        <footer class="footer">By Tom</footer>
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


  /* Styles de base */
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

/* Styles de base pour le conteneur */
.first-page-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 90%; /* Ajuste la largeur pour les petits écrans */
  max-width: 400px; /* Limite la largeur maximale */
  padding: 20px;
  background: linear-gradient(180deg, #0056b3, #d6e4ff);
  border-radius: 10px; /* Coins arrondis */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Ajoute une ombre légère */
  text-align: center;
}
  
  .logo {
    align-self: start;
    width: 70%;
    height: auto;
    margin-bottom: 20px;
  }
  
  .title {
    font-size: 28px;
    font-weight: bold;
    color: #333;
    margin-bottom: 10px;
  }
  
  .subtitle {
    font-size: 16px;
    color: #666;
    margin-bottom: 30px;
  }
  
  .button-group {
    display: flex;
    flex-direction: column;
    gap: 15px;
    width: 100%;
  }
  
  button {
    width: 100%;
    padding: 12px;
    font-size: 16px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .btn-primary {
    background-color: #007bff;
    color: #fff;
  }
  
  .btn-primary:hover {
    background-color: #0056b3;
  }
  
  .btn-secondary {
    background-color: #000;
    color: #fff;
  }
  
  .btn-secondary:hover {
    background-color: #333;
  }
  
  .footer {
    margin-top: 20px;
    font-size: 12px;
    color: #615f5f;
  }
  
  /* Media queries */
  @media (max-width: 768px) {
    .first-page-container {
      background: linear-gradient(180deg, #0056b3, #d6e4ff);
    }
    .logo {
      width: 70%;
    }
  
    .title {
      font-size: 24px;
    }
  
    .subtitle {
      font-size: 14px;
    }
  
    button {
      font-size: 14px;
      padding: 10px;
    }

    .footer {
      font-size: 16px;
      color: #000;
  }
  }
  
  @media (max-width: 480px) {
    .first-page-container {
        background: linear-gradient(180deg, #0056b3, #d6e4ff);
  }
    .logo {
      width: 70%;
    }
  
    .title {
      font-size: 20px;
    }
  
    .subtitle {
      font-size: 12px;
    }
  
    button {
      font-size: 16px;
      padding: 8px;
      width: 100%;
      height: 6vh;
    }

    .footer {
      font-size: 16px;
      color: #000;
  }
  }
  </style>