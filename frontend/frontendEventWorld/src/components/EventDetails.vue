<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-indigo-100 flex items-center justify-center p-4">
    <div class="max-w-7xl w-full bg-white rounded-lg shadow-lg overflow-hidden">
      <!-- Overlay pour fermer -->
      <div class="flex flex-col md:flex-row h-full">
        <!-- Colonne gauche : Détails et édition -->
        <div class="md:w-2/3 p-6 bg-gray-50 overflow-y-auto space-y-6">
          <!-- Header avec image et titre -->
          <div class="flex flex-col md:flex-row gap-6">
            <div class="flex-shrink-0">
              <img
                :src="imagePreviewUrl || getEventImageUrl(selectedEvent.picture)"
                alt="Image actuelle"
                class="w-80 h-auto rounded-lg border border-gray-300 shadow-md"
              />
              <div class="mt-4 bg-blue-50 p-4 rounded-lg border-2 border-dashed border-blue-300">
                <label for="file-upload" class="block text-sm font-medium text-blue-700 cursor-pointer">📁 Changer l'image :</label>
                <input
                  type="file"
                  id="file-upload"
                  @change="onImageChange"
                  accept="image/*"
                  class="mt-2 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                />
              </div>
            </div>
            <div class="flex-1 space-y-4">
              <h2 class="text-3xl font-bold text-purple-800">Votre évènement</h2>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Nom de l'événement</label>
                <input
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                  type="text"
                  v-model="editedEvent.name"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
                <textarea
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500 resize-none"
                  v-model="editedEvent.description"
                  rows="4"
                ></textarea>
              </div>
            </div>
          </div>

          <!-- Champs d'édition -->
          <div class="bg-white p-6 rounded-lg shadow-md border border-purple-200">
            <h3 class="text-xl font-bold text-purple-800 mb-4">Détails de l'événement</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Date début</label>
                <input
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                  type="date"
                  v-model="editedEvent.date_start"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Date fin</label>
                <input
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                  type="date"
                  v-model="editedEvent.date_end"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Lieu</label>
                <input
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                  type="text"
                  v-model="editedEvent.location"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Adresse</label>
                <input
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                  type="text"
                  v-model="editedEvent.address"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Code postal</label>
                <input
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                  type="text"
                  v-model="editedEvent.postal_code"
                  @input="validateNumber"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Ville</label>
                <input
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                  type="text"
                  v-model="editedEvent.city"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Nombre de places</label>
                <input
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                  type="number"
                  v-model="editedEvent.number_place"
                />
              </div>
            </div>
          </div>

          <!-- Gestion des prix -->
          <div class="bg-white p-6 rounded-lg shadow-md border border-purple-200">
            <h3 class="text-xl font-bold text-purple-800 mb-4">Gestion des prix</h3>
            <div v-for="(price, index) in editedEvent.price_categories" :key="index" class="flex gap-2 mb-2 items-end">
              <div class="flex-1">
                <label class="block text-sm font-medium text-gray-700 mb-1">Catégorie</label>
                <input
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                  type="text"
                  v-model="price.label"
                  placeholder="ex: Standard, VIP"
                />
              </div>
              <div class="w-24">
                <label class="block text-sm font-medium text-gray-700 mb-1">Prix (€)</label>
                <input
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                  type="number"
                  v-model="price.value"
                  placeholder="10"
                />
              </div>
              <button
                class="bg-red-600 text-white px-3 py-2 rounded-lg hover:bg-red-700 transition-colors duration-200"
                @click="removePrice(index)"
              >
                ❌
              </button>
            </div>
            <button
              class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors duration-200 mt-4"
              @click="addPrice"
            >
              ➕ Ajouter un prix
            </button>
          </div>

          <!-- Utilisateurs temporaires -->
          <div class="bg-white p-6 rounded-lg shadow-md border border-purple-200">
            <h3 class="text-xl font-bold text-purple-800 mb-4">Utilisateurs temporaires</h3>
            <div v-if="temporaryScanners?.length" class="space-y-4">
              <div v-for="scanner in temporaryScanners" :key="scanner.id" class="bg-gray-50 p-4 rounded-lg border border-gray-200">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                  <input
                    class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                    v-model="scanner.display_name"
                    placeholder="Alias"
                  />
                  <input
                    class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                    v-model="scanner.email"
                    type="email"
                    placeholder="Email"
                  />
                </div>
                <div class="flex gap-4 mb-4">
                  <label class="flex items-center">
                    <input type="checkbox" v-model="scanner.can_scan" class="mr-2" />
                    Peut scanner
                  </label>
                  <label class="flex items-center">
                    <input type="checkbox" v-model="scanner.can_sell" class="mr-2" />
                    Peut vendre
                  </label>
                </div>
                <p v-if="scanner.expires_at" class="text-sm text-gray-600 mb-2">Expire le : {{ formatDate(scanner.expires_at) }}</p>
                <p v-if="scanner.last_seen_at" class="text-sm text-gray-600 mb-4">Dernière activité : {{ formatDate(scanner.last_seen_at) }}</p>
                <div class="flex gap-2 flex-wrap">
                  <button
                    class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-200"
                    @click="updateTempUser(scanner)"
                  >
                    💾 Enregistrer
                  </button>
                  <button
                    class="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors duration-200"
                    @click="deleteTempUser(scanner.id)"
                  >
                    🗑️ Supprimer
                  </button>
                  <button
                    class="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors duration-200"
                    @click="goToTempUserAccess(scanner.access_token)"
                  >
                    🔗 Voir accès
                  </button>
                  <button
                    class="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors duration-200"
                    @click="copyTempUserAccess(scanner.access_token)"
                  >
                    📋 Copier lien
                  </button>
                  <button
                    class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors duration-200"
                    @click="sendTempUserAccess(scanner)"
                  >
                    ✉️ Envoyer lien
                  </button>
                </div>
              </div>
            </div>
            <div class="mt-6">
              <h4 class="text-lg font-semibold text-purple-800 mb-4">Ajouter un utilisateur temporaire</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <input
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                  v-model="newTempUser.alias"
                  placeholder="Alias"
                />
                <input
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                  v-model="newTempUser.email"
                  type="email"
                  placeholder="Email"
                />
              </div>
              <div class="flex gap-4 mb-4">
                <label class="flex items-center">
                  <input type="checkbox" v-model="newTempUser.can_scan" class="mr-2" />
                  Peut scanner
                </label>
                <label class="flex items-center">
                  <input type="checkbox" v-model="newTempUser.can_sell" class="mr-2" />
                  Peut vendre
                </label>
              </div>
              <button
                class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors duration-200"
                @click="createTempUser"
              >
                ➕ Ajouter
              </button>
            </div>
          </div>

          <!-- Lien d'invitation -->
          <div v-if="invitationLink" class="bg-blue-50 p-4 rounded-lg border border-blue-200">
            <p class="text-sm text-blue-700"><strong>Lien d'invitation :</strong></p>
            <div class="flex flex-col md:flex-row md:items-center gap-2">
              <a :href="invitationLink" target="_blank" class="text-blue-600 underline break-all">{{ invitationLink }}</a>
              <button
                class="bg-gray-600 text-white px-3 py-2 rounded-lg hover:bg-gray-700 transition-colors duration-200 text-sm"
                @click="copyInvitationLink"
              >
                📋 Copier lien
              </button>
            </div>
          </div>

          <!-- Boutons -->
          <div class="flex justify-end gap-4">
            <button
              class="bg-gray-600 text-white px-6 py-3 rounded-lg hover:bg-gray-700 transition-colors duration-200 font-semibold"
              @click="goBackToEvents"
            >
              Retour
            </button>
            <button
              class="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-colors duration-200 font-semibold"
              @click="saveChanges"
            >
              Enregistrer
            </button>
          </div>
        </div>

        <!-- Colonne droite : Réservation -->
        <div class="md:w-1/3 p-6 bg-white border-l border-gray-200 overflow-y-auto space-y-6">
          <h3 class="text-2xl font-bold text-purple-800">Coordonnées client</h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Prénom</label>
              <input
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                type="text"
                placeholder="Votre prénom"
                v-model="firstname"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Nom</label>
              <input
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                type="text"
                placeholder="Votre nom"
                v-model="lastname"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <input
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                type="email"
                placeholder="Votre e-mail"
                v-model="email"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Téléphone</label>
              <input
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                type="text"
                placeholder="Votre N° de téléphone"
                v-model="phone"
                @input="validateNumber"
              />
            </div>
          </div>

          <h3 class="text-2xl font-bold text-purple-800">Réserver vos places</h3>
          <div v-for="(ticket, index) in selectedTickets" :key="index" class="space-y-2 bg-gray-50 p-4 rounded-lg">
            <select
              v-if="ticketTypes.length > 1"
              v-model="ticket.type"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
            >
              <option v-for="option in ticketTypes" :key="option.name" :value="option.name">
                {{ option.price.label }} - {{ option.price.value }} €
              </option>
            </select>
            <p v-else-if="ticketTypes.length === 1" class="text-sm text-gray-700">
              <strong>{{ ticketTypes[0]?.label || 'Type inconnu' }} :</strong> {{ ticketTypes[0]?.value ?? '0' }} €
            </p>
            <div class="flex items-center gap-2">
              <input
                class="w-20 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500"
                type="number"
                min="1"
                v-model="ticket.quantity"
                @input="calculateTotal"
              />
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
            class="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 transition-colors duration-200 font-semibold"
            @click="addTicket"
          >
            ➕ Ajouter un autre ticket
          </button>

          <div class="bg-purple-50 p-4 rounded-lg border border-purple-200">
            <p class="text-lg font-bold text-center text-purple-800">Total : {{ total }} €</p>
          </div>
          <button
            class="w-full bg-green-600 text-white py-3 px-4 rounded-lg hover:bg-green-700 transition-colors duration-200 font-semibold"
            @click="bookTickets"
          >
            Réserver vos places
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useEventStore } from '@/stores/eventStore';
import { useTicketStore } from '@/stores/ticketStore';
import { useRoute, useRouter } from 'vue-router';
import { fetchInvitationByEventId, sendTempAccessLink } from '@/utils/api_utils';
import { useTicketLogic } from '@/utils/useTicketLogic';
import { validateNumber } from '@/utils/validators';
import { getEventImageUrl, handleImageUpload } from '@/utils/imageEvent';
import { confirmAndNavigate } from '@/utils/navigation';



