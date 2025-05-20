<template>
  <div class="main-container">
    
    <!-- Contenu principal -->
    <div class="content">
      <!-- Colonne droite : Construction du billet -->
      <div class="right-panel">
        <!-- Ajouter une image -->
        <div class="form-group image-upload">
          <label for="image">Ajouter une image</label>
          <input type="file" id="image" @change="onImageSelect" />
        </div>

        <!-- Aperçu du billet -->
        <div class="ticket-preview">
          <h3>Aperçu du billet</h3>
          <div class="ticket-content">
            
            <div class="ticket-details">
              <p><strong>Titre :</strong> {{ form.name }}</p>
              <pre class="ticket-description"><strong>Description :</strong> {{ form.description }}</pre>
              <p><strong>Lieu :</strong> {{ form.location }}</p>
              <p><strong>Date :</strong> {{ form.date_start }} - {{ form.date_end }}</p>
              <p><strong>Ville :</strong> {{ form.city }}</p>
              <p><strong>Type :</strong> {{ form.type_event }}</p>
              <p><strong>Nombre de places :</strong> {{ form.number_place }}</p>
            </div>
            <!-- Afficher l'image si elle est sélectionnée -->
            <img :src="imagePreview" alt="Aperçu de l'image" class="ticket-image" v-if="imagePreview" />
          </div>
        </div>
        
        <!-- Boutons Valider et Annuler -->
        <div class="form-group row buttons">
            <div><button type="button" class="button-cancel" @click="resetForm">Réinitialiser</button></div>
            <div><button type="button" class="button-cancel-back" @click="goBackToEvents">Retour</button></div>
            <div><button type="submit" class="button-valid" @click="createEvent">Valider</button></div>
        </div>
      </div>
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
              maxlength="1020"
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
          <div class="temporary-user-section">
            <div class="user-limit-input">
              <label>Utilisateurs temporaires :</label>
              <input type="number" v-model.number="event.temp_user_limit" min="0" max="100" />
            </div>

            <div class="temporary-user-list">
              <div class="temporary-user-card" v-for="(user, index) in temporaryUserData" :key="index">
                <h4>Démonstration type {{ index + 1 }}</h4>
                <input v-model="user.alias" placeholder="Alias (ex: Sophie)" />
                <input v-model="user.email" placeholder="E-mail (ex: sophie@email.com)" />
                <label><input type="checkbox" v-model="user.can_scan" /> Peut scanner</label>
                <label><input type="checkbox" v-model="user.can_sell" /> Peut vendre</label>
              </div>
            </div>
          </div>

              <div v-if="temporaryUsers && temporaryUsers.length">
                <h3>Utilisateurs temporaires créés !</h3>
                <!-- <ul>
                  <li v-for="user in temporaryUsers" :key="user.username">
                    {{ user.username }} - Scan: <a :href="user.scan_link" target="_blank">Lien scan</a>,
                    Vente: <a :href="user.sell_link" target="_blank">Lien vente</a>
                  </li>
                </ul> -->
              </div>
         
          

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
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, reactive } from 'vue';
import { useEventStore } from '@/stores/eventStore';
import { useRouter } from 'vue-router';
import { useAuthStore } from "@/stores/authStore";
import { handleImageUpload } from '@/utils/imageEvent';
import { confirmAndNavigate } from '@/utils/navigation';


export default {
  
  setup() {
    const eventStore = useEventStore();
    const invitationLink = computed(() => eventStore.invitationLink);
    const authStore = useAuthStore();
    const router = useRouter();

    const menuOpen = ref(false);
    const searchQuery = ref("");

    const event = reactive({
      name: '',
      start_date: '',
      end_date: '',
      temp_user_limit: 0,
    });
    const submitEvent = async () => {
      console.log("Submitting event:", event);
      await eventStore.createEventWithTemporaryUsers(event);
    };
    const loading = computed(() => eventStore.loading);
    const error = computed(() => eventStore.error);
    const temporaryUsers = computed(() => eventStore.temporaryUsers);

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


    const goBackToEvents = () => {
      confirmAndNavigate("Êtes-vous sûr de vouloir revenir au menu ?", router, "/Menu");
    };

    return {
      event,
      loading,
      error,
      temporaryUsers,
      submitEvent,
      menuOpen,
      searchQuery,
      toggleMenu,
      goToMenu,
      goToScan,
      handleLogout,
      goBackToEvents,
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
      selectedImage: null, 
      imagePreview: null,  

      temporaryUserData: [
      {
        alias: '',
        email: '',
        can_scan: true,
        can_sell: true
      }
    ]
    };
  },
  watch: 
  {
  "event.temp_user_limit"(newVal) {
    this.generateTemporaryUserData();
  },
  "form.date_start"(newDateStart) {
    // Si date_end est vide ou antérieure à date_start, mettez-la à jour
    if (!this.form.date_end || this.form.date_end < newDateStart) {
      this.form.date_end = newDateStart;
    }
  },
  },
  methods: {
    
    generateTemporaryUserData() {
    const limit = this.event.temp_user_limit || 0;
    this.temporaryUserData = Array.from({ length: limit }, (_, i) => ({
      alias: `TempUser${i + 1}`,
      email: `temp${i + 1}@eventworld.com`,
      can_scan: true,
      can_sell: true
    }));
    },

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
      
      onImageSelect(event) {
        const { file, preview } = handleImageUpload(event);
        this.selectedImage = file;
        this.imagePreview = preview;
  },

async createEvent() {
  const eventStore = useEventStore();
  try {
    const formData = new FormData();
    for (const key in this.form) {
      const value = this.form[key];
      formData.append(key, Array.isArray(value) ? JSON.stringify(value) : value);
    }

    formData.append('temp_user_limit', this.event.temp_user_limit);
    formData.append("temp_user_temp_data",JSON.stringify(this.temporaryUserData));

    if (this.selectedImage) {
      formData.append('picture', this.selectedImage);
    }

    // 👇 Appel 1 : créer l'événement
    //await eventStore.createEvent(formData);

    // ✅ Crée une copie propre
    const formDataForTempUsers = new FormData();
    for (let pair of formData.entries()) {
      formDataForTempUsers.append(pair[0], pair[1]);
    }

    // 👇 Appel 2 : créer les utilisateurs temporaires
    await eventStore.createEventWithTemporaryUsers(formDataForTempUsers);

    this.success = true;
    this.error = null;
    confirm('Événement créé avec succès !');
    this.resetForm();
  } catch (err) {
    this.success = false;
    this.error = 'Erreur lors de la création de l\'évènement.';
  }
},
// fonction à modifier ci dessus

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
        temporaryUsers: '',
      };
      this.event.temp_user_limit = 0;
      this.temporaryUserData = []; // 👈 reset ici
      this.imagePreview = null;
      this.selectedImage = null;
    },
  },
};
</script>

<style scoped>
@import '@/assets/styles/Menu.css';
@import '@/assets/styles/CreateEvent.css';
</style>