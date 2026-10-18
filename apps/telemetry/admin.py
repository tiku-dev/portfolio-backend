from django.contrib import admin
from .models import VisitLog, InteractionMetric


@admin.register(VisitLog)
class VisitLogAdmin(admin.ModelAdmin):
    list_display = ('method', 'path', 'status_code', 'response_time_ms', 'timestamp')
    list_filter = ('method', 'status_code')
    search_fields = ('path', 'user_agent', 'referrer')
    readonly_fields = ('path', 'method', 'ip_hash', 'referrer', 'user_agent', 'status_code', 'response_time_ms', 'timestamp')


@admin.register(InteractionMetric)
class InteractionMetricAdmin(admin.ModelAdmin):
    list_display = ('interaction_type', 'target_identifier', 'timestamp')
    list_filter = ('interaction_type',)
    search_fields = ('target_identifier',)
    readonly_fields = ('interaction_type', 'target_identifier', 'timestamp')
