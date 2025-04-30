<template>
  <div class="event-card-container">
    <!-- Chargement en cours -->
    <div v-if="loading" class="loading">Loading...</div>

    <!-- Message d'erreur -->
    <div v-if="error" class="error">{{ error }}</div>

    <!-- Liste des événements -->
    <div v-if="events.length" class="event-list">
      <div
        v-for="event in events"
        :key="event.id"
        class="event-card"
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
/* Conteneur principal */
.event-card-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
  width: 100vw;
}

/* Liste des événements */
.event-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

/* Carte d'événement */
.event-card {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 15px;
  cursor: pointer;
  transition: box-shadow 0.3s ease;
}

.event-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Titre de l'événement */
.event-title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 10px;
}

/* Bouton de suppression */
.btn-delete {
  margin-top: 10px;
  padding: 5px 10px;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.btn-delete:hover {
  background: #a71d2a;
}

/* Chargement */
.loading {
  text-align: center;
  font-size: 1rem;
  color: #666;
}

/* Message d'erreur */
.error {
  text-align: center;
  font-size: 1rem;
  color: red;
}

/* Aucun événement */
.no-events {
  text-align: center;
  font-size: 1rem;
  color: #666;
}
</style>