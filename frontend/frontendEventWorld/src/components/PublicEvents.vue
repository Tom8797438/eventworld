<template>
    <div class="container-public-event">

      <div class="public-container-button">
          <button @click="goToLogin">Connexion</button>
      </div>
      <div class="search-bar">
          <input type="text" placeholder="Rechercher par titre"/>
          <button>Rechercher</button>
        </div>
      <div class="public-container-event-card">
          <p v-if="store.loading">Chargement des événements publics...</p>
          <p v-if="store.error">{{ store.error }}</p>
          <p v-if="!store.events.length && !store.loading">Aucun événement public trouvé.</p>

          <EventCard
          class="public-event-card"
          :title="'Découvrez tous les événements'"
          :showDelete="false"
          :events="store.events"
          :loading="store.loading"
          :error="store.error"
          :noBackground="true" 
          :fromPublic="true"
        /><!--noBackground : couleur de fond-->
        
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


<style scoped>
@import '@/assets/styles/PublicEvents.css';


</style>