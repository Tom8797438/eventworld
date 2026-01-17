<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-indigo-100 p-6">
    <div class="max-w-3xl mx-auto bg-white rounded-lg shadow-lg border border-purple-200 p-6 space-y-6">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-purple-800">Mon Profil</h1>
          <p class="text-sm text-gray-600">Informations du compte</p>
        </div>
        <button
          class="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors duration-200 text-sm"
          @click="goBack"
        >
          Retour
        </button>
      </div>

      <div class="grid gap-4 md:grid-cols-2">
        <div class="bg-gray-50 rounded-lg p-4 border border-gray-200">
          <p class="text-xs text-gray-500">Nom d'utilisateur</p>
          <p class="text-lg font-semibold text-gray-800">{{ user?.username || '-' }}</p>
        </div>
        <div class="bg-gray-50 rounded-lg p-4 border border-gray-200">
          <p class="text-xs text-gray-500">Email</p>
          <p class="text-lg font-semibold text-gray-800">{{ user?.email || '-' }}</p>
        </div>
        <div class="bg-gray-50 rounded-lg p-4 border border-gray-200">
          <p class="text-xs text-gray-500">Role</p>
          <p class="text-lg font-semibold text-gray-800">{{ user?.role || '-' }}</p>
        </div>
        <div class="bg-gray-50 rounded-lg p-4 border border-gray-200">
          <p class="text-xs text-gray-500">Statut</p>
          <p class="text-lg font-semibold text-gray-800">Actif</p>
        </div>
      </div>

      <div class="bg-indigo-50 border border-indigo-200 rounded-lg p-4 text-sm text-indigo-700">
        Pour modifier vos informations, contactez le support ou l'administrateur.
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';

const router = useRouter();
const authStore = useAuthStore();
const user = computed(() => authStore.user);

onMounted(async () => {
  if (!authStore.user) {
    await authStore.autoLogin();
  }
});

const goBack = () => {
  router.push({ name: 'menu' });
};
</script>
