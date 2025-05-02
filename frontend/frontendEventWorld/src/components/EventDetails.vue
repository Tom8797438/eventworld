<template>
  <div class="overlay" @click="goBackToEvents">
    <div class="event-card" @click.stop>
      <!-- Colonne gauche -->
      <div class="event-details">
        <h2 class="event-title">Votre évènement : {{ selectedEvent?.name || 'Non spécifié' }}</h2>
        <input class="input-modif" type="text" v-model="editedEvent.name" />

        <p><strong>Description : </strong> {{ truncate(selectedEvent.description, 10) || 'Non spécifié' }}</p>
        <textarea class="textarea input-modif" v-model="editedEvent.description"></textarea>

        <p><strong>Date début : </strong> {{ selectedEvent.date_start || 'Non spécifié' }}</p>
        <input class="input-modif" type="date" v-model="editedEvent.date_start" />

        <p><strong>Date fin : </strong> {{ selectedEvent.date_end || 'Non spécifié' }}</p>
        <input class="input-modif" type="date" v-model="editedEvent.date_end" />

        <p><strong>Lieu : </strong> {{ selectedEvent.location || 'Non spécifié' }}</p>
        <input class="input-modif" type="text" v-model="editedEvent.location" />

        <p><strong>Adresse : </strong> {{ selectedEvent.address || 'Non spécifié' }}</p>
        <input class="input-modif" type="text" v-model="editedEvent.address" />

        <p><strong>Code postal : </strong> {{ selectedEvent.postal_code || 'Non spécifié' }}</p>
        <input class="input-modif" type="text" v-model="editedEvent.postal_code" />

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

        <div v-for="(price, index) in editedEvent.price_categories" :key="index" class="price-editor">
        <label>Type de prix : </label>
        <input class="input-modif" type="text" v-model="price.label" placeholder="ex: Standard" />
          <div>
            <label><strong>Prix Unitaire (ht €) :</strong></label>
            <input class="input-modif" type="number" v-model="price.value" placeholder="ex: 10" />
          </div>
            <div>
              <label for="type_event">Type</label>
              <select class="input-modif" v-model="editedEvent.type_event" id="type_event">
                <option v-for="(label, value) in types" :key="value" :value="value">
                  {{ label }}
                </option>
              </select>
            </div>
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
import { useRoute, useRouter } from 'vue-router';
import { fetchInvitationByEventId } from '@/utils/api_utils';

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

    const firstname = ref('');
    const lastname = ref('');
    const email = ref('');
    const phone = ref('');

    const ticketTypes = ref([]);
    const editedEvent = ref({});

    const selectedEvent = computed(() => eventStore.events.find(event => event.id === eventId));

    onMounted(async () => {
      if (!selectedEvent.value) {
        console.error('Événement introuvable');
        router.push('/Menu'); // Redirige vers le menu si l'événement n'existe pas
        return;
      }

      if (selectedEvent.value) {
        editedEvent.value = { ...selectedEvent.value };

        if (selectedEvent.value.price_categories) {
          ticketTypes.value = Object.entries(selectedEvent.value.price_categories).map(([key, value]) => ({
            name: key,
            label: key.charAt(0).toUpperCase() + key.slice(1),
            price: value,
          }));
        }

        try {
          const invitation = await fetchInvitationByEventId(selectedEvent.value.id);
          if (invitation && invitation.id) {
            invitationLink.value = `${window.location.origin}/invitation/${invitation.id}`;
          } else {
            console.warn("Aucune invitation trouvée pour cet événement.");
          }
        } catch (err) {
          console.error("Erreur lors de la récupération du lien d'invitation :", err);
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
    };
  },
};
</script>

<style scoped>
/* @import '@/assets/styles/EventDetails.css'; */
/* Conteneur principal */
.overlay {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 70px); 
  width: 100vw; /* Occupe toute la largeur de la fenêtre */
  background: linear-gradient(135deg, #7ab8fa, #62a9f5, #007bff); /* Dégradé moderne */
  padding: 20px;
  box-sizing: border-box; /* Inclut les bordures et le padding dans les dimensions */
  overflow: hidden; /* Empêche le scrolling */
}

/* Carte principale */
.event-card {
  display: flex;
  flex-direction: row;
  gap: 20px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 20px;
  width: 100%;
  height: 100%; /* La carte occupe toute la hauteur disponible */
  box-sizing: border-box;
  overflow: hidden;
}

/* Colonne gauche : Détails de l'événement */
.event-details {
  flex: 2; /* 2/3 de la largeur */
  display: flex;
  flex-direction: column;
  gap: 15px;
  background: #efefef;
  color:#000;

  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow-y: auto; /* Ajoute un scrolling interne si nécessaire */
}

.event-title {
  font-size: 1.8rem;
  font-weight: bold;
  color: #333;
  text-align: left;
}

.input-modif {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 1rem;
}

.textarea {
  min-height: 100px;
  resize: vertical;
}

.invitation-link-section {
  margin-top: 1rem;
  background: #e6f7ff;
  padding: 10px;
  border-radius: 6px;
}

.invitation-link-section .link a {
  color: #007bff;
  text-decoration: none;
}

.container-button-save {
  display: flex;
  justify-content: flex-end;
  margin-top: 1rem;
}


.add-price,
.delete-price {
  display: flex;
  justify-content:flex-end;
  margin-top: 1rem;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  padding: 5px 10px;
  margin-top: 10px;
  transition: background 0.3s;
  float: center;
}
.button-save{
  background: #28a745;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s;
  margin: 0 5px;
}

.button-save:hover{
  background: #218838;
}

.button-save.back {
  background: #6c757d;
}
.button-save.back:hover {
  background: #5a6268;
}

/* Colonne droite : Réservation */
.booking-section {
  flex: 1; /* 1/3 de la largeur */
  display: flex;
  flex-direction: column;
  gap: 15px;
  background: #fff;
  color: #000;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow-y: auto; /* Ajoute un scrolling interne si nécessaire */
}

.booking-section h3{
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
  text-align: left;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.input-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 1rem;
}

.ticket-selection {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 1rem;
}

.quantity-selection {
  width: 60px;
  padding: 5px;
  text-align: center;
}

.delete-ticket {
  background: #dc3545;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 6px;
  cursor: pointer;
  margin-left: 10px;
}

.delete-ticket:hover {
  background: #c82333;
}

.add-ticket {
  background: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s;
}

.add-ticket:hover {
  background: #0056b3;
}

.total {
  font-size: 1.2rem;
  font-weight: bold;
  color: #333;
  text-align: right;
}

/* Responsive Design */
@media (max-width: 768px) {
  .event-card {
    flex-direction: column;
    height: auto;  /* Permet à la carte de s'adapter au contenu */
  }

  .event-details,
  .booking-section {
    padding: 10px;
  }

  .input-modif,
  .ticket-selection,
  .quantity-selection {
    font-size: 0.9rem;
  }

  .button-save,
  .add-ticket {
    font-size: 0.9rem;
    padding: 8px 15px;
  }
}

@media (max-width: 480px) {
  .event-title {
    font-size: 1.5rem;
  }

  .input-modif,
  .ticket-selection,
  .quantity-selection {
    font-size: 0.8rem;
  }

  .button-save,
  .add-ticket {
    font-size: 0.8rem;
    padding: 6px 10px;
  }
}
</style>
