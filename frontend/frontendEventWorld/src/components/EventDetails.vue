<template>
  <div class="overlay" @click="goBackToEvents">
    <div class="event-card" @click.stop>
      <!-- Colonne gauche -->
    <div class="event-details">
      <div class="event-header-row">

          <div class="left-col">
            <h2 class="event-title">Votre évènement : {{ selectedEvent?.name || 'Non spécifié' }}</h2>
            <input class="input-modif" type="text" v-model="editedEvent.name" />

            <p><strong>Description : </strong> {{ truncate(selectedEvent.description, 10) || 'Non spécifié' }}</p>
            <textarea class="textarea input-modif" v-model="editedEvent.description"></textarea>
          </div>

          <div class="right-col">
            <div class="current-image">
              <img
                  :src="imagePreviewUrl || getEventImageUrl(selectedEvent.picture)"
                  alt="Image actuelle"
                  class="event-image-preview"
                />
            </div>

            <div class="upload-image">
              <label for="file-upload">📁 Changer l'image :</label>
              <input type="file" id="file-upload" @change="onImageChange" accept="image/*" />
            </div>
          </div>

      </div>      

        <p><strong>Date début : </strong> {{ selectedEvent.date_start || 'Non spécifié' }}</p>
        <input class="input-modif" type="date" v-model="editedEvent.date_start" />

        <p><strong>Date fin : </strong> {{ selectedEvent.date_end || 'Non spécifié' }}</p>
        <input class="input-modif" type="date" v-model="editedEvent.date_end" />

        <p><strong>Lieu : </strong> {{ selectedEvent.location || 'Non spécifié' }}</p>
        <input class="input-modif" type="text" v-model="editedEvent.location" />

        <p><strong>Adresse : </strong> {{ selectedEvent.address || 'Non spécifié' }}</p>
        <input class="input-modif" type="text" v-model="editedEvent.address" />

        <p><strong>Code postal : </strong> {{ selectedEvent.postal_code || 'Non spécifié' }}</p>
        <input class="input-modif" type="text" v-model="editedEvent.postal_code" required @input="validateNumber"/>

        <p><strong>Ville : </strong> {{ selectedEvent.city || 'Non spécifié' }}</p>
        <input class="input-modif" type="text" v-model="editedEvent.city" />

        <p><strong>Places disponibles : </strong> {{ selectedEvent.remaining_places || 'Non spécifié' }}</p>
        <input class="input-modif" type="number" v-model="editedEvent.number_place" />

        <div class="price-editor">
          <h3>Gestion des prix</h3>
            <div v-for="(price, index) in editedEvent.price_categories" :key="index" class="price-item">
              <label>Type de prix :</label>
                <input
                  class="input-modif"
                  type="text"
                  v-model="price.label"
                  placeholder="ex: Standard, VIP"
                />
              <label>Prix (€) :</label>
                <input
                  class="input-modif"
                  type="number"
                  v-model="price.value"
                  placeholder="ex: 10"
                />
                <button class="delete-price" @click="removePrice(index)">❌</button>
                
             
            </div>
            <button class="add-price" @click="addPrice">➕ Ajouter un prix</button>
      </div>

        <div v-if="invitationLink" class="invitation-link-section">
          <p><strong>Lien d'invitation :</strong></p>
          <div class="link"><a :href="invitationLink" target="_blank">{{ invitationLink }}</a></div>
        </div>

        <div class="container-button-save">
          <button class="button-save back" @click="goBackToEvents">Retour</button>
          <button class="button-save" @click="saveChanges">Enregistrer</button>
        </div>
      
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
          <input type="email" placeholder="Votre e-mail" v-model="email" required/>
        </div>
        <div class="input-group">
          <label>Téléphone</label>
          <input type="text" placeholder="Votre N° de téléphone" v-model="phone" required @input="validateNumber"/>
        </div>
       
        <!-- Si plusieurs types de prix, on affiche une liste déroulante -->
        <h3>Réserver vos places</h3>

        <div v-for="(ticket, index) in selectedTickets" :key="index" >
          <label v-if="ticketTypes.length > 1">Type de place</label>
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
        <button @click="bookTickets" class="add-ticket">Réserver vos places</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useEventStore } from '@/stores/eventStore';
import { useTicketStore } from '@/stores/ticketStore';
import { useRoute, useRouter } from 'vue-router';
import { fetchInvitationByEventId } from '@/utils/api_utils';
import { useTicketLogic } from '@/utils/useTicketLogic';
import { validateNumber } from '@/utils/validators';
import { getEventImageUrl, handleImageUpload } from '@/utils/imageEvent';


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

    const saveChanges = async () => {
  try {
    const formData = new FormData();

    // Ajouter tous les champs édités
    Object.entries(editedEvent.value).forEach(([key, value]) => {
      if (key !== 'price_categories') {
        formData.append(key, value);
      } else {
        formData.append(key, JSON.stringify(value)); // price_categories au format JSON
      }
    });

    // Ajouter l'image si une nouvelle a été choisie
    if (newImageFile.value) {
      formData.append('picture', newImageFile.value);
    }

    await eventStore.updateEvent(editedEvent.value.id, formData);
    alert("Événement mis à jour !");
    
    // Rafraîchir après la sauvegarde pour voir la nouvelle image immédiatement
    await eventStore.fetchEvents();
    newImageFile.value = null;

  } catch (err) {
    console.error(err);
    alert("Erreur lors de la mise à jour.");
  }
  imagePreviewUrl.value = '';

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
    };
  },
};
</script>

<style scoped>
@import '@/assets/styles/EventDetails.css';

</style>
