from django.contrib import admin
from django.contrib.auth.admin import UserAdmin \
    as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class LessonInline(admin.TabularInline):
    """View lessons for a given module."""

    model = models.Lesson
    classes = ['collapse']


class TextBlockInline(admin.TabularInline):
    """View TextBlocks in Lesson/Exercise Admin Pages"""

    model = models.TextBlock
    classes = ['collapse']


class TopicInline(admin.TabularInline):
    """View Topics for a given Module"""

    model = models.Topic
    classes = ['collapse']


class ModuleInline(admin.TabularInline):
    """View Modules for a given Language."""

    model = models.Module
    classes = ['collapse']


class LessonAdmin(admin.ModelAdmin):

    inlines = [TextBlockInline]


class ExerciseAdmin(admin.ModelAdmin):

    inlines = [TextBlockInline]


class ModuleAdmin(admin.ModelAdmin):
    """Custom admin interface for modules"""
    
    inlines = [TopicInline]


class LanguageAdmin(admin.ModelAdmin):
    """Custom admin interface for languages.""" 

    inlines = [ModuleInline]


class TopicAdmin(admin.ModelAdmin):
    """Custom admin interface for topics."""

    inlines = [LessonInline]


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    ordering = ['id']
    list_display = ['email', 'name']

    fieldsets = (
        (
            None, {
                'fields': ('email', 'password',)
            }
        ),
        (
            _('Permissions'), {
                'fields': (
                    'is_active', 'is_staff', 'is_superuser',
                ),
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )

    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )

admin.site.register(models.User, UserAdmin)
admin.site.register(models.UserProfile)
admin.site.register(models.Language, LanguageAdmin)
admin.site.register(models.Module, ModuleAdmin)
admin.site.register(models.Topic, TopicAdmin)
admin.site.register(models.TextBlock)
admin.site.register(models.Exercise, ExerciseAdmin)
admin.site.register(models.Lesson, LessonAdmin)
