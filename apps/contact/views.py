import threading
import logging
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Inquiry
from .serializers import InquiryCreateSerializer
from .throttling import ContactSubmissionThrottle

logger = logging.getLogger(__name__)


def send_email_async(subject, body, to_email):
    def _target():
        try:
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@portfolio.local')
            send_mail(
                subject=subject,
                message=body,
                from_email=from_email,
                recipient_list=[to_email],
                fail_silently=False,
            )
            print(f"[Contact Email] Notification successfully sent to {to_email}")
        except Exception as e:
            logger.exception("Failed to send contact notification email: %s", e)
            print(f"[Contact Email Error] Could not send email to {to_email}: {e}")

    thread = threading.Thread(target=_target, daemon=True)
    thread.start()


class ContactSubmissionView(generics.CreateAPIView):
    """
    Submits a contact inquiry with rate limiting, honeypot spam protection,
    and asynchronous email notification dispatch.
    """
    permission_classes = [AllowAny]
    serializer_class = InquiryCreateSerializer
    throttle_classes = [ContactSubmissionThrottle]

    def perform_create(self, serializer):
        # Extract client IP
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = self.request.META.get('REMOTE_ADDR')

        inquiry = serializer.save(ip_address=ip)

        # Only send email if not flagged as bot spam
        if not inquiry.is_spam:
            notification_target = getattr(settings, 'NOTIFICATION_EMAIL', 'admin@example.com')
            email_subject = f"📬 Portfolio Lead from {inquiry.name}: {inquiry.subject}"
            email_body = (
                f"You received a new message from your portfolio backend!\n\n"
                f"From: {inquiry.name} ({inquiry.email})\n"
                f"Subject: {inquiry.subject}\n"
                f"IP: {ip}\n\n"
                f"Message:\n{inquiry.message}\n"
            )
            send_email_async(email_subject, email_body, notification_target)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'success': True,
            'message': 'Thank you! Your message has been safely received. I will get back to you shortly.',
        }, status=status.HTTP_201_CREATED)
