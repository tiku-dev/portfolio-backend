from django.urls import path
from .views import PublicTelemetryStatsView, RecordInteractionView

app_name = 'telemetry'

urlpatterns = [
    path('stats/', PublicTelemetryStatsView.as_view(), name='public-stats'),
    path('track/', RecordInteractionView.as_view(), name='track-interaction'),
]

