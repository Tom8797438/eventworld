import { defineStore } from 'pinia';
import { fetchEvents, createEvent, deleteEvent } from "@/utils/api_utils";

export const useEventStore = defineStore('eventStore', {
  state: () => ({
    events: [],
    eventDetails: {},
    loading: false,
    error: null,
    selectedEvent: null,
  }),
  actions: {
    setSelectedEvent(event) {
      console.log("store setSelectedEvent ", event);
      this.selectedEvent = event;
    },

    async fetchEvents() {
      try {
        this.loading = true;
        const data = await fetchEvents();
        this.events = data;
      } catch (err) {
        this.error = "Échec de la récupération des événements.";
      } finally {
        this.loading = false;
      }
    },

    async createEvent(eventData) {
      try {
        console.log("createEvent eventStore.js : ", eventData);
        this.loading = true;
        await createEvent(eventData);
        await this.fetchEvents(); // Rafraîchit la liste après création
      } catch (err) {
        this.error = "Erreur lors de la création de l'événement.";
        throw err;
      } finally {
        this.loading = false;
      }
    },

    async deleteEvent(Id) {
      try {
          console.log("Suppression de l'événement :", Id);
          this.loading = true;
  
          // Stocker temporairement l'événement supprimé
          const eventIndex = this.events.findIndex(event => event.id === Id);
          const deletedEvent = this.events[eventIndex];
  
          // Suppression optimiste
          this.events.splice(eventIndex, 1);
  
          // Appel API pour suppression réelle
          await deleteEvent(Id);
          
          console.log("Événement supprimé avec succès !");
      } catch (err) {
          this.error = "Impossible de supprimer l'événement.";
  
          // Restaurer l'événement en cas d'échec
          if (deleteEvent) {
              this.events.splice(eventIndex, 0, deletedEvent);
          }
  
          console.error("Erreur de suppression :", err);
      } finally {
          this.loading = false;
      }
    },
  },
});
