from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from EventWorldApp.models import TemporaryScanner
from rest_framework import status
from django.core import signing

class HeartbeatView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        cookie_token = request.COOKIES.get("scanner_auth")
        if not cookie_token:
            return Response({"error": "Authentification manquante."}, status=403)

        try:
            access_token = signing.loads(cookie_token)
            scanner = TemporaryScanner.objects.get(access_token=access_token)
            if not scanner.is_active():
                return Response({"error": "Lien expiré"}, status=403)

            scanner.last_seen_at = timezone.now()
            scanner.save(update_fields=["last_seen_at"])

            return Response({"status": "heartbeat reçu"})
        except signing.BadSignature:
            return Response({"error": "Token invalide."}, status=403)
        except TemporaryScanner.DoesNotExist:
            return Response({"error": "Scanner introuvable"}, status=404)

