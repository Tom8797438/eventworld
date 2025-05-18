from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from EventWorldApp.models import Evenement, TemporaryScanner
from EventWorldApp.utils.serializers import TemporaryScannerSerializer

class EventTemporaryScannersListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        try:
            event = Evenement.objects.get(id=event_id, organisateur=request.user)
            scanners = TemporaryScanner.objects.filter(event=event)
            serializer = TemporaryScannerSerializer(scanners, many=True)
            return Response(serializer.data)
        except Evenement.DoesNotExist:
            return Response({"error": "Événement introuvable ou accès refusé."}, status=404)
