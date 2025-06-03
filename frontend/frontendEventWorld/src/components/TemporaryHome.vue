<template>
  <div class="temp-access">
    <h1>Bienvenue {{ alias }}</h1>
    <p>Événement : {{ eventName }}</p>

    <div class="actions">
      <button v-if="canScan" @click="goToScan">📷 Scanner</button>
      <button v-if="canSell" @click="goToSell">💸 Vendre</button>
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
