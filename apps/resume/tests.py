from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.resume.models import BioProfile, Experience, Education
from datetime import date


class ResumeAPITests(APITestCase):
    def setUp(self):
        BioProfile.objects.create(
            full_name='Jane Doe',
            headline='Cloud Architect',
            email='jane@example.com',
            location='Berlin, Germany'
        )
        Experience.objects.create(
            company='TechCorp',
            role='Senior Backend Engineer',
            start_date=date(2022, 1, 1),
            is_current=True,
            summary='Building systems',
            achievements=['Delivered 99.99% uptime']
        )
        Education.objects.create(
            institution='Technical University',
            degree='B.Sc.',
            field_of_study='Informatics',
            start_year=2016,
            end_year=2019
        )

    def test_resume_json_endpoint(self):
        url = reverse('resume:resume-data')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['profile']['full_name'], 'Jane Doe')
        self.assertEqual(len(response.data['experiences']), 1)
        self.assertEqual(response.data['experiences'][0]['company'], 'TechCorp')

    def test_resume_pdf_download(self):
        url = reverse('resume:resume-pdf-download')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        # Check PDF signature
        content = b"".join(response.streaming_content)
        self.assertTrue(content.startswith(b'%PDF-'))
