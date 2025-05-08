// src/utils/navigation.js
export function confirmAndNavigate(message = "Êtes-vous sûr de vouloir revenir au menu ?", router, route = "/Menu") {
    if (window.confirm(message)) {
      router.push(route);
    }
  }
  