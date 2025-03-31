from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class IsOrganizerOrAssociation(BasePermission):
    """
    ✅ Autorise uniquement les organisateurs et les associations à accéder à une API spécifique.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["organisateur", "association", "etudiant"]

class IsStudentOrHigher(BasePermission):
    """
    ✅ Autorise uniquement les étudiants et les rôles supérieurs à certaines actions.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["organisateur", "association", "etudiant"]

class IsSelfUserOrAdmin(BasePermission):
    """
    ✅ Un utilisateur peut voir/modifier ses propres informations, sauf si c'est un admin.
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj or request.user.is_staff

class IsNotStudent(BasePermission):
    """
    ❌ Interdit l'accès aux utilisateurs avec le rôle 'etudiant'
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == "etudiant":
            raise PermissionDenied(detail="Les étudiants n'ont pas accès à cette fonctionnalité.")
        return True
