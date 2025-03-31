<template>
    <div class="container-public-event">

      <div class="container-event-card">
          <p v-if="store.loading">Chargement des événements publics...</p>
          <p v-if="store.error">{{ store.error }}</p>
          <p v-if="!store.events.length && !store.loading">Aucun événement public trouvé.</p>

        <EventCard
          class="public-event-card"
          :title="'Découvrez tous les événements'"
          :showDelete="false"
          :events="events"
          :loading="loading"
          :error="error"
          :noBackground="true" 
        /><!--noBackground : couleur de fond-->
        <div class="container-button">
          <button @click="goToLogin">Connexion</button>
        </div>

      </div>
    
    </div>

</template>

<script setup>
import { useEventStore } from '@/stores/eventStore';
import EventCard from './EventCard.vue';
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';


const router = useRouter();
const goToLogin = () => {
  router.push('/login');
};

const store = useEventStore();

onMounted(async () => {
    await store.fetchEvents(true);
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