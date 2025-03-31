from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from EventWorldApp.models import Evenement
from EventWorldApp.utils.serializers import EventSerializer
from EventWorldApp.permissions import IsOrganizerOrAssociation

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Récupère les événements accessibles selon le rôle de l'utilisateur"""
        user = self.request.user
        if user.is_authenticated and user.role in ["organisateur", "association", "etudiant", "autre"]:
            return Evenement.objects.filter(organisator=user)
        return Evenement.objects.filter(type_event="public")

    def create(self, request, *args, **kwargs):
        """Crée un événement avec une structure dynamique des prix"""
        data = request.data
        user = request.user  # Récupération de l'utilisateur connecté

        # Vérifie si l'utilisateur a le droit de créer cet événement
        if not user.can_create_event(data.get("type_event")):
            return Response({"error": "no access."}, status=status.HTTP_403_FORBIDDEN)

        # Création de l'événement
        event = Evenement.objects.create(
            name=data["name"],
            description=data.get("description", ""),
            date_start=data["date_start"],
            date_end=data["date_end"],
            location=data["location"],
            address=data["address"],
            postal_code=data["postal_code"],
            city=data["city"],
            number_place=data["number_place"],
            type_event=data["type_event"],
            price_categories=data.get("price_categories", {}),
            organisator=user,
        )

        return Response({"message": "Événement créé avec succès !", "event_id": event.id}, status=status.HTTP_201_CREATED)

