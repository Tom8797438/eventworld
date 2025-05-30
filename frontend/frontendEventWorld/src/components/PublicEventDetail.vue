<template>
    <div class="overlay" @click="goBackToEvents">
      <div class="event-card" @click.stop v-if="selectedEvent">
        <!-- Colonne gauche -->
        <div class="event-details">
          <h2 class="event-title">{{ selectedEvent?.name || 'Non spécifié' }}</h2>
          <p ><strong>Description:</strong></p>
          <textarea readonly class="description"> {{ selectedEvent.description || 'Non spécifié' }}</textarea>
          <p><strong>Date début:</strong> {{ selectedEvent.date_start || 'Non spécifié' }}</p>
          <p><strong>Date fin:</strong> {{ selectedEvent.date_end || 'Non spécifié' }}</p>
          <p><strong>Lieu :</strong> {{ selectedEvent.location || 'Non spécifié' }}</p>
          <p><strong>Adresse :</strong> {{ selectedEvent.address || 'Non spécifié' }}</p>
          <p><strong>Ville :</strong> {{ selectedEvent.city || 'Non spécifié' }}</p>
          <p><strong>Places disponibles :</strong> {{ selectedEvent.remaining_places  || 'Non spécifié' }}</p>
        </div>
  
        <!-- Colonne droite : Réservation -->
        <div class="booking-section">
          <h3>Vos coordonnées</h3>
          <div class="input-group">
            <label>Nom</label>
            <input type="text" placeholder="Votre nom" v-model="firstname" required @input="validateTextOnly"/>
          </div>
          <div class="input-group">
            <label>Prénom</label>
            <input type="text" placeholder="Votre prénom" v-model="lastname" required @input="validateTextOnly"/>
          </div>
          <div class="input-group">
            <label>E-mail</label>
            <input type="email" placeholder="Votre e-mail" v-model="email" required @input="isValidEmail"/>
          </div>
          <div class="input-group">
            <label>Téléphone</label>
            <input type="text" placeholder="Votre N° de téléphone" v-model="phone" required @input="validateNumber"/>
          </div>
  
          <!-- Si plusieurs types de prix, on affiche une liste déroulante -->
          <h3>Réserver vos places</h3>
  
          <div v-for="(ticket, index) in selectedTickets" :key="index" >
            <label v-if="ticketTypes.length > 1" >Type de place</label>
            <select v-if="ticketTypes.length > 1" v-model="ticket.type" class="ticket-selection">
              <option v-for="option in ticketTypes" :key="option.name" :value="option.name">
                {{ option.price.label }} - {{ option.price.value }} € 
              </option>
            </select>
  
            <p v-else><strong>{{ ticketTypes[0].price.label }} :</strong>{{ ticketTypes[0].price.value }} €</p>
  
            <div class="input-group">
              <label>Quantité</label>
              <input type="number" min="1" v-model="ticket.quantity" @input="calculateTotal" class="quantity-selection"/>
              <button class="delete-ticket" @click="removeTicket(index)">❌</button>
            </div>
  
          </div>
  
          <button v-if="ticketTypes.length > 1" class="add-ticket" @click="addTicket">➕ Ajouter un autre ticket</button>
  
          <p class="total">Total : {{ total }} €</p>
          <button @click="bookTickets">Réserver vos places</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import {onMounted, ref, computed } from 'vue';
  import { usePublicEventStore } from '@/stores/publicEventStore';
  import { useTicketStore } from '@/stores/ticketStore';
  import { useRouter } from 'vue-router';
  import { validateNumber, validateTextOnly,isValidEmail } from '@/utils/validators';
  
  export default {
    setup() {
      const router = useRouter();
      const publicEventStore = usePublicEventStore();
      const ticketStore = useTicketStore();
  
      const firstname = ref('');
      const lastname = ref('');
      const email = ref('');
      const phone = ref('');
      const selectedEvent = computed(() => publicEventStore.selectedEvent);
      const ticketTypes = ref([]);
      const selectedTickets = ref([]);
  
      onMounted(() => {
    if (!selectedEvent.value) {
      router.push('/accueil');
      return;
    }

    // Initialisation des types de tickets
    if (selectedEvent.value.price_categories) {
      ticketTypes.value = Object.entries(selectedEvent.value.price_categories).map(([key, value]) => ({
        name: key,
        label: key.charAt(0).toUpperCase() + key.slice(1),
        price: value,
      }));
    }

    selectedTickets.value = [{ type: ticketTypes.value[0]?.name || '', quantity: 1 }];
  });
  
      const total = computed(() => {
        return selectedTickets.value.reduce((sum, ticket) => {
          const ticketType = ticketTypes.value.find(t => t.name === ticket.type);
          return sum + (ticket.quantity * (ticketType?.price.value || 0));
        }, 0);
      });
  
      const calculateTotal = () => {
      };
  
      const addTicket = () => {
        if (ticketTypes.value.length > 1) {
          selectedTickets.value.push({ type: ticketTypes.value[0].name, quantity: 1 });
        }
      };
  
      const removeTicket = (index) => {
        selectedTickets.value.splice(index, 1);
      };
  
      const bookTickets = async () => {
        const eventName = selectedEvent.value.name;
        const ticketsToCreate = selectedTickets.value
          .filter(ticket => ticket.quantity > 0)
          .map(ticket => {
            const ticketType = ticketTypes.value.find(t => t.name === ticket.type);
            // Vérification à l’intérieur du map()
            return {
              firstname: firstname.value.trim(),
              lastname: lastname.value.trim(),
              email: email.value.trim(),
              phone: phone.value.trim(),
              quantity: ticket.quantity,
              price: ticketType?.price.value || 0,
              ticket_type: ticketType.price.label,
              event_name: eventName, // attention c'est la
            };
          });
        if (ticketsToCreate.length === 0) {
          alert("Veuillez sélectionner au moins un ticket.");
          return;
        }
  
        try {
          await ticketStore.createTickets(selectedEvent.value.id, ticketsToCreate);
          alert("Réservation réussie !");
          resetForm();
          goBackToEvents();
        } catch (error) {
          console.error("Erreur lors de la réservation :", error);
          alert("Une erreur est survenue lors de la réservation.");
        }
      };
  
      const goBackToEvents = () => {
        publicEventStore.selectedEvent = null;
        router.push('/accueil');
      };
  
      const resetForm = () => {
        firstname.value = "";
        lastname.value = "";
        email.value = "";
        phone.value = "";
        selectedTickets.value = [{ type: ticketTypes.value[0]?.name || '', quantity: 1 }];
      };
  
      return {
        ticketTypes,
        selectedEvent,
        selectedTickets,
        total,
        firstname,
        lastname,
        email,
        phone,
        calculateTotal,
        bookTickets,
        addTicket,
        removeTicket,
        goBackToEvents,
        resetForm,
        validateNumber,
        validateTextOnly,
        isValidEmail,
      };
    },
  };
  </script>
  
  <style scoped>
  @import '@/assets/styles/PublicEventDetails.css';
  </style>
  