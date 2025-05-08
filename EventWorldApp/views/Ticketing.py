from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from EventWorldApp.models import Evenement, Ticketing
from django.contrib.auth import get_user_model
from EventWorldApp.utils.serializers import TicketSerializer
from EventWorldApp.utils.event_count import calculate_remaining_places  # ✅ à importer
from rest_framework.permissions import AllowAny
import uuid

User = get_user_model()

class TicketCreateView(APIView):
    """
    Vue pour gérer la création des billets pour un événement.
    """
    permission_classes = [AllowAny] 

    def post(self, request, *args, **kwargs):
        event_id = request.data.get('id')
        event = get_object_or_404(Evenement, id=event_id)

        tickets_data = request.data.get('tickets', [])
        created_tickets = []

        # ✅ Calcul du total demandé
        total_requested = sum(ticket.get("quantity", 0) for ticket in tickets_data)
        remaining = calculate_remaining_places(event)

        # ✅ Bloquer si trop de tickets demandés
        if total_requested > remaining:
            return Response(
                {"error": f"Pas assez de places disponibles. Il reste {remaining} places."},
                status=status.HTTP_400_BAD_REQUEST
            )

        base_ticket_data = {
            "event": event.id,
            "user": event.organisator.id,
            "status": "valid",
        }

        for ticket_data in tickets_data:
            ticket_type = ticket_data.get("ticket_type")
            if not ticket_type:
                return Response({"error": "Le type de billet est requis."}, status=status.HTTP_400_BAD_REQUEST)

            for _ in range(ticket_data["quantity"]):
                ticket_instance = {
                    "qr_code": uuid.uuid4(),
                    "ticket_type": ticket_type,
                }
                ticket_instance.update(base_ticket_data)
                ticket_instance.update(ticket_data)
                ticket_instance["quantity"] = 1

                serializer = TicketSerializer(data=ticket_instance)
                if serializer.is_valid():
                    serializer.save()
                    ticket_data_serialized = serializer.data
                    ticket_data_serialized["event_name"] = event.name
                    created_tickets.append(ticket_data_serialized)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"created_tickets": created_tickets}, status=status.HTTP_201_CREATED)
