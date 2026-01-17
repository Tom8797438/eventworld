from django.core.mail import send_mail
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from EventWorldApp.models import Evenement, Ticketing, TemporaryScanner


class SendTicketEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id, ticket_id):
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

        try:
            ticket = Ticketing.objects.get(id=ticket_id, event=event)
        except Ticketing.DoesNotExist:
            return Response({"error": "Ticket introuvable."}, status=404)

        target_email = request.data.get("email") or ticket.email
        if not target_email:
            return Response({"error": "Email manquant pour l'envoi."}, status=400)

        subject = f"Votre ticket - {event.name}"
        message = (
            f"Bonjour,\n\n"
            f"Voici votre ticket pour l'évènement : {event.name}\n"
            f"Type de ticket : {ticket.ticket_type or 'N/A'}\n"
            f"QR Code : {ticket.qr_code}\n"
            f"Statut : {ticket.status}\n\n"
            f"Merci et à bientôt."
        )

        send_mail(subject, message, None, [target_email], fail_silently=False)

        return Response({"message": "Email envoyé avec succès."})
