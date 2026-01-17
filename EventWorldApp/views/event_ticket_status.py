from django.db.models import Count
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from EventWorldApp.models import Evenement, Ticketing, TemporaryScanner


class EventTicketStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        try:
            event = Evenement.objects.get(id=event_id)
        except Evenement.DoesNotExist:
            return Response({"error": "Événement introuvable."}, status=404)

        user = request.user
        is_owner = event.organisator == user
        is_temp_scanner = TemporaryScanner.objects.filter(
            user=user,
            event=event,
            expires_at__gt=timezone.now(),
        ).exists()

        if not is_owner and not is_temp_scanner:
            return Response({"error": "Accès interdit."}, status=403)

        tickets_qs = Ticketing.objects.filter(event=event)

        summary = {"valid": 0, "used": 0, "invalid": 0}
        for row in tickets_qs.values("status").annotate(count=Count("id")):
            summary[row["status"]] = row["count"]

        tickets = list(
            tickets_qs.order_by("-scan_timestamp", "-created_at").values(
                "id",
                "ticket_type",
                "status",
                "scan_timestamp",
                "firstname",
                "lastname",
                "email",
            )
        )

        return Response(
            {
                "event_id": str(event.id),
                "event_name": event.name,
                "summary": summary,
                "tickets": tickets,
            }
        )
