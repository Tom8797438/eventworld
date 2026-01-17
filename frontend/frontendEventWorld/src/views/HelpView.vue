<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-indigo-100 p-6">
    <div class="max-w-4xl mx-auto bg-white rounded-lg shadow-lg border border-purple-200 p-6 space-y-6">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-purple-800">Aide</h1>
          <p class="text-sm text-gray-600">Comment utiliser l'application</p>
        </div>
        <button
          class="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors duration-200 text-sm"
          @click="goBack"
        >
          Retour
        </button>
      </div>

      <div class="space-y-4">
        <div class="bg-gray-50 rounded-lg p-4 border border-gray-200">
          <h2 class="text-lg font-semibold text-gray-800">1. Creer un evenement</h2>
          <p class="text-sm text-gray-600">
            Va dans "Nouvel evenement", renseigne les infos, les prix et ajoute les utilisateurs temporaires si besoin.
          </p>
        </div>
        <div class="bg-gray-50 rounded-lg p-4 border border-gray-200">
          <h2 class="text-lg font-semibold text-gray-800">2. Vendre et generer des tickets</h2>
          <p class="text-sm text-gray-600">
            Utilise la page de l'evenement pour reserver et generer les tickets.
          </p>
        </div>
        <div class="bg-gray-50 rounded-lg p-4 border border-gray-200">
          <h2 class="text-lg font-semibold text-gray-800">3. Scanner les tickets</h2>
          <p class="text-sm text-gray-600">
            Ouvre "Scanner" et verifie les QR codes. Le premier scan valide le ticket.
          </p>
        </div>
        <div class="bg-gray-50 rounded-lg p-4 border border-gray-200">
          <h2 class="text-lg font-semibold text-gray-800">4. Suivi</h2>
          <p class="text-sm text-gray-600">
            Depuis le menu, utilise "Suivi" pour voir les stats et envoyer les tickets par email.
          </p>
        </div>
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
