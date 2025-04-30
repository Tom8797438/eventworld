<template>
  <div class="main-container">
    <!-- Barre de navigation -->
    <header class="navbar">
      <div class="navbar-left">
        <img src="@/assets/styles/logo.png" alt="Logo" class="logo" @click="toggleMenu"/>
        <h1 class="app-title">Créer un événement</h1>
      </div>
      <!-- Menu déroulant -->
    <div class="dropdown-menu" :class="{ open: menuOpen }">
          <a class="sutitle-menu" @click="goToMenu">Menu</a>
          <a class="sutitle-menu" @click="goToScan">Scanner</a>
          <a class="sutitle-menu" @click="handleLogout">Déconnexion</a>
    </div>

      <div class="navbar-right">
        <img src="@/assets/styles/profile.png" alt="Profile" class="profile-picture" />
      </div>
    </header>

    <!-- Contenu principal -->
    <div class="content">
      <!-- Colonne gauche : Formulaire -->
      <div class="left-panel">
        <form @submit.prevent="createEvent" class="form-container">

          <!-- Titre -->
          <div class="form-group row">
            <div class="form-group-item">
              <label for="name">Evènement</label>
              <input v-model="form.name" type="text" id="name" required />
            </div>
          </div>

          <!-- Description -->
          <div class="form-group row">
            <div class="form-group-item">
              <label for="description">Description</label>
              <input 
              v-model="form.description" 
              type="text" 
              id="description" 
              required 
              maxlength="1920"
              />
            </div>    
          </div>

          <!-- Lieu et Adresse -->
          <div class="form-group row">
            <div class="form-group-item">
              <label for="location">Lieu</label>
              <input v-model="form.location" type="text" id="location" required placeholder="Salle de spectacle"/>
            </div>
            <div class="form-group-item">
              <label for="address">Adresse</label>
              <input v-model="form.address" type="text" id="address" required />
            </div>
          </div>

          <!-- Code postal et Ville -->
          <div class="form-group row">
            <div class="form-group-item">
              <label for="postal_code">Code Postal</label>
              <input v-model="form.postal_code" type="text" id="postal_code" required @input="validatePostalCode"/>
            </div>
            <div class="form-group-item">
              <label for="city">Ville</label>
              <input v-model="form.city" type="text" id="city" required />
            </div>
          </div>

          <!-- Dates -->
          <div class="form-group row">
            <div class="form-group-item">
              <label for="date_start">Date début</label>
              <input v-model="form.date_start" type="date" id="date_start" required />
            </div>
            <div class="form-group-item">
              <label for="date_end">Date fin</label>
              <input v-model="form.date_end" type="date" id="date_end" :min="form.date_start" required />
            </div>
          </div>

          <!-- Type et Nombre de places -->
          <div class="form-group row">
            <div class="form-group-item">
              <label for="type_event">Type</label>
              <select v-model="form.type_event" id="type_event" required>
                <option v-for="(label, value) in types" :key="value" :value="value">
                  {{ label }}
                </option>
              </select>
            </div>
            <div class="form-group-item">
              <label for="number_place">Nombre de places</label>
              <input v-model="form.number_place" type="number" id="number_place" required />
            </div>
          </div>

          <!-- Tarification -->
          <div class="form-group row">
            <div class="form-group-item">
              <div class="tarification-header">
                <label>Tarification</label>
                <button @click.prevent="addPrice" class="button-add-price">➕</button>
              </div>
              <div class="price-container" v-for="(price, index) in form.price_categories" :key="index">
                <input v-model="price.label" placeholder="Type place (ex: Standard, VIP)" />
                <input v-model="price.value" type="number" placeholder="Prix en €" />
                <button @click.prevent="removePrice(index)" class="button-remove-price">❌</button>
              </div>
            </div>
          </div>

          <!-- Utilisateur temporaire -->
          <div class="form-group">
            <label>
              <input type="checkbox" v-model="form.temporary_user" />
              Utilisateur temporaire
            </label>
                    <!-- Message de statut -->
        <p v-if="success" class="success">L'inscription est faite !
        </p>
        <p v-if="error" class="error">{{ error }}
        </p>

        <!-- Section pour la génération du lien d'invitation -->
        <div v-if="createdEventId" class="invitation-section">
            <button @click="handleGenerateInvitation" class="button-invite">Lien d'invitation</button>
              <p v-if="invitationLink">
                  Lien généré : 
                <a :href="invitationLink" target="_blank">{{ invitationLink }}</a>
              </p>
        </div>
          </div>

          <!-- Boutons Valider et Annuler -->
          <div class="form-group row buttons">
            <button type="submit" class="button-valid">Valider</button>
            <button type="button" class="button-cancel" @click="resetForm">Annuler</button>
          </div>
        </form>
      </div>

      <!-- Colonne droite : Construction du billet -->
      <div class="right-panel">
        <!-- Ajouter une image -->
        <div class="form-group image-upload">
          <label for="image">Ajouter une image</label>
          <input type="file" id="image" @change="handleImageUpload" />
        </div>

        <!-- Aperçu du billet -->
        <div class="ticket-preview">
          <h3>Aperçu du billet</h3>
          <div class="ticket">
            <img :src="imagePreview" alt="Aperçu de l'image" class="ticket-image" v-if="imagePreview" />
            <p><strong>Titre :</strong> {{ form.name }}</p>
            <pre class="ticket-description"><strong>Description :</strong> {{ form.description }}</pre>
            <p><strong>Lieu :</strong> {{ form.location }}</p>
            <p><strong>Date :</strong> {{ form.date_start }} - {{ form.date_end }}</p>
            <p><strong>Ville :</strong> {{ form.city }}</p>
            <p><strong>Type :</strong> {{ form.type_event }}</p>
            <p><strong>Nombre de places :</strong> {{ form.number_place }}</p>
            <div class="qr-code">
              <img :src="qrCodeImage" alt="QR Code" v-if="qrCodeImage" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref} from 'vue';
