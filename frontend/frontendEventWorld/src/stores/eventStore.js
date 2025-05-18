import { defineStore } from 'pinia';
import { fetchEvents, createEvent, updateEvent, deleteEvent, generateInvitation, fetchInvitationById, createEventWithTempUsers } from "@/utils/api_utils";
import { getEventImageUrl } from '@/utils/imageEvent';

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
      //console.log("store setSelectedEvent ", event);
      this.selectedEvent = event;
    },
    resetEvents() {
      this.events = [];
      this.loading = false;
      this.error = null;
    },

    async fetchEvents() {
      try {
        this.loading = true;
        this.events = []; // Nettoyage avant rechargement
    
        const data = await fetchEvents();
    
        // Transformez price_categories en tableau pour chaque événement
        this.events = data.map(event => {
          if (event.price_categories && typeof event.price_categories === 'object' && !Array.isArray(event.price_categories)) {
            event.price_categories = Object.entries(event.price_categories).map(([label, value]) => ({
              label,
              value,
            }));
          }
          event.image= event.picture;

          return event;
        });
      } catch (err) {
        this.error = "Échec de la récupération des événements.";
      } finally {
        this.loading = false;
      }
    },
    
    async createEvent(eventData) {
      try {
        this.loading = true;
    
        // Créer l'événement via l'API
        const createdEvent = await createEvent(eventData);
    
        // Option 1 : Si l'API retourne directement l'invitation associée,
        // par exemple via une propriété "invitation_id", vous pouvez utiliser :
        if (createdEvent.invitation_id) {
          const invitation = await fetchInvitationById(createdEvent.invitation_id);
          this.invitationLink = `${window.location.origin}/invitation/${invitation.id}`;
        } else {
        }
    
        // Rafraîchir la liste des événements
        await this.fetchEvents();
        console.log("fetchEvents :", fetchEvents);
      } catch (err) {
        this.error = "Erreur lors de la création de l'événement.";
        throw err;
      } finally {
        this.loading = false;
      }
    },

    async updateEvent(eventId, updatedData) {
      try {
        //console.log("createEvent eventStore.js : ", eventData);
        this.loading = true;
        await updateEvent(eventId, updatedData);
        await this.fetchEvents(); // Rafraîchit la liste après modification
      } catch (err) {
        this.error = "Erreur lors de la modification de l'événement.";
        throw err;
      } finally {
        this.loading = false;
      }
    },
    

    async deleteEvent(Id) {
      try {
          this.loading = true;
  
          // Stocker temporairement l'événement supprimé
          const eventIndex = this.events.findIndex(event => event.id === Id);
          const deletedEvent = this.events[eventIndex];
  
          // Suppression optimiste
          this.events.splice(eventIndex, 1);
  
          // Appel API pour suppression réelle
          await deleteEvent(Id);
          
      } catch (err) {
          this.error = "Impossible de supprimer l'événement.";
  
          // Restaurer l'événement en cas d'échec
          if (deleteEvent) {
              this.events.splice(eventIndex, 0, deleteEvent);
          }
  
          console.error("Erreur de suppression :", err);
      } finally {
          this.loading = false;
      }
    },
    async generateInvitation(eventId, email = null) {
      try {
        this.loading = true;
        // Appel à l'API sécurisée pour générer une invitation.
        const invitation = await generateInvitation(eventId, email);
        return invitation;
      } catch (err) {
        this.error = "Erreur lors de la génération de l'invitation.";
        throw err;
      } finally {
        this.loading = false;
      }
    },

    // ⚡️ Nouvelle action dédiée uniquement à la création avec utilisateurs temporaires
    async createEventWithTemporaryUsers(payload) {
        try {
      this.loading = true;
      this.error = null;

      const response = await createEventWithTempUsers(payload);

      // Stockage réactif
      this.temporaryUsers = response.temporary_users;
      this.invitationLinks = response.temporary_users.map(user => ({
        alias: user.alias,
        scan_link: user.scan_link,
        sell_link: user.sell_link,
      }));

      // Actualise la liste complète
        await this.fetchEvents();
      } catch (err) {
        this.error = err.response?.data || "Erreur lors de la création d'événement avec utilisateurs temporaires.";
        throw err;
      } finally {
        this.loading = false;
      }
    },
  },
});
