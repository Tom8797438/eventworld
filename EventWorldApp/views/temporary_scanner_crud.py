from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from EventWorldApp.models import Evenement, TemporaryScanner
from django.utils.crypto import get_random_string
from rest_framework import status
import uuid
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class TemporaryScannerDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, scanner_id):
        try:
            scanner = TemporaryScanner.objects.select_related("event").get(id=scanner_id)
            event = scanner.event
            if event.organisator != request.user:
                            return Response({"error": "Accès interdit."}, status=403)

            scanner.display_name = request.data.get("alias", scanner.display_name)
            scanner.email = request.data.get("email", scanner.email)
            scanner.can_scan = request.data.get("can_scan", scanner.can_scan)
            scanner.can_sell = request.data.get("can_sell", scanner.can_sell)
            scanner.save()

            return Response({"message": "Utilisateur temporaire mis à jour avec succès."})
        except Evenement.DoesNotExist:
            return Response({"error": "Événement introuvable ou non autorisé."}, status=403)
        except TemporaryScanner.DoesNotExist:
            return Response({"error": "Utilisateur temporaire introuvable."}, status=404)

    def delete(self, request, scanner_id):
        try:
            scanner = TemporaryScanner.objects.select_related("event").get(id=scanner_id)
            event = scanner.event
            if event.organisator != request.user:
                return Response({"error": "Accès interdit."}, status=403)
            
            scanner.user.delete()  # supprime aussi l'utilisateur lié
            scanner.delete()
            
            # décrémentation du compteur dans l'événement
            if event.temp_user_limit > 0:
                event.temp_user_limit = max(0, event.temp_user_limit - 1)
                event.save()
                
            return Response({"message": "Utilisateur temporaire supprimé avec succès."})
        except Evenement.DoesNotExist:
            return Response({"error": "Événement introuvable ou non autorisé."}, status=403)
        except TemporaryScanner.DoesNotExist:
            return Response({"error": "Utilisateur temporaire introuvable."}, status=404)

class TemporaryScannerListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
                try:
                    event = Evenement.objects.get(id=event_id, organisator=request.user)
                    scanners = TemporaryScanner.objects.filter(event=event)

                    data = []
                    for s in scanners:
                        data.append({
                            "id": str(s.id),
                            "alias": s.display_name,
                            "email": s.email,
                            "can_scan": s.can_scan,
                            "can_sell": s.can_sell,
                            "tickets_scanned": s.tickets_scanned,
                            "tickets_sold": s.tickets_sold,
                            "is_online": s.is_online(),
                            "access_link": f"https://tyzer.top/access/temp/{s.access_token}/"
                        })

                    return Response(data)
                except Evenement.DoesNotExist:
                    return Response({"error": "Événement introuvable ou non autorisé."}, status=403)


class TemporaryScannerCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        event_id = request.data.get("event_id")
        try:
            event = Evenement.objects.get(id=event_id, organisator=request.user)
        except Evenement.DoesNotExist:
            return Response({"error": "Événement introuvable ou non autorisé."}, status=403)

        alias = request.data.get("alias")
        email = request.data.get("email")
        can_scan = request.data.get("can_scan", False)
        can_sell = request.data.get("can_sell", False)

        if not alias or not email:
            return Response({"error": "Alias et email requis."}, status=400)

        # Génération d'un mot de passe aléatoire
        password = get_random_string(length=10)

        # Création de l'utilisateur Django
        user = User.objects.create_user(
            username=f"temp_{uuid.uuid4().hex[:10]}",
            email=email,
            password=password
        )

        # Création du TemporaryScanner
        scanner = TemporaryScanner.objects.create(
            user=user,
            event=event,
            display_name=alias,
            email=email,
            can_scan=can_scan,
            can_sell=can_sell,
            access_token=uuid.uuid4(),
            expires_at=event.date_end + timedelta(days=1) if event.date_end else timezone.now() + timedelta(days=1)
        )

        # Incrémentation du compteur sur l'événement
        event.temp_user_limit = event.temp_user_limit + 1
        event.save()

        return Response({
            "message": "Utilisateur temporaire créé avec succès.",
            "scanner_id": scanner.id,
            "access_token": scanner.access_token
        }, status=status.HTTP_201_CREATED)