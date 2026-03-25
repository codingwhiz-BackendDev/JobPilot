from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=255, null=True)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    link = models.URLField(null=True)
    remote = models.BooleanField(default=True)
    country = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company}"