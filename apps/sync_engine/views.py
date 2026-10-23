from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .services import GitHubSyncService
from apps.resume.models import BioProfile


class GitHubStatsView(APIView):
    """
    Returns live or cached GitHub statistics and repositories for the portfolio owner.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        username = request.query_params.get('username')
        force = request.query_params.get('force', '').lower() in ('true', '1')

        if not username:
            profile = BioProfile.objects.first()
            if profile and profile.github_url:
                username = profile.github_url.rstrip('/').split('/')[-1]
            else:
                username = 'tiku-dev'

        data = GitHubSyncService.sync_github_profile(username=username, force_refresh=force, sync_projects=True)
        return Response(data, status=status.HTTP_200_OK)
