<template>
  <div class="cadre-scan" :key="componentKey">
    <div class="camera-frame">
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
        Sélection de la caméra
        <select v-model="selectedConstraints" class="selection-camera">
          <option
            v-for="option in constraintOptions"
            :key="option.label"
            :value="option.constraints"
          >
            {{ option.label }}
          </option>
        </select>
      </p>

      <!-- Mise à jour : Utilisation de `status` -->
      <div class="scan-response" v-if="scanResponse">
        <div class="status-icon" :class="statusClass">
          <FontAwesomeIcon v-if="scanResponse.status === 'success'" :icon="['fas', 'thumbs-up']" class="success-icon"/>
          <FontAwesomeIcon v-if="scanResponse.status === 'used'" :icon="['fas', 'thumbs-up']" class="warning-icon"/>
          <FontAwesomeIcon v-if="scanResponse.status === 'invalid'" :icon="['fas', 'times-circle']" class="error-icon"/>
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

    // 🧠 Si c'est un JSON encodé en string, on le parse
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
      case "sucess":
        return "success-icon";
      case "used":
        return "warning-icon";
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

<style scoped>
@import '@/assets/styles/QrCodeScanner.css'

</style>
