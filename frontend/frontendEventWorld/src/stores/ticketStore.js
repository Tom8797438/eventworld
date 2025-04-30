import { defineStore } from 'pinia';
import { generateTicketPdf } from '@/utils/generateTicketPdf';
import { purchaseTickets } from "@/utils/api_utils";

export const useTicketStore = defineStore('ticketStore', {
  state: () => ({
    tickets: [], // Stockage local des tickets créés
  }),

  actions: {
    async createTickets(eventId, ticketData) {
      try {
        
        const createdTickets = await purchaseTickets(eventId, ticketData);
        // Générer les PDFs des billets
        for (const ticket of createdTickets.created_tickets) {
          await generateTicketPdf(ticket);
        }

        // Mise à jour du state
        this.tickets = createdTickets.created_tickets;

        return createdTickets;
      } catch (error) {
        console.error("Erreur lors de la création des tickets :", error);
        throw error;
      }
    },
  },
});
