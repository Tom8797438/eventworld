from django.contrib import admin
from .models import User, Profil, Evenement, Ticketing, Payment, InvitationNotification

# Enregistrement des modèles pour l'administration
admin.site.register(User)
admin.site.register(Profil)
admin.site.register(Evenement)
admin.site.register(Ticketing)
admin.site.register(Payment)
admin.site.register(InvitationNotification)
