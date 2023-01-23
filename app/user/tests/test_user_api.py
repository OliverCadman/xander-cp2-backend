from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from core import models


CREATE_USER_URL = reverse('user:create')
CREATE_TOKEN_URL = reverse('user:token')
MANAGE_USER_URL = reverse('user:manage_user')
PROFILE_URL = reverse('user:user_profile')

def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(
        **params
    )


class PublicUserAPITests(TestCase):
    """Testing public features of the User API"""
    
    def setUp(self):
        self.client = APIClient()

    
    def test_create_user_successful(self):
        """Test POST request to create new user."""

        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test'
        }

        res = self.client.post(
            CREATE_USER_URL, payload
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])

        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
    
    def test_user_with_email_exists_throws_error(self):
        """Test error returned if user with email address already exists."""

        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name'
        }

        create_user(**payload)

        res = self.client.post(
            CREATE_USER_URL,
            payload
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_too_short_throws_error(self):
        """Test error raised when password less than 5 chars."""

        payload = {
            'email': 'test@example.com',
            'password': 'test',
            'name': 'Test'
        }

        res = self.client.post(
            CREATE_USER_URL,
            payload
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        )
        self.assertFalse(user_exists)

    
    def test_create_token(self):
        """Test generation of Auth Token for valid creds"""

        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'testpass123'
        }

        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password']
        }

        res = self.client.post(CREATE_TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_create_token_bad_credentials(self):
        """Test Token API returns error if invalid credentials"""

        create_user(email='test@example.com', password='testpass123')

        payload = {
            'email': 'test@example.com',
            'password': 'someotherpassword'
        }

        res = self.client.post(CREATE_TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)
    
    def test_create_token_with_blank_password_raises_error(self):
        """Test POST request without password raises error."""

        payload = {
            'email': 'test@example.com',
            'password': ''
        }

        res = self.client.post(CREATE_TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_retrieving_user_unauthorized(self):
        """Test 401 error if retrieving user without authentication"""

        res = self.client.get(MANAGE_USER_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
            name='Test Name'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_retrieve_auth_profile_successful(self):
        """Test retrieving an auth profile for logged-in user."""

        res = self.client.get(MANAGE_USER_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data,
            {
                'name': self.user.name,
                'email': self.user.email
            }
        )
    
    def test_update_auth_user_profile(self): 
        """Test updating auth user profile for authenticated user."""

        payload = {
            'name': 'Updated name',
            'password': 'newpassword123'
        }

        res = self.client.patch(MANAGE_USER_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_user_profile(self):
        """Test getting user profile for user."""

        test_res_data = {
            'first_name': None,
            'last_name': None,
            'cohort_number': None
        }

        res = self.client.get(PROFILE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for i in test_res_data.keys():
            self.assertIn(i, res.data)
    
    def test_update_user_profile(self):
        """Test updating user profile"""

        payload = {
            'first_name': 'Test First Name',
            'last_name': 'Test Last Name',
            'cohort_number': 9
        }

        res = self.client.patch(PROFILE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        profile = models.UserProfile.objects.get(
            auth_user=self.user
        )

        self.assertEqual(profile.first_name, payload['first_name'])
        self.assertEqual(profile.last_name, payload['last_name'])
        self.assertEqual(profile.cohort_number, payload['cohort_number'])
