import time
import requests
from django.conf import settings
from django.utils import timezone
from django.core.cache import cache
from apps.projects.models import Project


class GitHubSyncService:
    """
    Synchronizes public GitHub statistics (stars, public repos, followers)
    and updates Project records with their live GitHub metrics.
    """
    CACHE_KEY = 'portfolio_github_stats'
    CACHE_TTL = 3600  # 1 hour

    @classmethod
    def sync_github_profile(cls, username: str = 'octocat'):
        cached = cache.get(cls.CACHE_KEY)
        if cached:
            return cached

        headers = {'Accept': 'application/vnd.github.v3+json'}
        github_token = getattr(settings, 'GITHUB_TOKEN', None)
        if github_token:
            headers['Authorization'] = f"token {github_token}"

        try:
            # 1. Fetch user stats
            user_url = f"https://api.github.com/users/{username}"
            u_resp = requests.get(user_url, headers=headers, timeout=5)
            u_data = u_resp.json() if u_resp.status_code == 200 else {}

            # 2. Fetch repos to sum stars and match projects
            repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
            r_resp = requests.get(repos_url, headers=headers, timeout=5)
            repos_data = r_resp.json() if r_resp.status_code == 200 else []

            total_stars = 0
            total_forks = 0
            repo_map = {}

            if isinstance(repos_data, list):
                for r in repos_data:
                    stars = r.get('stargazers_count', 0)
                    forks = r.get('forks_count', 0)
                    total_stars += stars
                    total_forks += forks
                    repo_map[r.get('name', '').lower()] = {
                        'stars': stars,
                        'forks': forks,
                        'url': r.get('html_url')
                    }

            # 3. Update existing Project records in DB if GitHub URL matches
            for project in Project.objects.exclude(github_url=''):
                for repo_name, repo_info in repo_map.items():
                    if repo_name in project.github_url.lower():
                        project.github_stars = repo_info['stars']
                        project.github_forks = repo_info['forks']
                        project.save(update_fields=['github_stars', 'github_forks'])

            payload = {
                'username': username,
                'public_repos': u_data.get('public_repos', len(repos_data)),
                'followers': u_data.get('followers', 0),
                'total_stars': total_stars,
                'total_forks': total_forks,
                'synced_at': timezone.now().isoformat()
            }
            cache.set(cls.CACHE_KEY, payload, cls.CACHE_TTL)
            return payload

        except Exception as exc:
            return {
                'error': f"Failed to sync GitHub: {str(exc)}",
                'username': username,
                'synced_at': timezone.now().isoformat()
            }


class HealthProbeService:
    """
    Pings all active projects with demo URLs and updates their operational health status.
    """
    @classmethod
    def probe_all_projects(cls):
        projects = Project.objects.exclude(demo_url='', health_check_url='')
        results = []

        for p in projects:
            target_url = p.health_check_url or p.demo_url
            try:
                start = time.perf_counter()
                resp = requests.get(target_url, timeout=5)
                latency = round((time.perf_counter() - start) * 1000, 2)
                p.health_status = 'healthy' if 200 <= resp.status_code < 400 else 'degraded'
                p.last_health_check = timezone.now()
                p.save(update_fields=['health_status', 'last_health_check'])
                results.append({'slug': p.slug, 'status': p.health_status, 'latency_ms': latency})
            except Exception as e:
                p.health_status = 'offline'
                p.last_health_check = timezone.now()
                p.save(update_fields=['health_status', 'last_health_check'])
                results.append({'slug': p.slug, 'status': 'offline', 'error': str(e)})

        return results

