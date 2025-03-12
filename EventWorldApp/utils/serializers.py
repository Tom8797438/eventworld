from rest_framework import serializers
from EventWorldApp.models import User, Profil, Evenement, Ticketing

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password", "role"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  # Création sécurisée
        return user

class ProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profil
        fields = "__all__"
        
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evenement
        fields = "__all__"
        read_only_fields = ('code_evenement',) 

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model= Ticketing
        fields = "__all__"