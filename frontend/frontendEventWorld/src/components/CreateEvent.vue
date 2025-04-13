<template>
  <div class="card">
      <h1 class="title">Créer un Évènement</h1>
      <div class="create-event-container">
        <!-- Formulaire de création d'évènement -->
        <form @submit.prevent="createEvent" class="form-container">
          
          <div class="form-group">
            <label for="name">Evènement</label>
            <input v-model="form.name" type="text" id="name" required />
          </div>
    
          <div class="form-group">
            <label for="description">Description</label>
            <input v-model="form.description" type="text" id="description" required />
          </div>

          <div class="form-group">
            <label for="date">Date début</label>
            <input v-model="form.date_start" type="date" id="date_start" required />
          </div>

          <div class="form-group">
            <label for="date">Date fin</label>
            <input v-model="form.date_end" type="date" id="date_end" required />
          </div>
    
          <div class="form-group">
            <label for="location">Lieu</label>
            <input v-model="form.location" type="text" id="location" required />
          </div>
    
          <div class="form-group">
            <label for="address">Adresse</label>
            <input v-model="form.address" type="text" id="address" required />
          </div>

          <div class="form-group">
            <label for="postal_code">CP</label>
            <input v-model="form.postal_code" type="number" id="postal_code" required />
          </div>
    
          <div class="form-group">
            <label for="city">Ville</label>
            <input v-model="form.city" type="text" id="city" required />
          </div>
    
          <div class="form-group">
            <label for="number_place">Nbr Places</label>
            <input v-model="form.number_place" type="number" id="number_place" required />
          </div>
          
          <div class="form-group">
            <label for="type_event">Type</label>
            <select v-model="form.type_event" id="type_event" required>
              <option v-for="(label, value) in types" :key="value" :value="value">
                {{ label }}
              </option>
            </select>
          </div>
          <div class="form-group">
          <label>Prix</label>
          <button @click.prevent="addPrice" class="button-add-price">➕</button>
        </div>

          <div class="form-group">
            <button type="submit" class="button-valid">Valider</button>
          </div>
          
        </form>
    
        <!-- Message de statut -->
        <p v-if="success" class="success">well done !
        </p>
        <p v-if="error" class="error">{{ error }}
        </p>

      </div>
      <div class="form-group">
          <div class="price-container" v-for="(price, index) in form.price_categories" :key="index">
            <label>Tarification</label>
            <input v-model="price.label" placeholder="Ex: Standard, VIP" />
            <input v-model="price.value" type="number" placeholder="Prix en €" />
            <button @click.prevent="removePrice(index)" class="button-remove-price">❌</button>
          </div>
        </div>
    </div>
  </template>
  
  <script>
  import { useEventStore } from '@/stores/eventStore';
  // import { createEvent } from '@/utils/api_utils';
  
  export default {
    name: 'CreateEvent',
    data() {
      return {
        form: {
          name: '',
          description: '',
          date_start: '',
          date_end: '',
          location: '',
          address: '',
          postal_code:'',
          city: '',
          type_event:'',
          number_place: null,
          price_categories: [],
        },
        types: {
        public: "Public",
        private: "Privé",
        limited: "Limité",
      },
        success: false,
        error: null,
      };
    },
    methods: {
      addPrice() { this.form.price_categories.push({ label: '', value: null }); },
      removePrice(index) { this.form.price_categories.splice(index, 1); },
      async createEvent() {
  const eventStore = useEventStore();

  try {
    console.log('Payload envoyé:', { data: this.form });
    await eventStore.createEvent(this.form);
    this.success = true;
    this.error = null;
    this.resetForm();
  } catch (err) {
    console.error('Erreur lors de la création:', err.response?.data || err.message);
    this.success = false;
    this.error = 'Erreur lors de la création de l\'évènement.';
  }
},

      resetForm() {
        this.form = {
          name: '',
          event_date: '',
          description: '',
          location: '',
          address: '',
          city: '',
          total_seats: null,
          price_standard: null,
          price_vip: null,
          price_pmr: null,
        };
      },
    },
  };
  </script>
  
  <style scoped>
@import '@/assets/styles/CreateEvent.css'
</style>
