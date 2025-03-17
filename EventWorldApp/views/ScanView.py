from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from EventWorldApp.models import Ticketing

class ScanTicket (APIView):
    
    def receiptScan(self, request, *args, **kwargs):
        qr_code = request.data.get('qr_code')
        if not qr_code:
            return Response({"message": "QR Code manquant"}, status=status.HTTP_400_BAD_REQUEST)

        ticket = get_object_or_404(Ticketing, qr_code=qr_code)

        if ticket.status == "used":
                return Response(
                {"message": "Ce ticket a déjà été utilisé", "status": "used"},
                status=status.HTTP_200_OK,
            )

        # Mise à jour du statut en "used"
        ticket.status = "used"
        ticket.save()

        return Response(
            {"message": "Ticket validé avec succès", "status": "success"},
            status=status.HTTP_200_OK,
        )
        
        