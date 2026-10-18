from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .services import GitHubSyncService
from apps.resume.models import BioProfile


class GitHubStatsView(APIView):
    """
    Returns live or cached GitHub statistics for the portfolio owner.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        username = request.query_params.get('username')
        if not username:
            profile = BioProfile.objects.first()
            if profile and profile.github_url:
                username = profile.github_url.rstrip('/').split('/')[-1]
            else:
                username = 'octocat'

        data = GitHubSyncService.sync_github_profile(username=username)
        return Response(data, status=status.HTTP_200_OK)
