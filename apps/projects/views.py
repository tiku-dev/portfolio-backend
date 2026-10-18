import time
import requests
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Tag, Project
from .serializers import TagSerializer, ProjectListSerializer, ProjectDetailSerializer


class TagListView(generics.ListAPIView):
    """List all technology tags, optionally filtered by category."""
    permission_classes = [AllowAny]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name']
    pagination_class = None


class ProjectListView(generics.ListAPIView):
    """List all projects with filtering by category, tag, or featured status."""
    permission_classes = [AllowAny]
    serializer_class = ProjectListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['featured', 'health_status', 'tags__slug']
    search_fields = ['title', 'tagline', 'problem_statement']
    ordering_fields = ['order', 'created_at', 'github_stars']

    def get_queryset(self):
        return Project.objects.prefetch_related('tags', 'metrics').all()


class ProjectDetailView(generics.RetrieveAPIView):
    """Retrieve full case-study details of a project by slug."""
    permission_classes = [AllowAny]
    serializer_class = ProjectDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Project.objects.prefetch_related('tags', 'metrics', 'architecture_nodes').all()


class ProjectLivePingView(APIView):
    """
    Real-time health probe for a project's live deployment.
    Executes an active HTTP GET request, records latency and HTTP status,
    and updates the database.
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        try:
            project = Project.objects.get(slug=slug)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found.'}, status=status.HTTP_404_NOT_FOUND)

        target_url = project.health_check_url or project.demo_url
        if not target_url:
            return Response({
                'status': 'offline',
                'detail': 'No demo or health check URL configured for this project.',
                'latency_ms': None
            }, status=status.HTTP_200_OK)

        start = time.perf_counter()
        try:
            resp = requests.get(target_url, timeout=5)
            latency_ms = round((time.perf_counter() - start) * 1000, 2)
            is_healthy = 200 <= resp.status_code < 400
            new_status = 'healthy' if is_healthy else 'degraded'
            
            project.health_status = new_status
            project.last_health_check = timezone.now()
            project.save(update_fields=['health_status', 'last_health_check'])

            return Response({
                'status': new_status,
                'http_code': resp.status_code,
                'latency_ms': latency_ms,
                'target_url': target_url,
                'checked_at': project.last_health_check
            }, status=status.HTTP_200_OK)
        except requests.RequestException as exc:
            project.health_status = 'offline'
            project.last_health_check = timezone.now()
            project.save(update_fields=['health_status', 'last_health_check'])

            return Response({
                'status': 'offline',
                'error': str(exc),
                'latency_ms': None,
                'target_url': target_url,
                'checked_at': project.last_health_check
            }, status=status.HTTP_200_OK)
