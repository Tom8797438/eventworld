<template>
  <div class="cadre-scan" v-if="canScan && authorizedEventId">
    <div class="camera-frame" :key="componentKey">
      <qrcode-stream
        :constraints="selectedConstraints"
        :formats="selectedBarcodeFormats"
        @decode="onDecode"
        @error="onError"
        @detect="onDetect"
        @camera-on="onCameraReady"
      />
    </div>

    <div class="section-scan">
      <p class="selection-camera">
        Caméra :
        <select v-model="selectedConstraints">
          <option v-for="option in constraintOptions" :key="option.label" :value="option.constraints">
            {{ option.label }}
          </option>
        </select>
      </p>

      <div class="scan-response" v-if="scanResponse">
        <div :class="['status-icon', statusClass]">
          <font-awesome-icon v-if="scanResponse.status === 'success'" icon="fas fa-thumbs-up" />
          <font-awesome-icon v-if="scanResponse.status === 'used'" icon="fas fa-exclamation-circle" />
          <font-awesome-icon v-if="scanResponse.status === 'invalid'" icon="fas fa-times-circle" />
          <p>{{ scanResponse.message }}</p>
        </div>
      </div>
    </div>
  </div>

  <div v-else>
    <p>⛔ Vous n'avez pas le droit de scanner ou le lien est invalide.</p>
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
@import '@/assets/styles/QrCodeScanner.css';

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
}
</style>
