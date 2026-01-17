<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-indigo-100 flex flex-col">
    <!-- Contenu principal -->
    <div class="flex flex-col md:flex-row gap-6 p-6 flex-1">
      <!-- Colonne droite : Tableau de bord -->
      <div class="md:w-1/3 bg-white rounded-lg shadow-lg p-6 border border-purple-200">
        <div class="mb-6">
          <input
            type="text"
            placeholder="Rechercher un événement"
            v-model="searchQuery"
            class="w-full px-4 py-3 border border-purple-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-white text-gray-900 shadow-sm"
          />
        </div>
        <h2 class="text-3xl font-bold text-purple-800 mb-6 text-center">Tableau de Bord</h2>
        <div class="space-y-4">
          <div class="bg-gradient-to-r from-indigo-100 to-purple-100 p-4 rounded-lg shadow-md">
            <p class="text-lg font-semibold text-gray-800 mb-2">Statistiques des Événements</p>
            <div class="grid grid-cols-1 gap-3">
              <div class="flex items-center justify-between bg-white p-3 rounded-md shadow-sm">
                <div class="flex items-center">
                  <div class="w-8 h-8 bg-indigo-500 rounded-full flex items-center justify-center mr-3">
                    <span class="text-white font-bold text-sm">T</span>
                  </div>
                  <span class="text-gray-700">Total des événements :</span>
                </div>
                <strong class="text-indigo-600 text-lg">{{ events.length }}</strong>
              </div>
              <div class="flex items-center justify-between bg-white p-3 rounded-md shadow-sm">
                <div class="flex items-center">
                  <div class="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center mr-3">
                    <span class="text-white font-bold text-sm">A</span>
                  </div>
                  <span class="text-gray-700">Événements à venir :</span>
                </div>
                <strong class="text-purple-600 text-lg">{{ upcomingEvents }}</strong>
              </div>
              <div class="flex items-center justify-between bg-white p-3 rounded-md shadow-sm">
                <div class="flex items-center">
                  <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center mr-3">
                    <span class="text-white font-bold text-sm">P</span>
                  </div>
                  <span class="text-gray-700">Événements passés :</span>
                </div>
                <strong class="text-blue-600 text-lg">{{ pastEvents }}</strong>
              </div>
            </div>
          </div>
          <DashboardMenu
            :total="events.length"
            :upcoming="upcomingEvents"
            :past="pastEvents"
            :sold="soldPlaces"
            :available="availablePlaces"
          />
        </div>
      </div>

      <!-- Colonne gauche : Liste des événements -->
      <div class="md:w-2/3 bg-white rounded-lg shadow-lg p-6 border border-indigo-200 overflow-y-auto">
        <div class="space-y-4">
          <!-- Chargement en cours -->
          <div v-if="loading" class="text-center text-gray-500 text-lg">Loading...</div>

          <!-- Message d'erreur -->
          <div v-if="error" class="text-center text-red-500 text-lg">{{ error }}</div>

          <!-- Liste des événements -->
          <div v-if="filteredEvents.length" class="grid gap-4 lg:grid-cols-2 xl:grid-cols-3">
            <div
              v-for="event in filteredEvents"
              :key="event.id"
              class="bg-gradient-to-r from-white to-purple-50 border border-purple-200 rounded-lg p-4 shadow-md hover:shadow-lg transition-shadow duration-300 flex flex-col gap-4"
            >
              <!-- Conteneur pour image et détails -->
              <div class="flex flex-col md:flex-row md:items-center gap-4 flex-1">
                <!-- Image de l'événement -->
                <img
                  class="w-full md:w-24 md:h-24 object-cover rounded-lg flex-shrink-0"
                  :src="getEventImageUrl(event.picture)"
                  alt="Event Image"
                />

                <!-- Détails de l'événement -->
                <div class="flex-1">
                  <h3 class="text-xl font-bold text-purple-800 mb-2">{{ event.name || 'Nom non spécifié' }}</h3>
                  <p class="text-sm text-gray-600 mb-1"><strong>Date :</strong> {{ event.date_start || 'Non spécifiée' }}</p>
                  <p class="text-sm text-gray-600 mb-1"><strong>Description :</strong> {{ truncate(event.description, 50) || 'Non spécifiée' }}</p>
                  <p class="text-sm text-gray-600 mb-1"><strong>Lieu :</strong> {{ event.location || 'Non spécifié' }}</p>
                  <p class="text-sm text-gray-600 mb-1"><strong>Ville :</strong> {{ event.city || 'Non spécifiée' }}</p>
                  <p class="text-sm text-gray-600 mb-2">
                    <strong>Taux de remplissage :</strong>
                    <span :class="getFillingRate(event) > 80 ? 'text-green-600' : getFillingRate(event) > 50 ? 'text-orange-600' : 'text-red-600'">
                      {{ getFillingRate(event) }}%
                    </span>
                  </p>
                  <DashbordCardMenu
                    :sold="event.number_place - (event.remaining_places ?? event.number_place)"
                    :total="event.number_place"
                  />
                </div>
              </div>

              <!-- Boutons en bas -->
              <div class="flex flex-row gap-2 mt-auto justify-center">
                <button
                  v-if="showDelete"
                  class="bg-gradient-to-r from-indigo-500 to-indigo-600 text-white px-3 py-2 md:px-4 md:py-3 rounded-xl shadow-lg hover:from-indigo-600 hover:to-indigo-700 hover:shadow-xl transform hover:scale-105 transition-all duration-200 font-semibold text-sm md:text-base cursor-pointer"
                  @click="goToEventScanStatus(event)"
                >
                  Suivi
                </button>
                <button
                  v-if="showDelete"
                  class="bg-gradient-to-r from-purple-500 to-purple-600 text-white px-3 py-2 md:px-4 md:py-3 rounded-xl shadow-lg hover:from-purple-600 hover:to-purple-700 hover:shadow-xl transform hover:scale-105 transition-all duration-200 font-semibold text-sm md:text-base cursor-pointer"
                  @click="goToEventDetails(event)"
                >
                  Modifier
                </button>
                <button
                  v-if="showDelete"
                  class="bg-gradient-to-r from-red-500 to-red-600 text-white px-3 py-2 md:px-4 md:py-3 rounded-xl shadow-lg hover:from-red-600 hover:to-red-700 hover:shadow-xl transform hover:scale-105 transition-all duration-200 font-semibold text-sm md:text-base cursor-pointer"
                  @click.stop="deleteEventHandler(event)"
                >
                  Supprimer
                </button>
              </div>
            </div>
          </div>

          <!-- Aucun événement -->
          <div v-if="!loading && filteredEvents.length === 0" class="text-center text-gray-500 text-lg">
            Aucun événement trouvé.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useEventStore } from '@/stores/eventStore';
