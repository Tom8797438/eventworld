<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-300 via-blue-100 to-purple-400 flex items-center justify-center p-4">
    <div class="max-w-md w-full bg-gradient-to-b from-purple-500 to-blue-200 p-8 rounded-lg shadow-lg text-center">
      <img src="@/assets/styles/pictures/Logo.png" alt="Event World Logo" class="w-3/4 mx-auto mb-6" />
      <div class="space-y-4">
        <button
          @click="goToLogin"
          class="w-full bg-indigo-600 text-white py-3 px-6 rounded-lg hover:bg-indigo-700 transition-colors duration-200 font-semibold"
        >
          Log In
        </button>
        <button
          @click="goToRegister"
          class="w-full bg-gray-800 text-white py-3 px-6 rounded-lg hover:bg-gray-900 transition-colors duration-200 font-semibold"
        >
          Register
        </button>
      </div>
      <footer class="mt-6 text-sm text-gray-600">
        <a href="" class="text-gray-800 hover:text-blue-600 font-bold transition-colors duration-200">by ZuWeb</a>
      </footer>
    </div>
  </div>
</template>
  
  <script>
  export default {
    name: 'FirstPage',
    methods: {
      goToLogin() {
        this.$router.push('/login'); 
      },
      goToRegister() {
        this.$router.push('/register');
      },
    },
  };
  </script>
