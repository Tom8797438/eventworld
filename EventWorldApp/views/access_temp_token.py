from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from EventWorldApp.models import TemporaryScanner
from rest_framework import status
from django.core import signing
from django.http import JsonResponse

class TemporaryAccessView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            scanner = TemporaryScanner.objects.get(access_token=token)
            if not scanner.is_active():
                return Response({"error": "Lien expiré."}, status=403)

            # Maj timestamps
            now = timezone.now()
            if not scanner.first_access_at:
                scanner.first_access_at = now
            scanner.last_seen_at = now
            scanner.save()

            signed_token = signing.dumps(str(scanner.access_token))
            response = JsonResponse({
                "alias": scanner.display_name,
                "can_scan": scanner.can_scan,
                "can_sell": scanner.can_sell,
                "event": scanner.event.name,
                "event_id": str(scanner.event.id)
            })
            response.set_cookie(
                key="scanner_auth",
                value=signed_token,
                httponly=True,
                secure=True,
                samesite="Lax",
                max_age=60 * 60 * 6  # 6 heures
            )
            return response
        except TemporaryScanner.DoesNotExist:
            return Response({"error": "Lien invalide"}, status=404)
