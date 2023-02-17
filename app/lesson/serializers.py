from rest_framework import serializers
from core import models
from lesson.client.S3Client import S3Client
from django.conf import settings


class LanguageSerializer(serializers.ModelSerializer):
    """Serializer for Language Model"""

    class Meta:
        model = models.Language
        fields = ['language_name', 'id']
        read_only_fields = ['id']


class LessonSerializer(serializers.ModelSerializer):
    """Serializer for Lessons"""

    class Meta:
        model = models.Lesson
        fields = '__all__'
    
    def create(self, validated_data):
        """Create a lesson."""

        lesson = models.Lesson.objects.create(**validated_data)
        return lesson


class ExerciseSerializer(serializers.ModelSerializer):
    """Serializer for Exercises"""    


    exercise_starter_code = serializers.SerializerMethodField()
    expected_output_code = serializers.SerializerMethodField()

    class Meta:
        model = models.Exercise
        fields = '__all__'
    
    def create(self, validated_data):
        """Create an exercise"""
        starter_code = validated_data.pop('starter_code', '')
        expected_output = validated_data.pop('expected_output', '')
        
        starter_code_id = self.write_to_s3_object(starter_code)
        if starter_code_id:
            print('GOT STARTER CODE ID:', starter_code_id)
            expected_output_id = self.write_to_s3_object(expected_output)
            if expected_output_id:
                print('GOT EXPECTED OUTPUT ID:', expected_output_id)
                exercise = models.Exercise.objects.create(
                    **validated_data, 
                    starter_code=starter_code_id, 
                    expected_output=expected_output_id
                )
                print('CREATED EXERCISE: ', exercise)
                return exercise
        else:
            error = 'Error saving code to S3. Cancelling post...'
            return serializers.ValidationError(error)
    
    def get_exercise_starter_code(self, obj):
        client = S3Client(
            region='us-east-2',
            access_key=settings.AWS_ACCESS_KEY_ID,
            secret_key=settings.AWS_SECRET_ACCESS_KEY
        )

        starter_code = client.read_object(f'{obj.starter_code}.txt')
        return starter_code
    
    def get_expected_output_code(self, obj):
        client = S3Client(
            region='us-east-2',
            access_key=settings.AWS_ACCESS_KEY_ID,
            secret_key=settings.AWS_SECRET_ACCESS_KEY
        )

        starter_code = client.read_object(f'{obj.expected_output}.txt')
        return starter_code

    
    
    def write_to_s3_object(self, string):

        client = S3Client(
            region='us-east-2',
            access_key=settings.AWS_ACCESS_KEY_ID,
            secret_key=settings.AWS_SECRET_ACCESS_KEY
        )

        res = client.write_object(string)
        return res


class TopicSerializer(serializers.ModelSerializer):
    """Serializer for Topic Models"""

    topic_exercises = ExerciseSerializer(many=True, required=False)
    lessons = LessonSerializer(many=True, required=False)
    
    class Meta:
        model = models.Topic
        fields = ['topic_name', 'module', 'topic_exercises', 'lessons']
    
    def create(self, validated_data):
        topic = models.Topic.objects.create(**validated_data)
        return topic


class ModuleSerializer(serializers.ModelSerializer):
    """Serializer for Modules"""
    
    class Meta:
        model = models.Module
        fields = '__all__'
    

    def create(self, validated_data):
        """Create a module."""

        module = models.Module.objects.create(**validated_data)
        return module



class TextBlockSerializer(serializers.ModelSerializer):
    """Serializer for Text Blocks"""
    class Meta:
        model = models.TextBlock
        fields = '__all__'
    

    def create(self, validated_data):
        """Create a module."""

        textblock = models.TextBlock.objects.create(**validated_data)
        return textblock


