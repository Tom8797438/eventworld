from django.test import TestCase
from django.contrib.auth import get_user_model
from EventWorldApp.models import Evenement
from datetime import date

User = get_user_model()

class EventModelTest(TestCase):
    def setUp(self):
        # Création d'un utilisateur avec rôle autorisé
        self.user = User.objects.create_user(
            username="testuser",
            password="123456",
            role="organisateur" 
        )

    def test_create_event(self):
        event = Evenement.objects.create(
            name="Concert",
            city="Saint-Denis",
            date_start=date.today(),
            date_end=date.today(),
            location="Théâtre",
            address="1 rue du spectacle",
            postal_code="97400",
            organisator=self.user,
        )
        self.assertEqual(event.name, "Concert")
        self.assertEqual(event.city, "Saint-Denis")
        self.assertEqual(event.organisator.username, "testuser")
