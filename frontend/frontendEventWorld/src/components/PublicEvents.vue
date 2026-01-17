<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-indigo-100 p-6">
    <div class="max-w-7xl mx-auto space-y-6">
      <!-- Bouton de connexion -->
      <div class="flex justify-end">
        <button
          @click="goToLogin"
          class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors duration-200"
        >
          Connexion
        </button>
      </div>

      <!-- Barre de recherche -->
      <div class="flex gap-4 max-w-md">
        <input
          type="text"
          placeholder="Rechercher par titre"
          class="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        />
        <button class="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors duration-200">
          Rechercher
        </button>
      </div>

      <!-- Contenu des événements -->
      <div class="space-y-4">
        <p v-if="store.loading" class="text-center text-gray-500 text-lg">Chargement des événements publics...</p>
        <p v-if="store.error" class="text-center text-red-500 text-lg">{{ store.error }}</p>
        <p v-if="!store.events.length && !store.loading" class="text-center text-gray-500 text-lg">Aucun événement public trouvé.</p>

        <EventCard
          class="grid gap-6 md:grid-cols-2 lg:grid-cols-3"
          :title="'Découvrez tous les événements'"
          :showDelete="false"
          :events="store.events"
          :loading="store.loading"
          :error="store.error"
          :noBackground="true"
          :fromPublic="true"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { usePublicEventStore } from '@/stores/publicEventStore';
import EventCard from './EventCard.vue';
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';


const router = useRouter();
const goToLogin = () => {
  router.push('/FirstPage'); // Redirige vers la page de connexion
};

const store = usePublicEventStore();

onMounted(async () => {
    await store.fetchPublicEvents(true);
});
</script>