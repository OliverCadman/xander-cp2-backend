from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

"""
Production storage for image files
"""


class MediaStorage(S3Boto3Storage):
    """
    Define location for media/image files
    """

    location = settings.MEDIAFILES_LOCATION
