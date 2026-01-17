<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-indigo-100 flex items-center justify-center p-6" :key="componentKey">
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
          class="w-full h-64"
        />
      </div>

      <!-- Section de sélection et statut -->
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Sélection de la caméra</label>
          <select
            v-model="selectedConstraints"
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option
              v-for="option in constraintOptions"
              :key="option.label"
              :value="option.constraints"
            >
              {{ option.label }}
            </option>
          </select>
        </div>

        <!-- Statut du scan -->
        <div v-if="scanResponse" class="flex items-center justify-center p-4 rounded-lg border" :class="statusBorderClass">
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
            <span class="text-sm font-medium" :class="statusTextClass">{{ scanResponse.message || 'Statut inconnu' }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from "vue";
import { QrcodeStream } from "vue-qrcode-reader";
import { useScanStore } from "@/stores/scanStore.js";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faThumbsUp, faExclamationCircle, faTimesCircle } from '@fortawesome/free-solid-svg-icons';
import { library } from '@fortawesome/fontawesome-svg-core';

library.add(faThumbsUp, faExclamationCircle, faTimesCircle);


export default {
  components: {
    QrcodeStream,
    FontAwesomeIcon,
  },
  setup() {
    const scanStore = useScanStore();
    const result = ref(""); // Résultat brut du dernier scan
    const scanResponse = ref(null); // Réponse après validation
    
    const componentKey = ref(0);

    function resetScanner() {
  console.log("Réinitialisation du scanner...");
  scanResponse.value = null;  // Effacer la réponse du scan
  result.value = "";  // Effacer le dernier QR code scanné
  componentKey.value += 1; // Force Vue à recréer le composant
}

    // Fonction exécutée lors de la détection d'un QR code
    async function onDecode(decodedString) {
  try {
    console.log("QR Code brut détecté :", decodedString);

    let qrData;

    // Si c'est un JSON encodé en string, on le parse
    try {
      qrData = JSON.parse(decodedString);
    } catch (e) {
      qrData = decodedString; // Si ce n'est pas du JSON, on garde la string brute
    }

    // Si c'est un objet avec la clé "qr_code", on extrait sa valeur
    const qrCodeToCheck = typeof qrData === "object" && qrData.qr_code ? qrData.qr_code : qrData;

    const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
    if (!uuidRegex.test(qrCodeToCheck)) {
      throw new Error("QR Code invalide (non conforme au format UUID)");
    }

    const response = await scanStore.scanTicket({qr_code: qrCodeToCheck});
    scanResponse.value = response;
    console.log("Réponse du scan :", response);

    setTimeout(() => {
      scanResponse.value = null;
      result.value = "";
      componentKey.value += 1;
    }, 2000);
  } catch (error) {
    console.error("Erreur lors de la validation du scan :", error);
    scanResponse.value = { status: "invalid", message: error.message };
  }
}


    // Détection des QR codes
    function onDetect(detectedCodes) {
      console.log("Codes détectés :", detectedCodes);

      if (detectedCodes && detectedCodes.length > 0) {
        const rawValue = detectedCodes[0].rawValue;
        result.value = rawValue;
        console.log("Contenu détecté brut :", rawValue);
        onDecode(rawValue); // Passe le contenu détecté à `onDecode`
      } else {
        result.value = "Aucun code détecté";
      }
    }

    const selectedConstraints = ref({ facingMode: "environment" });
    const constraintOptions = ref([
      { label: "Caméra arrière", constraints: { facingMode: "environment" } },
      { label: "Caméra avant", constraints: { facingMode: "user" } },
    ]);

    const statusClass = computed(() => {
    if (!scanResponse.value) return "";
    switch (scanResponse.value.status) {
      //case "valid":
      case "success":
        return "success-icon";
      case "used":
        return "warning-icon";
      case "fraud":
        return "error-icon";
      case "invalid":
        return "error-icon";
      default:
        return "";
    }
  });

    async function onCameraReady() {
      try {
        const devices = await navigator.mediaDevices.enumerateDevices();
        const videoDevices = devices.filter(({ kind }) => kind === "videoinput");

        constraintOptions.value = [
          ...constraintOptions.value,
          ...videoDevices.map(({ deviceId, label }) => ({
            label: label.length > 30 ? `${label.slice(0, 30)}...` : label, // Tronquer le label si nécessaire
            constraints: { deviceId },
          })),
        ];
      } catch (err) {
        console.error("Erreur lors de la configuration de la caméra :", err);
      }
    }

    const barcodeFormats = ref({
      qr_code: true, // Activer uniquement le QR code
    });

    const selectedBarcodeFormats = computed(() =>
      Object.keys(barcodeFormats.value).filter((format) => barcodeFormats.value[format])
    );

    function onError(err) {
      console.error("Erreur lors du scan :", err);
    }

    return {
      componentKey,
      resetScanner,
      result,
      scanResponse,
      selectedConstraints,
      constraintOptions,
      barcodeFormats,
      selectedBarcodeFormats,
      onDecode,
      onDetect,
      onError,
      onCameraReady,
    };
  },
};
</script>

