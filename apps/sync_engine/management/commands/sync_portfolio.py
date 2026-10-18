from django.core.management.base import BaseCommand
from apps.sync_engine.services import GitHubSyncService, HealthProbeService
from apps.resume.models import BioProfile


class Command(BaseCommand):
    help = 'Synchronizes GitHub metrics and probes live project health statuses.'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='GitHub username to sync', default=None)

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("🚀 Starting portfolio sync..."))

        username = options['username']
        if not username:
            profile = BioProfile.objects.first()
            if profile and profile.github_url:
                username = profile.github_url.rstrip('/').split('/')[-1]
            else:
                username = 'octocat'

        self.stdout.write(f"Syncing GitHub stats for '{username}'...")
        stats = GitHubSyncService.sync_github_profile(username)
        self.stdout.write(self.style.SUCCESS(f"✅ GitHub Stats: {stats}"))

        self.stdout.write("Probing project live demo health endpoints...")
        probes = HealthProbeService.probe_all_projects()
        self.stdout.write(self.style.SUCCESS(f"✅ Health Probes Completed: {len(probes)} checked."))

