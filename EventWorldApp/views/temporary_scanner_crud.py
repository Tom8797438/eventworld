from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from EventWorldApp.models import Evenement, TemporaryScanner


class TemporaryScannerDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, event_id, scanner_id):
        try:
            event = Evenement.objects.get(id=event_id, organisator=request.user)
            scanner = TemporaryScanner.objects.get(id=scanner_id, event=event)

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

    def delete(self, request, event_id, scanner_id):
        try:
            event = Evenement.objects.get(id=event_id, organisator=request.user)
            scanner = TemporaryScanner.objects.get(id=scanner_id, event=event)
            scanner.user.delete()  # supprime aussi l'utilisateur lié
            scanner.delete()
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