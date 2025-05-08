<template>
  <div class="overlay" v-if="event">
    <div class="event-card" @click.stop>
      <!-- Colonne gauche : Détails de l'événement -->
      <div class="event-details">
        <h2 class="event-title">{{ event.name || 'Non spécifié' }}</h2>
        <img
                  class="event-image"
                  :src="getEventImageUrl(event.picture)"
                  alt="Event Image"
                />
        <p><strong>Description:</strong></p>
        <textarea readonly class="description">{{ event.description || 'Non spécifié' }}</textarea>
        <p><strong>Date début :</strong> {{ event.date_start || 'Non spécifié' }}</p>
        <p><strong>Date fin :</strong> {{ event.date_end || 'Non spécifié' }}</p>
        <p><strong>Lieu :</strong> {{ event.location || 'Non spécifié' }}</p>
        <p><strong>Adresse :</strong> {{ event.address || 'Non spécifié' }}</p>
        <p><strong>Ville :</strong> {{ event.city || 'Non spécifié' }}</p>
        <p><strong>Places disponibles :</strong> {{ event.number_place || 'Non spécifié' }}</p>
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

        <h3>Réserver vos places</h3>
<div
  v-for="(ticket, index) in selectedTickets"
  :key="index"
  class="ticket-line"
>
  <!-- Type de place -->
  <div class="ticket-field">
    <label>Type de place</label>
    <select v-model="ticket.type" class="ticket-selection">
      <option v-for="option in ticketTypes" :key="option.name" :value="option.name">
        {{ option.price.label }} - {{ option.price.value || 'Gratuit' }} €
      </option>
    </select>
  </div>

  <!-- Quantité -->
  <div class="ticket-field small">
    <label>Quantité</label>
    <input type="number" min="1" v-model="ticket.quantity" class="quantity-selection" />
  </div>

  <!-- Bouton supprimer -->
  <button
    v-if="!isFreeEvent"
    class="delete-ticket"
    @click="removeTicket(index)"
  >
    ❌
  </button>
</div>


        <!-- Bouton "Ajouter un autre ticket" uniquement si ce n'est pas gratuit et qu'il y a plusieurs prix -->
        
        <p class="total">Total : {{ total }} €</p>
        <div class="button-validation">
          <button @click="bookTickets">Valider</button>
          <button v-if="!isFreeEvent && !isSinglePriceEvent" class="add-ticket" @click="addTicket">➕ Ajouter un ticket</button>
        </div>  
      </div>
    </div>
  </div>

  <p v-else-if="error" class="error">{{ error }}</p>
  <p v-else>Chargement...</p>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useTicketStore } from '@/stores/ticketStore';
import { fetchInvitationById } from '@/utils/api_utils';
import { useTicketLogic } from '@/utils/useTicketLogic';
import { validateNumber, validateTextOnly, isValidEmail } from '@/utils/validators';
import { getEventImageUrl } from '@/utils/imageEvent';

const route = useRoute();
const router = useRouter();
const invitationId = route.params.id;

const ticketStore = useTicketStore();

const event = ref(null);
const error = ref(null);

const firstname = ref('');
const lastname = ref('');
const email = ref('');
const phone = ref('');

const {
  ticketTypes,
  selectedTickets,
  total,
  initializeTickets,
  addTicket,
  removeTicket
} = useTicketLogic();

onMounted(async () => {
  try {
    const invitation = await fetchInvitationById(invitationId);
    event.value = invitation.event;

    const priceCategories = event.value.price_categories;
    initializeTickets(priceCategories);
  } catch (err) {
    console.error("Erreur lors du chargement de l'invitation :", err);
    error.value = "Invitation invalide ou expirée.";
  }
});

const isSinglePriceEvent = computed(() => ticketTypes.value.length === 1);
const isFreeEvent = computed(() => isSinglePriceEvent.value && ticketTypes.value[0].price.value === 0);

const bookTickets = async () => {
  if (!firstname.value.trim() || !lastname.value.trim() || !email.value.trim() || !phone.value.trim()) {
    alert("Veuillez remplir tous les champs.");
    return;
  }
  if (!isValidEmail(email.value)) {
    alert("Veuillez saisir une adresse e-mail valide.");
    return;
  }
  if (selectedTickets.value.some(ticket => !ticket.type || ticket.quantity <= 0)) {
    alert("Veuillez vérifier chaque ticket (type et quantité).");
    return;
  }

  const ticketsToCreate = selectedTickets.value.map(ticket => {
    const ticketType = ticketTypes.value.find(t => t.name === ticket.type);
    return {
      firstname: firstname.value.trim(),
      lastname: lastname.value.trim(),
      email: email.value.trim(),
      phone: phone.value.trim(),
      quantity: ticket.quantity,
      price: ticketType?.price.value || 0,
      ticket_type: ticketType?.price.label || 'Gratuit',
      event_name: event.value.name,
    };
  });

  try {
    await ticketStore.createTickets(event.value.id, ticketsToCreate);
    alert("Réservation réussie !");
    resetForm();
    goBackToAccueil();
  } catch (e) {
    console.error("Erreur de réservation :", e);
    alert("Une erreur est survenue.");
  }
};

const resetForm = () => {
  firstname.value = '';
  lastname.value = '';
  email.value = '';
  phone.value = '';
  selectedTickets.value = [{ type: ticketTypes.value[0]?.name || 'free', quantity: 1 }];
};

const goBackToAccueil = () => {
  router.push('/accueil');
};
</script>


<style scoped>
@import '@/assets/styles/InvitationEventView.css';
@import '@/assets/styles/EventDetails.css';
/*sur charge de la class css*/
.event-image{
  width: 25%;
}
</style>