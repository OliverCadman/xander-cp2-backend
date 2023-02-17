from django.urls import path, include
from lesson import views
from rest_framework.routers import DefaultRouter

app_name = 'lesson'

router = DefaultRouter()
router.register('modules', views.ModuleViewSet)
router.register('topics', views.TopicViewSet)
router.register('languages', views.LanguageViewSet)
router.register('textblocks', views.TextBlockViewSet)
router.register('lessons', views.LessonViewSet)
router.register('exercises', views.ExerciseViewSet)

urlpatterns = [
    path('', include(router.urls))
]