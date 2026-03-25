from django.db import models
from django.utils import timezone


class Company(models.Model):
    """
    A company that posts jobs on the scraped sources.
    """

    name = models.CharField(max_length=255, unique=True)
    website_url = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, default="")
    description = models.TextField(blank=True, default="")

    # Small text logo (e.g. "TC") used by your frontend.
    logo_text = models.CharField(max_length=10, blank=True, default="")

    scraped_source = models.CharField(max_length=100, default="weworkremotely")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.logo_text and self.name:
            # Keep it deterministic and frontend-friendly.
            parts = [p for p in self.name.replace(".", " ").split() if p]
            if len(parts) >= 2:
                self.logo_text = (parts[0][0] + parts[1][0]).upper()
            else:
                self.logo_text = self.name[:2].upper()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Job(models.Model):
    """
    A job listing captured by Scrapy.
    """

    company = models.ForeignKey(Company, related_name="jobs", on_delete=models.CASCADE)
    job_url = models.URLField(unique=True)

    title = models.CharField(max_length=500)
    location = models.CharField(max_length=255, blank=True, default="")
    job_type = models.CharField(max_length=255, blank=True, default="")

    # Your frontend expects these fields to exist.
    salary = models.CharField(max_length=255, blank=True, default="")
    salary_range = models.CharField(max_length=64, blank=True, default="")

    # Stored as JSON so we can put your tag chips here.
    tags = models.JSONField(default=list, blank=True)

    posted_text = models.CharField(max_length=255, blank=True, default="")
    description = models.TextField(blank=True, default="")

    # Sometimes the real application link requires an account.
    apply_url = models.URLField(blank=True, null=True)

    scraped_term = models.CharField(max_length=255, blank=True, default="")
    scraped_at = models.DateTimeField(default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["location"]),
            models.Index(fields=["scraped_term"]),
            models.Index(fields=["scraped_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.title} @ {self.company.name}"
