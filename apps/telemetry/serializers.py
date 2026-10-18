from rest_framework import serializers
from .models import VisitLog, InteractionMetric


class InteractionMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = InteractionMetric
        fields = ['id', 'interaction_type', 'target_identifier', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class TelemetrySummarySerializer(serializers.Serializer):
    total_requests_served = serializers.IntegerField()
    average_response_time_ms = serializers.FloatField()
    unique_visitors_est = serializers.IntegerField()
    top_endpoints = serializers.ListField(child=serializers.DictField())
    interaction_counts = serializers.DictField()
    uptime_status = serializers.CharField()

