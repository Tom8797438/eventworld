<template>
  <div v-if="canScan && authorizedEventId" class="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-indigo-100 flex items-center justify-center p-6">
    <div class="max-w-md w-full space-y-6 bg-white p-6 rounded-lg shadow-lg">
      <!-- Cadre de la caméra -->
      <div class="relative bg-gray-200 rounded-lg overflow-hidden border-2 border-purple-300">
        <qrcode-stream
          :constraints="selectedConstraints"
          :formats="selectedBarcodeFormats"
          @decode="onDecode"
          @error="onError"
          @detect="onDetect"
          @camera-on="onCameraReady"
          :key="componentKey"
          class="w-full h-64"
        />
      </div>

      <!-- Section de sélection et statut -->
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Caméra :</label>
          <select
            v-model="selectedConstraints"
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option v-for="option in constraintOptions" :key="option.label" :value="option.constraints">
              {{ option.label }}
            </option>
          </select>
        </div>

        <!-- Statut du scan -->
        <div v-if="scanResponse" class="p-4 rounded-lg border" :class="statusBorderClass">
          <div class="flex items-center space-x-2">
            <FontAwesomeIcon
              v-if="scanResponse.status === 'success'"
              :icon="['fas', 'thumbs-up']"
              class="text-green-600 text-2xl"
            />
            <FontAwesomeIcon
              v-if="scanResponse.status === 'used'"
              :icon="['fas', 'exclamation-circle']"
              class="text-yellow-600 text-2xl"
            />
            <FontAwesomeIcon
              v-if="scanResponse.status === 'fraud'"
              :icon="['fas', 'exclamation-circle']"
              class="text-red-600 text-2xl"
            />
            <FontAwesomeIcon
              v-if="scanResponse.status === 'invalid'"
              :icon="['fas', 'times-circle']"
              class="text-red-600 text-2xl"
            />
            <p class="text-sm font-medium" :class="statusTextClass">{{ scanResponse.message }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Accès refusé -->
  <div v-else class="min-h-screen bg-gradient-to-br from-red-50 to-red-100 flex items-center justify-center p-6">
    <div class="max-w-md w-full text-center bg-white p-6 rounded-lg shadow-lg">
      <p class="text-red-600 text-lg">⛔ Vous n'avez pas le droit de scanner ou le lien est invalide.</p>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { QrcodeStream } from 'vue-qrcode-reader';
import { useScanStore } from '@/stores/scanStore';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

export default {
  components: {
    QrcodeStream,
    FontAwesomeIcon,
  },
  setup() {
    const scanStore = useScanStore();
    const route = useRoute();
    const router = useRouter();

    const token = route.params.token;
    const authorizedEventId = ref(null);
    const canScan = ref(false);
    const scanResponse = ref(null);
    const componentKey = ref(0);

    const selectedConstraints = ref({ facingMode: 'environment' });
    const constraintOptions = ref([
      { label: 'Caméra arrière', constraints: { facingMode: 'environment' } },
      { label: 'Caméra avant', constraints: { facingMode: 'user' } },
    ]);

    const barcodeFormats = ref({ qr_code: true });
    const selectedBarcodeFormats = computed(() =>
      Object.keys(barcodeFormats.value).filter((key) => barcodeFormats.value[key])
    );

    const statusClass = computed(() => {
      if (!scanResponse.value) return '';
      switch (scanResponse.value.status) {
        case 'success':
          return 'success-icon';
        case 'used':
          return 'warning-icon';
        case 'invalid':
          return 'error-icon';
        default:
          return '';
      }
    });

    async function onDecode(decodedString) {
      try {
        let qrData = decodedString;
        try {
          qrData = JSON.parse(decodedString);
        } catch {}

        const qrCode = typeof qrData === 'object' ? qrData.qr_code : qrData;
        const uuidRegex = /^[0-9a-f-]{36}$/i;
        if (!uuidRegex.test(qrCode)) throw new Error('QR Code invalide');

        const response = await scanStore.scanTicket({ qr_code: qrCode });

        // 🔐 Vérifie si le billet scanné est lié à l'événement autorisé
        if (response.event_id && response.event_id !== authorizedEventId.value) {
          scanResponse.value = {
            status: 'invalid',
            message: 'Ce billet ne correspond pas à votre événement.',
          };
        } else {
          scanResponse.value = response;
        }

        setTimeout(() => {
          scanResponse.value = null;
          componentKey.value += 1;
        }, 2500);
      } catch (err) {
        console.error(err);
        scanResponse.value = { status: 'invalid', message: err.message };
      }
    }

    function onDetect(codes) {
      if (codes && codes.length) onDecode(codes[0].rawValue);
    }

    function onError(err) {
      console.error('Erreur caméra :', err);
    }

    async function onCameraReady() {
      try {
        const devices = await navigator.mediaDevices.enumerateDevices();
        const videoDevices = devices.filter((d) => d.kind === 'videoinput');
        videoDevices.forEach((device) => {
          constraintOptions.value.push({
            label: device.label,
            constraints: { deviceId: device.deviceId },
          });
        });
      } catch (err) {
        console.error(err);
      }
    }

    onMounted(async () => {
      try {
        const res = await axios.get(`/api/access/temp/${token}`);
        canScan.value = res.data.can_scan;
        authorizedEventId.value = res.data.event_id; // <-- assure-toi que `event_id` est renvoyé par l'API
        if (!canScan.value) throw new Error('Pas de droits de scan.');
      } catch (err) {
        console.error(err);
        alert("Accès non autorisé ou expiré.");
        router.push('/');
      }
    });

    return {
      selectedConstraints,
      constraintOptions,
      selectedBarcodeFormats,
      scanResponse,
      statusClass,
      onDecode,
      onDetect,
      onError,
      onCameraReady,
      canScan,
      authorizedEventId,
      componentKey,
    };
  },
};
</script>

<style scoped>
/* @import '@/assets/styles/QrCodeScanner.css';

.success-icon {
  color: green;
}
.warning-icon {
  color: orange;
}
.error-icon {
  color: red;
}

.cadre-scan {
 height: 100vh;
} */
</style>
