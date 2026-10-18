"""
Asynchronous background tasks for Celery.
These can be registered with Celery Beat to execute periodically.
"""
try:
    from celery import shared_task
except ImportError:
    # Fallback decorator if celery is not installed in the environment
    def shared_task(func):
        return func

from .services import GitHubSyncService, HealthProbeService
from apps.resume.models import BioProfile


@shared_task
def sync_github_task():
    profile = BioProfile.objects.first()
    username = 'octocat'
    if profile and profile.github_url:
        parts = profile.github_url.rstrip('/').split('/')
        if parts:
            username = parts[-1]

    return GitHubSyncService.sync_github_profile(username=username)


@shared_task
def probe_projects_health_task():
    return HealthProbeService.probe_all_projects()

