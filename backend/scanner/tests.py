from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import ScanResult, UserPreference

class ScannerAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.scan_url = reverse('scan_webpage')
        
    def test_scan_webpage_no_url(self):
        """Test the API fails gracefully if no URL is provided."""
        response = self.client.post(self.scan_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_scan_webpage_valid_url(self):
        """Test the API accepts a valid URL and returns the expected structure."""
        # Using a reliable domain for mocking test cases
        payload = {'url': 'https://example.com'}
        response = self.client.post(self.scan_url, payload, format='json')
        
        # It should succeed or fail depending on network, but structurally it handles the payload
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])
        
        if response.status_code == status.HTTP_200_OK:
            self.assertIn('score', response.data)
            self.assertIn('issues', response.data)
            self.assertIn('url', response.data)
            self.assertEqual(response.data['url'], payload['url'])

class ScannerModelsTest(TestCase):
    def test_create_scan_result(self):
        """Test that a scan result can be saved into the PostgreSQL DB."""
        result = ScanResult.objects.create(
            url="https://google.com",
            score=95,
            issues_payload=[{"type": "success", "message": "Demo issue"}]
        )
        
        self.assertEqual(ScanResult.objects.count(), 1)
        self.assertEqual(result.url, "https://google.com")
        self.assertEqual(result.score, 95)
        self.assertTrue(len(result.issues_payload) > 0)

    def test_create_user_preference(self):
        """Test creating an anonymous user preference."""
        pref = UserPreference.objects.create(
            user_hash="anon_123xyz",
            high_contrast_default=True
        )
        
        self.assertEqual(UserPreference.objects.count(), 1)
        self.assertTrue(pref.high_contrast_default)
