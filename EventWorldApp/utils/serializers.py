from rest_framework import serializers
from EventWorldApp.models import User, Profil, Evenement, Ticketing, TemporaryScanner, InvitationNotification
from EventWorldApp.utils.event_count import calculate_remaining_places

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password", "role"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  # Création sécurisée
        return user


class TemporaryScannerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    event = serializers.StringRelatedField()
    class Meta:
        model = TemporaryScanner
        fields = ['id', 'user', 'event', 'expires_at', 'can_scan', 'can_sell', 'is_active', 'tickets_scanned', 'tickets_sold']
        extra_kwargs = {
            'can_sell': {'default': True},
            'can_scan': {'default': True}
        }

class ProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profil
        fields = "__all__"
        
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evenement
        fields = "__all__"
        read_only_fields = ('code_evenement', 'organisator','created_at', 'updated_at') 

class TemporaryScannerSerializerLight(serializers.ModelSerializer):
    class Meta:
        model = TemporaryScanner
        fields = [
            'id', 'display_name', 'email', 'access_token',
            'can_scan', 'can_sell', 'tickets_scanned',
            'tickets_sold', 'last_seen_at'
        ]

class EventDetailSerializer(serializers.ModelSerializer):
    temporary_scanners = TemporaryScannerSerializerLight(many=True, read_only=True)

    class Meta:
        model = Evenement
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model= Ticketing
        fields = "__all__"
        
class EvenementForInvitationSerializer(serializers.ModelSerializer):
    remaining_places = serializers.SerializerMethodField()

    class Meta:
        model = Evenement
        fields = (
            'id', 'name', 'description', 'date_start', 'date_end',
            'location', 'address', 'postal_code', 'city',
            'type_event', 'number_place', 'price_categories', 'picture',
            'remaining_places'  # champ calculé à inclure
        )

    def get_remaining_places(self, obj):
        return calculate_remaining_places(obj)

class InvitationNotificationSerializer(serializers.ModelSerializer):
    event = EvenementForInvitationSerializer(read_only=True)
    
    class Meta:
        model = InvitationNotification
        fields = ('id', 'event', 'email', 'status', 'created_at')