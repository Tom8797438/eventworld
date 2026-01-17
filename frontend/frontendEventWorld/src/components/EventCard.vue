<template>
  <div class="space-y-6 p-6">
    <!-- Chargement en cours -->
    <div v-if="loading" class="text-center text-gray-500 text-lg">Loading...</div>

    <!-- Message d'erreur -->
    <div v-if="error" class="text-center text-red-500 text-lg">{{ error }}</div>

    <!-- Liste des événements -->
    <div v-if="events.length" class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="event in events"
        :key="event.id"
        class="bg-white border border-purple-200 rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow duration-300 cursor-pointer"
        @click="goToEventDetails(event)"
      >
        <h3 class="text-xl font-bold text-purple-800 mb-4">{{ event.name || 'Nom non spécifié' }}</h3>
        <div class="space-y-2 text-sm text-gray-700">
          <p><strong>Date :</strong> {{ event.date_start || 'Non spécifiée' }}</p>
          <p><strong>Description :</strong> {{ event.description || 'Non spécifiée' }}</p>
          <p><strong>Lieu :</strong> {{ event.location || 'Non spécifié' }}</p>
          <p><strong>Ville :</strong> {{ event.city || 'Non spécifiée' }}</p>
          <p><strong>Places restantes :</strong> {{ event.number_place || 'Non spécifiées' }}</p>
        </div>
        <div class="mt-4 flex justify-end">
        <button
          v-if="showDelete"
          class="w-full md:w-auto bg-red-600 text-white py-2 px-4 rounded-lg hover:bg-red-700 transition-colors duration-200"
          @click.stop="deleteEventHandler(event)"
        >
          Supprimer
        </button>
        </div>
      </div>
    </div>

    <!-- Aucun événement -->
    <div v-if="!loading && events.length === 0" class="text-center text-gray-500 text-lg">
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