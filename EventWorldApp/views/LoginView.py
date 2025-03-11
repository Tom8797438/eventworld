from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from EventWorldApp.models import Profil, User  
from EventWorldApp.utils.serializers import UserSerializer, ProfilSerializer
import json 

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("Données reçues:", json.dumps(request.data, indent=2))
        user_data = request.data.get("user", {})
        profil_data = request.data.get("profil", {})

        # Création de l'utilisateur
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            
            # Assignation du groupe Django correspondant au rôle
            role_group = Group.objects.filter(name=user.role).first()
            if role_group:
                user.groups.add(role_group)

            # Création du profil lié à l'utilisateur
            profil_data["user"] = user.id
            profil_serializer = ProfilSerializer(data=profil_data)

            if profil_serializer.is_valid():
                profil_serializer.save()
                return Response({"message": "Utilisateur créé avec succès !"}, status=status.HTTP_201_CREATED)

            # Supprime l'utilisateur si le profil échoue
            user.delete()

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
