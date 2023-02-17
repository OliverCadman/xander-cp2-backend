"""Tests for data models"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from moto import mock_s3
import boto3
from django.conf import settings

from core.models import (
    UserProfile,
    Language,
    Module,
    Topic, 
    TextBlock,
    Lesson,
    Exercise
)

from unittest.mock import patch


def create_user(email='test@example.com', password='testpass123'):
    return get_user_model().objects.create_user(
        email=email,
        password=password
    )

def create_language():
    """Create and return a test language"""
    return Language.objects.create(
        language_name='Test Language'
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


class LMSModelTests(TestCase):
    """Tests for the various LMS Data Models"""

    def test_create_language(self):
        """Test creating a language object."""

        language_name = 'Test Language'

        language = Language.objects.create(
            language_name=language_name
        )
        
        self.assertEqual(language.language_name, language_name)
        self.assertEqual(language.__str__(), language_name)


    def test_create_module(self):
        """Test creating a module object, with a language relation."""

        module_name = 'Test Module'

        language = Language.objects.create(
            language_name='Test Language'
        )

        module = Module.objects.create(
            language=language,
            module_name=module_name
        )

        self.assertEqual(module.language, language)
        self.assertEqual(module.module_name, module_name)
        self.assertEqual(len(language.modules.all()), 1)

    def test_create_topic(self):
        """Test creating a topic."""

        topic_name = 'Test Topic'
        module_name = 'Test Module'

        language = Language.objects.create(
            language_name='Test Language'
        )

        module = Module.objects.create(
            module_name=module_name,
            language=language
        )

        topic = Topic.objects.create(
            topic_name=topic_name,
            module=module
        )

        self.assertEqual(module.language, language)
        self.assertEqual(module.module_name, module_name)
        self.assertEqual(len(language.modules.all()), 1)
        self.assertEqual(topic.module, module)
        self.assertEqual(topic.topic_name, topic_name)
        self.assertEqual(len(module.topics.all()), 1)
    
    def test_create_textblock(self):

        text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit,'\
            ' sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'\
            ' Nunc sed augue lacus viverra vitae congue. Non consectetur a erat nam at lectus urna duis.'\
            ' Sed egestas egestas fringilla phasellus faucibus scelerisque eleifend donec.'\
            'Blandit cursus risus at ultrices mi. Lorem donec massa sapien faucibus et molestie.'\
            ' Nisl condimentum id venenatis a condimentum vitae sapien pellentesque habitant.'\
            ' Feugiat in ante metus dictum at tempor. Sociis natoque penatibus'\
            ' et magnis dis parturient montes nascetur.'\
            ' Egestas egestas fringilla phasellus faucibus scelerisque eleifend donec. '\
            'Nunc vel risus commodo viverra. Enim ut tellus elementum sagittis vitae et.'\
            ' Velit aliquet sagittis id consectetur purus ut.'
        
        text_format = 1
        paragraph_number = 1
        language = Language.objects.create(
            language_name='Test Language'
        )

        module = Module.objects.create(
            language=language,
            module_name='Test Module'
        )

        topic = Topic.objects.create(
            module=module,
            topic_name='Test Topic'
        )

        lesson = Lesson.objects.create(
            topic=topic,
            lesson_name='Test Lesson'
        )

        textblock = TextBlock.objects.create(
            lesson=lesson,
            text=text,
            text_format=text_format,
            paragraph_number=paragraph_number
        )

        self.assertEqual(textblock.lesson, lesson)


    def test_textblock_paragraph_num_increment(self):
        """
        Test the paragraph_number field increases
        with each creation of textblock object.
        """

        test_starter_code = f'function testStarter()'
        test_expected_output = f'Test Expected Output'

        text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit,'\
            ' sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'\
            ' Nunc sed augue lacus viverra vitae congue. Non consectetur a erat nam at lectus urna duis.'\
            ' Sed egestas egestas fringilla phasellus faucibus scelerisque eleifend donec.'\
            'Blandit cursus risus at ultrices mi. Lorem donec massa sapien faucibus et molestie.'\
            ' Nisl condimentum id venenatis a condimentum vitae sapien pellentesque habitant.'\
            ' Feugiat in ante metus dictum at tempor. Sociis natoque penatibus'\
            ' et magnis dis parturient montes nascetur.'\
            ' Egestas egestas fringilla phasellus faucibus scelerisque eleifend donec. '\
            'Nunc vel risus commodo viverra. Enim ut tellus elementum sagittis vitae et.'\
            ' Velit aliquet sagittis id consectetur purus ut.'
        
        text_format = 1

        language = Language.objects.create(
            language_name='Test Language'
        )

        module = Module.objects.create(
            language=language,
            module_name='Test Module'
        )

        topic = Topic.objects.create(
            module=module,
            topic_name='Test Topic'
        )

        exercise = Exercise.objects.create(
            topic=topic,
            exercise_name='Test Exercise',
            starter_code=test_starter_code,
            expected_output=test_expected_output,

        )

        for i in range(5):
            textblock = TextBlock.objects.create(
                text=text,
                exercise=exercise,
                text_format=text_format,
                paragraph_number=i
            )

            self.assertEqual(textblock.exercise, exercise)
        self.assertEqual(len(exercise.exercise_textblocks.all()), 5)
    
    def test_create_lesson(self):
        """Test Creating a Lesson"""

        lesson_name = 'Test Lesson'

        language = create_language()

        module = Module.objects.create(
            language=language,
            module_name='Test Module'
        )

        topic = Topic.objects.create(
            module=module,
            topic_name='Test Topic'
        )

        lesson = Lesson.objects.create(
            topic=topic,
            lesson_name='Test Lesson'
        )

        self.assertEqual(str(lesson), lesson_name)

        text = 'Test Text Block'
        
        for _ in range(5):
            textblock = TextBlock.objects.create(
                lesson=lesson,
                text=text,
                paragraph_number=1,
                text_format=1
            )

            self.assertEqual(textblock.lesson, lesson)
        self.assertEqual(len(lesson.lesson_textblocks.all()), 5)


    def test_create_exercise(self):
        """Test creating an exercise."""

        exercise_name = 'Test Exercise'

        language = Language.objects.create(
            language_name='Test Language'
        )

        module = Module.objects.create(
            language=language,
            module_name='Test Module'
        )

        topic = Topic.objects.create(
            module=module,
            topic_name='Test Topic'
        )

        exercise = Exercise.objects.create(
            topic=topic,
            exercise_name=exercise_name
        )

        self.assertEqual(str(exercise), exercise_name)
