from django.contrib.auth.mixins import UserPassesTestMixin

class IsOwnerOrSharedReadOnly(UserPassesTestMixin):
    """Vérifie que l'utilisateur est propriétaire ou a un accès partagé"""
    def test_func(self):
        note = self.get_object()
        user = self.request.user
        
        return (note.user == user or 
                note.shares.filter(user=user, permission__in=['READ', 'WRITE']).exists())