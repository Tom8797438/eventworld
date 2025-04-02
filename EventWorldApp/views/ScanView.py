from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from EventWorldApp.models import Ticketing, TemporaryScanner
from rest_framework.permissions import IsAuthenticated
from EventWorldApp.permissions import IsNotStudent
from django.utils import timezone

class ScanTicket (APIView):
    
    permission_classes = [IsAuthenticated, IsNotStudent]
    
    def post(self, request, *args, **kwargs):
        qr_code = request.data.get('qr_code')        
        if not qr_code:
            return Response({"message": "QR Code manquant ou id"}, status=status.HTTP_400_BAD_REQUEST)

        ticket = get_object_or_404(Ticketing, qr_code=qr_code)
        print("receiptScan variable ticket: ",ticket)
        event = ticket.event  
        print("receiptScan variable ticket: ",event)
        user = request.user
        is_owner = event.organisator == user
        is_temp_scanner = TemporaryScanner.objects.filter(
            user=user, 
            event=event, 
            can_scan=True, 
            expires_at__gt=timezone.now()
        ).exists()
        
        if not is_owner and not is_temp_scanner:
            return Response(
                {"message": "Vous n'avez pas l'autorisation de scanner ce ticket."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Vérifie que l'utilisateur est bien l'organisateur de l'événement
        # if event.organisator  != request.user:  # ou .organizer selon ton modèle
        #     return Response(
        #         {"message": "Vous n'êtes pas autorisé à scanner les tickets pour cet événement."},
        #         status=status.HTTP_403_FORBIDDEN
        #     )
        
        if ticket.status == "used":
                return Response(
                {"message": "Ce ticket a déjà été utilisé", "status": "used"},
                status=status.HTTP_200_OK,
            )
        # ✅ Vérifie si l'utilisateur est l'organisateur OU un scanneur temporaire actif
        event = ticket.event
        

        # Mise à jour du statut en "used"
        ticket.status = "used"
        ticket.scan_timestamp = timezone.now()
        ticket.save()

        return Response(
            {"message": "Ticket validé avec succès", "status": "success"},
            status=status.HTTP_200_OK,
        )
        
        