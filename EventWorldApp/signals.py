from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Evenement, InvitationNotification

@receiver(post_save, sender=Evenement)
def create_invitation_for_event(sender, instance, created, **kwargs):
    # Créer une invitation automatiquement si l'événement vient d'être créé
    if created:
        print(f"Création d'une invitation pour l'événement {instance.id}")
        InvitationNotification.objects.create(event=instance, email="")
