<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click="goBackToEvents">
    <div class="max-w-6xl w-full mx-4 bg-white rounded-lg shadow-lg overflow-hidden flex flex-col md:flex-row" @click.stop v-if="selectedEvent">
      <!-- Colonne gauche : Détails de l'événement -->
      <div class="md:w-2/3 p-6 bg-gray-50 space-y-4">
        <h2 class="text-2xl font-bold text-purple-800">{{ selectedEvent?.name || 'Non spécifié' }}</h2>
        <div class="space-y-2 text-sm text-gray-700">
          <p><strong>Description:</strong></p>
          <textarea
            readonly
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-white resize-none"
            rows="4"
          >
            {{ selectedEvent.description || 'Non spécifié' }}
          </textarea>
          <p><strong>Date début:</strong> {{ selectedEvent.date_start || 'Non spécifié' }}</p>
          <p><strong>Date fin:</strong> {{ selectedEvent.date_end || 'Non spécifié' }}</p>
          <p><strong>Lieu :</strong> {{ selectedEvent.location || 'Non spécifié' }}</p>
          <p><strong>Adresse :</strong> {{ selectedEvent.address || 'Non spécifié' }}</p>
          <p><strong>Ville :</strong> {{ selectedEvent.city || 'Non spécifié' }}</p>
          <p><strong>Places disponibles :</strong> {{ selectedEvent.remaining_places || 'Non spécifié' }}</p>
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
          <div v-if="ticketTypes.length > 1">
            <label class="block text-sm font-medium text-gray-700 mb-1">Type de place</label>
            <select
              v-model="ticket.type"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            >
              <option v-for="option in ticketTypes" :key="option.name" :value="option.name">
                {{ option.price.label }} - {{ option.price.value }} €
              </option>
            </select>
          </div>
          <p v-else class="text-sm text-gray-700">
            <strong>{{ ticketTypes[0]?.price.label }} :</strong> {{ ticketTypes[0]?.price.value }} €
          </p>
          <div class="flex items-center gap-2">
            <div class="flex-1">
              <label class="block text-sm font-medium text-gray-700 mb-1">Quantité</label>
              <input
                type="number"
                min="1"
                v-model="ticket.quantity"
                @input="calculateTotal"
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
            <button
              class="bg-red-600 text-white px-3 py-2 rounded-lg hover:bg-red-700 transition-colors duration-200"
              @click="removeTicket(index)"
            >
              ❌
            </button>
          </div>
        </div>

        <button
          v-if="ticketTypes.length > 1"
          @click="addTicket"
          class="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors duration-200"
        >
          ➕ Ajouter un autre ticket
        </button>

        <p class="text-lg font-bold text-right text-purple-800">Total : {{ total }} €</p>
        <button
          @click="bookTickets"
          class="w-full bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700 transition-colors duration-200"
        >
          Réserver vos places
        </button>
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
