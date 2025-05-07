from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
# from django.contrib.auth.models import User
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
# start partie reset password
from django.contrib.auth import get_user_model

from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework.permissions import AllowAny

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
    
# reset password
User = get_user_model()

class ResetPasswordRequestView(APIView):
    permission_classes = [AllowAny]  # accès sans token
    def post(self, request):
        email = request.data.get('email')
        print (email)
        if not email:
            return Response({'error': 'Email requis'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Aucun utilisateur avec cet email'}, status=status.HTTP_404_NOT_FOUND)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = f"{settings.FRONTEND_URL}/reset-password-confirm/{uid}/{token}"

        send_mail(
            subject='Réinitialisation de votre mot de passe',
            message=f'Cliquez sur le lien suivant pour réinitialiser votre mot de passe : {reset_url}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        return Response({'message': 'Email de réinitialisation envoyé'}, status=status.HTTP_200_OK)
    
class ResetPasswordConfirmView(APIView):
    permission_classes = [AllowAny]  # accès sans token
    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        password = request.data.get('password')

        if not all([uid, token, password]):
            return Response({'error': 'Champs manquants'}, status=400)

        try:
            user_id = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=user_id)
        except Exception:
            return Response({'error': 'Lien invalide'}, status=400)

        if not default_token_generator.check_token(user, token):
            return Response({'error': 'Token invalide ou expiré'}, status=400)

        user.set_password(password)
        user.save()

        return Response({'message': 'Mot de passe mis à jour'}, status=200)