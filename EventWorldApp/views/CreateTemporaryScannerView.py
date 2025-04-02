from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

class CreateTemporaryScannerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_email = request.data.get("email")
        event_id = request.data.get("event_id")
        days = int(request.data.get("days", 1))

        try:
            user = User.objects.get(email=user_email)
            event = Evenement.objects.get(id=event_id)

            if event.organisator != request.user:
                return Response({"error": "Vous n'êtes pas l'organisateur de cet événement."}, status=403)

            expires_at = timezone.now() + timedelta(days=days)

            TemporaryScanner.objects.update_or_create(
                user=user,
                event=event,
                defaults={"can_scan": True, "expires_at": expires_at}
            )

            return Response({"message": f"Profil {user.username} autorisé à scanner jusqu'au {expires_at}."}, status=201)
        except User.DoesNotExist:
            return Response({"error": "Utilisateur introuvable."}, status=404)
        except Evenement.DoesNotExist:
            return Response({"error": "Événement introuvable."}, status=404)