import { useEventStore } from '@/stores/eventStore';
import { useRouter } from 'vue-router';
import { useAuthStore } from "@/stores/authStore";


export default {
  name: 'CreateEvent',
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();

    const menuOpen = ref(false);
    const searchQuery = ref("");

    // Basculer le menu
    const toggleMenu = () => {
      menuOpen.value = !menuOpen.value;
    };

    // Rediriger vers la création d'événements
    const goToMenu = () => {
      router.push({ name: "menu" });
    };

    // Rediriger vers le scan QR Code
    const goToScan = () => {
      router.push({ name: "QrCodeScanner" });
    };

    // Fonction pour gérer la déconnexion
    const handleLogout = () => {
      authStore.logoutUser(router);
      router.push({ name: "login" });
    };

    return {
      menuOpen,
      searchQuery,
      toggleMenu,
      goToMenu,
      goToScan,
      handleLogout,
    };
  },
  data() {
    return {
      form: {
        name: '',
        description: '',
        date_start: '',
        date_end: '',
        location: '',
        address: '',
        postal_code: '',
        city: '',
        contact_email: '',
        contact_phone: '',
        type_event: '',
        number_place: null,
        price_categories: [],
        temporary_user: false,
      },
      types: {
        public: 'Public',
        private: 'Privé',
        limited: 'Limité',
      },
      success: false,
      error: null,
      createdEventId: null,
      invitationLink: '',
    };
  },
  watch: {
    "form.date_start"(newDateStart) {
      // Si date_end est vide ou antérieure à date_start, mettez-la à jour
      if (!this.form.date_end || this.form.date_end < newDateStart) {
        this.form.date_end = newDateStart;
      }
    },
  },
  methods: {
    
    validatePostalCode(event) {
    const value = event.target.value;
    // Supprime tout caractère non numérique
    event.target.value = value.replace(/\D/g, '');
    this.form.postal_code = event.target.value;
    },
    addPrice() {
      this.form.price_categories.push({ label: '', value: null });
    },
    removePrice(index) {
      this.form.price_categories.splice(index, 1);
    },
    handleImageUpload(event) {
      const file = event.target.files[0];
      console.log('Image sélectionnée :', file);
    },    
    async handleGenerateInvitation() {
        const eventStore = useEventStore();
        if (!this.createdEventId) return;
        try {
          const invitation = await eventStore.generateInvitation(this.createdEventId);
          // Génère le lien d’invitation sécurisé en se basant sur l'UUID de l'invitation.
          this.invitationLink = `${window.location.origin}/invitation/${invitation.id}`;
        } catch (err) {
          console.error('Erreur lors de la génération de l’invitation:', err);
        }
      },
    async createEvent() {
      const eventStore = useEventStore();
      try {
        await eventStore.createEvent(this.form);
        this.success = true;
        this.error = null;
        this.createdEventId = eventStore.events[0]?.id;
        confirm(
      `Événement créé avec succès !\n\nCopiez le lien d'invitation :\n${this.invitationLink}`
    );
        this.resetForm();
      } catch (err) {
        console.error('Erreur lors de la création :', err);
        this.success = false;
        this.error = "Erreur lors de la création de l'évènement.";
      }
    },



    resetForm() {
      this.form = {
        name: '',
        description: '',
        date_start: '',
        date_end: '',
        location: '',
        address: '',
        postal_code: '',
        city: '',
        contact_email: '',
        contact_phone: '',
        type_event: '',
        number_place: null,
        price_categories: [],
        temporary_user: false,
      };
    },
  },
};
</script>

