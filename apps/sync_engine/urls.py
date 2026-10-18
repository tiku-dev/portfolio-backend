from django.urls import path
from .views import GitHubStatsView

app_name = 'sync_engine'

urlpatterns = [
    path('github/', GitHubStatsView.as_view(), name='github-stats'),
]

