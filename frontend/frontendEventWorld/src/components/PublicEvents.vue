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
  router.push('/login');
};

const store = usePublicEventStore();

onMounted(async () => {
    await store.fetchPublicEvents(true);
});
</script>

<!-- <script>
import EventCard from './EventCard.vue'
import { useEventStore } from '@/stores/eventStore'

export default {
  name: 'PublicEvents',
  components: { EventCard },
  data() {
    return {
      events: [],
      loading: false,
      error: '',
    }
  },
  async mounted() {
    const store = useEventStore()
    this.loading = true
    try {
      await store.fetchEvents()
      this.events = store.events
    } catch (e) {
      this.error = "Erreur de chargement"
    } finally {
      this.loading = false
    }
  }
}
</script> -->

<style scoped>
@import '@/assets/styles/PublicEvents.css';


</style>