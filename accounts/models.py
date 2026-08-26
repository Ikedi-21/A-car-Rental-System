from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Extends Django's built-in User with the extra fields our CRS needs
    (phone, address). Kept as a separate model with a OneToOne link
    rather than a custom User model — swapping the User model mid-project
    is painful and there's no real need for it here.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    is_admin_profile = models.BooleanField(default=False)  # separate from is_staff — this flags dashboard access specifically
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"