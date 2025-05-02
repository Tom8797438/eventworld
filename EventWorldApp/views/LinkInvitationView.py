# views.py (suite)
from EventWorldApp.models import InvitationNotification, Evenement
from EventWorldApp.utils.serializers import InvitationNotificationSerializer, EventSerializer
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view

class EventInvitationDetailView(generics.RetrieveAPIView):
    """
    Endpoint public pour afficher les détails de l'événement via l'invitation.
    L'URL sera par exemple /api/invitation/<invitation_id>/.
    """
    queryset = InvitationNotification.objects.all()
    serializer_class = InvitationNotificationSerializer
    lookup_field = 'id'
    permission_classes = [permissions.AllowAny]

class CreateDraftEventView(generics.CreateAPIView):
    """
    Endpoint pour créer un brouillon d’événement.
    Seul un utilisateur authentifié peut créer un brouillon.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        # Associer l’utilisateur authentifié et fixer le statut en draft.
        serializer.save(organisateur=self.request.user, status="draft")

class GenerateInvitationView(generics.CreateAPIView):
    """
    Endpoint pour générer une invitation pour un événement donné.
    Seul l’organisateur de l’événement peut générer une invitation.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InvitationNotificationSerializer

    def post(self, request, *args, **kwargs):
        event_id = request.data.get("event_id")
        email = request.data.get("email", "")  # optionnel

        # Vérifier que l'événement existe
        try:
            event = Evenement.objects.get(id=event_id)
        except Evenement.DoesNotExist:
            return Response({"error": "Événement non trouvé."},
                            status=status.HTTP_404_NOT_FOUND)

        # Vérifier que l'utilisateur est bien l'organisateur
        if event.organisator != request.user:
            return Response({"error": "Accès non autorisé."},
                            status=status.HTTP_403_FORBIDDEN)

        # Créer l'invitation, le token est généré automatiquement via l'UUID défini dans le modèle
        invitation = InvitationNotification.objects.create(event=event, email=email)
        serializer = self.get_serializer(invitation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_invitation_by_event_id(request):
    event_id = request.query_params.get('event_id')
    if not event_id:
        return Response({"error": "event_id requis"}, status=status.HTTP_400_BAD_REQUEST)

    invitation = InvitationNotification.objects.filter(event__id=event_id).first()

    if not invitation:
        return Response({"error": "Invitation non trouvée"}, status=status.HTTP_404_NOT_FOUND)

    serializer = InvitationNotificationSerializer(invitation)
    return Response(serializer.data, status=status.HTTP_200_OK)  # ✅ IL MANQUAIT CE RETURN

   