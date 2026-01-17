<template>
  <div v-if="event" class="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-indigo-100 flex items-center justify-center p-4">
    <div class="max-w-6xl w-full bg-white rounded-lg shadow-lg overflow-hidden flex flex-col md:flex-row">
      <div class="md:w-2/3 p-6 bg-gray-50 space-y-4">
        <h2 class="text-2xl font-bold text-purple-800">{{ event.name || 'Non spécifié' }}</h2>
        <img
          class="w-full h-64 object-cover rounded-lg border border-gray-300"
          :src="getEventImageUrl(event.picture)"
          alt="Event Image"
        />
        <div class="space-y-2 text-sm text-gray-700">
          <p><strong>Description:</strong></p>
          <p class="bg-white p-3 rounded-lg border border-gray-200">{{ event.description || 'Non spécifié' }}</p>
          <p><strong>Date début :</strong> {{ event.date_start || 'Non spécifié' }}</p>
          <p><strong>Date fin :</strong> {{ event.date_end || 'Non spécifié' }}</p>
          <p><strong>Lieu :</strong> {{ event.location || 'Non spécifié' }}</p>
          <p><strong>Adresse :</strong> {{ event.address || 'Non spécifié' }}</p>
          <p><strong>Ville :</strong> {{ event.city || 'Non spécifié' }}</p>
          <p><strong>Places restantes :</strong> {{ event.remaining_places ?? 'Non spécifié' }}</p>
        </div>
      </div>

      <!-- Colonne droite : Réservation -->
      <div class="md:w-1/3 p-6 bg-white border-l border-gray-200 space-y-6">
        <h3 class="text-xl font-bold text-purple-800">Vos coordonnées</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nom</label>
            <input
              type="text"
              placeholder="Votre nom"
              v-model="firstname"
              required
              @input="validateTextOnly"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Prénom</label>
            <input
              type="text"
              placeholder="Votre prénom"
              v-model="lastname"
              required
              @input="validateTextOnly"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">E-mail</label>
            <input
              type="email"
              placeholder="Votre e-mail"
              v-model="email"
              required
              @input="isValidEmail"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Téléphone</label>
            <input
              type="text"
              placeholder="Votre N° de téléphone"
              v-model="phone"
              required
              @input="validateNumber"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>
        </div>

        <h3 class="text-xl font-bold text-purple-800">Réserver vos places</h3>
        <div v-for="(ticket, index) in selectedTickets" :key="index" class="space-y-2">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Type de place</label>
            <select
              v-model="ticket.type"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            >
              <option v-for="option in ticketTypes" :key="option.name" :value="option.name">
                {{ option.price.label }} - {{ option.price.value || 'Gratuit' }} €
              </option>
            </select>
          </div>
          <div class="flex items-center gap-2">
            <div class="flex-1">
              <label class="block text-sm font-medium text-gray-700 mb-1">Quantité</label>
              <input
                type="number"
                min="1"
                v-model="ticket.quantity"
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
            <button
              v-if="!isFreeEvent"
              class="bg-red-600 text-white px-3 py-2 rounded-lg hover:bg-red-700 transition-colors duration-200 mt-6"
              @click="removeTicket(index)"
            >
              ❌
            </button>
          </div>
        </div>

        <p class="text-lg font-bold text-right text-purple-800">Total : {{ total }} €</p>
        <div class="space-y-2">
          <button
            @click="bookTickets"
            class="w-full bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700 transition-colors duration-200"
          >
            Valider
          </button>
          <button
            v-if="!isFreeEvent && !isSinglePriceEvent"
            @click="addTicket"
            class="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors duration-200"
          >
            ➕ Ajouter un ticket
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de places épuisées -->
    <div v-if="showNoSeatsModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-lg shadow-lg max-w-sm w-full text-center">
        <p class="text-red-600 mb-4">❌ Désolé mais, il n'y a plus de places pour cet événement.</p>
        <button
          @click="showNoSeatsModal = false"
          class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-200"
        >
          OK
        </button>
      </div>
    </div>
  </div>

  <div v-else-if="error" class="min-h-screen flex items-center justify-center">
    <p class="text-red-500 text-lg">{{ error }}</p>
  </div>
  <div v-else class="min-h-screen flex items-center justify-center">
    <p class="text-gray-500 text-lg">Chargement...</p>
  </div>
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

const showNoSeatsModal = ref(false);

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
  if (event.value.remaining_places === 0) {
    showNoSeatsModal.value = true;
    return;
  }

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
