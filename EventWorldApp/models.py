from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import timedelta

# Modèle utilisateur personnalisé
class User(AbstractUser):
    ORGANIZER = "organisateur"
    ASSOCIATION = "association"
    STUDENT = "etudiant"
    OTHER = "autre"
    
    ROLE_CHOICES = [
        (ORGANIZER, "Organisateur"),
        (ASSOCIATION, "Association"),
        (STUDENT, "Étudiant"),
        (OTHER, "Autre"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ORGANIZER)

    # Ajout `related_name` évitant les conflits avec auth.User
    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)


    def can_create_event(self, event_type):
        """ Vérifie si l'utilisateur peut créer un type d'événement """
        if self.role in [self.ORGANIZER, self.ASSOCIATION]:  
            return True  # Organisateur & Association → Tout type d'événement possible
        elif self.role == self.STUDENT and event_type in ["private", "limited"]:
            return True  # Étudiant → Événements privés et restreints
        elif self.role == self.OTHER and event_type == "private":
            return True  # Autre → Seulement des événements privés
        return False  # Accès refusé

    def __str__(self):
        return f"{self.username} ({self.role})"


#  Gestion des profils
class Profil(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    company_name = models.CharField(max_length=100, unique=True)
    company_number = models.CharField(max_length=25, unique=True)
    civility = models.CharField(max_length=10, blank=True, null=True)
    name_contact = models.CharField(max_length=100)
    surname_contact = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile_phone = models.CharField(max_length=10, blank=True, null=True)
    landline_phone = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.company_name} ({self.user.role})"

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profils"


# Gestion des événements
class Evenement(models.Model):
    TYPE_EVENT = [("public", "Public"), ("private", "Privé"), ("limited", "Limité")]
    TYPE_STATUS = [
        ("draft", "Draft"),
        ("current", "Current"),
        ("finished", "Finished"),
        ("cancelled", "Cancelled"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code_evenement = models.CharField(max_length=255, unique=True, blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    date_start = models.DateField()
    date_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    organisator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    number_place = models.IntegerField(default=0)
    type_event = models.CharField(max_length=20, choices=TYPE_EVENT, default="private")
    status = models.CharField(max_length=20, choices=TYPE_STATUS, default="draft")
    # Stocke dynamiquement les prix sous forme de JSON { "standard": 10, "vip": 20, "pmr": 5 }
    price_categories = models.JSONField(default=dict, blank=True, null=True)
    picture = models.ImageField(upload_to="event_pictures/", blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.code_evenement})"

    def save(self, *args, **kwargs):
        """ ✅ Vérifie les permissions avant de sauvegarder """
        if not self.organisator.can_create_event(self.type_event):
            raise ValueError(f"L'utilisateur {self.organisator.username} ({self.organisator.role}) n'a pas le droit de créer un événement {self.type_event}.")
        
        if not self.code_evenement:  # Si le champ est vide, on génère un code unique
            self.code_evenement = str(uuid.uuid4())[:8]  # Générer un identifiant court
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
        ordering = ["-created_at"]

class TemporaryScanner(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="temporary_scanner")
    event = models.ForeignKey(Evenement, on_delete=models.CASCADE, related_name="temporary_scanners")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    can_scan = models.BooleanField(default=True)

    def is_active(self):
        return self.can_scan and timezone.now() < self.expires_at

    def __str__(self):
        return f"{self.user.username} - Scan pour {self.event.name} (jusqu'à {self.expires_at})"

# Gestion des tickets et QR Codes
class Ticketing(models.Model):
    STAT_STATUS = [("valid", "Valid"), ("used", "Used"), ("invalid", "Invalid")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Evenement, on_delete=models.CASCADE, related_name="tickets")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    qr_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Sécurisation avec UUID
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STAT_STATUS, default="valid")
    scan_timestamp = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    firstname = models.CharField(max_length=100, blank=True)
    lastname = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    ticket_type = models.CharField(max_length=50, blank=True)
    def __str__(self):
        return f"Ticket {self.id} - {self.event.name} - {self.user.username} - {self.status}"

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        ordering = ["-created_at"]


# Gestion des paiements
class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket = models.ForeignKey(Ticketing, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.CharField(
        max_length=20, choices=[("pending", "Pending"), ("completed", "Completed"), ("failed", "Failed")], default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - Ticket {self.ticket.id} - {self.payment_status}"

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ["-created_at"]


# Gestion des invitations
class InvitationNotification(models.Model):
    STATUS_CHOICES = [("sent", "Sent"), ("accepted", "Accepted"), ("refused", "Refused")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Evenement, on_delete=models.CASCADE, related_name="invitations")
    email = models.EmailField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="sent")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invitation for {self.email} - {self.event.name} - {self.status}"

    class Meta:
        verbose_name = "Invitation"
        verbose_name_plural = "Invitations"
        ordering = ["-created_at"]
