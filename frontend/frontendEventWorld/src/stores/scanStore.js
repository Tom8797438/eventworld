import { defineStore } from "pinia";
import { checkTicketStatus } from "@/utils/api_utils"; // Appel API centralisé

export const useScanStore = defineStore("scanStore", {
  actions: {
    async scanTicket(qrCodeContent) {
      try {
        console.log("🚀 Début du scan :", qrCodeContent);

        if (!qrCodeContent) {
          console.error(" QR Code vide ou invalide.");
          return { message: "QR Code invalide", status: "error" };
        }

        // ✅ Vérification du QR Code avec l'API
        const response = await checkTicketStatus(qrCodeContent);
        console.log("Réponse API :", response);

        return {
          message: response.message,
          status: response.status,
        };
      } catch (error) {
        console.error("Erreur lors du scan :", error);
        return { message: "Erreur lors du scan", status: "error" };
      }
    },
  },
});
