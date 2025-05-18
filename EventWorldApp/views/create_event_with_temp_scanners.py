import uuid
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import timedelta
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from django.utils.timezone import make_aware
from datetime import datetime, time
from EventWorldApp.models import User  # ✅ IMPORT MANQUANT
from EventWorldApp.models import Evenement, TemporaryScanner, InvitationNotification
from EventWorldApp.utils.serializers import EventSerializer


class CreateEventWithTemporaryScanners(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        event_data = request.data.copy()
        print("temp_user_limit reçu dans le POST :", event_data.get("temp_user_limit"))
        # 🔧 Correction ici
        temp_user_limit_raw = event_data.get("temp_user_limit", 0)
        if isinstance(temp_user_limit_raw, list):
            temp_user_limit_raw = temp_user_limit_raw[0]
        temp_user_limit = min(int(temp_user_limit_raw), 100)

        event_serializer = EventSerializer(data=event_data)
        if event_serializer.is_valid():
            event = event_serializer.save(organisator=request.user, temp_user_limit=temp_user_limit)

            expires_at = make_aware(datetime.combine(event.date_end + timedelta(days=1), time.min))
            temp_user_temp_data = request.data.get("temp_user_temp_data", [])

            if isinstance(temp_user_temp_data, str):
                import json
                temp_user_temp_data = json.loads(temp_user_temp_data)
            
            temp_users_info = []
            for i in range(temp_user_limit):
                user_info = temp_user_temp_data[i] if i < len(temp_user_temp_data) else {}
                alias = user_info.get("alias", f"TempUser{i+1}")
                email = user_info.get("email", f"temp{i+1}@eventworld.com")
                can_scan = user_info.get("can_scan", True)
                can_sell = user_info.get("can_sell", True)

                password = get_random_string(length=10)
                username = f"tempuser_{uuid.uuid4().hex[:6]}"

                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )

                scanner = TemporaryScanner.objects.create(
                    user=user,
                    event=event,
                    email=email,
                    display_name=alias,
                    expires_at=expires_at,
                    can_scan=can_scan,
                    can_sell=can_sell
                )

                InvitationNotification.objects.create(event=event, email=email)

                temp_users_info.append({
                    "alias": alias,
                    "email": email,
                    "username": user.username,
                    "password": password,
                    "access_link": f"https://tyzer.top/access/temp/{scanner.access_token}/"
                })


            return Response({
                "event_id": event.id,
                "temporary_users": temp_users_info
            }, status=201)
        print(event_serializer.errors)
        return Response(event_serializer.errors, status=400)
