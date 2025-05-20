from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from .views.CreateTemporaryScannerView import CreateTemporaryScannerView
from .views.create_event_with_temp_scanners import CreateEventWithTemporaryScanners
from .views.event_temporary_scanners_list import EventTemporaryScannersListView
from .views.temporary_scanner_status import TemporaryScannerStatusView

from .views.authView import ProtectedView, UserProfileView, ResetPasswordRequestView, ResetPasswordConfirmView
from .views.LoginView import RegisterView
from .views.EventView import EventViewSet
from .views.Ticketing import TicketCreateView
from .views.ScanView import ScanTicket
from .views.LinkInvitationView import CreateDraftEventView, GenerateInvitationView, EventInvitationDetailView, get_invitation_by_event_id
from rest_framework.routers import DefaultRouter

from .views.temporary_scanner_crud import (TemporaryScannerDetailView, TemporaryScannerListView)
from EventWorldApp.views.access_temp_token import TemporaryAccessView

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')

urlpatterns = [
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('user/', UserProfileView.as_view(), name='user_profile'),
    
    path('reset-password/', ResetPasswordRequestView.as_view(), name='reset-password'),
    path('reset-password-confirm/', ResetPasswordConfirmView.as_view(), name='reset-password-confirm'),

    path('register/', RegisterView.as_view(), name='register'),
    path('tickets/',TicketCreateView.as_view(), name='tickets'),
    path('scan_ticket/',ScanTicket.as_view(),name='scan_ticket'),
    
    path('events/draft/', CreateDraftEventView.as_view(), name='create-draft-event'),
    path('invitation/', GenerateInvitationView.as_view(), name='generate-invitation'),
    
    path('create-temporary-scanner/', CreateTemporaryScannerView.as_view(), name='create-temporary-scanner'),
    path('event/create-with-temp-users/', CreateEventWithTemporaryScanners.as_view()),
    path('event/<uuid:event_id>/temporary-scanners/', EventTemporaryScannersListView.as_view(), name="temporary_scanner_list"),
    path('event/<uuid:event_id>/temporary-scanner/<uuid:scanner_id>/', TemporaryScannerDetailView.as_view(), name="temporary_scanner_detail"),
    path('temporary-scanner/status/', TemporaryScannerStatusView.as_view()),
    path('temporary-scanner/<uuid:scanner_id>/', TemporaryScannerDetailView.as_view(), name='update-temporary-scanner'),
    
    path('invitation/<uuid:id>/', EventInvitationDetailView.as_view(), name='event-invitation-detail'),
    path("invitation/by-event/", get_invitation_by_event_id, name="get-invitation-by-event-id"),
    
    path("event/<uuid:event_id>/temporary-users/", TemporaryScannerListView.as_view(), name="temporary-user-list"),
    path("event/<uuid:event_id>/temporary-user/<uuid:scanner_id>/", TemporaryScannerDetailView.as_view(), name="temporary-user-detail"),
    path("access/temp/<uuid:token>/", TemporaryAccessView.as_view(), name="temporary-access"),
    
    path('', include(router.urls)),
]

