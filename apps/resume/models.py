from django.db import models
from apps.projects.models import Tag


class BioProfile(models.Model):
    full_name = models.CharField(max_length=128)
    headline = models.CharField(max_length=255, help_text="e.g. Senior Backend Engineer | Distributed Systems & Python")
    summary = models.TextField()
    email = models.EmailField()
    location = models.CharField(max_length=128)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    available_for_hire = models.BooleanField(default=True)
    availability_notice = models.CharField(max_length=128, default="Immediately available for remote/hybrid roles")

    class Meta:
        verbose_name = "Bio & Profile"
        verbose_name_plural = "Bio & Profile"

    def __str__(self):
        return self.full_name


class Experience(models.Model):
    company = models.CharField(max_length=128)
    role = models.CharField(max_length=128)
    location = models.CharField(max_length=128, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    summary = models.TextField(blank=True)
    achievements = models.JSONField(default=list, help_text="List of technical accomplishments")
    tags = models.ManyToManyField(Tag, blank=True, related_name='experiences')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-start_date']

    def __str__(self):
        return f"{self.role} at {self.company}"


class Education(models.Model):
    institution = models.CharField(max_length=128)
    degree = models.CharField(max_length=128)
    field_of_study = models.CharField(max_length=128)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(null=True, blank=True)
    details = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-start_year']

    def __str__(self):
        return f"{self.degree} in {self.field_of_study} - {self.institution}"
