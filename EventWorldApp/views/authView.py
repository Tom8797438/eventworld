from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]  # 🔐 Seuls les utilisateurs connectés peuvent accéder

    def get(self, request):
        return Response({"message": "Accès autorisé uniquement aux utilisateurs authentifiés"})

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # 🔐 Seuls les utilisateurs connectés peuvent accéder

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_superuser": user.is_superuser,  # Pour savoir si c'est un admin
        }, status=status.HTTP_200_OK)