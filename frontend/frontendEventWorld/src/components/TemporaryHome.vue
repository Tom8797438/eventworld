<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-indigo-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white p-8 rounded-lg shadow-lg text-center">
      <div>
        <h1 class="text-3xl font-bold text-purple-800">Bienvenue {{ alias }}</h1>
        <p class="text-gray-600 mt-2">Événement : {{ eventName }}</p>
      </div>

      <div class="space-y-4">
        <button
          v-if="canScan"
          @click="goToScan"
          class="w-full bg-indigo-600 text-white py-3 px-6 rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200 text-lg"
        >
          📷 Scanner
        </button>
        <button
          v-if="canSell"
          @click="goToSell"
          class="w-full bg-purple-600 text-white py-3 px-6 rounded-lg hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-colors duration-200 text-lg"
        >
          💸 Vendre
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'TemporaryHome',
  data() {
    return {
      alias: '',
      canScan: false,
      canSell: false,
      eventName: '',
      token: this.$route.params.token
    };
  },
  async created() {
    try {
      const response = await axios.get(`/api/access/temp/${this.token}`);
      this.alias = response.data.alias;
      this.canScan = response.data.can_scan;
      this.canSell = response.data.can_sell;
      this.eventName = response.data.event;
    } catch (err) {
      alert("Lien invalide ou expiré");
      this.$router.push("/");
    }
  },
  methods: {
    goToScan() {
      this.$router.push(`/scanner/${this.token}`);
    },
    goToSell() {
      this.$router.push(`/vente/${this.token}`);
    }
  }
};
</script>
