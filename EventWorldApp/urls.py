from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views.authView import ProtectedView, UserProfileView
from .views.LoginView import RegisterView
from .views.EventView import EventViewSet
from .views.Ticketing import TicketCreateView
from .views.ScanView import ScanTicket
from .views.LinkInvitationView import CreateDraftEventView, GenerateInvitationView, EventInvitationDetailView, get_invitation_by_event_id
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')

urlpatterns = [
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('user/', UserProfileView.as_view(), name='user_profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('tickets/',TicketCreateView.as_view(), name='tickets'),
    path ('scan_ticket/',ScanTicket.as_view(),name='scan_ticket'),
    
    path('events/draft/', CreateDraftEventView.as_view(), name='create-draft-event'),
    path('invitation/', GenerateInvitationView.as_view(), name='generate-invitation'),
    
    path('invitation/<uuid:id>/', EventInvitationDetailView.as_view(), name='event-invitation-detail'),
    path("invitation/by-event/", get_invitation_by_event_id, name="get-invitation-by-event-id"),
    path('', include(router.urls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
