from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.projects.models import Tag, Project, ProjectMetric


class ProjectAPITests(APITestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name='Django', category='backend')
        self.project = Project.objects.create(
            title='Realtime Event Pipeline',
            slug='realtime-pipeline',
            tagline='Scalable pipeline',
            problem_statement='Tackling bottleneck',
            architecture_overview='Built with Celery & Redis',
            featured=True,
            order=1,
            demo_url='https://example.com'
        )
        self.project.tags.add(self.tag)
        self.metric = ProjectMetric.objects.create(
            project=self.project,
            label='Throughput',
            value='10k req/s'
        )

    def test_list_projects(self):
        url = reverse('projects:project-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Realtime Event Pipeline')

    def test_project_detail(self):
        url = reverse('projects:project-detail', kwargs={'slug': 'realtime-pipeline'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], 'realtime-pipeline')
        self.assertEqual(len(response.data['metrics']), 1)
        self.assertEqual(response.data['metrics'][0]['label'], 'Throughput')

    def test_filter_by_tag(self):
        url = reverse('projects:project-list') + '?tags__slug=django'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(results), 1)

    def test_tags_list(self):
        url = reverse('projects:tag-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)
