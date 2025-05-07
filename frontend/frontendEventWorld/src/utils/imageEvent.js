// utils/imageEvent.js

/**
 * Gère l'importation d'une image et retourne le fichier sélectionné ainsi que l'aperçu.
 * @param {Event} event - L'événement déclenché lors de la sélection de fichier.
 * @returns {Object} - { file: File|null, preview: string|null }
 */
export function handleImageUpload(event) {
    const file = event.target.files[0];
    if (file && file.type.startsWith('image/')) {
      const preview = URL.createObjectURL(file);  // Génère une URL temporaire pour l'aperçu
      return { file, preview };
    } else {
      console.error("Le fichier sélectionné n'est pas une image.");
      return { file: null, preview: null };
    }
  }
  

const BACKEND_URL = 'http://127.0.0.1:8000'; // à adapter selon ton env réel

export function getEventImageUrl(imagePath) {
  if (!imagePath) return 'https://via.placeholder.com/100';
  // Gère les URLs absolues ou stockées comme /media/...
  if (imagePath.startsWith('http')) return imagePath;
  return `${BACKEND_URL}${imagePath}`;
}

