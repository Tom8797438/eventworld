from django.urls import path, include
from .views.authView import ProtectedView, UserProfileView
from .views.LoginView import RegisterView
from .views.EventView import EventViewSet
from .views.Ticketing import TicketCreateView
from .views.ScanView import ScanTicket
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')

urlpatterns = [
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('user/', UserProfileView.as_view(), name='user_profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('tickets/',TicketCreateView.as_view(), name='tickets'),
    path ('scan_ticket/',ScanTicket.as_view(),name='scan_ticket'),
    path('', include(router.urls)),
]
