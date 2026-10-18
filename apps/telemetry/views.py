from django.db.models import Avg, Count
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import VisitLog, InteractionMetric
from .serializers import InteractionMetricSerializer, TelemetrySummarySerializer


class PublicTelemetryStatsView(APIView):
    """
    Public live telemetry stats showing real backend metrics:
    total requests, average latency, visitor interactions, and top visited endpoints.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        total_requests = VisitLog.objects.count()
        avg_latency = VisitLog.objects.aggregate(avg=Avg('response_time_ms'))['avg'] or 0.0
        unique_ips = VisitLog.objects.values('ip_hash').distinct().count()

        top_paths = list(
            VisitLog.objects.values('path')
            .annotate(count=Count('path'))
            .order_by('-count')[:5]
        )

        interaction_aggregates = (
            InteractionMetric.objects.values('interaction_type')
            .annotate(count=Count('id'))
        )
        interaction_counts = {item['interaction_type']: item['count'] for item in interaction_aggregates}

        data = {
            'total_requests_served': total_requests,
            'average_response_time_ms': round(avg_latency, 2),
            'unique_visitors_est': unique_ips,
            'top_endpoints': top_paths,
            'interaction_counts': interaction_counts,
            'uptime_status': 'Operational 🟢',
        }
        serializer = TelemetrySummarySerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RecordInteractionView(generics.CreateAPIView):
    """
    Endpoint for frontend to record user interactions (e.g., clicking on project demo or downloading resume).
    """
    permission_classes = [AllowAny]
    serializer_class = InteractionMetricSerializer
    queryset = InteractionMetric.objects.all()
