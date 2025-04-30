import { defineStore } from 'pinia';
import { fetchEvents, createEvent, updateEvent, deleteEvent, generateInvitation, fetchInvitationById } from "@/utils/api_utils";

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

    // async fetchEvents(publicOnly = false) {
    //   try {
    //     this.loading = true;
    //      // Vide les événements précédents avant un nouveau chargement
    //     this.events = [];

    //     const data = await fetchEvents();
    //     // this.events = data;
    //     // 💡 Filtrage selon le mode
    //     this.events = publicOnly
    //     ? data.filter(event => event.type_event === 'public')
    //     : data;
    //   } catch (err) {
    //     this.error = "Échec de la récupération des événements.";
    //   } finally {
    //     this.loading = false;
    //   }
    // },

    async fetchEvents() {
      try {
        this.loading = true;
        this.events = []; // Nettoyage avant rechargement
    
        const data = await fetchEvents();
        this.events = data; // Ne filtre plus, car c’est pour un utilisateur connecté
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
  },
});
