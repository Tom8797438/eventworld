<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-indigo-100">
    <FirstPage />
  </div>
</template>

<script>
import FirstPage from '@/components/FirstPage.vue';

export default {
    name : 'FirstPageView',
    components :{
      FirstPage,
    },
    
};
</script>