<style scoped>
@import '@/assets/styles/Menu.css';


.card {
  width: 100vw;
  margin: 0 auto;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background: #fff;
}

.logo{
  width: 16%;
  height: 16%;
}

.title {
  text-align: center;
  margin-bottom: 18px;
  color: #000;
}

.app-title{
  display: flex;
  position: relative;
  left: 35%;
  font-size: 2em;
}

.form-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  color: #000;
}

.form-group.row {
  display: flex;
  justify-content: space-between; /* Ajoute un espace entre les champs */
  gap: 20px; /* Ajoute un espacement entre les colonnes */
}

.form-group-item {
  flex: 1; /* Chaque champ occupe une largeur égale */
}

.form-group-item label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group-item input,
.form-group-item select {
  width: 100%; /* S'assure que les champs occupent toute la largeur disponible */
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.price-container {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top:2%
}

.tarification-header {
  display: flex;
  align-items: center; /* Aligne verticalement le label et le bouton */
  justify-content: space-between; /* Ajoute de l'espace entre le label et le bouton */
  gap: 10px; /* Ajoute un espacement entre le label et le bouton */
}

.tarification-header label {
  font-weight: bold;
}

.button-add-price,
.button-remove-price {
  background: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  padding: 5px 10px;
}

.button-valid {
  background: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px;
  cursor: pointer;
}

.button-cancel {
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px;
  cursor: pointer;
}
.content {
  display: flex;
  flex-direction: row;
  gap: 20px;
}

.left-panel .right-panel{
  display: flex;
  flex-direction: column;
  gap: 20px;
  background: #f9f9f9;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.left-panel {
  flex: 1; /* 2/3 de la largeur */
}

.right-panel {
  flex: 2; /* 1/3 de la largeur */
}

.image-upload {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.ticket-preview h3{
  text-align: center;
  margin-bottom: 10px;
  color: #000;
  background-color: #bdbaba;
}

.ticket-preview {
  background: #fff;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%; /* S'assure que le conteneur occupe toute la largeur disponible */
  max-width: 100%; /* Empêche tout dépassement horizontal */
  box-sizing: border-box; /* Inclut les bordures et le padding dans la largeur totale */
 }

.ticket {
  display: flex;
  flex-direction: column;
  align-items: left;
  gap: 10px;
  width: 100%; /* S'assure que le contenu occupe toute la largeur disponible */
  max-width: 100%; /* Empêche tout dépassement horizontal */
  box-sizing: border-box; /* Inclut les bordures et le padding dans la largeur totale */
  color: #000;
}

.ticket-description {
  font-family: inherit;        /* Préserve la police générale */
  white-space: pre-wrap;       /* Respecte les retours à la ligne du texte */
  overflow-wrap: break-word;   /* Coupe les mots longs si nécessaire */
  word-break: break-word;      /* Force le retour à la ligne même pour les longs mots */
  max-height: 60%;           /* Limite la hauteur pour éviter l'agrandissement de ticket-preview */
  overflow-y: auto;            /* Ajoute une barre de défilement verticale si besoin */
  margin: 0;                   /* Supprime marges non désirées */
  padding: 0;                  /* Supprime padding non désiré */
}


.ticket img {
  max-width: 100%; /* Empêche l'image de dépasser la largeur du conteneur */
  height: auto; /* Maintient les proportions de l'image */
  border-radius: 10px;
}

.qr-code img {
  max-width: 150px; /* Limite la taille du QR code */
  height: auto; /* Maintient les proportions du QR code */
  margin: 0 auto; /* Centre le QR code */
}

.event-description {
  background: #fff;
  padding: 15px;
  border-radius: 4px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 100%; /* S'assure que le conteneur occupe toute la largeur disponible */
  max-width: 100%; /* Empêche tout dépassement horizontal */
  overflow: hidden; /* Cache tout contenu qui dépasse */
  box-sizing: border-box; /* Inclut les bordures et le padding dans la largeur totale */
}

.event-description textarea {
  width: 100%; /* S'adapte à la largeur du conteneur */
  max-width: 100%; /* Empêche tout dépassement horizontal */
  height: 100px; /* Limite la hauteur pour éviter les débordements */
  resize: vertical; /* Permet uniquement un redimensionnement vertical */
  border: 1px solid #ccc; /* Ajoute une bordure visible */
  padding: 10px;
  font-size: 1rem;
  color: #333;
  box-sizing: border-box; /* Inclut le padding et la bordure dans la largeur totale */
}

.event-description textarea:focus {
  outline: none;
  border-color: #6200ea;
  box-shadow: 0 0 5px rgba(98, 0, 234, 0.5);
  border-radius: 4px;
}


/* Responsive */
@media (max-width: 768px) {

  .logo{
    width: 40%;
  }

  .app-title{
    display: block;
    position: static;
    float: right;
    font-size: 0.8em;
    text-align: center;
  }

  .profile-picture {
      display: none;
  }
 
  .dropdown-menu{
    display: flex;
    position: relative;
    width: 62%;
    height: auto;
  }

  .form-group-item input,
  .form-group-item select {
    width: 100%; /* S'assure que les champs occupent toute la largeur disponible */
    padding: 8px;
    border: 1px solid #747373;
    border-radius: 6px;
    box-sizing: border-box;
  }

  .ticket {
    width: 100%; /* S'assure que le contenu occupe toute la largeur disponible */
    max-width: 100%; /* Empêche tout dépassement horizontal */
  }

  .qr-code img {
    max-width: 100px; /* Réduit la taille du QR code pour les petits écrans */
  }

  .event-description {
    width: 100%; /* S'assure que le conteneur occupe toute la largeur disponible en mobile */
    max-width: 100%; /* Empêche tout dépassement horizontal */
  }

  .event-description textarea {
    width: 100%; /* S'adapte à la largeur du conteneur */
    max-width: 100%; /* Empêche tout dépassement horizontal */
    height: 80px; /* Réduit la hauteur pour les petits écrans */
  }
  .content {
    flex-direction: column; /* Les colonnes passent en disposition verticale */
    width: 100%; /* S'assure que la colonne occupe toute la largeur disponible */
    max-width: 100%; /* Empêche tout dépassement horizontal */
    margin: auto; /* Centre la colonne */
    padding: 10px; /* Réduit le padding pour les petits écrans */
    box-sizing: border-box; /* Inclut le padding et les bordures dans la largeur totale */
    background: #85a1b4;
  }

  .right-panel {
    order: 1; /* Place la colonne droite en dessous de la colonne gauche */
    padding: 10px;
    max-height: 100vw; /* Permet à la colonne de s'adapter à la hauteur du contenu */
    background: #d9d9d9;
  }

  .ticket-preview {
    padding: 8px;
    gap: 8px;
    background: #cac8c8;
  }

  .ticket-description{
    max-height: 62px;
    overflow-y: auto;
  }

  .ticket-preview h3 {
    font-size: 1rem;
    margin-bottom: 8px;
    background: none;
  }

  .left-panel {
    order: -1; /* Place la colonne gauche en dessous */
  }
}
</style>