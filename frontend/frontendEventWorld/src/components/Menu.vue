<template>
    <div class="main-container bg-pan-left">
      
      <!-- Bouton central -->
      <div class="central-circle" @click="toggleMenu">
        <i class="icon-main" :class="{ rotate: menuOpen }">☰</i>
      </div>
  
      <!-- Menu circulaire -->
      <div class="circle-menu" :class="{ show: menuOpen }" @click="toggleMenu">

        <div
          v-for="(item, index) in menuItems"
          :key="index"
          class="menu-item"
          :class="`pos-${index + 1}`"
          @click.stop="item.action"
        >
          <div class="icon-text-container">
            <font-awesome-icon :icon="item.icon" class="menu-icon" />
            <p class="menu-label">{{ item.label }}</p>
          </div>
        </div>
      </div>

      <!-- Overlay pour fermer EventCard -->
      <div v-if="showEventCard" class="overlay" @click="closeEventCard">
        <div class="event-card-container" @click.stop>
          <EventCard />
        </div>
      </div>

      <!-- Overlay pour fermer CreateEvent -->
      <div v-if="showCreateEvent" class="overlay" @click="closeCreateEvent">
        <div class="event-card-container" @click.stop>
          <CreateEvent />
        </div>
      </div>
 

    <!-- Overlay pour fermer QrCodeScanner -->
    <div v-if="showQrCodeScanner" class="overlay" @click="closeQrCodeScanner">
        <div class="event-card-container" @click.stop>
          <QrCodeScanner />
        </div>
      </div>
    </div>
  </template>
    

  <script setup>
  import { computed, ref } from 'vue';
  import EventCard from '@/components/EventCard.vue';
  import CreateEvent from '@/components/CreateEvent.vue';
  import { useAuthStore } from '@/stores/authStore';
  import { useRouter } from 'vue-router';
  import QrCodeScanner from '@/components/QrCodeScanner.vue';
  import { useEventStore } from '@/stores/eventStore';


  const authStore = useAuthStore();
  const router = useRouter();
  const eventStore = useEventStore();


  // État pour ouvrir/fermer le menu
  const menuOpen = ref(false);
  
  // Etat pour afficher le lecteur de QrCode
  const showQrCodeScanner = ref(false);


  // Fonction pour fermer EventCard
  const closeQrCodeScanner = () => {
    showQrCodeScanner.value = false;
  };


  // État pour afficher EventCard
  const showEventCard = ref(false);
  

  // État pour afficher CreateEvent
  const showCreateEvent = ref(false);
  
  // Fonction pour basculer le menu
  const toggleMenu = () => {
    menuOpen.value = !menuOpen.value; // Inverse l'état (ouvert/fermé)
  };
  
  // Fonction pour fermer EventCard
  const closeEventCard = () => {
    showEventCard.value = false;
  };
  
  // Fonction pour fermer EventCard
  const closeCreateEvent = () => {
    showCreateEvent.value = false;
  };
  

  // const isNotStudent = authStore.isNotStudent;

  const isNotStudent = computed(() => authStore.user?.role !== 'etudiant');


  // Items du menu
  // ✅ Liste complète
const allMenuItems = [
  {
    label: 'Nouveau',
    icon: 'fas fa-calendar-plus',
    action: () => showCreateEvent.value = true,
  },
  {
    label: 'Scanner',
    icon: 'fas fa-qrcode',
    action: () => showQrCodeScanner.value = true,
    show: isNotStudent,
  },
  {
  label: 'Évènements',
  icon: 'fas fa-calendar',
  action: async () => {
    eventStore.resetEvents();       // 👌 fonctionne maintenant
    await eventStore.fetchEvents(); // 🔁 charge les bons events
    showEventCard.value = true;     // 👁️ affiche
  },
},

  {
    label: 'Déconnexion',
    icon: 'fas fa-sign-out-alt',
    action: () => handleLogout(),
  },
];

const menuItems = computed(() =>
  allMenuItems.filter(item => item.show === undefined || item.show.value)
);



// Fonction pour gérer la déconnexion
const handleLogout = () => {
  authStore.logoutUser(router); // Passe l'instance du routeur au store
};
  </script>
  

<style scoped>

@import '@/assets/styles/Menu.css'
</style>
