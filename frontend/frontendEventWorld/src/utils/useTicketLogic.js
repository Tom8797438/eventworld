import { ref, computed } from 'vue';

export function useTicketLogic() {
  const ticketTypes = ref([]);
  const selectedTickets = ref([{ type: '', quantity: 1 }]);

  const initializeTickets = (priceCategories) => {
    console.log('Price Categories (reçu dans initializeTickets):', priceCategories);

    if (typeof priceCategories === 'string') {
      try {
        priceCategories = JSON.parse(priceCategories);
        console.log('Price Categories (après parsing JSON):', priceCategories);
      } catch (e) {
        console.error('Erreur lors de la transformation de price_categories :', e);
        priceCategories = [];
      }
    } else if (typeof priceCategories === 'object' && !Array.isArray(priceCategories)) {
      priceCategories = Object.entries(priceCategories).map(([label, value]) => ({
        label,
        value,
      }));
      console.log('Price Categories (après transformation d\'objet en tableau):', priceCategories);
    } else if (!Array.isArray(priceCategories)) {
      priceCategories = [];
    }

    // Transformez priceCategories en ticketTypes uniquement si des prix sont définis
    if (priceCategories.length > 0) {
      ticketTypes.value = priceCategories.map((price) => ({
        name: price.label.toLowerCase(),
        label: price.label,
        price: { value: price.value, label: price.label },
      }));
    } else {
      // Si aucun prix n'est défini, ajoutez une option "Gratuit"
      ticketTypes.value = [{ name: 'free', label: 'Gratuit', price: { value: 0, label: 'Gratuit' } }];
    }

    console.log('Ticket Types (final):', ticketTypes.value);

    selectedTickets.value = [{ type: ticketTypes.value[0]?.name || 'free', quantity: 1 }];
  };

  const total = computed(() => {
    return selectedTickets.value.reduce((sum, ticket) => {
      const ticketType = ticketTypes.value.find(t => t.name === ticket.type);
      return sum + (ticket.quantity * (ticketType?.price.value || 0));
    }, 0);
  });

  const addTicket = () => {
    if (ticketTypes.value.length > 1) {
      selectedTickets.value.push({ type: ticketTypes.value[0]?.name || 'free', quantity: 1 });
    }
  };

  const removeTicket = (index) => {
    selectedTickets.value.splice(index, 1);
  };

  return {
    ticketTypes,
    selectedTickets,
    total,
    initializeTickets,
    addTicket,
    removeTicket,
  };
}