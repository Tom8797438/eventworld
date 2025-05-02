<template>
  <div class="overlay" v-if="event">
    <div class="event-card" @click.stop>
      <!-- Colonne gauche : Détails de l'événement -->
      <div class="event-details">
        <h2 class="event-title">{{ event.name || 'Non spécifié' }}</h2>
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

        <h3>Réserver vos places</h3>
        <div v-for="(ticket, index) in selectedTickets" :key="index" class="input-group">
          <!-- Si un seul prix -->
          <p v-if="isSinglePriceEvent">
            <strong>{{ ticketTypes[0]?.price?.label || 'Gratuit' }} :</strong> {{ ticketTypes[0]?.price?.value || '0' }} €
          </p>
          <!-- Si plusieurs prix -->
          <div v-else>
            <label>Type de place</label>
            <select v-model="ticket.type" class="ticket-selection">
              <option v-for="option in ticketTypes" :key="option.name" :value="option.name">
                {{ option.price.label }} - {{ option.price.value || 'Gratuit' }} €
              </option>
            </select>
          </div>
          <div class="input-group">
            <label>Quantité</label>
            <input type="number" min="1" v-model="ticket.quantity" class="quantity-selection" />
            <!-- Bouton supprimer uniquement si ce n'est pas gratuit -->
            <button v-if="!isFreeEvent" class="delete-ticket" @click="removeTicket(index)">❌</button>
          </div>
        </div>

        <!-- Bouton "Ajouter un autre ticket" uniquement si ce n'est pas gratuit et qu'il y a plusieurs prix -->
        <button v-if="!isFreeEvent && !isSinglePriceEvent" class="add-ticket" @click="addTicket">➕ Ajouter un autre ticket</button>
        <p class="total">Total : {{ total }} €</p>
        <button @click="bookTickets">Réserver vos places</button>
      </div>
    </div>
  </div>

  <p v-else-if="error" class="error">{{ error }}</p>
  <p v-else>Chargement...</p>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useTicketStore } from '@/stores/ticketStore';
import { fetchInvitationById } from '@/utils/api_utils';

export default {
  name: 'InvitationEventView',
  setup() {
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
    const ticketTypes = ref([]);
    const selectedTickets = ref([]);

    onMounted(async () => {
      try {
        const invitation = await fetchInvitationById(invitationId);
        event.value = invitation.event;

        if (event.value.price_categories && Object.keys(event.value.price_categories).length > 0) {
          ticketTypes.value = Object.entries(event.value.price_categories).map(([key, value]) => ({
            name: key,
            label: key.charAt(0).toUpperCase() + key.slice(1),
            price: value,
          }));
        } else {
          // Ajouter une option "Gratuit" si aucun prix n'est défini
          ticketTypes.value = [{ name: 'free', label: 'Gratuit', price: { value: 0, label: 'Gratuit' } }];
        }

        selectedTickets.value = [{ type: ticketTypes.value[0]?.name || 'free', quantity: 1 }];
      } catch (err) {
        console.error("Erreur lors du chargement de l'invitation :", err);
        error.value = "Invitation invalide ou expirée.";
      }
    });

    const total = computed(() => {
      return selectedTickets.value.reduce((sum, ticket) => {
        const ticketType = ticketTypes.value.find(t => t.name === ticket.type);
        return sum + (ticket.quantity * (ticketType?.price.value || 0));
      }, 0);
    });

    // Détermine si l'événement est gratuit
    const isSinglePriceEvent = computed(() => {
        return ticketTypes.value.length === 1;
      });

    const isFreeEvent = computed(() => {
      return isSinglePriceEvent.value && ticketTypes.value[0].price.value === 0;
    });

    const addTicket = () => {
      selectedTickets.value.push({ type: ticketTypes.value[0]?.name || 'free', quantity: 1 });
    };

    const removeTicket = (index) => {
      selectedTickets.value.splice(index, 1);
    };

    const bookTickets = async () => {
      const ticketsToCreate = selectedTickets.value
        .filter(ticket => ticket.quantity > 0)
        .map(ticket => {
          const ticketType = ticketTypes.value.find(t => t.name === ticket.type);
          return {
            firstname: firstname.value,
            lastname: lastname.value,
            email: email.value,
            phone: phone.value,
            quantity: ticket.quantity,
            price: ticketType?.price.value || 0,
            ticket_type: ticketType?.price.label || 'Gratuit',
            event_name: event.value.name,
          };
        });

      if (ticketsToCreate.length === 0) {
        alert("Veuillez sélectionner au moins un ticket.");
        return;
      }

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
      firstname.value = "";
      lastname.value = "";
      email.value = "";
      phone.value = "";
      selectedTickets.value = [{ type: ticketTypes.value[0]?.name || 'free', quantity: 1 }];
    };

    const goBackToAccueil = () => {
      router.push('/accueil');
    };

    return {
      event,
      error,
      firstname,
      lastname,
      email,
      phone,
      selectedTickets,
      ticketTypes,
      total,
      isFreeEvent,
      bookTickets,
      addTicket,
      removeTicket,
      goBackToAccueil,
    };
  },
};
</script>

<style scoped>

/* Conteneur principal */
/* .overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  overflow-y: auto; 
  padding: 10px; 
  box-sizing: border-box;  
}*/

