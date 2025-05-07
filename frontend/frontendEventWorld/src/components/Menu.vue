<template>
  
    <div class="main-container">
      <!-- Contenu principal -->
      <div class="content">
        <!-- Colonne droite : Tableau de bord -->
        <div class="right-panel">
          <div class="search-bar">
            <input type="text" placeholder="Search event" v-model="searchQuery" />
          </div>
          <h2 class="dashboard-title">Dashboard</h2>
          <div class="dashboard-content">
            <p>Statistiques des événements :</p>
            <ul>
              <li class="event-item">Total des événements : <strong>{{ events.length }}</strong></li>
              <li class="event-item">Événements à venir : <strong>{{ upcomingEvents }}</strong></li>
              <li class="event-item">Événements passés : <strong>{{ pastEvents }}</strong></li>
            </ul>
          </div>
        </div>
        <!-- Colonne gauche : Liste des événements -->
        <div class="left-panel">
        
  
          <div class="event-card-container">
            <!-- Chargement en cours -->
            <div v-if="loading" class="loading">Loading...</div>
  
            <!-- Message d'erreur -->
            <div v-if="error" class="error">{{ error }}</div>
  
            <!-- Liste des événements -->
            <div v-if="filteredEvents.length" class="event-list">
              <div
                v-for="event in filteredEvents"
                :key="event.id"
                class="event-card"
              >

                <!-- Détails de l'événement -->
                <div class="event-details">
                  <h3 class="event-title">{{ event.name || 'Nom non spécifié' }}</h3>
                  <p><strong class="event-item">Date :</strong> {{ event.date_start || 'Non spécifiée' }}</p>
                  <p><strong class="event-item">Description :</strong> {{ truncate(event.description, 50) || 'Non spécifiée' }}</p>
                  <p><strong class="event-item">Lieu :</strong> {{ event.location || 'Non spécifié' }}</p>
                  <p><strong class="event-item">Ville :</strong> {{ event.city || 'Non spécifiée' }}</p>
                  <p><strong class="event-item">Places restantes :</strong> {{ event.number_place || 'Non spécifiées' }}</p>
                </div>
                <!-- Image de l'événement -->
                <img
                  class="event-image"
                  :src="getEventImageUrl(event.picture)"
                  alt="Event Image"
                />
                <button
                  v-if="showDelete"
                  class="btn-delete modificate"
                  @click="goToEventDetails(event)"
                >
                  Modifier
                </button>
                <button
                  v-if="showDelete"
                  class="btn-delete"
                  @click.stop="deleteEventHandler(event)"
                >
                  Supprimer
                </button>
              </div>
            </div>
  
            <!-- Aucun événement -->
            <div v-if="!loading && filteredEvents.length === 0" class="no-events">
              Aucun événement trouvé.
            </div>
          </div>
        </div>
      </div>
    </div>

  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue';
  import { useEventStore } from '@/stores/eventStore';
  import { useRouter } from 'vue-router';
  import { getEventImageUrl } from '@/utils/imageEvent';

  const router = useRouter();
  const eventStore = useEventStore();
  
  const searchQuery = ref('');
  const showDelete = ref(true);
  
  // Fonction pour tronquer le texte
  const truncate = (text, maxLength) => {
    if (!text) return '';
    return text.length > maxLength ? text.slice(0, maxLength) + '…' : text;
  };
  
  
  onMounted(() => {
    eventStore.fetchEvents();
  });
  
  // Liste des événements
  const events = computed(() => eventStore.events);
  const loading = computed(() => eventStore.loading);
  const error = computed(() => eventStore.error);
  
  // Filtrer les événements en fonction de la recherche
  const filteredEvents = computed(() => {
    if (!searchQuery.value) return events.value;
    return events.value.filter((event) =>
      event.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
  });
  
  // Statistiques pour le tableau de bord
  const upcomingEvents = computed(() =>
    events.value.filter((event) => new Date(event.date_start) > new Date()).length
  );
  
  const pastEvents = computed(() =>
    events.value.filter((event) => new Date(event.date_start) <= new Date()).length
  );
  
  // Rediriger vers les détails de l'événement
  const goToEventDetails = (event) => {
    router.push({
      name: 'EventDetails',
      params: { id: event.id },
    });
  }; 
  
  // Supprimer un événement
  const deleteEventHandler = async (event) => {
    if (confirm('Voulez-vous vraiment supprimer cet événement ?')) {
      try {
        await eventStore.deleteEvent(event.id);
      } catch (error) {
        console.error('Erreur lors de la suppression :', error);
      }
    }
  };
  </script>
  
  <style scoped>
  @import '@/assets/styles/Menu.css';
  </style>