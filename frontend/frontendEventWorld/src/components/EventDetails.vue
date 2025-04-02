<template>
  <div class="overlay" @click="goBackToEvents">
    <div class="event-card" @click.stop>
      <!-- Colonne gauche -->
      <div class="event-details">
        <h2 class="event-title">{{ selectedEvent?.name || 'Non spécifié' }}</h2>
        <input class="input-modif" type="text" v-model="editedEvent.name" />

        <p><strong>Description:</strong> {{ truncate(selectedEvent.description, 20) || 'Non spécifié' }}</p>
        <textarea class="textarea input-modif" v-model="editedEvent.description"></textarea>

        <p><strong>Date début:</strong> {{ selectedEvent.date_start || 'Non spécifié' }}</p>
        <input class="input-modif" type="date" v-model="editedEvent.date_start" />

        <p><strong>Date fin:</strong> {{ selectedEvent.date_end || 'Non spécifié' }}</p>
        <input class="input-modif" type="date" v-model="editedEvent.date_end" />

        <p><strong>Lieu :</strong> {{ selectedEvent.location || 'Non spécifié' }}</p>
        <input class="input-modif" type="text" v-model="editedEvent.location" />

        <p><strong>Adresse :</strong> {{ selectedEvent.address || 'Non spécifié' }}</p>
        <input class="input-modif" type="text" v-model="editedEvent.address" />

        <p><strong>Ville :</strong> {{ selectedEvent.city || 'Non spécifié' }}</p>
        <input class="input-modif" type="text" v-model="editedEvent.city" />

        <p><strong>Places disponibles :</strong> {{ selectedEvent.remaining_places || 'Non spécifié' }}</p>
        <input class="input-modif" type="number" v-model="editedEvent.number_place" />

        <button @click="saveChanges">Enregistrer les modifications</button>
      </div>

      <!-- Colonne droite : Réservation -->
      <div class="booking-section">
        <h3>Coordonnées client</h3>
        <div class="input-group">
          <label>Nom</label>
          <input type="text" placeholder="Votre nom" v-model="firstname" />
        </div>
        <div class="input-group">
          <label>Prénom</label>
          <input type="text" placeholder="Votre prénom" v-model="lastname" />
        </div>
        <div class="input-group">
          <label>E-mail</label>
          <input type="email" placeholder="Votre e-mail" v-model="email" />
        </div>
        <div class="input-group">
          <label>Téléphone</label>
          <input type="text" placeholder="Votre N° de téléphone" v-model="phone" />
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

          <p v-else-if="ticketTypes.length === 1">
            <strong>{{ ticketTypes[0]?.label || 'Type inconnu' }} :</strong>
            {{ ticketTypes[0]?.value ?? '0' }} €
          </p>
          <p v-else>
            Aucun tarif disponible.
          </p>


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
import { ref, computed, onMounted } from 'vue';
import { useEventStore } from '@/stores/eventStore';
import { useTicketStore } from '@/stores/ticketStore';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();
    const eventStore = useEventStore();
    const ticketStore = useTicketStore();

    const firstname = ref('');
    const lastname = ref('');
    const email = ref('');
    const phone = ref('');

    const ticketTypes = ref([]);
    const editedEvent = ref({});

    const selectedEvent = computed(() => {
      if (!eventStore.selectedEvent) {
        console.error("Aucun événement sélectionné");
        router.push('/Menu');
        return null;
      }
      return eventStore.selectedEvent;
    });

    onMounted(() => {
      if (selectedEvent.value) {
        editedEvent.value = { ...selectedEvent.value };

        if (selectedEvent.value.price_categories) {
          ticketTypes.value = Object.entries(selectedEvent.value.price_categories).map(([key, value]) => ({
            name: key,
            label: key.charAt(0).toUpperCase() + key.slice(1),
            price: value,
          }));
        }
      }
    });

    const selectedTickets = ref([{ type: ticketTypes.value[0]?.name || '', quantity: 1 }]);

    const total = computed(() => {
      return selectedTickets.value.reduce((sum, ticket) => {
        const ticketType = ticketTypes.value.find(t => t.name === ticket.type);
        return sum + (ticket.quantity * (ticketType?.price.value || 0));
      }, 0);
    });

    const saveChanges = async () => {
      try {
        await eventStore.updateEvent(editedEvent.value.id, editedEvent.value);
        alert("Événement mis à jour !");
      } catch (err) {
        console.error(err);
        alert("Erreur lors de la mise à jour.");
      }
    };

    const calculateTotal = () => {};

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
          return {
            firstname: firstname.value.trim(),
            lastname: lastname.value.trim(),
            email: email.value.trim(),
            phone: phone.value.trim(),
            quantity: ticket.quantity,
            price: ticketType?.price.value || 0,
            ticket_type: ticketType?.price.label || 'N/A',
            event_name: eventName,
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
      eventStore.selectedEvent = null;
      router.push('/Menu');
    };

    const resetForm = () => {
      firstname.value = "";
      lastname.value = "";
      email.value = "";
      phone.value = "";
      selectedTickets.value = [{ type: ticketTypes.value[0]?.name || '', quantity: 1 }];
    };
    function truncate(text, maxLength) {
  if (!text) return '';
  return text.length > maxLength ? text.slice(0, maxLength) + '…' : text;
}

    return {
      truncate,
      saveChanges,
      ticketTypes,
      selectedEvent,
      editedEvent,
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
    };
  },
};
</script>

<style scoped>
@import '@/assets/styles/EventDetails.css';
</style>
