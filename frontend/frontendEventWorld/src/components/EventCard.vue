<template>
  <div class="event-card-container">
    <!-- Chargement en cours -->
    <div v-if="loading" class="loading">Loading...</div>

    <!-- Message d'erreur -->
    <div v-if="error" class="error">{{ error }}</div>

    <!-- Liste des événements -->
    <div v-if="events.length" class="event-list">
      <div class="event-card"
        v-for="event in events"
        :key="event.id"
        
        @click="goToEventDetails(event)"
      >
        <h3 class="event-title">{{ event.name || 'Nom non spécifié' }}</h3>
        <p><strong>Date :</strong> {{ event.date_start || 'Non spécifiée' }}</p>
        <p><strong>Description :</strong> {{ event.description || 'Non spécifiée' }}</p>
        <p><strong>Lieu :</strong> {{ event.location || 'Non spécifié' }}</p>
        <p><strong>Ville :</strong> {{ event.city || 'Non spécifiée' }}</p>
        <p><strong>Places restantes :</strong> {{ event.number_place || 'Non spécifiées' }}</p>
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
    <div v-if="!loading && events.length === 0" class="no-events">
      Aucun événement trouvé.
    </div>
  </div>
</template>
  
  <script>
  import { useEventStore } from '@/stores/eventStore';
  import { mapState, mapActions } from 'pinia';
  
  export default {
  name: 'EventCard',
  props: {
    showDelete: {
      type: Boolean,
      default: true,
    },
  },
  computed: {
    ...mapState(useEventStore, ['events', 'loading', 'error']),
  },
  methods: {
    ...mapActions(useEventStore, ['fetchEvents', 'deleteEvent']),

    async deleteEventHandler(event) {
      if (confirm('Voulez-vous vraiment supprimer cet événement ?')) {
        try {
          await this.deleteEvent(event.id);
        } catch (error) {
          console.error('Erreur lors de la suppression :', error);
        }
      }
    },

    goToEventDetails(event) {
      console.log('Événement sélectionné :', event);
      this.$router.push({
        name: 'EventDetails',
        params: { id: event.id },
      });
    },
  },
};
  </script> 
  
  <style scoped>
@import '@/assets/styles/EventCard.css';
</style>