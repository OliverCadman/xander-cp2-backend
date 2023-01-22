from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, 
    PermissionsMixin,
    BaseUserManager
)

from django.dispatch import receiver
from django.db.models.signals import post_save


class UserManager(BaseUserManager):
    """Custom Manager for User Model"""
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a new user"""

        if not email:
            raise ValueError('Please supply an email address.')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a new superuser"""

        superuser = self.create_user(email, password)
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.save(using=self.db)

        return superuser
    

class User(AbstractBaseUser, PermissionsMixin):
    """Custom User Model (without 'username' field)"""

    email = models.EmailField(max_length=244, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()


class UserProfile(models.Model):
    """User Profile model, related to Auth User Model"""

    COHORT_9 = 9
    COHORT_10 = 10
    COHORT_11 = 11
    COHORT_12 = 12
    COHORT_13 = 13
    COHORT_14 = 14

    COHORT_CHOICES = (
        (COHORT_9, 'Cohort 9'),
        (COHORT_10, 'Cohort 10'),
        (COHORT_11, 'Cohort 11'),
        (COHORT_12, 'Cohort 12'),
        (COHORT_13, 'Cohort 13'),
        (COHORT_14, 'Cohort 14')
    )

    auth_user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=244, null=True)
    last_name = models.CharField(max_length=244, null=True)
    cohort_number = models.IntegerField(choices=COHORT_CHOICES, null=True)

    def __str__(self):
        return f'Profile: {self.auth_user.email}'



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create a User Profile when a new user registers.
    
    If user already exists, save the instance.
    """
    if created:
        UserProfile.objects.create(auth_user=instance)
    
    instance.userprofile.save()
