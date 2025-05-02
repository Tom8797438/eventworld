
<template>
  <component :is="layout">
    <router-view />
  </component>
</template>

<script>
import BaseLayout from './components/LayoutBase.vue';

export default {
  computed: {
    layout() {
      return this.$route.meta.layout || 'div'; // Utilise LayoutBase ou un conteneur simple
    },
  },
};
</script>