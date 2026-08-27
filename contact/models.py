from django.db import models


class ContactQuery(models.Model):
    """
    A message submitted through the public Contact Us form. status lets
    admin mark it as handled without deleting the record — matches FR18
    in the CRS ("view and manage Contact Us queries").
    """
    STATUS_CHOICES = [
        ('new', 'New'),
        ('resolved', 'Resolved'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} — {self.name}"


class Subscriber(models.Model):
    """
    Newsletter signups from the footer form. Kept as its own model rather
    than folding into ContactQuery since it's a completely different
    purpose (marketing list vs. support inbox) — FR22 treats them as
    separate admin-manageable things.
    """
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class ContactDetails(models.Model):
    """
    Single-row model holding the site's contact info (address, phone,
    email) that admin can edit via FR21. Not tied to a user or any FK —
    the view will always fetch the first (and only) row, creating a
    default one if it doesn't exist yet.
    """
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    map_embed = models.TextField(blank=True)  # optional iframe embed code

    def __str__(self):
        return "Contact Details"