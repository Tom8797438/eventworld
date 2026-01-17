<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-indigo-100 flex flex-col">
    <div class="p-6 flex flex-col gap-6">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 class="text-3xl font-bold text-purple-800">Suivi des scans</h1>
          <p class="text-gray-600 text-sm" v-if="eventName">Evenement : {{ eventName }}</p>
        </div>
        <button
          class="bg-white border border-purple-200 text-purple-700 px-4 py-2 rounded-lg shadow-sm hover:bg-purple-50 transition"
          @click="goBack"
        >
          Retour
        </button>
      </div>

      <div class="grid gap-4 md:grid-cols-3">
        <div class="bg-white rounded-lg shadow-md p-4 border border-green-200">
          <p class="text-sm text-gray-500">Reste a passer</p>
          <p class="text-2xl font-bold text-green-600">{{ ticketSummary.valid }}</p>
        </div>
        <div class="bg-white rounded-lg shadow-md p-4 border border-blue-200">
          <p class="text-sm text-gray-500">Scannes</p>
          <p class="text-2xl font-bold text-blue-600">{{ ticketSummary.used }}</p>
        </div>
        <div class="bg-white rounded-lg shadow-md p-4 border border-red-200">
          <p class="text-sm text-gray-500">Fraudes</p>
          <p class="text-2xl font-bold text-red-600">{{ ticketSummary.invalid }}</p>
        </div>
      </div>

      <div class="grid gap-6 md:grid-cols-2">
        <div class="bg-white rounded-lg shadow-lg p-6 border border-indigo-200">
          <h2 class="text-xl font-semibold text-purple-800 mb-4">Tickets</h2>
          <div class="mb-4">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Rechercher par nom ou prenom"
              class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
            />
          </div>
          <div v-if="ticketsLoading" class="text-gray-500">Chargement des tickets...</div>
          <div v-else-if="ticketsError" class="text-red-500">{{ ticketsError }}</div>
          <div v-else-if="filteredTickets.length === 0" class="text-gray-500">Aucun ticket trouve.</div>
          <div v-else class="space-y-3 max-h-[420px] overflow-y-auto">
            <div
              v-for="ticket in filteredTickets"
              :key="ticket.id"
              class="flex flex-col gap-2 p-3 rounded-lg border border-gray-200 bg-gray-50"
            >
              <div class="flex items-center justify-between">
                <div class="flex flex-col">
                  <span class="font-semibold text-gray-800">
                    {{ ticket.ticket_type || 'Ticket' }}
                  </span>
                  <span v-if="ticket.firstname || ticket.lastname" class="text-xs text-gray-500">
                    {{ [ticket.firstname, ticket.lastname].filter(Boolean).join(' ') }}
                  </span>
                </div>
                <div class="flex items-center gap-2">
                  <button
                    class="text-xs font-semibold px-3 py-1 rounded-md border border-purple-200 text-purple-700 bg-white hover:bg-purple-50"
                    @click="toggleTicket(ticket.id)"
                  >
                    {{ expandedTicketId === ticket.id ? 'Masquer' : 'Voir' }}
                  </button>
                  <span
                    class="text-xs font-semibold px-2 py-1 rounded-full"
                    :class="statusBadgeClass(ticket.status)"
                  >
                    {{ statusLabel(ticket.status) }}
                  </span>
                </div>
              </div>
              <div v-if="expandedTicketId === ticket.id" class="bg-white rounded-md border border-gray-200 p-3">
                <p class="text-xs text-gray-600">Email : {{ ticket.email || 'Non renseigne' }}</p>
                <p class="text-xs text-gray-600">
                  Scan : {{ ticket.scan_timestamp ? formatDate(ticket.scan_timestamp) : 'Non scanne' }}
                </p>
                <div class="mt-2 flex flex-col gap-2">
                  <input
                    type="email"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
                    :placeholder="ticket.email ? ticket.email : 'Email de destination'"
                    v-model="emailOverrides[ticket.id]"
                  />
                  <button
                    class="bg-indigo-600 text-white text-xs font-semibold px-3 py-2 rounded-md hover:bg-indigo-700 disabled:opacity-60"
                    :disabled="isSending(ticket.id)"
                    @click="sendTicketEmail(ticket)"
                  >
                    {{ isSending(ticket.id) ? 'Envoi...' : 'Envoyer par mail' }}
                  </button>
                  <p v-if="sendStatus[ticket.id]" class="text-xs text-gray-600">{{ sendStatus[ticket.id] }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-lg p-6 border border-purple-200">
          <h2 class="text-xl font-semibold text-purple-800 mb-4">Utilisateurs temporaires</h2>
          <div v-if="eventStore.loading" class="text-gray-500">Chargement des utilisateurs...</div>
          <div v-else-if="eventStore.error" class="text-red-500">{{ eventStore.error }}</div>
          <div v-else-if="temporaryScanners.length === 0" class="text-gray-500">Aucun utilisateur temporaire.</div>
          <div v-else class="space-y-3 max-h-[420px] overflow-y-auto">
            <div
              v-for="scanner in temporaryScanners"
              :key="scanner.id"
              class="flex items-center justify-between p-3 rounded-lg border border-gray-200 bg-gray-50"
            >
              <div class="flex items-center gap-3">
                <span
                  class="w-3 h-3 rounded-full"
                  :class="isOnline(scanner.last_seen_at) ? 'bg-green-500' : 'bg-red-500'"
                ></span>
                <div>
                  <p class="font-semibold text-gray-800">{{ scanner.display_name }}</p>
                  <p class="text-xs text-gray-500">{{ scanner.email }}</p>
                </div>
              </div>
              <div class="text-right text-xs text-gray-600">
                <p>Scans : <span class="font-semibold">{{ scanner.tickets_scanned ?? 0 }}</span></p>
                <p>Ventes : <span class="font-semibold">{{ scanner.tickets_sold ?? 0 }}</span></p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useEventStore } from '@/stores/eventStore';
