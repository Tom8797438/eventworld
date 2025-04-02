import { defineStore } from 'pinia';
import { fetchEvents } from '@/utils/api_utils';

export const usePublicEventStore = defineStore('publicEventStore', {
  state: () => ({
    events: [],
    loading: false,
    error: null,
    selectedEvent: null,
  }),

  actions: {
    async fetchPublicEvents() {
      this.loading = true;
      this.error = null;
      this.events = []; // Nettoie avant le chargement

      try {
        const data = await fetchEvents();
        this.events = data.filter(event => event.type_event === 'public');
      } catch (err) {
        this.error = "Échec de la récupération des événements publics.";
      } finally {
        this.loading = false;
      }
    },
   // ✅ Méthode pour sélectionner un event (appelée dans EventCard.vue)
   setSelectedEvent(event) {
    this.selectedEvent = event;
  }
}
});
