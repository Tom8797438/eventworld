from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]  # Seuls les utilisateurs connectés peuvent accéder

    def get(self, request):
        return Response({"message": "Accès autorisé uniquement aux utilisateurs authentifiés"})

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Seuls les utilisateurs connectés peuvent accéder

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_superuser": user.is_superuser,  # Pour savoir si c'est un admin
        }, status=status.HTTP_200_OK)
        
        
class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            data = response.data
            response.set_cookie(
                key="access_token",
                value=data["access"],
                httponly=True,
                secure=False,  # 🔐 à passer à True en production HTTPS
                samesite='Lax',
                max_age=3600,
                path='/',
            )
            response.set_cookie(
                key="refresh_token",
                value=data["refresh"],
                httponly=True,
                secure=False,
                samesite='Lax',
                max_age=7 * 24 * 3600,
                path='/',
            )
        return response