import { fetchEventTicketStatus, sendTicketByEmail } from '@/utils/api_utils';
import { isValidEmail } from '@/utils/validators';

const route = useRoute();
const router = useRouter();
const eventStore = useEventStore();

const eventId = computed(() => route.params.id);
const eventName = computed(() => {
  const event = eventStore.events.find((item) => item.id === eventId.value);
  return event?.name || '';
});

const tickets = ref([]);
const ticketSummary = ref({ valid: 0, used: 0, invalid: 0 });
const ticketsLoading = ref(false);
const ticketsError = ref('');
const searchQuery = ref('');
const expandedTicketId = ref(null);
const emailOverrides = ref({});
const sendingTicketIds = ref({});
const sendStatus = ref({});

const temporaryScanners = computed(() => eventStore.temporaryScanners);
const filteredTickets = computed(() => {
  const query = searchQuery.value.trim().toLowerCase();
  if (!query) return tickets.value;
  return tickets.value.filter((ticket) => {
    const firstname = (ticket.firstname || '').toLowerCase();
    const lastname = (ticket.lastname || '').toLowerCase();
    return firstname.includes(query) || lastname.includes(query);
  });
});

const statusLabel = (status) => {
  if (status === 'used') return 'Scanne';
  if (status === 'invalid') return 'Fraude';
  if (status === 'valid') return 'Reste a passer';
  return 'Inconnu';
};

const statusBadgeClass = (status) => {
  if (status === 'used') return 'bg-blue-100 text-blue-700';
  if (status === 'invalid') return 'bg-red-100 text-red-700';
  if (status === 'valid') return 'bg-green-100 text-green-700';
  return 'bg-gray-100 text-gray-700';
};

const isOnline = (lastSeenAt) => {
  if (!lastSeenAt) return false;
  const lastSeen = new Date(lastSeenAt).getTime();
  return Date.now() - lastSeen < 5 * 60 * 1000;
};

const formatDate = (value) => {
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString();
};

const toggleTicket = (ticketId) => {
  expandedTicketId.value = expandedTicketId.value === ticketId ? null : ticketId;
};

const isSending = (ticketId) => !!sendingTicketIds.value[ticketId];

const sendTicketEmail = async (ticket) => {
  const overrideEmail = emailOverrides.value[ticket.id]?.trim();
  const targetEmail = overrideEmail || ticket.email;
  sendStatus.value[ticket.id] = '';

  if (!targetEmail || !isValidEmail(targetEmail)) {
    sendStatus.value[ticket.id] = "Email invalide.";
    return;
  }

  sendingTicketIds.value[ticket.id] = true;
  try {
    await sendTicketByEmail(eventId.value, ticket.id, overrideEmail || null);
    sendStatus.value[ticket.id] = "Email envoye.";
  } catch (error) {
    sendStatus.value[ticket.id] = "Erreur lors de l'envoi.";
  } finally {
    sendingTicketIds.value[ticket.id] = false;
  }
};

const loadTickets = async () => {
  ticketsLoading.value = true;
  ticketsError.value = '';
  try {
    const data = await fetchEventTicketStatus(eventId.value);
    ticketSummary.value = data.summary || { valid: 0, used: 0, invalid: 0 };
    tickets.value = data.tickets || [];
  } catch (error) {
    ticketsError.value = "Erreur lors du chargement des tickets.";
  } finally {
    ticketsLoading.value = false;
  }
};

const goBack = () => {
  router.push({ name: 'menu' });
};

onMounted(async () => {
  if (!eventStore.events.length) {
    await eventStore.fetchEvents();
  }
  await Promise.all([
    loadTickets(),
    eventStore.loadTemporaryScanners(eventId.value),
  ]);
});
</script>