.overlay {
  display: flex;
  flex-direction: column;
  height: 100vh; 
  width: 100vw; /* Occupe toute la largeur de la fenêtre */
  background: linear-gradient(135deg, #7ab8fa, #62a9f5, #007bff); /* Dégradé moderne */
  padding: 20px;
  box-sizing: border-box; /* Inclut les bordures et le padding dans les dimensions */
  overflow: hidden; /* Empêche le scrolling */
  justify-content: center;
  align-items: center;
}

/* Carte principale */
.event-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: row;
  max-width: 1200px;
  height: 100vh; 
  width: 100vw;
  overflow: hidden;
  height: auto;
  max-height: 90vh; /* Limite la hauteur pour éviter de dépasser l'écran */
  overflow-y: auto; /* Permet le défilement interne si le contenu dépasse */
}

/* Colonne gauche : Détails de l'événement */
.event-details {
  flex: 1;
  padding: 20px;
  background: #ccc;
  color:#000;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.event-title {
  font-size: 1.8rem;
  font-weight: bold;
  color: #333;
  text-align: center;
}

.description {
  width: 100%;
  min-height: 100px;
  resize: none;
  border: 1px solid #ccc;
  border-radius: 6px;
  padding: 10px;
  font-size: 1rem;
  color: #333;
  background: #fff;
  box-sizing: border-box;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.description:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

/* Colonne droite : Réservation */
.booking-section {
  flex: 1;
  padding: 20px;
  background: #fff;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.booking-section h3 {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
  text-align: center;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.input-group label {
  font-weight: bold;
  color: #333;
}

.input-group input,
.ticket-selection,
.quantity-selection {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 1rem;
  box-sizing: border-box;
}

.input-group input:focus,
.ticket-selection:focus,
.quantity-selection:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

.ticket-selection {
  appearance: none;
  background: #fff;
  cursor: pointer;
}

.quantity-selection {
  width: 60px;
  text-align: center;
}

/* Boutons */
.add-ticket,
.delete-ticket,
button {
  background: #007bff;
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s;
}

.add-ticket:hover,
button:hover {
  background: #0056b3;
}

.delete-ticket {
  background: #dc3545;
  margin-left: 10px;
}

.delete-ticket:hover {
  background: #c82333;
}

.total {
  font-size: 1.2rem;
  font-weight: bold;
  color: #333;
  text-align: right;
}

/* Messages d'erreur */
.error {
  color: red;
  font-weight: bold;
  text-align: center;
  margin-top: 20px;
}

/* Responsive Design */
.event-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: row;
  max-height: 100vh;
  width: 100vw;
  /* overflow: hidden; */
  height: auto;
}

/* Colonne gauche : Détails de l'événement */
.event-details {
  flex: 1;
  padding: 20px;
  background: #f9f9f9;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.event-title {
  font-size: 1.8rem;
  font-weight: bold;
  color: #333;
  text-align: center;
}

.description {
  width: 100%;
  min-height: 100px;
  resize: none;
  border: 1px solid #ccc;
  border-radius: 6px;
  padding: 10px;
  font-size: 1rem;
  color: #333;
  background: #fff;
  box-sizing: border-box;
}

.description:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

/* Colonne droite : Réservation */
.booking-section {
  flex: 1;
  padding: 20px;
  background: #fff;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.input-group label {
  font-weight: bold;
  color: #333;
}

.input-group input,
.ticket-selection,
.quantity-selection {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 1rem;
  box-sizing: border-box;
}

.input-group input:focus,
.ticket-selection:focus,
.quantity-selection:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

.ticket-selection {
  appearance: none;
  background: #fff;
  cursor: pointer;
}

.quantity-selection {
  width: 60px;
  text-align: center;
}

/* Boutons */
.add-ticket,
.delete-ticket,
button {
  background: #007bff;
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s;
  width: auto; /* Ajuste automatiquement la largeur */
}

.add-ticket:hover,
button:hover {
  background: #0056b3;
}

.delete-ticket {
  background: #dc3545;
  margin-left: 10px;
}

.delete-ticket:hover {
  background: #c82333;
}

.total {
  font-size: 1.2rem;
  font-weight: bold;
  color: #333;
  text-align: right;
}

/* Messages d'erreur */
.error {
  color: red;
  font-weight: bold;
  text-align: center;
  margin-top: 20px;
}

/* Responsive Design */

/* Tablettes et petits écrans */
@media (max-width: 768px) {
  .event-card {
    flex-direction: column;
    /* max-width: 100%; */
    height: auto;
    border-radius:0;

  }

  .event-details,
  .booking-section {
    padding: 15px;
  }

  .event-title {
    font-size: 1.5rem;
  }

  .add-ticket,
  .delete-ticket,
  button {
    font-size: 0.9rem;
    padding: 8px 12px;
  }

  /* Boutons côte à côte */
  .button-group {
    display: flex;
    justify-content: space-between;
    gap: 10px; /* Espacement entre les boutons */
  }

  .add-ticket,
  .delete-ticket,
  button {
    flex: 1; /* Les boutons prennent une largeur égale */
    max-width: 48%; /* Limite la largeur pour qu'ils soient côte à côte */
  }

  .total {
    font-size: 1rem;
  }
}

/* Smartphones */
@media (max-width: 480px) {
  .event-title {
    font-size: 1.2rem;
  }

  .input-group input,
  .ticket-selection,
  .quantity-selection {
    font-size: 0.8rem;
  }

  .add-ticket,
  .delete-ticket,
  button {
    font-size: 0.8rem;
    padding: 6px 10px;
  }

  .button-group {
    gap: 5px; /* Réduit l'espacement entre les boutons */
  }

  .add-ticket,
  .delete-ticket,
  button {
    max-width: 48%; /* Assure que les boutons restent côte à côte */
  }

  .total {
    font-size: 0.9rem;
  }

  .overlay {
    padding: 5px; /* Réduction du padding pour les très petits écrans */
  }
}
</style>