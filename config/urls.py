from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.db import connection


class HealthCheckView(APIView):
    """
    Standard container orchestration healthcheck probe (/api/health/).
    Verifies database connectivity and system availability.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        db_healthy = True
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        except Exception:
            db_healthy = False

        status_code = status.HTTP_200_OK if db_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
        return Response({
            'status': 'healthy' if db_healthy else 'unhealthy',
            'database': 'connected' if db_healthy else 'disconnected',
            'framework': 'Django 5.x',
            'api_version': 'v1'
        }, status=status_code)


class APIRootDirectoryView(APIView):
    """
    Welcome & Index directory for the Portfolio Backend API.
    Provides immediate discoverability for all endpoints.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        base = request.build_absolute_uri('/api/v1/')
        return Response({
            'message': 'Welcome to the Professional Portfolio Backend API 🚀',
            'version': '1.0.0',
            'endpoints': {
                'projects': f"{base}projects/",
                'project_tags': f"{base}projects/tags/",
                'resume_data': f"{base}resume/",
                'resume_pdf_download': f"{base}resume/pdf/?focus=backend",
                'contact_submit': f"{base}contact/",
                'terminal_cli': f"{base}terminal/execute/",
                'telemetry_stats': f"{base}telemetry/stats/",
                'sync_github': f"{base}sync/github/",
                'health_check': request.build_absolute_uri('/api/health/'),
            },
            'terminal_quickstart': 'POST /api/v1/terminal/execute/ with {"command": "help"}'
        })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', HealthCheckView.as_view(), name='health-check'),
    path('api/v1/', APIRootDirectoryView.as_view(), name='api-root'),

    # Modular Portfolio Endpoints
    path('api/v1/projects/', include('apps.projects.urls', namespace='projects')),
    path('api/v1/resume/', include('apps.resume.urls', namespace='resume')),
    path('api/v1/contact/', include('apps.contact.urls', namespace='contact')),
    path('api/v1/terminal/', include('apps.terminal.urls', namespace='terminal')),
    path('api/v1/telemetry/', include('apps.telemetry.urls', namespace='telemetry')),
    path('api/v1/sync/', include('apps.sync_engine.urls', namespace='sync_engine')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
