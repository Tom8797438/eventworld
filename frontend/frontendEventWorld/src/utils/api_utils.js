// on centralise les appels API
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api/",
  headers: { "Content-Type": "application/json" },
});

// Générer un numéro de commande
export async function genererNumeroCommande(prefixe) {
  try {
    const response = await api.get("generer_le_numero_commande", {
      params: { prefixe },
    });
    return response.data;
  } catch (error) {
    console.log("Erreur lors de la génération du numéro de commande :", error);
    throw error;
  }
}

