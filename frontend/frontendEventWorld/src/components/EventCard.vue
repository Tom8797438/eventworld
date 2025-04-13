<template>
    <div class="card" :class="{ 'no-background': noBackground }">
      <!-- <h1 class="first-title">Évènement à venir</h1> -->
      <h1 class="first-title">{{ title || 'Évènement à venir' }}</h1>
      <slot name="header-action" />
      <!-- Chargement en cours -->
      <div v-if="loading" class="loading">Loading...</div>
  
      <!-- Message d'erreur -->
      <div v-if="error" class="error">{{ error }}</div>
  
      <!-- Liste des événements en forme de cartes virtuel -->
      <div v-if="events.length" class="events-container">
        
        <div v-for="event in events" 
          :key="event.id" 
          class="event-card" 
          @click="goToEventDetails(event)"
          > 
          <h3 class="event-title">{{ event.name }}         
          <font-awesome-icon  
          v-if="showDelete"
            @click.stop="deleteEventHandler(event)" 
            :icon="['fas', 'trash']" 
            class="delete-icon"
        /> </h3>
          <!-- <p><strong>ID:</strong> {{ event.id }}</p> -->
          <p><strong>Date:</strong> {{ event.date_start || 'Not specified' }}</p>
          <p><strong>Location:</strong> {{ event.location || 'Not specified' }}</p>
          <p><strong>City:</strong> {{ event.city || 'Not specified' }}</p>
          <p><strong>Place restantes:</strong> {{ event.number_place || 'Not specified' }}</p>
        </div>
        
      </div>
  
      <!-- Aucun événement -->
      <div v-if="!loading && events.length === 0" class="no-events">
        No events found.
      </div>
    </div>
  </template>
  
  <script>
  import { useEventStore } from '@/stores/eventStore';
  import { usePublicEventStore } from '@/stores/publicEventStore'; // 👈 important
  import { mapState, mapActions } from 'pinia';
  
  export default {
    name: 'EventCard',
    props: {
      title: String,
      showDelete: {
        type: Boolean,
        default: true,
      },
      noBackground: {
        type: Boolean,
        default: false,
      },
      fromPublic: {
        type: Boolean,
        default: false,
      }
    },
  
    computed: {
      ...mapState(useEventStore, ['events', 'loading', 'error']),
    },
  
    methods: {
      ...mapActions(useEventStore, ['fetchEvents', 'setSelectedEvent', 'deleteEvent']),
  
      async deleteEventHandler(event) {
        if (confirm("Voulez-vous vraiment supprimer cet événement ?")) {
          try {
            await this.deleteEvent(event.id);
          } catch (error) {
            console.error("Erreur lors de la suppression :", error);
          }
        }
      },
  
      goToEventDetails(event) {
        console.log('Événement sélectionné : ', event);
  
        if (this.fromPublic) {
          const publicStore = usePublicEventStore(); // 👈 store public
          publicStore.setSelectedEvent(event);       // 👈 on stocke dans le bon store
          this.$router.push({
            name: 'PublicEventDetail',
            params: { id: event.id }
          });
        } else {
          this.setSelectedEvent(event); // store privé
          this.$router.push({
            name: 'EventDetails',
          });
        }
      }
    },
  
    mounted() {
      if (!this.events.length) {
        this.fetchEvents(); 
      }
    }
  };
  </script>
  
  
  
  <style scoped>
@import '@/assets/styles/Event.css'
  </style>
  