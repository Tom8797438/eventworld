<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-indigo-100 flex flex-col">
    <!-- Contenu principal -->
    <div class="flex flex-col md:flex-row gap-6 p-6 flex-1">
      <!-- Colonne droite : Aperçu et boutons -->
      <div class="md:w-1/3 bg-white rounded-lg shadow-lg p-6 border border-purple-200 space-y-6">
        <!-- Upload image -->
        <div>
          <label for="image" class="block text-sm font-medium text-gray-700 mb-2">Ajouter une image</label>
          <input
            type="file"
            id="image"
            @change="onImageSelect"
            class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-purple-50 file:text-purple-700 hover:file:bg-purple-100"
          />
        </div>

        <!-- Aperçu du billet -->
        <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
          <h3 class="text-lg font-bold text-center text-purple-800 mb-4">Aperçu du billet</h3>
          <div class="flex flex-col md:flex-row gap-4">
            <div class="flex-1 text-sm text-gray-700 space-y-2">
              <p><strong>Titre :</strong> {{ form.name }}</p>
              <p><strong>Description :</strong> <span class="whitespace-pre-wrap">{{ form.description }}</span></p>
              <p><strong>Lieu :</strong> {{ form.location }}</p>
              <p><strong>Date :</strong> {{ form.date_start }} - {{ form.date_end }}</p>
              <p><strong>Ville :</strong> {{ form.city }}</p>
              <p><strong>Type :</strong> {{ form.type_event }}</p>
              <p><strong>Nombre de places :</strong> {{ form.number_place }}</p>
            </div>
            <img
              v-if="imagePreview"
              :src="imagePreview"
              alt="Aperçu de l'image"
              class="w-20 h-20 object-cover rounded-lg border border-gray-300"
            />
          </div>
        </div>

        <!-- Boutons -->
        <div class="flex flex-col gap-3">
          <button
            @click="resetForm"
            class="w-full bg-red-600 text-white py-2 px-4 rounded-lg hover:bg-red-700 transition-colors duration-200"
          >
            Réinitialiser
          </button>
          <button
            @click="goBackToEvents"
            class="w-full bg-gray-600 text-white py-2 px-4 rounded-lg hover:bg-gray-700 transition-colors duration-200"
          >
            Retour
          </button>
          <button
            @click="createEvent"
            class="w-full bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700 transition-colors duration-200"
          >
            Valider
          </button>
        </div>
      </div>

      <!-- Colonne gauche : Formulaire -->
      <div class="md:w-2/3 bg-white rounded-lg shadow-lg p-6 border border-indigo-200 space-y-6">
        <form @submit.prevent="createEvent" class="space-y-6">
          <!-- Titre -->
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700 mb-2">Titre Évènement</label>
            <input
              v-model="form.name"
              type="text"
              id="name"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          <!-- Description et Lieu -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label for="description" class="block text-sm font-medium text-gray-700 mb-2">Description</label>
              <textarea
                v-model="form.description"
                id="description"
                required
                maxlength="1020"
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 resize-none"
                rows="4"
              ></textarea>
            </div>
            <div class="space-y-4">
              <div>
                <label for="location" class="block text-sm font-medium text-gray-700 mb-2">Lieu</label>
                <input
                  v-model="form.location"
                  type="text"
                  id="location"
                  required
                  placeholder="Salle de spectacle"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                />
              </div>
              <div>
                <label for="address" class="block text-sm font-medium text-gray-700 mb-2">Adresse</label>
                <input
                  v-model="form.address"
                  type="text"
                  id="address"
                  required
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                />
              </div>
            </div>
          </div>

          <!-- Dates, Type, Places -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label for="date_start" class="block text-sm font-medium text-gray-700 mb-2">Date début</label>
              <input
                v-model="form.date_start"
                type="date"
                id="date_start"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
            <div>
              <label for="date_end" class="block text-sm font-medium text-gray-700 mb-2">Date fin</label>
              <input
                v-model="form.date_end"
                type="date"
                id="date_end"
                :min="form.date_start"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
            <div>
              <label for="type_event" class="block text-sm font-medium text-gray-700 mb-2">Type</label>
              <select
                v-model="form.type_event"
                id="type_event"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              >
                <option v-for="(label, value) in types" :key="value" :value="value">{{ label }}</option>
              </select>
            </div>
          </div>

          <!-- Places, Code postal, Ville -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label for="number_place" class="block text-sm font-medium text-gray-700 mb-2">Places</label>
              <input
                v-model="form.number_place"
                type="number"
                id="number_place"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
            <div>
              <label for="postal_code" class="block text-sm font-medium text-gray-700 mb-2">Code Postal</label>
              <input
                v-model="form.postal_code"
                type="text"
                id="postal_code"
                required
                @input="validatePostalCode"
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
            <div>
              <label for="city" class="block text-sm font-medium text-gray-700 mb-2">Ville</label>
              <input
                v-model="form.city"
                type="text"
                id="city"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
          </div>

          <!-- Tarification -->
          <div>
            <div class="flex justify-between items-center mb-2">
              <label class="block text-sm font-medium text-gray-700">Tarification</label>
              <button
                @click.prevent="addPrice"
                class="bg-purple-600 text-white px-3 py-1 rounded-lg hover:bg-purple-700 transition-colors duration-200"
              >
                ➕
              </button>
            </div>
            <div v-for="(price, index) in form.price_categories" :key="index" class="flex gap-2 mb-2">
              <input
                v-model="price.label"
                placeholder="Type place (ex: Standard, VIP)"
                class="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              />
              <input
                v-model="price.value"
                type="number"
                placeholder="Prix en €"
                class="w-24 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              />
              <button
                @click.prevent="removePrice(index)"
                class="bg-red-600 text-white px-3 py-2 rounded-lg hover:bg-red-700 transition-colors duration-200"
              >
                ❌
              </button>
            </div>
          </div>

          <!-- Utilisateurs temporaires -->
          <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
            <div class="flex items-center gap-4 mb-4">
              <label class="text-sm font-medium text-gray-700">Utilisateurs temporaires :</label>
              <input
                type="number"
                v-model.number="event.temp_user_limit"
                min="0"
                max="12"
                placeholder="12"
                class="w-20 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
            <div class="grid gap-4 md:grid-cols-2">
              <div
                v-for="(user, index) in temporaryUserData"
                :key="index"
                class="bg-white p-4 rounded-lg border border-gray-200 shadow-sm"
              >
                <h4 class="font-semibold text-purple-800 mb-2">Démonstration type {{ index + 1 }}</h4>
                <div class="space-y-2">
                  <input
                    v-model="user.alias"
                    placeholder="Alias (ex: Sophie)"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  />
                  <input
                    v-model="user.email"
                    placeholder="E-mail (ex: sophie@email.com)"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  />
                  <div class="flex gap-4">
                    <label class="flex items-center">
                      <input type="checkbox" v-model="user.can_scan" class="mr-2" />
                      Scanner
                    </label>
                    <label class="flex items-center">
                      <input type="checkbox" v-model="user.can_sell" class="mr-2" />
                      Vendre
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Messages -->
          <p v-if="success" class="text-green-600 text-sm">L'inscription est faite !</p>
          <p v-if="error" class="text-red-600 text-sm">{{ error }}</p>

          <!-- Lien d'invitation -->
          <div v-if="createdEventId" class="bg-blue-50 p-4 rounded-lg border border-blue-200">
            <button
              @click="handleGenerateInvitation"
              class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-200 mb-2"
            >
              Lien d'invitation
            </button>
            <p v-if="invitationLink" class="text-sm text-blue-700">
              Lien généré :
              <a :href="invitationLink" target="_blank" class="underline break-all">{{ invitationLink }}</a>
            </p>
            <button
              v-if="invitationLink"
              @click="copyInvitationLink"
              class="bg-gray-600 text-white px-3 py-2 rounded-lg hover:bg-gray-700 transition-colors duration-200 text-sm mt-2"
            >
              📋 Copier lien
            </button>
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
  watch: {
    "event.temp_user_limit"(newVal) {
      this.generateTemporaryUserData();
    },
    "form.date_start"(newDateStart) {
      if (!this.form.date_end || this.form.date_end < newDateStart) {
        this.form.date_end = newDateStart;
      }
    },
  },
  methods: {
    limitTempUser(event) {
      let value = Number(event.target.value);
      if (value > 12) {
        value = 12;
        event.target.value = 12;
      }
      if (value < 0) {
        value = 0;
        event.target.value = 0;
      }
      this.event.temp_user_limit = value;
      this.generateTemporaryUserData();
    },
    generateTemporaryUserData() {
      const limit = this.event.temp_user_limit || 0;
      if (limit > 12) limit = 12;
      this.temporaryUserData = Array.from({ length: limit }, (_, i) => ({
        alias: `TempUser${i + 1}`,
        email: `temp${i + 1}@eventworld.com`,
        can_scan: true,
        can_sell: true
      }));
    },
    validatePostalCode(event) {
      const value = event.target.value;
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
        this.invitationLink = `${window.location.origin}/invitation/${invitation.id}`;
      } catch (err) {
        console.error('Erreur lors de la génération de l’invitation:', err);
      }
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
        formData.append("temp_user_temp_data", JSON.stringify(this.temporaryUserData));
        if (this.selectedImage) {
          formData.append('picture', this.selectedImage);
        }
        const formDataForTempUsers = new FormData();
        for (let pair of formData.entries()) {
          formDataForTempUsers.append(pair[0], pair[1]);
        }
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
      this.temporaryUserData = [];
      this.imagePreview = null;
      this.selectedImage = null;
    },
  },
};
</script>
