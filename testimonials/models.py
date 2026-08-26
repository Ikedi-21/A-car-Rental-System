from django.db import models
from django.contrib.auth.models import User


class Testimonial(models.Model):
    """
    A review left by a registered user. is_active controls whether it
    shows up publicly — admin can toggle this off instead of deleting,
    per FR17 in the CRS ("activate/deactivate testimonials").
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='testimonials')
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)  # 1–5, optional in the UI but stored either way
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Testimonial by {self.user.username}"