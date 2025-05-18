from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from EventWorldApp.utils.serializers import TemporaryScannerSerializer

class TemporaryScannerStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if hasattr(request.user, 'temporary_scanner'):
            serializer = TemporaryScannerSerializer(request.user.temporary_scanner)
            return Response(serializer.data)
        return Response({"error": "Aucune session temporaire trouvée."}, status=404)
