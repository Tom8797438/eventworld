from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Gestion des profils
class Profil(models.Model):
    TYPE_ORGANISATOR_CHOICES = [
        ('organisateur', 'Organisateur'),
        ('association', 'Association'),
        ('etudiant', 'Étudiant'),
        ('autre', 'Autre'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profil")
    company_name = models.CharField(max_length=100, unique=True)
    company_number = models.CharField(max_length=25, unique=True)
    type_organisator = models.CharField(
        max_length=20, 
        choices=TYPE_ORGANISATOR_CHOICES, 
        default='organisateur'
    )
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
        return f"{self.company_name} ({self.get_type_organisator_display()})"

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profils"


# Gestion des événements
class Evenement(models.Model):
    TYPE_EVENT = [
        ('public', 'Public'),
        ('private', 'Privé'),
        ('limited', 'Limité'),
    ]
    TYPE_STATUS = [
        ('draft','Draft'), 
        ('current', 'Current'), 
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code_evenement = models.CharField(
        max_length=13, 
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{13}$',
                message="Le code évènement doit contenir exactement 13 chiffres."
            )
        ],
        help_text="Entrez un code évènement de 13 chiffres."
    )
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True, null=True)
    date_start = models.DateField()
    date_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price_1 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price_2 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price_3 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price_4 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price_5 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price_6 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    location = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    organisator = models.ForeignKey(Profil, on_delete=models.CASCADE, related_name="events")
    number_place = models.IntegerField(default=0)
    type_event = models.CharField(max_length=20, choices=TYPE_EVENT, default='private')
    status = models.CharField(max_length=20, choices=TYPE_STATUS, default='draft')

    def __str__(self):
        return f"{self.name} ({self.code_evenement})"

    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
        ordering = ['name']


# Gestion des tickets et QR Codes
class Ticketing(models.Model):
    STAT_STATUS = [
        ('valid', 'Valid'),
        ('used', 'Used'),
        ('invalid', 'Invalid'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Evenement, on_delete=models.CASCADE, related_name="tickets")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    qr_code = models.CharField(max_length=255, unique=True, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STAT_STATUS, default='valid')
    scan_timestamp = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket {self.id} - {self.event.name} - {self.user.username} - {self.status}"

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        ordering = ['-created_at']


# Gestion des paiements
class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket = models.ForeignKey(Ticketing, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - Ticket {self.ticket.id} - {self.payment_status}"

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ['-created_at']


# Gestion des invitations
class InvitationNotification(models.Model):
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Evenement, on_delete=models.CASCADE, related_name="invitations")
    email = models.EmailField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invitation for {self.email} - {self.event.name} - {self.status}"

    class Meta:
        verbose_name = "Invitation"
        verbose_name_plural = "Invitations"
        ordering = ['-created_at']
