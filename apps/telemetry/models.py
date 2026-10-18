import hashlib
from django.db import models


class VisitLog(models.Model):
    path = models.CharField(max_length=512, db_index=True)
    method = models.CharField(max_length=10)
    ip_hash = models.CharField(max_length=64, db_index=True, help_text="SHA-256 hashed anonymized IP")
    referrer = models.CharField(max_length=512, blank=True, default='')
    user_agent = models.CharField(max_length=512, blank=True, default='')
    status_code = models.PositiveSmallIntegerField(default=200)
    response_time_ms = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Visit Log'
        verbose_name_plural = 'Visit Logs'

    def __str__(self):
        return f"{self.method} {self.path} ({self.status_code}) - {self.response_time_ms:.1f}ms"


class InteractionMetric(models.Model):
    INTERACTION_TYPES = [
        ('PROJECT_VIEW', 'Project View'),
        ('DEMO_CLICK', 'Live Demo Click'),
        ('GITHUB_CLICK', 'GitHub Repo Click'),
        ('RESUME_DOWNLOAD', 'Resume Download'),
        ('TERMINAL_COMMAND', 'Terminal Command Executed'),
    ]

    interaction_type = models.CharField(max_length=32, choices=INTERACTION_TYPES, db_index=True)
    target_identifier = models.CharField(max_length=255, blank=True, default='', help_text="e.g. project slug or tag")
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.interaction_type}: {self.target_identifier}"
