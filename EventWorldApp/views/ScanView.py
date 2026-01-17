from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from EventWorldApp.models import Ticketing, TemporaryScanner
from django.db.models import F
from rest_framework.permissions import IsAuthenticated
from EventWorldApp.permissions import IsNotStudent
from django.utils import timezone

class ScanTicket (APIView):
    
    permission_classes = [IsAuthenticated, IsNotStudent]
    
    def post(self, request, *args, **kwargs):
        qr_code = request.data.get('qr_code')        
        if not qr_code:
            return Response({"message": "QR Code manquant ou id"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ticket = Ticketing.objects.get(qr_code=qr_code)
        except Ticketing.DoesNotExist:
            return Response(
                {"message": "Fraude : QR code inconnu", "status": "fraud"},
                status=status.HTTP_200_OK,
            )
        event = ticket.event 
        user = request.user
        is_owner = event.organisator == user
        temp_scanner = TemporaryScanner.objects.filter(
            user=user, 
            event=event, 
            can_scan=True, 
            expires_at__gt=timezone.now()
        ).first()
        is_temp_scanner = temp_scanner is not None
        
        if not is_owner and not is_temp_scanner:
            return Response(
                {"message": "Fraude : billet pour un autre evenement", "status": "fraud"},
                status=status.HTTP_200_OK
            )
        
        # Vérifie que l'utilisateur est bien l'organisateur de l'événement
        # if event.organisator  != request.user:  # ou .organizer selon ton modèle
        #     return Response(
        #         {"message": "Vous n'êtes pas autorisé à scanner les tickets pour cet événement."},
        #         status=status.HTTP_403_FORBIDDEN
        #     )
        
        if ticket.status == "used":
                return Response(
                {"message": "Non valide : deja scanne", "status": "used"},
                status=status.HTTP_200_OK,
            )
        # Vérifie si l'utilisateur est l'organisateur OU un scanneur temporaire actif
        event = ticket.event
        

        # Mise à jour du statut en "used"
        ticket.status = "used"
        ticket.scan_timestamp = timezone.now()
        ticket.save()

        if temp_scanner:
            TemporaryScanner.objects.filter(id=temp_scanner.id).update(
                tickets_scanned=F("tickets_scanned") + 1,
                last_seen_at=timezone.now(),
            )

        return Response(
            {"message": "Ticket validé avec succès", "status": "success"},
            status=status.HTTP_200_OK,
        )
        
        
