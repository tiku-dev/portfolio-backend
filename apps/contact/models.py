from django.db import models


class Inquiry(models.Model):
    STATUS_CHOICES = [
        ('unread', 'Unread ✉️'),
        ('responded', 'Responded ✅'),
        ('spam', 'Spam Flagged 🚫'),
        ('archived', 'Archived 📦'),
    ]

    name = models.CharField(max_length=128)
    email = models.EmailField()
    subject = models.CharField(max_length=255, blank=True, default="Portfolio Inbound Message")
    message = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unread')
    is_spam = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Inquiries'

    def __str__(self):
        return f"From {self.name} ({self.email}) - {self.status}"
