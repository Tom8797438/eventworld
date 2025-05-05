<template>
    <div class="base-layout">
      <!-- Barre de navigation -->
      <header class="navbar">
        <div class="navbar-left">
          <!-- <img src="@/assets/styles/logo.png" alt="Logo" class="logo" @click="toggleMenu" /> -->
          <div class="menu-icon" @click="toggleMenu">
          <div></div><!-- Barre centrale -->
          </div>
          <h1 class="app-title">EventWorld</h1>
        </div>
  
        <!-- Menu déroulant -->
        <div class="dropdown-menu" :class="{ open: menuOpen }">
          <a class="sutitle-menu" @click="goToMenu">Accueil</a>
          <a class="sutitle-menu" @click="goToCreat">Nouvel événement</a>
          <a class="sutitle-menu" @click="goToScan">Scanner</a>
          <a class="sutitle-menu" @click="handleLogout">Déconnexion</a>
        </div>
  
        <div class="navbar-right">
          <img src="@/assets/styles/profile.png" alt="Profile" class="profile-picture" />
        </div>
      </header>
  
      <!-- Contenu principal -->
      <main class="content">
        <slot /> <!-- Contenu des pages enfants -->
      </main>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import { useAuthStore } from '@/stores/authStore';
  
  export default {
    name: 'BaseLayout',
    setup() {
      const menuOpen = ref(false);
      const router = useRouter();
      const authStore = useAuthStore();
  
      const toggleMenu = () => {
        menuOpen.value = !menuOpen.value;
      };
  
      const goToMenu = () => {
        toggleMenu();
        router.push({ name: 'menu' });
      };
      const goToCreat = () => {
        toggleMenu();
        router.push({ name: 'CreateEvent' });
      };
  
      const goToScan = () => {
        toggleMenu();
        router.push({ name: 'QrCodeScanner' });
      };
  
      const handleLogout = () => {
        toggleMenu();
        authStore.logoutUser(router);
        router.push({ name: 'login' });
      };
  
      return {
        menuOpen,
        toggleMenu,
        goToMenu,
        goToCreat,
        goToScan,
        handleLogout,
      };
    },
  };
  </script>
  
  <style scoped>
 @import '@/assets/styles/LayoutBase.css';
  </style>