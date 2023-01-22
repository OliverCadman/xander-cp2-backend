"""Tests for data models"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import UserProfile


def create_user(email='test@example.com', password='testpass123'):
    return get_user_model().objects.create_user(
        email=email,
        password=password
    )


class UserModelTests(TestCase):
    """Tests for the custom user model"""


    def test_user_model_created(self):
        """
        Test creating a user with email and password only is
        successful.
        """
        email = 'test@example.com'
        password = 'testpass123'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_email_normalized(self):
        """
        Test email is normalised when creating a new user.
        """
        test_emails = [
            ['test1@ExAMPle.com', 'test1@example.com'],
            ['test2@EXAMPLE.com', 'test2@example.com'],
            ['test3@example.COM', 'test3@example.com'],
            ['test4@example.com', 'test4@example.com']
        ]

        for email, expected_email in test_emails:
            user = get_user_model().objects.create_user(
                email=email,
                password='testpass123'
            )
            self.assertEqual(user.email, expected_email)


    def test_create_user_without_email_raises_error(self):
        """
        Test ValueError is raised when new user registers without email
        """
        
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email='',
                password='testpass123'
            )

    def test_create_superuser(self):
        """
        Test creating a superuser is successful.
        """

        email = 'test@example.com'
        password = 'testpass123'

        superuser = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

    def test_create_user_creates_userprofile(self):

        email = 'test@example.com'
        password = 'testpass123'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        user_profile = UserProfile.objects.get(
            auth_user=user
        )

        self.assertEqual(user_profile.auth_user, user)
