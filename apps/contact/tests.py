from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.contact.models import Inquiry


class ContactAPITests(APITestCase):
    def test_valid_contact_submission(self):
        url = reverse('contact:contact-submit')
        payload = {
            'name': 'Recruiter Bob',
            'email': 'bob@talent.com',
            'subject': 'Senior Backend Role at ScaleCo',
            'message': 'We love your portfolio architecture. Let us talk!',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        
        inquiry = Inquiry.objects.get(email='bob@talent.com')
        self.assertFalse(inquiry.is_spam)
        self.assertEqual(inquiry.name, 'Recruiter Bob')

    def test_honeypot_spam_trap(self):
        url = reverse('contact:contact-submit')
        payload = {
            'name': 'Bot Scraper',
            'email': 'bot@spam.com',
            'subject': 'Crypto Offer',
            'message': 'Click here',
            'website_url_hp': 'http://malicious-spam-url.com'  # Bot fills hidden field
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        inquiry = Inquiry.objects.get(email='bot@spam.com')
        self.assertTrue(inquiry.is_spam)
        self.assertEqual(inquiry.status, 'spam')
