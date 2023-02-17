from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Module, Topic, Language, TextBlock, Lesson, Exercise
from lesson import serializers

from lesson.client.S3Client import S3Client
from django.conf import settings

class ModuleViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ModuleSerializer
    queryset = Module.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class TopicViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TopicSerializer
    queryset = Topic.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = self.get_queryset()        
        serializer = serializers.TopicSerializer(queryset, many=True)
        print(serializer.data)
        return Response(serializer.data)


class LanguageViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.LanguageSerializer
    queryset = Language.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class LessonViewSet(viewsets.ModelViewSet):
    """View for Lesson API"""

    serializer_class = serializers.LessonSerializer
    queryset = Lesson.objects.all()
    authentication_classes= [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class TextBlockViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TextBlockSerializer
    queryset = TextBlock.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class ExerciseViewSet(viewsets.ModelViewSet):
    """View for Exercise API"""

    serializer_class = serializers.ExerciseSerializer
    queryset = Exercise.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