export default {
  setup() {
    const types = {
      public: "Public",
      private: "Privé",
      limited: "Limité"
    };
    const route = useRoute();
    const router = useRouter();
    const eventStore = useEventStore();
    const ticketStore = useTicketStore();

    const eventId = route.params.id; // Récupère l'ID de l'événement depuis les paramètres de la route
    const invitationLink = ref('');
    const newImageFile = ref(null);      // pour stocker la nouvelle image sélectionnée
    const imagePreviewUrl = ref('');     // pour l'aperçu

    const firstname = ref('');
    const lastname = ref('');
    const email = ref('');
    const phone = ref('');

    // const ticketTypes = ref([]);
    const editedEvent = ref({});

    const selectedEvent = computed(() => eventStore.events.find(event => event.id === eventId));
    const { ticketTypes, selectedTickets, total, initializeTickets, addTicket, removeTicket } = useTicketLogic();
    
    const temporaryScanners = computed(() => eventStore.temporaryScanners);

    // Ajout de nouvel utilisateur temporaire
    const newTempUser = ref({
      alias: '',
      email: '',
      can_scan: false,
      can_sell: false,
    });


    onMounted(async () => {
  if (!selectedEvent.value) {
    console.error('Événement introuvable');
    router.push('/Menu');
    return;
  }

  const rawEvent = { ...selectedEvent.value };

  // Normalise les prix AVANT de copier dans editedEvent
  let normalizedPrices = [];

  if (typeof rawEvent.price_categories === 'string') {
    try {
      normalizedPrices = JSON.parse(rawEvent.price_categories);
    } catch (e) {
      console.error('Erreur de parsing JSON :', e);
      normalizedPrices = [];
    }
  } else if (typeof rawEvent.price_categories === 'object' && !Array.isArray(rawEvent.price_categories)) {
    normalizedPrices = Object.entries(rawEvent.price_categories).map(([label, value]) => ({ label, value }));
  } else if (Array.isArray(rawEvent.price_categories)) {
    normalizedPrices = rawEvent.price_categories;
  }

  // Mise à jour de editedEvent avec prix bien formatés
  editedEvent.value = {
    ...rawEvent,
    price_categories: normalizedPrices,
  };

  // Appel logique tickets (copie défensive si modif plus tard)
  initializeTickets(JSON.parse(JSON.stringify(normalizedPrices)));

  try {
    const invitation = await fetchInvitationByEventId(rawEvent.id);
    if (invitation && invitation.id) {
      invitationLink.value = `${window.location.origin}/invitation/${invitation.id}`;
    } else {
      console.warn('Aucune invitation trouvée pour cet événement.');
    }
   // Chargement des utilisateurs temporaires
    await eventStore.loadTemporaryScanners(rawEvent.id);

  } catch (err) {
    console.error('Erreur lors de la récupération du lien d\'invitation :', err);
  }
});

const onImageChange = (event) => {
  const { file, preview } = handleImageUpload(event);
  if (file) {
    newImageFile.value = file;
    imagePreviewUrl.value = preview;
  }
};

const deleteTempUser = async(scannerId) => {
    if (confirm("Supprimer cet utilisateur temporaire ?")) {
      try {
      await eventStore.deleteTemporaryScanner(scannerId);
      await eventStore.loadTemporaryScanners(editedEvent.value.id);
      alert("Utilisateur Supprimer !");

      } catch (err) {
        alert("Erreur lors de la suppression.");
        console.error(err);
      }
    }
  };
  const updateTempUser = async(scanner) => {
    try {
      const payload = {
        alias: scanner.display_name,
        email: scanner.email,
        can_scan: scanner.can_scan,
        can_sell: scanner.can_sell
      };
      console.log("Update scanner ID :", scanner.id);
      await eventStore.updateTemporaryScanner(scanner.id, payload);
      alert("Utilisateur mis à jour !");

    } catch (err) {
      alert("Erreur lors de la mise à jour.");
      console.error(err);
    }
  };

const saveChanges = async () => {
  try {
    const hasImage = newImageFile.value instanceof File;

    if (hasImage) {
      const formData = new FormData();

      Object.entries(editedEvent.value).forEach(([key, value]) => {
        if (value === null || value === undefined || value === '') return;

        if (key === 'price_categories') {
          formData.append(key, JSON.stringify(value));
        } else {
          formData.append(key, String(value));
        }
      });

      formData.append('picture', newImageFile.value);

      await eventStore.updateEvent(editedEvent.value.id, formData, true); // true = formData

    } else {
      // JSON pur si pas d'image
      const jsonPayload = {};
      Object.entries(editedEvent.value).forEach(([key, value]) => {
        if (value === null || value === undefined || value === '') return;
        if (key === 'picture') return; // NE PAS envoyer picture sans image
        jsonPayload[key] = key === 'price_categories' ? JSON.stringify(value) : value;
      });

      await eventStore.updateEvent(editedEvent.value.id, jsonPayload, false); // false = JSON
    }

    alert("Événement mis à jour !");
    await eventStore.fetchEvents();
    newImageFile.value = null;
    imagePreviewUrl.value = '';
    router.push('/Menu');

  } catch (err) {
    const errorMsg = err.response?.data?.picture?.[0];
    if (errorMsg === "Upload a valid image. The file you uploaded was either not an image or a corrupted image.") {
    alert("❌ L'image est invalide. Veuillez importer une image correcte (format JPG, PNG, etc.).");
  } else {
    console.error('❌ Erreur lors de la mise à jour :', err.response?.data || err.message);
    alert("Erreur lors de la mise à jour.");
  } }
};

    const calculateTotal = () => {};

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
    const addPrice = () => {
      editedEvent.value.price_categories.push({ label: '', value: 0 });
    };

    const removePrice = (index) => {
      editedEvent.value.price_categories.splice(index, 1);
    };
    // Fonction pour revenir en arrière vers la liste des événements
    const goBackToEvents = () => {
      confirmAndNavigate("Êtes-vous sûr de vouloir revenir au menu ?", router, "/Menu");
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

    // champs pour les utilisateurs temporaires
    const createTempUser = async () => {
  if (!newTempUser.value.alias || !newTempUser.value.email) {
    alert("Alias et email sont obligatoires.");
    return;
  }

  const payload = {
    alias: newTempUser.value.alias,
    email: newTempUser.value.email,
    can_scan: newTempUser.value.can_scan,
    can_sell: newTempUser.value.can_sell,
    event_id: editedEvent.value.id,
  };

  try {
    await eventStore.createTemporaryScanner(payload);
    await eventStore.loadTemporaryScanners(editedEvent.value.id);  // Refresh
    newTempUser.value = { alias: '', email: '', can_scan: false, can_sell: false };
    alert("Utilisateur temporaire ajouté !");
  } catch (err) {
    console.error("Erreur lors de la création :", err);
    alert("Erreur lors de l'ajout.");
  }
};

    return {
      addPrice,
      removePrice,
      selectedEvent,
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
      types,
      invitationLink,
      validateNumber,
      onImageChange,
      getEventImageUrl,
      imagePreviewUrl,
      newImageFile,
      eventStore,
      temporaryScanners,
      updateTempUser,
      deleteTempUser,
      newTempUser,
      createTempUser,
    };
  },

methods: {

    editTempUser(scanner) {
      alert(`Prévoir ici l'édition de ${scanner.display_name}`);
    },

    goToTempUserAccess(token) {
      window.open(this.getTempAccessLink(token), "_blank");
    },
    getTempAccessLink(token) {
      return `${window.location.origin}/access/temp/${token}`;
    },
    async copyTempUserAccess(token) {
      const link = this.getTempAccessLink(token);
      try {
        await navigator.clipboard.writeText(link);
        alert("Lien copie.");
      } catch (err) {
        console.error(err);
        alert("Impossible de copier le lien.");
      }
    },
    async sendTempUserAccess(scanner) {
      if (!scanner?.id) return;
      const eventId = this.editedEvent?.id;
      if (!eventId) return;
      try {
        await sendTempAccessLink(eventId, scanner.id, scanner.email);
        alert("Lien envoye par mail.");
      } catch (err) {
        console.error(err);
        alert("Erreur lors de l'envoi du lien.");
      }
    },

    formatDate(date) {
      return new Date(date).toLocaleString();
    },
    async copyInvitationLink() {
      if (!this.invitationLink) return;
      try {
        await navigator.clipboard.writeText(this.invitationLink);
        alert("Lien copie.");
      } catch (err) {
        console.error(err);
        alert("Impossible de copier le lien.");
      }
    }
  }
};
</script>
