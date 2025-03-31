import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '@/views/LoginView.vue';
import EventpublicView from '@/views/EventpublicView.vue';
import MenuView from '@/views/MenuView.vue'; // Vue pour le menu principal
import { useAuthStore } from '@/stores/authStore'; // Importation du store pour gérer l'authentification
import EventDetails from '@/components/EventDetails.vue';
import QrCodeScanner from "@/components/QrCodeScanner.vue";
import Register from '@/components/Register.vue';


const router = createRouter({
  
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/accueil',
      name: 'EventpublicView',
      component: EventpublicView, // Page publique de connexion
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView, // Page publique de connexion
    },
    {
      path: '/menu',
      name: 'menu',
      component: MenuView, // Page protégée (Menu principal)
      meta: { requiresAuth: true }, // Nécessite une authentification
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
    },
    {
      path: '/events/details', // Utilise documentId comme paramètre requis
      name: 'EventDetails',
      component: EventDetails,
      meta: { requiresAuth: true }, // Nécessite une authentification
    },
    
    {
      path: "/scan-qr-code",
      name: "QrCodeScanner",
      component: QrCodeScanner,
      meta: { requiresAuth: true }, // Nécessite une authentification
    },
    {
      path: '/:pathMatch(.*)*', // Redirection par défaut
      redirect: '/accueil',
    },
  ],
});

// Middleware pour gérer les routes protégées
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/accueil'); // Redirige vers la page de connexion si non authentifié
  } else if (to.name === 'login' && authStore.isAuthenticated) {
    next('/menu'); // Redirige vers le menu si déjà connecté
  } else {
    next(); // Continue vers la route demandée
  }
});

export default router