import { useRouter } from 'vue-router';
import { getEventImageUrl } from '@/utils/imageEvent';
import DashboardMenu from '@/components/charts/DashbordMenu.vue';
import DashbordCardMenu from '@/components/charts/DashbordCardMenu.vue';

const router = useRouter();
const eventStore = useEventStore();

const searchQuery = ref('');
const showDelete = ref(true);

// Fonction pour tronquer le texte
const truncate = (text, maxLength) => {
  if (!text) return '';
  return text.length > maxLength ? text.slice(0, maxLength) + '…' : text;
};

onMounted(() => {
  eventStore.fetchEvents();
});

// Liste des événements
const events = computed(() => eventStore.events);
const loading = computed(() => eventStore.loading);
const error = computed(() => eventStore.error);

// Filtrer les événements en fonction de la recherche
const filteredEvents = computed(() => {
  if (!searchQuery.value) return events.value;
  return events.value.filter((event) =>
    event.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

// Statistiques pour le tableau de bord
const upcomingEvents = computed(() =>
  events.value.filter((event) => new Date(event.date_start) > new Date()).length
);

const soldPlaces = computed(() =>
  events.value.reduce((sum, e) => sum + (e.number_place - (e.remaining_places ?? e.number_place)), 0)
);
const availablePlaces = computed(() =>
  events.value.reduce((sum, e) => sum + (e.remaining_places ?? e.number_place), 0)
);

const pastEvents = computed(() =>
  events.value.filter((event) => new Date(event.date_start) <= new Date()).length
);

// dashboard par card
const getFillingRate = (event) => {
  const total = event.number_place || 0;
  const remaining = event.remaining_places ?? total;
  const sold = total - remaining;
  return total > 0 ? Math.round((sold / total) * 100) : 0;
};

// Rediriger vers les détails de l'événement
const goToEventDetails = (event) => {
  router.push({
    name: 'EventDetails',
    params: { id: event.id },
  });
};

const goToEventScanStatus = (event) => {
  router.push({
    name: 'EventScanStatus',
    params: { id: event.id },
  });
};

// Supprimer un événement
const deleteEventHandler = async (event) => {
  if (confirm('Voulez-vous vraiment supprimer cet événement ?')) {
    try {
      await eventStore.deleteEvent(event.id);
    } catch (error) {
      console.error('Erreur lors de la suppression :', error);
    }
  }
};
</script>
