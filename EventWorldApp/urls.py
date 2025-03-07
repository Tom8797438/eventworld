from django.urls import path
from .views.authView import ProtectedView, UserProfileView

urlpatterns = [
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('user/', UserProfileView.as_view(), name='user_profile'),
]
