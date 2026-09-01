from django.db import models


class SiteContent(models.Model):
    page_key = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.page_key