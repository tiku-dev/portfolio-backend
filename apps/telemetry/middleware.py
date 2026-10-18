import hashlib
import time
from .models import VisitLog


class TelemetryMiddleware:
    """
    Non-intrusive, privacy-preserving telemetry middleware.
    Hashes the client's IP to preserve visitor privacy (GDPR compliant),
    measures execution duration, and logs visits to the API endpoints.
    """
    EXCLUDE_PREFIXES = ('/admin/', '/static/', '/media/', '/favicon.ico')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(self.EXCLUDE_PREFIXES):
            return self.get_response(request)

        start_time = time.perf_counter()
        response = self.get_response(request)
        duration_ms = (time.perf_counter() - start_time) * 1000.0

        # Anonymize IP via SHA-256
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '')

        ip_hash = hashlib.sha256(ip.encode('utf-8')).hexdigest() if ip else ''

        # Asynchronously or gracefully record log without failing the request
        try:
            VisitLog.objects.create(
                path=request.path[:512],
                method=request.method[:10],
                ip_hash=ip_hash,
                referrer=request.META.get('HTTP_REFERER', '')[:512],
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:512],
                status_code=response.status_code,
                response_time_ms=round(duration_ms, 2)
            )
        except Exception:
            # Telemetry failures should never interrupt normal request flow
            pass

        return response

