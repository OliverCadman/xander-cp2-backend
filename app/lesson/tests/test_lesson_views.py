from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from core import models
from lesson import serializers

from unittest.mock import patch
from moto import mock_s3

import boto3


MODULE_LIST_URL = reverse('lesson:module-list')
TOPIC_LIST_URL = reverse('lesson:topic-list')
TEXTBLOCK_LIST_URL = reverse('lesson:textblock-list')
LESSON_LIST_URL = reverse('lesson:lesson-list')
EXERCISE_LIST_URL = reverse('lesson:exercise-list')


def module_detail_url(module_id):
    return reverse('lesson:module-detail', args=[module_id])


def topic_detail_url(topic_id):
    return reverse('lesson:topic-detail', args=[topic_id])


def create_user(**params):
    """Create and return a test user."""

    user = get_user_model().objects.create_user(
        **params
    )

    return user


def create_language():
    """Create and return a test language."""

    language = models.Language.objects.create(
        language_name='Test Language'
    )
    return language


def create_module(module_name):

    language = create_language()

    module = models.Module.objects.create(
        language=language,
        module_name=module_name
    )

    return module


def create_topic(topic_name, module):
    topic = models.Topic.objects.create(
        topic_name=topic_name,
        module=module
    )

    return topic

def create_topic_with_module(topic_name):

    module = create_module('Test Module')

    topic = models.Topic.objects.create(
        topic_name=topic_name,
        module=module
    )
    return topic


