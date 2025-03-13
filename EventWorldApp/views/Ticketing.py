from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from EventWorldApp.models import Evenement, Ticketing
from django.contrib.auth import get_user_model
from EventWorldApp.utils.serializers import TicketSerializer
import uuid

User = get_user_model()

class TicketCreateView(APIView):
    """
    Vue pour gérer la création des billets pour un événement.
    """

    def post(self, request, *args, **kwargs):
        # print("Données reçues :", request.data)
        event_id = request.data.get('id')
        event = get_object_or_404(Evenement, id=event_id)

        tickets_data = request.data.get('tickets', [])
        created_tickets = []

        base_ticket_data = {
            "event": event.id,
            "user": event.organisator.id,
            "status": "valid",
        }

        for ticket_data in tickets_data:
            ticket_type = ticket_data.get("ticket_type")
            if not ticket_type:
                return Response({"error": "Le type de billet est requis."}, status=status.HTTP_400_BAD_REQUEST)

            # Création d'un ticket UNIQUE par billet commandé
            for _ in range(ticket_data["quantity"]):
                ticket_instance = {
                    "qr_code": uuid.uuid4(),
                    "ticket_type": ticket_type,
                }
                ticket_instance.update(base_ticket_data)  # Appliquer les valeurs communes
                ticket_instance.update(ticket_data)  # Appliquer les valeurs spécifiques
                ticket_instance["quantity"] = 1

                serializer = TicketSerializer(data=ticket_instance)
                if serializer.is_valid():
                    serializer.save()
                    # ✅ Ajouter `event.name` à `serializer.data`
                    ticket_data_serialized = serializer.data
                    ticket_data_serialized["event_name"] = event.name

                    created_tickets.append(ticket_data_serialized)  # Ajouter la version modifiée

                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        #print("Tickets créés :", created_tickets)
        return Response({"created_tickets": created_tickets}, status=status.HTTP_201_CREATED)
