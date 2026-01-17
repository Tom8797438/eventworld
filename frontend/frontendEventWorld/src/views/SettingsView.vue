<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-indigo-100 p-6">
    <div class="max-w-4xl mx-auto bg-white rounded-lg shadow-lg border border-purple-200 p-6 space-y-6">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-purple-800">Parametres</h1>
          <p class="text-sm text-gray-600">Paiement, abonnement et support</p>
        </div>
        <button
          class="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors duration-200 text-sm"
          @click="goBack"
        >
          Retour
        </button>
      </div>

      <div class="grid gap-4 md:grid-cols-2">
        <div class="bg-gray-50 rounded-lg p-4 border border-gray-200 space-y-2">
          <h2 class="text-lg font-semibold text-gray-800">Moyen de paiement</h2>
          <p class="text-sm text-gray-600">Carte actuelle : **** 4242</p>
          <button class="bg-indigo-600 text-white px-3 py-2 rounded-md text-sm hover:bg-indigo-700">
            Modifier le paiement
          </button>
        </div>
        <div class="bg-gray-50 rounded-lg p-4 border border-gray-200 space-y-2">
          <h2 class="text-lg font-semibold text-gray-800">Abonnement</h2>
          <p class="text-sm text-gray-600">Plan : Standard</p>
          <button class="bg-red-600 text-white px-3 py-2 rounded-md text-sm hover:bg-red-700">
            Resilier l'abonnement
          </button>
        </div>
        <div class="bg-gray-50 rounded-lg p-4 border border-gray-200 space-y-2 md:col-span-2">
          <h2 class="text-lg font-semibold text-gray-800">Support</h2>
          <p class="text-sm text-gray-600">Une question ? Contactez-nous.</p>
          <button class="bg-purple-600 text-white px-3 py-2 rounded-md text-sm hover:bg-purple-700">
            Contacter le support
          </button>
        </div>
      </div>

      <div class="bg-indigo-50 border border-indigo-200 rounded-lg p-4 text-sm text-indigo-700">
        Ces actions sont des placeholders à brancher a l'API.
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();
const goBack = () => {
  router.push({ name: 'menu' });
};
</script>