class PublicLessonAPITests(TestCase):
    """Tests for unauthenticated requests."""

    def setUp(self):
        self.client = APIClient()
    
    def test_auth_required(self):
        """Test 401 response returned when attempt to access lessons list"""

        res = self.client.get(MODULE_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateLessonAPITests(TestCase):
    """Tests for authenticated requests."""

    def setUp(self):
        self.client = APIClient()

        email = 'test@example.com'
        password = 'testpass123'

        self.user = create_user(email=email, password=password)
        self.client.force_authenticate(self.user)
    
    
    def test_module_post(self):
        """Test POST request to create a module."""

        language = create_language()

        payload = {
            'module_name': 'Test Module',
            'language': language.id
        }

        res = self.client.post(MODULE_LIST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    
    def test_module_list_get(self):
        """Test GET request to list modules"""

        create_module('Test Module 1')
        create_module('Test Module 2')
        create_module('Test Module 3')
        create_module('Test Module 4')

        res = self.client.get(MODULE_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 4)
    
    def test_get_module_detail(self):
        """Test getting individual module"""

        module = create_module('Test Module 1')

        res = self.client.get(module_detail_url(module.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('module_name', res.data)

    def test_topic_post(self):
        """Test POST request to create a topic."""

        module = create_module('Test Module')

        topic_name = 'Test Topic'

        payload = {
            'topic_name': topic_name,
            'module': module.id
        }

        res = self.client.post(TOPIC_LIST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    
    # def test_topics_list(self):
    #     """Test GET request for list of topics"""

    #     module = create_module('Test Module')

    #     create_topic('Test Topic 1', module)
    #     create_topic('Test Topic 2', module)
    #     create_topic('Test Topic 3', module)
    #     create_topic('Test Topic 4', module)
    #     create_topic('Test Topic 5', module)

    #     res = self.client.get(TOPIC_LIST_URL)
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 5)

    def get_topic_detail(self):
        """Test GET request for individual topic"""

        topic = create_topic_with_module('Test Topic')
        res = self.client.get(topic_detail_url(topic.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('topic_name', res.data)

    def test_lesson_post(self):
        """Test POST request for individual lesson"""

        topic = create_topic_with_module('Test Topic')
        payload = {
            'topic': topic.id,
            'lesson_name': 'Test Lesson'
        }

        res = self.client.post(LESSON_LIST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        lessons = models.Lesson.objects.all()
        self.assertEqual(len(lessons), 1)
    
    def test_textblock_post(self):
        """Test POST request for creating text block"""

        topic = create_topic_with_module('Test Topic')

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
        
        payload = {
            'text': text,
            'topic': topic.id,
            'text_format': 1,
            'paragraph_number': 1
        }

        res = self.client.post(TEXTBLOCK_LIST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    # Needs credentials!
    # def test_exercise_post(self):
    #     """Test POST request to create exercise"""

    #     exercise_name = 'Test Exercise'

    #     starter_code = """
    #         function helloWorld() {}
    #     """

    #     expected_output = "[1, 2, 3]"

    #     topic = create_topic_with_module('Test Topic')

    #     payload = {
    #         'topic': topic.id,
    #         'exercise_name': exercise_name,
    #         'starter_code': starter_code,
    #         'expected_output': expected_output
    #     }

    #     res = self.client.post(EXERCISE_LIST_URL, payload, format='json')

    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)


class ExerciseListTests(TestCase):
    """
    Tests for interacting with S3 Objects
    to list exercises.
    """

    @mock_s3
    def setUp(self):
        self.s3_client = boto3.client('s3')
        self.client = APIClient()

        language = models.Language.objects.create(
            language_name='Test Language'
        )

        module = models.Module.objects.create(
            language=language,
            module_name='Test Module'
        )

        self.topic = models.Topic.objects.create(
            module=module,
            topic_name='Test Topic'
        )

        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123'
        )

        self.client.force_authenticate(self.user)
        

    @mock_s3
    def test_get_exercises(self):
        self.bucket_name = settings.AWS_BUCKET_NAME
        self.s3_client.create_bucket(Bucket=self.bucket_name)
    
        for i in range(5):
            test_starter_code_key = f'test-startercode-{i}'
            test_expected_output_key = f'test-expectedoutput-{i}'
            test_starter_code_file = f'{test_starter_code_key}.txt'
            test_expected_output_file = f'{test_expected_output_key}.txt'

            test_starter_code = f'function testStarter{i}()'
            test_expected_output = f'Test Expected Output {i}'
            exercise = models.Exercise.objects.create(
                topic=self.topic,
                exercise_name=f'Test Exercise {i}'
            )

            models.TextBlock.objects.create(
                exercise=exercise,
                text='Test Text Block Paragraph',
                paragraph_number=i,
                text_format=1
            )

            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Body=test_starter_code,
                Key=test_starter_code_file
            )

            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Body=test_expected_output,
                Key=test_expected_output_file
            )

            exercise.starter_code = test_starter_code_key
            exercise.expected_output = test_expected_output_key
            exercise.save()

        res = self.client.get(TOPIC_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        print(res.data)

        topics = models.Topic.objects.all()
        serializer = serializers.TopicSerializer(topics, many=True)
        self.assertEqual(res.data, serializer.data)
        
    
class LessonTests(TestCase):
    """Tests for Lessons API"""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client = APIClient()

        self.client.force_authenticate(self.user)
    
    def test_lesson_post(self):
        """Test POST request to Lesson List URL"""

        topic = create_topic_with_module('Test Topic')

        payload = {
            'lesson_name': 'Test Lesson',
            'topic': topic.id,
            'lesson_textblocks': [
                {
                    'text': 'Test Lesson Textblock 1',
                    'text_format': 1,
                    'paragraph_number': 1
                },
                {
                    'text': 'Test Lesson Textblock 2',
                    'text_format': 1,
                    'paragraph_number': 2,
                },
                {
                    'text': 'Test Lesson Textblock 3',
                    'text_format': 1,
                    'paragraph_number': 3
                }
            ]
        }

        res = self.client.post(LESSON_LIST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(LESSON_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        lessons = models.Lesson.objects.all()
        serializer = serializers.LessonSerializer(lessons, many=True)

        self.assertEqual(res.data, serializer.data)




