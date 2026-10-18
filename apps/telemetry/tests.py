from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.telemetry.models import VisitLog, InteractionMetric


class TelemetryTests(APITestCase):
    def test_middleware_records_visit(self):
        # Hit an API endpoint
        response = self.client.get(reverse('api-root'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if VisitLog recorded the entry
        logs = VisitLog.objects.filter(path=reverse('api-root'))
        self.assertTrue(logs.exists())
        log = logs.first()
        self.assertEqual(log.method, 'GET')
        self.assertEqual(log.status_code, 200)

    def test_public_stats_endpoint(self):
        url = reverse('telemetry:public-stats')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_requests_served', response.data)
        self.assertIn('average_response_time_ms', response.data)
        self.assertIn('uptime_status', response.data)

    def test_record_interaction(self):
        url = reverse('telemetry:track-interaction')
        payload = {
            'interaction_type': 'DEMO_CLICK',
            'target_identifier': 'sample-project'
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InteractionMetric.objects.filter(interaction_type='DEMO_CLICK').count(), 1)
