<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-indigo-100 flex flex-col">
    <!-- Barre de navigation -->
    <header class="bg-gradient-to-r from-indigo-600 to-purple-700 text-white shadow-lg">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between py-4">
          <div class="flex items-center gap-3">
            <img src="@/assets/styles/pictures/Logo.png" alt="Event World Logo" class="w-10 h-10 sm:w-11 sm:h-11 md:w-12 md:h-12">
            <h1 class="text-lg sm:text-xl md:text-2xl font-bold tracking-wide">EventWorld</h1>
          </div>

          <nav class="hidden md:flex items-center gap-2">
            <button
              class="px-3 py-2 rounded-lg hover:bg-purple-600 transition-colors duration-200"
              @click="goToMenu"
            >
              Accueil
            </button>
            <button
              class="px-3 py-2 rounded-lg hover:bg-purple-600 transition-colors duration-200"
              @click="goToCreat"
            >
              Nouvel événement
            </button>
            <button
              class="px-3 py-2 rounded-lg hover:bg-purple-600 transition-colors duration-200"
              @click="goToScan"
            >
              Scanner
            </button>
          </nav>

          <div class="flex items-center gap-2">
            <div class="relative">
              <button
                @click="toggleProfileMenu"
                class="cursor-pointer focus:outline-none focus:ring-2 focus:ring-purple-300 rounded-md p-2 hover:bg-purple-600 transition-colors duration-200"
              >
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
              </button>
              <div
                class="absolute top-12 right-0 w-48 md:w-64 bg-purple-300 text-gray-800 shadow-lg rounded-b-lg overflow-hidden transition-all duration-300 ease-in-out z-50 mt-1"
                :class="{ 'opacity-100 visible': profileMenuOpen, 'opacity-0 invisible': !profileMenuOpen }"
              >
                <a
                  class="cursor-pointer block px-4 py-3 hover:bg-purple-500 transition-colors duration-200"
                  @click="goToProfile"
                >
                  Mon Profil
                </a>
                <a
                  class="cursor-pointer block px-4 py-3 hover:bg-purple-500 transition-colors duration-200"
                  @click="goToSettings"
                >
                  Paramètres
                </a>
                <a
                  class="cursor-pointer block px-4 py-3 hover:bg-purple-500 transition-colors duration-200"
                  @click="goToHelp"
                >
                  Aide
                </a>
                <a
                  class="cursor-pointer block px-4 py-3 hover:bg-red-100 text-red-600 hover:text-red-700 transition-colors duration-200"
                  @click="handleLogout"
                >
                  Déconnexion
                </a>
              </div>
            </div>
            <button
              @click="toggleMenu"
              class="md:hidden cursor-pointer focus:outline-none focus:ring-2 focus:ring-purple-300 rounded-md p-2 hover:bg-purple-600 transition-colors duration-200"
            >
              <div class="w-6 h-0.5 bg-white mb-1 transition-transform duration-300" :class="{ 'rotate-45 translate-y-1.5': menuOpen }"></div>
              <div class="w-6 h-0.5 bg-white mb-1 transition-opacity duration-300" :class="{ 'opacity-0': menuOpen }"></div>
              <div class="w-6 h-0.5 bg-white transition-transform duration-300" :class="{ '-rotate-45 -translate-y-1.5': menuOpen }"></div>
            </button>
          </div>
        </div>
      </div>

      <div
        class="md:hidden bg-purple-300 text-gray-800 shadow-lg transition-all duration-300 ease-in-out"
        :class="{ 'max-h-96 opacity-100': menuOpen, 'max-h-0 opacity-0 overflow-hidden': !menuOpen }"
      >
        <div class="px-4 py-2 space-y-1">
          <button class="w-full text-left px-4 py-3 rounded-md hover:bg-purple-500" @click="goToMenu">
            Accueil
          </button>
          <button class="w-full text-left px-4 py-3 rounded-md hover:bg-purple-500" @click="goToCreat">
            Nouvel événement
          </button>
          <button class="w-full text-left px-4 py-3 rounded-md hover:bg-purple-500" @click="goToScan">
            Scanner
          </button>
        </div>
      </div>
    </header>

    <!-- Contenu principal -->
    <main class="flex-1 p-4 md:p-6">
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
    const profileMenuOpen = ref(false);
    const router = useRouter();
    const authStore = useAuthStore();

    const closeMenus = () => {
      menuOpen.value = false;
      profileMenuOpen.value = false;
    };

    const toggleMenu = () => {
      menuOpen.value = !menuOpen.value;
      profileMenuOpen.value = false; // Fermer l'autre menu
    };

    const toggleProfileMenu = () => {
      profileMenuOpen.value = !profileMenuOpen.value;
      menuOpen.value = false; // Fermer l'autre menu
    };

    const goToMenu = () => {
      closeMenus();
      router.push({ name: 'menu' });
    };
    const goToCreat = () => {
      closeMenus();
      router.push({ name: 'CreateEvent' });
    };

    const goToScan = () => {
      closeMenus();
      router.push({ name: 'QrCodeScanner' });
    };

    const goToProfile = () => {
      closeMenus();
      router.push({ name: 'Profile' });
    };

    const goToSettings = () => {
      closeMenus();
      router.push({ name: 'Settings' });
    };

    const goToHelp = () => {
      closeMenus();
      router.push({ name: 'Help' });
    };

    const handleLogout = () => {
      closeMenus();
      authStore.logoutUser(router);
      router.push({ name: 'login' });
    };

    return {
      menuOpen,
      profileMenuOpen,
      closeMenus,
      toggleMenu,
      toggleProfileMenu,
      goToMenu,
      goToCreat,
      goToScan,
      goToProfile,
      goToSettings,
      goToHelp,
      handleLogout,
    };
  },
};
</script>
