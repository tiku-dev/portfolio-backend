from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.projects.models import Tag, Project
from apps.resume.models import BioProfile


class TerminalCommandTests(APITestCase):
    def setUp(self):
        BioProfile.objects.create(
            full_name='Test Dev',
            headline='Backend Architect',
            email='dev@example.com',
            location='Remote'
        )
        t = Tag.objects.create(name='Python', category='backend')
        p = Project.objects.create(
            title='Sample Project',
            slug='sample-project',
            tagline='A fast demo',
            problem_statement='Testing',
            architecture_overview='Microservices'
        )
        p.tags.add(t)

    def test_execute_help(self):
        url = reverse('terminal:terminal-execute')
        response = self.client.post(url, {'command': 'help'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("PORTFOLIO DEVELOPER CONSOLE", response.data['output'])

    def test_execute_whoami(self):
        url = reverse('terminal:terminal-execute')
        response = self.client.post(url, {'command': 'whoami'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Test Dev", response.data['output'])

    def test_execute_skills_tree(self):
        url = reverse('terminal:terminal-execute')
        response = self.client.post(url, {'command': 'skills --tree'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("BACKEND", response.data['output'])
        self.assertIn("Python", response.data['output'])

    def test_execute_projects(self):
        url = reverse('terminal:terminal-execute')
        response = self.client.post(url, {'command': 'projects'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("sample-project", response.data['output'])

    def test_execute_cat_project(self):
        url = reverse('terminal:terminal-execute')
        response = self.client.post(url, {'command': 'cat project sample-project'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Sample Project", response.data['output'])
        self.assertIn("Microservices", response.data['output'])
