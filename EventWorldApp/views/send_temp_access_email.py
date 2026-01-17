from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from EventWorldApp.models import Evenement, TemporaryScanner


class SendTemporaryAccessEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id, scanner_id):
        try:
            event = Evenement.objects.get(id=event_id, organisator=request.user)
        except Evenement.DoesNotExist:
            return Response({"error": "Événement introuvable ou accès refusé."}, status=403)

        try:
            scanner = TemporaryScanner.objects.get(id=scanner_id, event=event)
        except TemporaryScanner.DoesNotExist:
            return Response({"error": "Utilisateur temporaire introuvable."}, status=404)

        target_email = request.data.get("email") or scanner.email
        if not target_email:
            return Response({"error": "Email manquant pour l'envoi."}, status=400)

        access_link = request.build_absolute_uri(f"/access/temp/{scanner.access_token}/")
        subject = f"Acces temporaire - {event.name}"
        message = (
            f"Bonjour,\n\n"
            f"Voici votre lien d'acces pour l'evenement : {event.name}\n"
            f"{access_link}\n\n"
            f"Merci."
        )

        send_mail(subject, message, None, [target_email], fail_silently=False)

        return Response({"message": "Email envoye avec succes.", "access_link": access_link})
