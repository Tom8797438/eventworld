import { createRouter, createWebHistory } from 'vue-router';
import BaseLayout from '@/components/LayoutBase.vue';
import LoginView from '@/views/LoginView.vue';
import EventpublicView from '@/views/EventpublicView.vue';
import PublicEventDetail from '@/components/PublicEventDetail.vue';
import MenuView from '@/views/MenuView.vue'; 
import { useAuthStore } from '@/stores/authStore'; 
import EventDetails from '@/components/EventDetails.vue';
import QrCodeScanner from "@/components/QrCodeScanner.vue";
import Register from '@/components/Register.vue';
import InvitationEventView from '@/components/InvitationEventView.vue';
import FirstPageView from '@/views/FirstPageView.vue';
import CreateEvent from '@/components/CreateEvent.vue';
import ResetPassword from '@/components/ResetPassword.vue';
import ResetPasswordConfirm from '@/components/ResetPasswordConfirm.vue';


const routes = [
    {
      path: '/accueil',
      name: 'EventpublicView',
      component: EventpublicView, // Page publique de connexion
    },
    {
      path: '/event-public/:id',
      name: 'PublicEventDetail',
      component: PublicEventDetail,
      meta: { requiresAuth: false },
    },    
    {
      path: '/FirstPage',
      name: 'FirstPage',
      component: FirstPageView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView, 
    },
    {
      path: '/ResetPassword',
      name: 'ResetPassword',
      component: ResetPassword,
    },
    {
      path: '/reset-password-confirm/:uid/:token',
      name: 'ResetPasswordConfirm',
      component: ResetPasswordConfirm,
    },
    
    {
      path: '/menu',
      name: 'menu',
      component: MenuView, // Page protégée (Menu principal)
      meta: { requiresAuth: true, layout: BaseLayout }, // Nécessite une authentification
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
      meta: { requiresAuth: true, layout: BaseLayout }, // Nécessite une authentification
    },
    {
      path: '/event/:id', // Route avec un paramètre dynamique `id`
      name: 'EventDetails',
      component: EventDetails,
      meta: { layout: BaseLayout },
    },
    {
      path: "/scan-qr-code",
      name: "QrCodeScanner",
      component: QrCodeScanner,
      meta: { requiresAuth: true, layout: BaseLayout }, // Nécessite une authentification
    },
    {
      path: '/:pathMatch(.*)*', // Redirection par défaut
      redirect: '/FirstPage',
    },
    {
      path: '/invitation/:id',
      name: 'InvitationEventView',
      component: InvitationEventView,
      meta: { requiresAuth: false },
    },   
    {
      path: '/CreateEvent',
      name: 'CreateEvent',
      component: CreateEvent,
      meta: { layout: BaseLayout },
    }, 
  ];
  const router = createRouter({
    history: createWebHistory(),
    routes,
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
