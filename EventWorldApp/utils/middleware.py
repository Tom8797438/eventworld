from django.utils import timezone
from django.http import JsonResponse
from EventWorldApp.models import TemporaryScanner

class TemporaryScannerEventRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if user.is_authenticated and hasattr(user, 'temporary_scanner'):
            scanner = user.temporary_scanner
            if not scanner.is_active():
                return JsonResponse({"error": "Votre accès a expiré."}, status=403)

            event_id = request.resolver_match.kwargs.get('event_id') or request.GET.get('event_id')
            if event_id and str(scanner.event.id) != event_id:
                return JsonResponse({"error": "Accès non autorisé à cet événement."}, status=403)

        return self.get_response(request)
